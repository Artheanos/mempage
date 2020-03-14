from django.core.exceptions import ValidationError
from django.db import models


class User(models.Model):
    username = models.CharField(max_length=50, null=False, unique=True)
    email = models.CharField(max_length=100, null=False, unique=True)
    password = models.CharField(max_length=70, null=False)
    # def validate_unique(self, exclude=None):
    #     if User.objects.filter(username=self.username).exists():
    #         raise ValidationError("There is someone with that username")
    #     if User.objects.filter(email=self.email).exists():
    #         raise ValidationError("There is someone with that email")
