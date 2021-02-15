from urllib.parse import quote

from django.db import models
from django.forms import ModelForm, TextInput
from django.utils import timezone

from userapp.models import User


class PostManager(models.Manager):
    def new_post(self, header, image, user):
        post = self.create(
            header=header,
            image=image,
            date=timezone.now(),
            user=user
        )
        return post


class Post(models.Model):
    header = models.CharField(max_length=80, null=False)
    image = models.CharField(max_length=20, null=False)
    date = models.DateTimeField(null=False)
    user = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True)

    objects = PostManager()

    def __str__(self):
        return f'Post "{self.header, self.image, self.date.ctime()}"'

    def image_url(self):
        return 'https://mempagebucket.s3.eu-central-1.amazonaws.com/media/' + quote(self.image)


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ('header',)
        widgets = {
            'header': TextInput(attrs={'class': 'form-control'})
        }


class Comment(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, null=False)
    post = models.ForeignKey(to=Post, on_delete=models.CASCADE, null=False)
    date = models.DateTimeField(null=False, auto_now_add=True)
    content = models.TextField(null=False)

    def __str__(self):
        return f'Comment by {self.user.username}'
