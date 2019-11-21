from django.conf.urls import include
from django.urls import path

urlpatterns = [
    path("", include("briefme_invoices.urls")),
]
