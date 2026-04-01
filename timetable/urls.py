# timetable/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.timetable_view, name='timetable_view'),
    path('add/', views.timetable_add, name='timetable_add'),
    path('edit/<int:timetable_id>/', views.timetable_edit, name='timetable_edit'),
    path('delete/<int:timetable_id>/', views.timetable_delete, name='timetable_delete'),
    path('teacher/<int:teacher_id>/', views.timetable_teacher, name='timetable_teacher'),
    path('export/json/', views.timetable_export_json, name='timetable_export_json'),
]