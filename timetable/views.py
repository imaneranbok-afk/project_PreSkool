# timetable/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Timetable, TimetableExport
from faculty.models import Teacher, Subject

@login_required
def timetable_view(request):
    """Affiche l'emploi du temps complet"""
    # Récupérer tous les cours
    timetable_entries = Timetable.objects.filter(is_active=True).select_related('subject', 'teacher')
    
    # Organiser par jour et horaire
    timetable_data = {}
    for entry in timetable_entries:
        day = entry.day
        if day not in timetable_data:
            timetable_data[day] = {}
        timetable_data[day][entry.time_slot] = entry
    
    # Ajouter tous les jours
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']
    time_slots = ['08:00', '09:45', '11:30', '14:00', '15:45', '17:30']
    
    context = {
        'timetable_data': timetable_data,
        'days': days,
        'time_slots': time_slots,
        'day_labels': dict(Timetable.DAYS_OF_WEEK),
        'time_labels': dict(Timetable.CLASS_TIMES),
    }
    return render(request, 'timetable/timetable.html', context)

@login_required
def timetable_teacher(request, teacher_id):
    """Affiche l'emploi du temps d'un enseignant"""
    teacher = get_object_or_404(Teacher, id=teacher_id)
    timetable_entries = Timetable.objects.filter(teacher=teacher, is_active=True).select_related('subject')
    
    # Organiser par jour
    timetable_data = {}
    for entry in timetable_entries:
        day = entry.day
        if day not in timetable_data:
            timetable_data[day] = []
        timetable_data[day].append(entry)
    
    context = {
        'teacher': teacher,
        'timetable_data': timetable_data,
        'days': dict(Timetable.DAYS_OF_WEEK),
        'time_labels': dict(Timetable.CLASS_TIMES),
    }
    return render(request, 'timetable/teacher-timetable.html', context)

@login_required
def timetable_add(request):
    """Ajouter un cours dans l'emploi du temps"""
    if request.method == 'POST':
        try:
            timetable = Timetable.objects.create(
                day=request.POST.get('day'),
                time_slot=request.POST.get('time_slot'),
                subject_id=request.POST.get('subject'),
                teacher_id=request.POST.get('teacher'),
                classroom=request.POST.get('classroom'),
                group=request.POST.get('group', ''),
                is_active=request.POST.get('is_active') == 'on'
            )
            messages.success(request, f'Cours ajouté avec succès: {timetable}')
            return redirect('timetable_view')
        except Exception as e:
            messages.error(request, f'Erreur: {str(e)}')
            return redirect('timetable_add')
    
    subjects = Subject.objects.all()
    teachers = Teacher.objects.filter(is_active=True)
    context = {
        'subjects': subjects,
        'teachers': teachers,
        'days': Timetable.DAYS_OF_WEEK,
        'time_slots': Timetable.CLASS_TIMES,
    }
    return render(request, 'timetable/add-timetable.html', context)

@login_required
def timetable_edit(request, timetable_id):
    """Modifier un cours"""
    timetable = get_object_or_404(Timetable, id=timetable_id)
    
    if request.method == 'POST':
        try:
            timetable.day = request.POST.get('day')
            timetable.time_slot = request.POST.get('time_slot')
            timetable.subject_id = request.POST.get('subject')
            timetable.teacher_id = request.POST.get('teacher')
            timetable.classroom = request.POST.get('classroom')
            timetable.group = request.POST.get('group', '')
            timetable.is_active = request.POST.get('is_active') == 'on'
            timetable.save()
            
            messages.success(request, 'Cours modifié avec succès!')
            return redirect('timetable_view')
        except Exception as e:
            messages.error(request, f'Erreur: {str(e)}')
            return redirect('timetable_edit', timetable_id=timetable_id)
    
    subjects = Subject.objects.all()
    teachers = Teacher.objects.filter(is_active=True)
    context = {
        'timetable': timetable,
        'subjects': subjects,
        'teachers': teachers,
        'days': Timetable.DAYS_OF_WEEK,
        'time_slots': Timetable.CLASS_TIMES,
    }
    return render(request, 'timetable/edit-timetable.html', context)

@login_required
def timetable_delete(request, timetable_id):
    """Supprimer un cours"""
    timetable = get_object_or_404(Timetable, id=timetable_id)
    timetable.delete()
    messages.success(request, 'Cours supprimé avec succès!')
    return redirect('timetable_view')

@login_required
def timetable_export_json(request):
    """Exporter l'emploi du temps en JSON"""
    timetable_entries = Timetable.objects.filter(is_active=True).select_related('subject', 'teacher')
    
    data = []
    for entry in timetable_entries:
        data.append({
            'day': entry.get_day_display(),
            'time_slot': entry.get_time_slot_display(),
            'subject': entry.subject.name,
            'teacher': f"{entry.teacher.first_name} {entry.teacher.last_name}",
            'classroom': entry.classroom,
            'group': entry.group,
        })
    
    # Sauvegarder l'export
    TimetableExport.objects.create(
        name=f"Export_{request.user.username}",
        format='json',
        data=data
    )
    
    return JsonResponse(data, safe=False)