from django.urls import path
from . import views
from .views import (
    GroceryItemListView,
    GroceryItemDetailView,
    GroceryItemCreateView,
    GroceryItemUpdateView,
    GroceryItemDeleteView,
    GroceryItemDeleteAllView,
    GroceryItemConfirmDeleteAllView,
    UserGroceryItemListView,
    ReminderListView,
    UserReminderListView,
    ReminderDetailView,
    ReminderCreateView,
    ReminderUpdateView,
    ReminderDeleteView,
)


urlpatterns = [
    # MAIN PAGE
    path('', views.home, name='app_home'),
    path('today/', views.today, name='app_today'),

    # SHOPPING LIST
    path('shopping_list/', GroceryItemListView.as_view(), name='app_groceryitem_list'),
    path('shopping_list/<int:pk>/', GroceryItemDetailView.as_view(), name='app_groceryitem_detail'),
    path('shopping_list/new/', GroceryItemCreateView.as_view(), name='app_groceryitem_create'),
    path('shopping_list/<int:pk>/update/', GroceryItemUpdateView.as_view(), name='app_groceryitem_update'),
    path('shopping_list/<int:pk>/delete/', GroceryItemDeleteView.as_view(), name='app_groceryitem_delete'),
    path('shopping_list/delete_all/', GroceryItemDeleteAllView.as_view(), name='app_groceryitem_delete_all'),
    path('shopping_list/confirm_delete_all/', GroceryItemConfirmDeleteAllView.as_view(),
         name='app_groceryitem_confirm_delete_all'),
    path('shopping_list/user/<str:username>/', UserGroceryItemListView.as_view(), name='app_user_groceryitem_list'),

    # REMINDERS
    path('reminders/', ReminderListView.as_view(), name='app_reminder_list'),
    path('reminders/<int:pk>/', ReminderDetailView.as_view(), name='app_reminder_detail'),
    path('reminders/new/', ReminderCreateView.as_view(), name='app_reminder_create'),
    path('reminders/<int:pk>/update/', ReminderUpdateView.as_view(), name='app_reminder_update'),
    path('reminders/<int:pk>/delete/', ReminderDeleteView.as_view(), name='app_reminder_delete'),
    path('reminders/user/<str:username>/', UserReminderListView.as_view(), name='app_user_reminder_list'),
]
