from django.urls import path
from . import views
from .views import (
    GroceryItemListView,
    GroceryItemDetailView,
    GroceryItemCreateView,
    GroceryItemUpdateView,
    GroceryItemDeleteView,
)


urlpatterns = [
    path('', views.home, name='app_home'),
    path('today/', views.today, name='app_today'),
    path('shopping_list/', GroceryItemListView.as_view(), name='app_groceryitem_list'),
    path('shopping_list/<int:pk>/', GroceryItemDetailView.as_view(), name='app_groceryitem_detail'),
    path('shopping_list/new/', GroceryItemCreateView.as_view(), name='app_groceryitem_create'),
    path('shopping_list/<int:pk>/update/', GroceryItemUpdateView.as_view(), name='app_groceryitem_update'),
    path('shopping_list/<int:pk>/delete/', GroceryItemDeleteView.as_view(), name='app_groceryitem_delete'),
    path('reminders/', views.reminders, name='app_reminders'),
]
