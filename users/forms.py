# users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser
from blog.models import Picture

class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email')

class ImageFileUploadForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('avatar',) 

class DummyGardenLog(forms.ModelForm):
    class Meta:
        model = Picture
        fields = ('photo',)

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'email')