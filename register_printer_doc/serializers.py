from rest_framework import serializers

from .models import RegisterPrinterDoc


class RegisterPrinterDocSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegisterPrinterDoc
        fields = '__all__'
