# faculty/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Teacher,Department,Subject
def index(request):
    if request.user.is_authenticated:
        if request.user.is_admin:
            return redirect('admin_dashboard')
        elif request.user.is_teacher:
            return redirect('teacher_dashboard')
        else:
            return redirect('student_dashboard')
    return render(request, 'Home/index.html')

@login_required
def admin_dashboard(request):
    return render(request, 'dashboard/admin-dashboard.html')

@login_required
def teacher_dashboard(request):
    return render(request, 'dashboard/teacher-dashboard.html')

@login_required
def student_dashboard(request):
    return render(request, 'students/student-dashboard.html')

# ========== Gestion des enseignants ==========

@login_required
def teacher_list(request):
    teachers = Teacher.objects.all()
    return render(request, 'faculty/teachers.html', {'teachers': teachers})

@login_required
def teacher_add(request):
    if request.method == 'POST':
        try:
            teacher = Teacher.objects.create(
                first_name=request.POST.get('first_name'),
                last_name=request.POST.get('last_name'),
                teacher_id=request.POST.get('teacher_id'),
                gender=request.POST.get('gender'),
                date_of_birth=request.POST.get('date_of_birth'),
                hire_date=request.POST.get('hire_date'),
                email=request.POST.get('email'),
                phone=request.POST.get('phone'),
                address=request.POST.get('address', ''),
                qualification=request.POST.get('qualification'),
                specialization=request.POST.get('specialization'),
                is_active=request.POST.get('is_active') == 'on'
            )
            messages.success(request, f'Enseignant {teacher.first_name} {teacher.last_name} ajouté avec succès!')
            return redirect('teacher_list')
        except Exception as e:
            messages.error(request, f'Erreur: {str(e)}')
            return redirect('teacher_add')
    
    return render(request, 'faculty/add-teacher.html')

@login_required
def teacher_view(request, teacher_id):
    teacher = get_object_or_404(Teacher, teacher_id=teacher_id)
    return render(request, 'faculty/teacher-details.html', {'teacher': teacher})

@login_required
def teacher_edit(request, teacher_id):
    teacher = get_object_or_404(Teacher, teacher_id=teacher_id)
    
    if request.method == 'POST':
        try:
            teacher.first_name = request.POST.get('first_name')
            teacher.last_name = request.POST.get('last_name')
            teacher.gender = request.POST.get('gender')
            teacher.date_of_birth = request.POST.get('date_of_birth')
            teacher.hire_date = request.POST.get('hire_date')
            teacher.email = request.POST.get('email')
            teacher.phone = request.POST.get('phone')
            teacher.address = request.POST.get('address', '')
            teacher.qualification = request.POST.get('qualification')
            teacher.specialization = request.POST.get('specialization')
            teacher.is_active = request.POST.get('is_active') == 'on'
            teacher.save()
            
            messages.success(request, f'Enseignant {teacher.first_name} {teacher.last_name} modifié avec succès!')
            return redirect('teacher_list')
        except Exception as e:
            messages.error(request, f'Erreur: {str(e)}')
            return redirect('teacher_edit', teacher_id=teacher_id)
    
    return render(request, 'faculty/edit-teacher.html', {'teacher': teacher})

@login_required
def teacher_delete(request, teacher_id):
    teacher = get_object_or_404(Teacher, teacher_id=teacher_id)
    teacher_name = f"{teacher.first_name} {teacher.last_name}"
    teacher.delete()
    messages.success(request, f'Enseignant {teacher_name} supprimé avec succès!')
    return redirect('teacher_list')



@login_required
def department_list(request):
    departments = Department.objects.all()
    return render(request, 'faculty/departments.html', {'departments': departments})

@login_required
def department_add(request):
    if request.method == 'POST':
        try:
            department = Department.objects.create(
                name=request.POST.get('name'),
                code=request.POST.get('code'),
                description=request.POST.get('description', ''),
                head_id=request.POST.get('head') if request.POST.get('head') else None
            )
            messages.success(request, f'Département {department.name} ajouté avec succès!')
            return redirect('department_list')
        except Exception as e:
            messages.error(request, f'Erreur: {str(e)}')
            return redirect('department_add')
    
    teachers = Teacher.objects.filter(is_active=True)
    return render(request, 'faculty/add-department.html', {'teachers': teachers})

@login_required
def department_view(request, department_id):
    department = get_object_or_404(Department, id=department_id)
    return render(request, 'faculty/department-details.html', {'department': department})

@login_required
def department_edit(request, department_id):
    department = get_object_or_404(Department, id=department_id)
    
    if request.method == 'POST':
        try:
            department.name = request.POST.get('name')
            department.code = request.POST.get('code')
            department.description = request.POST.get('description', '')
            department.head_id = request.POST.get('head') if request.POST.get('head') else None
            department.save()
            
            messages.success(request, f'Département {department.name} modifié avec succès!')
            return redirect('department_list')
        except Exception as e:
            messages.error(request, f'Erreur: {str(e)}')
            return redirect('department_edit', department_id=department_id)
    
    teachers = Teacher.objects.filter(is_active=True)
    return render(request, 'faculty/edit-department.html', {'department': department, 'teachers': teachers})

@login_required
def department_delete(request, department_id):
    department = get_object_or_404(Department, id=department_id)
    department_name = department.name
    department.delete()
    messages.success(request, f'Département {department_name} supprimé avec succès!')
    return redirect('department_list')



@login_required
def subject_list(request):
    subjects = Subject.objects.all().select_related('department', 'teacher')
    return render(request, 'faculty/subjects.html', {'subjects': subjects})

@login_required
def subject_add(request):
    if request.method == 'POST':
        try:
            subject = Subject.objects.create(
                name=request.POST.get('name'),
                code=request.POST.get('code'),
                description=request.POST.get('description', ''),
                department_id=request.POST.get('department'),
                teacher_id=request.POST.get('teacher') if request.POST.get('teacher') else None,
                credits=request.POST.get('credits', 3)
            )
            messages.success(request, f'Matière {subject.name} ajoutée avec succès!')
            return redirect('subject_list')
        except Exception as e:
            messages.error(request, f'Erreur: {str(e)}')
            return redirect('subject_add')
    
    departments = Department.objects.all()
    teachers = Teacher.objects.filter(is_active=True)
    return render(request, 'faculty/add-subject.html', {
        'departments': departments,
        'teachers': teachers
    })

@login_required
def subject_view(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    return render(request, 'faculty/subject-details.html', {'subject': subject})

@login_required
def subject_edit(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    
    if request.method == 'POST':
        try:
            subject.name = request.POST.get('name')
            subject.code = request.POST.get('code')
            subject.description = request.POST.get('description', '')
            subject.department_id = request.POST.get('department')
            subject.teacher_id = request.POST.get('teacher') if request.POST.get('teacher') else None
            subject.credits = request.POST.get('credits', 3)
            subject.save()
            
            messages.success(request, f'Matière {subject.name} modifiée avec succès!')
            return redirect('subject_list')
        except Exception as e:
            messages.error(request, f'Erreur: {str(e)}')
            return redirect('subject_edit', subject_id=subject_id)
    
    departments = Department.objects.all()
    teachers = Teacher.objects.filter(is_active=True)
    return render(request, 'faculty/edit-subject.html', {
        'subject': subject,
        'departments': departments,
        'teachers': teachers
    })

@login_required
def subject_delete(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    subject_name = subject.name
    subject.delete()
    messages.success(request, f'Matière {subject_name} supprimée avec succès!')
    return redirect('subject_list')