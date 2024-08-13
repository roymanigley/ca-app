from django.urls import path
from .views import CaPemView, SignedCertCreateView

urlpatterns = [
    path('ca.crt', CaPemView.as_view()),
    path('certificate/signed', SignedCertCreateView.as_view()),
]
