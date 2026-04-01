# student/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Student, Parent

def student_list(request):
    students = Student.objects.all()
    return render(request, 'students/students.html', {'students': students})

@login_required
def add_student(request):
    if request.method == 'POST':
        try:
            # Créer le parent
            parent = Parent.objects.create(
                father_name=request.POST.get('father_name', ''),
                father_occupation=request.POST.get('father_occupation', ''),
                father_mobile=request.POST.get('father_mobile', ''),
                father_email=request.POST.get('father_email', ''),
                mother_name=request.POST.get('mother_name', ''),
                mother_occupation=request.POST.get('mother_occupation', ''),
                mother_mobile=request.POST.get('mother_mobile', ''),
                mother_email=request.POST.get('mother_email', ''),
                present_address=request.POST.get('present_address', ''),
                permanent_address=request.POST.get('permanent_address', '')
            )
            
            # Créer l'étudiant (sans image)
            student = Student.objects.create(
                first_name=request.POST.get('first_name', ''),
                last_name=request.POST.get('last_name', ''),
                student_id=request.POST.get('student_id', ''),
                gender=request.POST.get('gender', ''),
                date_of_birth=request.POST.get('date_of_birth', ''),
                student_class=request.POST.get('student_class', ''),
                joining_date=request.POST.get('joining_date', ''),
                mobile_number=request.POST.get('mobile_number', ''),
                admission_number=request.POST.get('admission_number', ''),
                section=request.POST.get('section', ''),
                parent=parent
            )
            
            messages.success(request, f'Étudiant {student.first_name} {student.last_name} ajouté avec succès!')
            return redirect('student_list')
            
        except Exception as e:
            messages.error(request, f'Erreur: {str(e)}')
            return redirect('add_student')
    
    return render(request, 'students/add-student.html')

def view_student(request, student_id):
    student = get_object_or_404(Student, student_id=student_id)
    return render(request, 'students/student-details.html', {'student': student})

def edit_student(request, student_id):
    student = get_object_or_404(Student, student_id=student_id)
    if request.method == 'POST':
        try:
            # Mettre à jour l'étudiant
            student.first_name = request.POST.get('first_name')
            student.last_name = request.POST.get('last_name')
            student.gender = request.POST.get('gender')
            student.date_of_birth = request.POST.get('date_of_birth')
            student.student_class = request.POST.get('student_class')
            student.mobile_number = request.POST.get('mobile_number')
            student.section = request.POST.get('section')
            student.save()
            
            # Mettre à jour le parent
            parent = student.parent
            parent.father_name = request.POST.get('father_name')
            parent.father_occupation = request.POST.get('father_occupation')
            parent.father_mobile = request.POST.get('father_mobile')
            parent.father_email = request.POST.get('father_email')
            parent.mother_name = request.POST.get('mother_name')
            parent.mother_occupation = request.POST.get('mother_occupation')
            parent.mother_mobile = request.POST.get('mother_mobile')
            parent.mother_email = request.POST.get('mother_email')
            parent.present_address = request.POST.get('present_address')
            parent.permanent_address = request.POST.get('permanent_address')
            parent.save()
            
            messages.success(request, 'Étudiant modifié avec succès!')
            return redirect('student_list')
        except Exception as e:
            messages.error(request, f'Erreur: {str(e)}')
            return redirect('edit_student', student_id=student_id)
    
    return render(request, 'students/edit-student.html', {'student': student})

def delete_student(request, student_id):
    student = get_object_or_404(Student, student_id=student_id)
    student_name = f"{student.first_name} {student.last_name}"
    student.delete()
    messages.success(request, f'Étudiant {student_name} supprimé avec succès!')
    return redirect('student_list')