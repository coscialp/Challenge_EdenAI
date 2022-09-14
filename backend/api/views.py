from django.contrib.auth.models import User
from rest_framework.exceptions import PermissionDenied

from .serializers import RegisterSerializer, UserSerializer, KeyWordSerializer
from rest_framework import generics, viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import File, KeyWord
from .serializers import FileSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return User.objects.all()

    def retrieve(self, request, *args, **kwargs):
        if kwargs.get('pk') == 'me':
            return Response(self.get_serializer(request.user).data)
        return super().retrieve(request, args, kwargs)

class KeyWordViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = KeyWordSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        file_id = self.request.query_params.get('file_id')
        file = File.objects.filter(id=file_id, owner_id=self.request.user.pk)
        if file:
            return KeyWord.objects.filter(in_file=file_id)
        else:
            raise PermissionDenied()



class FileViewSet(viewsets.ModelViewSet):
    serializer_class = FileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return File.objects.filter(owner=user.pk)

    def create(self, request, *args, **kwargs):
        return super().create(request)