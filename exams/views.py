# exams/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Exam, Result
from faculty.models import Subject
from student.models import Student

# ========== Gestion des examens ==========

@login_required
def exam_list(request):
    exams = Exam.objects.all().select_related('subject')
    return render(request, 'exams/exams.html', {'exams': exams})

@login_required
def exam_add(request):
    if request.method == 'POST':
        try:
            exam = Exam.objects.create(
                name=request.POST.get('name'),
                exam_type=request.POST.get('exam_type'),
                subject_id=request.POST.get('subject'),
                date=request.POST.get('date'),
                start_time=request.POST.get('start_time'),
                end_time=request.POST.get('end_time'),
                room=request.POST.get('room'),
                total_marks=request.POST.get('total_marks', 100),
                passing_marks=request.POST.get('passing_marks', 50),
                description=request.POST.get('description', '')
            )
            messages.success(request, f'Examen "{exam.name}" ajouté avec succès!')
            return redirect('exam_list')
        except Exception as e:
            messages.error(request, f'Erreur: {str(e)}')
            return redirect('exam_add')
    
    subjects = Subject.objects.all()
    return render(request, 'exams/add-exam.html', {'subjects': subjects})

@login_required
def exam_view(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)
    results = exam.results.all().select_related('student')
    return render(request, 'exams/exam-details.html', {'exam': exam, 'results': results})

@login_required
def exam_edit(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)
    
    if request.method == 'POST':
        try:
            exam.name = request.POST.get('name')
            exam.exam_type = request.POST.get('exam_type')
            exam.subject_id = request.POST.get('subject')
            exam.date = request.POST.get('date')
            exam.start_time = request.POST.get('start_time')
            exam.end_time = request.POST.get('end_time')
            exam.room = request.POST.get('room')
            exam.total_marks = request.POST.get('total_marks', 100)
            exam.passing_marks = request.POST.get('passing_marks', 50)
            exam.description = request.POST.get('description', '')
            exam.save()
            
            messages.success(request, f'Examen "{exam.name}" modifié avec succès!')
            return redirect('exam_list')
        except Exception as e:
            messages.error(request, f'Erreur: {str(e)}')
            return redirect('exam_edit', exam_id=exam_id)
    
    subjects = Subject.objects.all()
    return render(request, 'exams/edit-exam.html', {'exam': exam, 'subjects': subjects})

@login_required
def exam_delete(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)
    exam_name = exam.name
    exam.delete()
    messages.success(request, f'Examen "{exam_name}" supprimé avec succès!')
    return redirect('exam_list')


# ========== Gestion des résultats ==========

@login_required
def result_add(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)
    
    if request.method == 'POST':
        try:
            student_id = request.POST.get('student')
            marks_obtained = request.POST.get('marks_obtained')
            remarks = request.POST.get('remarks', '')
            
            result, created = Result.objects.update_or_create(
                exam=exam,
                student_id=student_id,
                defaults={
                    'marks_obtained': marks_obtained,
                    'remarks': remarks
                }
            )
            
            messages.success(request, f'Résultat ajouté pour {result.student.first_name} {result.student.last_name}')
            return redirect('exam_view', exam_id=exam.id)
        except Exception as e:
            messages.error(request, f'Erreur: {str(e)}')
            return redirect('result_add', exam_id=exam.id)
    
    students = Student.objects.all()
    existing_results = exam.results.values_list('student_id', flat=True)
    return render(request, 'exams/add-result.html', {
        'exam': exam,
        'students': students,
        'existing_results': existing_results
    })

@login_required
def result_edit(request, result_id):
    result = get_object_or_404(Result, id=result_id)
    
    if request.method == 'POST':
        try:
            result.marks_obtained = request.POST.get('marks_obtained')
            result.remarks = request.POST.get('remarks', '')
            result.save()
            
            messages.success(request, f'Résultat modifié pour {result.student.first_name} {result.student.last_name}')
            return redirect('exam_view', exam_id=result.exam.id)
        except Exception as e:
            messages.error(request, f'Erreur: {str(e)}')
            return redirect('result_edit', result_id=result.id)
    
    return render(request, 'exams/edit-result.html', {'result': result})

@login_required
def result_delete(request, result_id):
    result = get_object_or_404(Result, id=result_id)
    exam_id = result.exam.id
    result.delete()
    messages.success(request, 'Résultat supprimé avec succès!')
    return redirect('exam_view', exam_id=exam_id)