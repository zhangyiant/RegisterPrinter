from django.shortcuts import render
from django.http import HttpResponse

from rest_framework import viewsets

from .models import RegisterPrinterDoc
from .serializers import RegisterPrinterDocSerializer


def index(request):
    return HttpResponse("Hello World.")

class RegisterPrinterDocViewSet(viewsets.ModelViewSet):
    queryset = RegisterPrinterDoc.objects.all()
    serializer_class = RegisterPrinterDocSerializer
