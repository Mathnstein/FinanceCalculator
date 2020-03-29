from django.urls import path

from . import views

# app_name = 'FinanceMath'
urlpatterns = [
    path('', views.index, name = 'index')
]