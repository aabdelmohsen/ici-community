from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='sport-home'),
    path('scanner', views.scanner, name='security-scanner')
]
