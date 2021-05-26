from django import forms
from django.forms import ModelForm, Select

from .models import *


class FormSession(forms.ModelForm):

    class Meta:
        model = Session
        fields = ('sessionId',)


class FormGrabacion(forms.ModelForm):

    class Meta:
        model = Grabaciones
        fields = ('sessionId', 'name', 'grabacionesId')
        widgets = {
            'agente': Select(attrs={'class': 'browser-default'}),
        }