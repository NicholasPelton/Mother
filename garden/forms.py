# garden/forms.py
from django import forms
from .models import Garden

class CreateGardenForm(forms.ModelForm):

    class Meta:
        model = Garden
        fields = ['name','stage', 'serial']
