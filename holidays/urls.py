# holidays/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.holiday_list, name='holiday_list'),
    path('add/', views.holiday_add, name='holiday_add'),
    path('view/<int:holiday_id>/', views.holiday_view, name='holiday_view'),
    path('edit/<int:holiday_id>/', views.holiday_edit, name='holiday_edit'),
    path('delete/<int:holiday_id>/', views.holiday_delete, name='holiday_delete'),
]