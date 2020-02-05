from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import RegisterPrinterDocViewSet


router = DefaultRouter()
router.register(
    'register-printer-docs',
    RegisterPrinterDocViewSet
)

urlpatterns = [
    path('', include(router.urls))
]
