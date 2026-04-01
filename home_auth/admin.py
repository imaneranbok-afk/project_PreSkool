# home_auth/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Rôles', {'fields': ('is_student', 'is_teacher', 'is_admin')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Rôles', {'fields': ('is_student', 'is_teacher', 'is_admin')}),
    )
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_student', 'is_teacher', 'is_admin')
    list_filter = ('is_student', 'is_teacher', 'is_admin', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email', 'first_name', 'last_name')

admin.site.register(CustomUser, CustomUserAdmin)