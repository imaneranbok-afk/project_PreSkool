# faculty/admin.py
from django.contrib import admin
from .models import Teacher

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('teacher_id', 'first_name', 'last_name', 'email', 'phone', 'specialization', 'is_active')
    search_fields = ('first_name', 'last_name', 'teacher_id', 'email')
    list_filter = ('gender', 'is_active', 'specialization')
    list_editable = ('is_active',)