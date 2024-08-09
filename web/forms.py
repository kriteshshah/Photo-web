from django import forms
from .models import Photo
from tinymce.widgets import TinyMCE


class PhotoForm(forms.ModelForm):
    description = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))

    class Meta:
        model = Photo
        fields = ['title', 'description', 'image', 'tags']
