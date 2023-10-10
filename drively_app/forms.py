from django import forms  
from .models import File

class BlogForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ['file_name', 'uploaded_at', 'user']