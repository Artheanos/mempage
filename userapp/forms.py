from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.core.validators import RegexValidator, validate_email

from .models import User
from .utils import match, encrypt


class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Username or email', 'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control'})
        }

    def clean(self):
        data = self.cleaned_data
        if '@' in data['username']:
            try:
                user = User.objects.get(email__iexact=data['username'])
                data['username'] = user.username
            except ObjectDoesNotExist:
                raise forms.ValidationError("Email not found")
        else:
            try:
                user = User.objects.get(username__iexact=data['username'])
            except ObjectDoesNotExist:
                raise forms.ValidationError("Username not found")

        if not match(data['password'], user.password):
            raise forms.ValidationError("Wrong password")

        return data


class RegisterForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirm Password'
    }))

    class Meta:
        model = User
        fields = '__all__'
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
            'password': forms.PasswordInput(attrs={'placeholder': 'Password'})
        }

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data['username']

        RegexValidator(
            r'^[\dA-Za-z_]+$',
            "Username can only contain letters, numbers and underscore"
        ).__call__(username)

        if len(username) < 4 or len(username) > 50:
            raise forms.ValidationError("Username must be between 4 and 50 characters long")

        validate_email(cleaned_data['email'])

        password = cleaned_data['password']
        confirm_password = cleaned_data['confirm_password']
        if len(password) < 8 or len(password) > 60:
            raise forms.ValidationError("Password must be at least 8 and at most 60 characters long")

        RegexValidator(
            r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).+$',
            'Password must contain at least one lowercase letter, one uppercase and one digit'
        ).__call__(password)

        RegexValidator(
            r'^[a-zA-Z\d@$!%*#?&]+$',
            'Password can contain lowercase letters, uppercase letters, digits, and any of @$!%*#?&'
        ).__call__(password)

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match")

        cleaned_data['password'] = encrypt(password)

        return cleaned_data


class EditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = 'username', 'email'
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data['username']

        RegexValidator(
            r'^[\dA-Za-z_]+$',
            "Username can only contain letters, numbers and underscore"
        ).__call__(username)

        if len(username) < 4 or len(username) > 50:
            raise forms.ValidationError("Username must be between 4 and 50 characters long")

        validate_email(cleaned_data['email'])

        return cleaned_data
