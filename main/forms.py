from django import forms
from django.forms import ModelForm
from .models import News
from django_summernote.widgets import SummernoteWidget


class Contact(forms.Form):
    name = forms.CharField(label='Your name',
                           max_length=100,
                           widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='Your e-mail',
                             max_length=100,
                             widget=forms.EmailInput({'class': 'form-control'}))
    phone = forms.IntegerField(label='Your phone number',
                               widget=forms.NumberInput({'class': 'form-control'}))
    topic = forms.CharField(label='Topic of inquiry', max_length=100,
                            widget=forms.TextInput({'class': 'form-control'}))
    details = forms.CharField(label='Your question', max_length=1000,
                              widget=forms.Textarea({'class': 'form-control'}))


class NewsForm(ModelForm):
    class Meta:
        model = News
        fields = ['name', 'image', 'description']
        widgets = {'description': SummernoteWidget(),
                   'name': forms.TextInput({'class': 'form-control', 'id': 'title'}),
                   'image': forms.ClearableFileInput({'class': 'form-control'})}
        labels = {'name': 'Title of the news:', 'image': 'Choose your picture:', 'description': 'Description of the news:'}
