# faculty/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/admin/', views.admin_dashboard, name='admin_dashboard'),
    path('dashboard/teacher/', views.teacher_dashboard, name='teacher_dashboard'),
    path('dashboard/student/', views.student_dashboard, name='student_dashboard'),
     # URLs pour les enseignants
    path('teachers/', views.teacher_list, name='teacher_list'),
    path('teachers/add/', views.teacher_add, name='teacher_add'),
    path('teachers/view/<str:teacher_id>/', views.teacher_view, name='teacher_view'),
    path('teachers/edit/<str:teacher_id>/', views.teacher_edit, name='teacher_edit'),
    path('teachers/delete/<str:teacher_id>/', views.teacher_delete, name='teacher_delete'),
    # URLs pour les départements
 path('departments/', views.department_list, name='department_list'),
    path('departments/add/', views.department_add, name='department_add'),
    path('departments/view/<int:department_id>/', views.department_view, name='department_view'),
    path('departments/edit/<int:department_id>/', views.department_edit, name='department_edit'),
    path('departments/delete/<int:department_id>/', views.department_delete, name='department_delete'),


     # URLs pour les matières
    path('subjects/', views.subject_list, name='subject_list'),
    path('subjects/add/', views.subject_add, name='subject_add'),
    path('subjects/view/<int:subject_id>/', views.subject_view, name='subject_view'),
    path('subjects/edit/<int:subject_id>/', views.subject_edit, name='subject_edit'),
    path('subjects/delete/<int:subject_id>/', views.subject_delete, name='subject_delete'),
]