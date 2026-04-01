# exams/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # URLs pour les examens
    path('', views.exam_list, name='exam_list'),
    path('add/', views.exam_add, name='exam_add'),
    path('view/<int:exam_id>/', views.exam_view, name='exam_view'),
    path('edit/<int:exam_id>/', views.exam_edit, name='exam_edit'),
    path('delete/<int:exam_id>/', views.exam_delete, name='exam_delete'),
    
    # URLs pour les résultats
    path('result/add/<int:exam_id>/', views.result_add, name='result_add'),
    path('result/edit/<int:result_id>/', views.result_edit, name='result_edit'),
    path('result/delete/<int:result_id>/', views.result_delete, name='result_delete'),
]