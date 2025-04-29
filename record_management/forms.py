# import form class from django
from django import forms
# import models
from .models import Record, RecordFile
# otther imports
from datetime import date
from django.forms import ClearableFileInput
from django.contrib.auth.models import User
from captcha.fields import CaptchaField


class RecordForm(forms.ModelForm):    
    typeId = forms.ChoiceField(choices=[
        ('NIT', 'NIT'),
        ('CC', 'Cédula de ciudadanía')
    ], widget=forms.Select(attrs={'class': 'form-control', 'name':'id_typeId', 'id':'id_typeId'}), label='Tipo de identificación')
    numberId = forms.IntegerField(widget=forms.TextInput(attrs={'class':'form-control', 'name':'numberId','placeholder': 'Número de identificación', 'pattern': '[0-9]+'}), label='Número de identificación')
    messageType = forms.ChoiceField(choices=[
        ('Comunicación', 'Comunicación'),
        ('Contrato', 'Contrato'),
        ('Solicitud de información', 'Solicitud de información'),
        ('Notificación', 'Notificación'),
        ('Requerimiento', 'Requerimiento'),
        ('Sanciones', 'Sanciones'),
        ('Cobros', 'Cobros')
    ], widget=forms.Select(attrs={'class': 'form-control'}), label='Tipo de documento')
    area = forms.ChoiceField(choices=[
        ('Informática', 'Informática'),
        ('Procesos', 'Procesos'),
        ('Contabilidad', 'Contabilidad'),
        ('Recursos Humanos', 'Recursos Humanos'),
        ('Compras', 'Compras'),
        ('Importaciones', 'Importaciones')
    ], widget=forms.Select(attrs={'class': 'form-control'}), label='Área a la que va dirigida la información')
    replyCheck = forms.BooleanField(initial=True, required=False, widget=forms.CheckboxInput(attrs={'class':'form-check-input'}), label='¿Se requiere una respuesta?')
    documentDate = forms.DateField(initial=date.today(), widget=forms.DateInput(attrs={'class':'form-control datetimepicker-input'}), label='Fecha del documento')
    captcha = CaptchaField()

    class Meta:
        model = Record
        fields = "__all__"
        widgets = {
            'userOwner': forms.HiddenInput(),
            'firstName': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Nombres', 'autocomplete':'given-name'}),
            'lastName': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Apellidos', 'autocomplete':'family-name'}),
            'email': forms.EmailInput(attrs={'class':'form-control', 'placeholder': 'Correo electrónico', 'autocomplete':'email'}),
            'subject': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Asunto'}),
            'contactperson': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Persona de contacto'}),
            'contractNumber': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'No. Contrato'}),
            'url': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Link de documento'}),
            'company': forms.Select(attrs={'class': 'form-control'}),
        }
