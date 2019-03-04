from django import forms
from django.forms import ModelForm
from .models import News
from django_summernote.widgets import SummernoteWidget


class Contact(forms.Form):
    name = forms.CharField(label='Your name',
                           max_length=100,
                           widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'name', 'placeholder': 'Your name*'}))
    email = forms.EmailField(label='Your e-mail',
                             max_length=100,
                             widget=forms.EmailInput({'class': 'form-control', 'id': 'email', 'placeholder': 'Your email*'}))
    phone = forms.IntegerField(label='Your phone number',
                               widget=forms.NumberInput({'class': 'form-control', 'id': 'phone', 'placeholder': 'Your phone*'}))
    topic = forms.CharField(label='Topic of inquiry', max_length=100,
                            widget=forms.TextInput({'class': 'form-control', 'id': 'topic', 'placeholder': 'Topic of inquiry*'}))
    details = forms.CharField(label='Your question', max_length=1000,
                              widget=forms.Textarea({'class': 'form-control', 'id': 'details', 'placeholder': 'Details*'}))


class NewsForm(ModelForm):
    class Meta:
        model = News
        fields = ['name', 'image', 'description']
        widgets = {'description': SummernoteWidget(),
                   'name': forms.TextInput({'class': 'form-control', 'id': 'title'}),
                   'image': forms.ClearableFileInput({'class': 'form-control'})}
        labels = {'name': 'Title of the news:', 'image': 'Choose your picture:',
                  'description': 'Description of the news:'}


class Appraisal(forms.Form):

    number = (('1', '1'),
              ('2', '2'),
              ('3', '3'),
              ('4', '4'),
              ('5', '5'),
              ('6', '6'),
              ('7', '7'),
              ('8', '8'),
              ('9', '9'),)

    name = forms.CharField(label='Your name',
                           max_length=100,
                           widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'name'}))
    email = forms.EmailField(label='Your e-mail',
                             max_length=100,
                             widget=forms.EmailInput({'class': 'form-control', 'id': 'email'}))
    phone = forms.IntegerField(label='Your phone number',
                               widget=forms.NumberInput({'class': 'form-control', 'id': 'phone'}))
    street_address = forms.CharField(label='Street address', max_length=100,
                                     widget=forms.TextInput({'class': 'form-control', 'id': 'address'}))
    suburb = forms.CharField(label='Suburb', max_length=100,
                             widget=forms.TextInput({'class': 'form-control', 'id': 'suburb'}))
    postcode = forms.IntegerField(label='Postcode',
                                  widget=forms.NumberInput({'class': 'form-control', 'id': 'postcode',
                                                            'placeholder': 'Postcode*'}))
    details = forms.CharField(label='Your question', max_length=1000,
                              widget=forms.Textarea({'class': 'form-control', 'id': 'details'}))
    bed = forms.ChoiceField(label='Bedrooms', choices=number, widget=forms.Select({'class': 'form-control',
                                                                                   'id': 'bedrooms'}))
    bath = forms.ChoiceField(label='Bathrooms', choices=number,
                             widget=forms.Select({'class': 'form-control', 'id': 'bathrooms'}))
    car = forms.ChoiceField(label='Carparks', choices=number,
                            widget=forms.Select({'class': 'form-control', 'id': 'carparks'}))