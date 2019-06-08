from .models import News
from django import forms
from django_summernote.widgets import SummernoteWidget


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['name', 'image', 'description']
        widgets = {'description': SummernoteWidget(),
                   'name': forms.TextInput({'class': 'form-control', 'id': 'title'}),
                   'image': forms.ClearableFileInput({'class': 'form-control'})}
        labels = {'name': 'Title of the news:', 'image': 'Choose your picture:',
                  'description': 'Description of the news:'}