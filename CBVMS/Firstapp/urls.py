from django.urls import path 
from .views import *

urlpatterns=[
    path('', StudentCBV.as_view(), name='studentapi')
]