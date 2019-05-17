from django import forms
from .models import Eleve


class photoForm(forms.ModelForm):

    class Meta:
        model = Eleve
        fields = ('idul', 'photo')


class videoBufferForm(forms.ModelForm):

    class Meta:
        model = Eleve
        fields = ('idul', 'videoSurveillance')


class audioBufferForm(forms.ModelForm):

    class Meta:
        model = Eleve
        fields = ('idul', 'soundSurveillance')
