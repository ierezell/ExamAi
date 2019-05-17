from rest_framework import serializers
from .models import Eleve


class UploadSerializer(serializers.ModelSerializer):

    class Meta:
        model = Eleve
        read_only_fields = ('photo')
