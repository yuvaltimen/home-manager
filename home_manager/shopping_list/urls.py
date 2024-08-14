from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='shopping_list_home'),
    path('about/', views.about, name='shopping_list_about'),
]
