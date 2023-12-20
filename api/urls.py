from django.urls import path
from . import views

urlpatterns = [
    path('parser_data/', views.getData),
    path('test/', views.getTest),
]
