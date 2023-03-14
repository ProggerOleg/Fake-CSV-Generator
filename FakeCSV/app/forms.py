from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import *


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input', 'rows': 3,
                                                                            'cols': 20, 'placeholder': 'Username'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input', 'rows': 3,
                                                                                 'cols': 20, 'placeholder': 'Password'}))


class SchemaForm(forms.ModelForm):
    class Meta:
        model = Schema
        fields = ['title', 'column_separator', 'string_separator']


class SchemaColumnForm(forms.Form):
    COLUMN_TYPES = (
        ('name', 'Full name'),
        ('building_number', 'Integer'),
        ('company', 'Compony'),
        ('job', 'Job'),
        ('email', 'Email'),
        ('phone_number', 'Phone number')
    )
    column_name = forms.CharField(max_length=50, label='Column name')
    type = forms.ChoiceField(choices=COLUMN_TYPES, label='Type')
    order = forms.IntegerField(min_value=0, label='Order', required=False)
    min_number = forms.IntegerField(min_value=0, label='From', required=False)
    max_number = forms.IntegerField(min_value=0, label='To', required=False)

    def clean(self):
        cleaned_data = super().clean()
        type = cleaned_data.get('type')
        order = cleaned_data.get('order')
        min_number = cleaned_data.get('min_value')
        max_number = cleaned_data.get('max_value')


class DataSetForm(forms.Form):
    rows = forms.IntegerField(min_value=1, label='Rows', required=True)
