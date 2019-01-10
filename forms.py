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
