from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from .models import File, KeyWord
import requests


def ocr(file):
    url = 'https://api.edenai.run/v2/ocr/ocr'
    files = {'files': file}
    payload = {
        "response_as_dict": "true",
        "attributes_as_list": "false",
        "show_original_response": "false",
        "providers": "['google']",
        "language": "fr"
    }
    headers = {
        "Accept": "application/json",
        "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoiMTVkMzY0OTctY2ZkZS00M2EzLTkzOWEtYzI0ZWQxMmFkOGMzIiwidHlwZSI6ImFwaV90b2tlbiJ9.Ser2Adh1dh1t1ud6tiA2S7_IlSXpwktd7qFD6v56hO4"
    }
    response = requests.post(url, data=payload, files=files, headers=headers)
    return response.json()['google']['text']


def keyword_extraction(text):
    url = "https://api.edenai.run/v2/text/keyword_extraction"

    payload = {
        "response_as_dict": True,
        "attributes_as_list": False,
        "show_original_response": False,
        "providers": "['amazon']",
        "language": "fr",
        "text": text,
    }
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoiMTVkMzY0OTctY2ZkZS00M2EzLTkzOWEtYzI0ZWQxMmFkOGMzIiwidHlwZSI6ImFwaV90b2tlbiJ9.Ser2Adh1dh1t1ud6tiA2S7_IlSXpwktd7qFD6v56hO4"
    }

    response = requests.post(url, json=payload, headers=headers)
    return response.json()['amazon']['items']


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
        )

        user.set_password(validated_data['password'])
        user.save()

        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class FileSerializer(serializers.ModelSerializer):
    size = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    filetype = serializers.SerializerMethodField()
    since_added = serializers.SerializerMethodField()
    class Meta:
        model = File
        fields = ('id', 'file', 'since_added', 'size', 'name', 'filetype', 'owner', 'text')

    def create(self, validated_data):
        file = File()
        file.file = validated_data['file']
        file.owner = validated_data['owner']
        file.text = ocr(file.file)
        file.save()

        keywords = keyword_extraction(file.text)
        for keyword in keywords:
            new_keyword = KeyWord()
            new_keyword.word = keyword['keyword']
            new_keyword.in_file = file
            new_keyword.save()
        return file
    def get_size(self, obj):
        file_size = ''
        if obj.file and hasattr(obj.file, 'size'):
            file_size = obj.file.size
        return file_size
    def get_name(self, obj):
        file_name = ''
        if obj.file and hasattr(obj.file, 'name'):
            file_name = obj.file.name
        return file_name
    def get_filetype(self, obj):
      filename = obj.file.name
      return filename.split('.')[-1]
    def get_since_added(self, obj):
        date_added = obj.date_created
        return date_added


class KeyWordSerializer(serializers.ModelSerializer):
    class Meta:
        model = KeyWord
        fields = ('id', 'word', 'in_file')