from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='app_today'),
    path('shopping_list/', views.shopping_list, name='app_shopping_list'),
    path('reminders/', views.reminders, name='app_remidners'),
]
