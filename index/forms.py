from django import forms
from .models import *

class LoginForm(forms.ModelForm):
  class Meta:
    model = User
    fields = ['uphone','upwd']
    labels = {
      'uphone':'手机号',
      'upwd':'密码'
    }
    widgets = {
      'uphone':forms.TextInput(
        attrs = {
          'class':"form-control",
          'placeholder':'11位手机号码'
        }
      ),
      'upwd':forms.PasswordInput(
        attrs = {
          'class':"form-control",
          'placeholder':'6-18位密码'
        }
      )
    }