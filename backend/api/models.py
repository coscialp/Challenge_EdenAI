from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone


class File(models.Model):
    id = models.AutoField(primary_key=True)
    file = models.FileField(null=True, max_length=255)
    date_created = models.DateTimeField(default = timezone.now)
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, default=None)
    text = models.TextField(null=True, default=None)
    def __str__(self):
        return str(self.file.name)


class KeyWord(models.Model):
    id = models.AutoField(primary_key=True)
    word = models.TextField(max_length=255)
    in_file = models.ForeignKey(File, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.word)