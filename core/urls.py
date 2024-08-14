from django.urls import path
from .views import SignedCertView, get_ca

urlpatterns = [
    path('', SignedCertView.as_view()),
    path('CA.crt', get_ca)
]
