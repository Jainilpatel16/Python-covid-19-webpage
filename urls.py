from django.urls import path
from . import views

urlpatterns = [
    path('covid19page' , views.covid19page, name= 'covid19page')
]