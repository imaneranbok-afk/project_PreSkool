# holidays/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Holiday

@login_required
def holiday_list(request):
    holidays = Holiday.objects.all()
    return render(request, 'holidays/holidays.html', {'holidays': holidays})

@login_required
def holiday_add(request):
    if request.method == 'POST':
        try:
            holiday = Holiday.objects.create(
                name=request.POST.get('name'),
                start_date=request.POST.get('start_date'),
                end_date=request.POST.get('end_date'),
                description=request.POST.get('description', ''),
                is_active=request.POST.get('is_active') == 'on'
            )
            messages.success(request, f'Congé "{holiday.name}" ajouté avec succès!')
            return redirect('holiday_list')
        except Exception as e:
            messages.error(request, f'Erreur: {str(e)}')
            return redirect('holiday_add')
    
    return render(request, 'holidays/add-holiday.html')

@login_required
def holiday_view(request, holiday_id):
    holiday = get_object_or_404(Holiday, id=holiday_id)
    return render(request, 'holidays/holiday-details.html', {'holiday': holiday})

@login_required
def holiday_edit(request, holiday_id):
    holiday = get_object_or_404(Holiday, id=holiday_id)
    
    if request.method == 'POST':
        try:
            holiday.name = request.POST.get('name')
            holiday.start_date = request.POST.get('start_date')
            holiday.end_date = request.POST.get('end_date')
            holiday.description = request.POST.get('description', '')
            holiday.is_active = request.POST.get('is_active') == 'on'
            holiday.save()
            
            messages.success(request, f'Congé "{holiday.name}" modifié avec succès!')
            return redirect('holiday_list')
        except Exception as e:
            messages.error(request, f'Erreur: {str(e)}')
            return redirect('holiday_edit', holiday_id=holiday_id)
    
    return render(request, 'holidays/edit-holiday.html', {'holiday': holiday})

@login_required
def holiday_delete(request, holiday_id):
    holiday = get_object_or_404(Holiday, id=holiday_id)
    holiday_name = holiday.name
    holiday.delete()
    messages.success(request, f'Congé "{holiday_name}" supprimé avec succès!')
    return redirect('holiday_list')