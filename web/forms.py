from django import forms
from tinymce.widgets import TinyMCE
from .models import Photo


class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['title', 'description', 'image', 'tags']
        widgets = {
            'description': TinyMCE(attrs={'cols': 80, 'rows': 30}),
        }
