# timetable/models.py
from django.db import models
from faculty.models import Teacher, Subject
from student.models import Student

class Timetable(models.Model):
    DAYS_OF_WEEK = [
        ('monday', 'Lundi'),
        ('tuesday', 'Mardi'),
        ('wednesday', 'Mercredi'),
        ('thursday', 'Jeudi'),
        ('friday', 'Vendredi'),
        ('saturday', 'Samedi'),
    ]
    
    CLASS_TIMES = [
        ('08:00', '08:00 - 09:30'),
        ('09:45', '09:45 - 11:15'),
        ('11:30', '11:30 - 13:00'),
        ('14:00', '14:00 - 15:30'),
        ('15:45', '15:45 - 17:15'),
        ('17:30', '17:30 - 19:00'),
    ]
    
    day = models.CharField(max_length=20, choices=DAYS_OF_WEEK, verbose_name="Jour")
    time_slot = models.CharField(max_length=10, choices=CLASS_TIMES, verbose_name="Horaire")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='timetable_entries', verbose_name="Matière")
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='timetable_entries', verbose_name="Enseignant")
    classroom = models.CharField(max_length=50, verbose_name="Salle de classe")
    group = models.CharField(max_length=50, blank=True, verbose_name="Groupe")
    is_active = models.BooleanField(default=True, verbose_name="Actif")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Emploi du temps"
        verbose_name_plural = "Emplois du temps"
        unique_together = ['day', 'time_slot', 'classroom']
        ordering = ['day', 'time_slot']
    
    def __str__(self):
        return f"{self.get_day_display()} - {self.get_time_slot_display()} - {self.subject.name}"

class TimetableExport(models.Model):
    """Modèle pour exporter l'emploi du temps"""
    name = models.CharField(max_length=200, verbose_name="Nom de l'export")
    format = models.CharField(max_length=20, choices=[('json', 'JSON'), ('pdf', 'PDF'), ('html', 'HTML')], default='html')
    created_at = models.DateTimeField(auto_now_add=True)
    data = models.JSONField(default=dict, blank=True, verbose_name="Données exportées")
    
    def __str__(self):
        return f"{self.name} - {self.created_at}"
    
    class Meta:
        verbose_name = "Export d'emploi du temps"
        verbose_name_plural = "Exports d'emplois du temps"