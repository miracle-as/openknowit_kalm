# forms.py
from django import forms
from .models import suggestion

class suggestionForm(forms.ModelForm):
    class Meta:
        model = suggestion
        fields = ['status']
