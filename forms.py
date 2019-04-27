from django import forms
from captcha.fields import CaptchaField, CaptchaTextInput


class CaptchaModelForm(forms.ModelForm):
    captcha = CaptchaField(widget=CaptchaTextInput(attrs={
        'class': 'form-control',
    }))


class CaptchaForm(forms.Form):
    captcha = CaptchaField(widget=CaptchaTextInput(attrs={
        'class': 'form-control',
    }))


class LoginForm(forms.Form):
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'aria-label': 'Username',
    }))

    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'aria-label': 'Password',
    }))
