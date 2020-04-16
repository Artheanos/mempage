import random, string

from PIL.Image import new
from django.db import models

from userapp import gmail_service
from userapp.utils import match, encrypt


class User(models.Model):
    username = models.CharField(max_length=50, null=False, unique=True)
    email = models.CharField(max_length=100, null=False, unique=True)
    password = models.CharField(max_length=70, null=False)

    @staticmethod
    def get_user(request):
        return User.objects.get(id=request.session.get('id'))

    def set_password(self, new_password):
        self.password = encrypt(new_password)

    def passwords_match(self, password):
        return match(password, self.password)

    def forgot_password(self):
        new_password = ''.join([random.choice(string.ascii_letters) for _ in range(10)])
        gmail_service.send_message(self.email, 'Mempage Password Recovery', f"Your new password is \"{new_password}\"")
        self.set_password(new_password)
        self.save()
