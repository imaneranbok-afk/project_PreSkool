# exams/models.py
from django.db import models
from faculty.models import Subject
from student.models import Student

class Exam(models.Model):
    EXAM_TYPES = [
        ('midterm', 'Examen mi-session'),
        ('final', 'Examen final'),
        ('quiz', 'Quiz'),
        ('practical', 'Examen pratique'),
        ('project', 'Projet'),
    ]
    
    name = models.CharField(max_length=200, verbose_name="Nom de l'examen")
    exam_type = models.CharField(max_length=20, choices=EXAM_TYPES, verbose_name="Type d'examen")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='exams', verbose_name="Matière")
    date = models.DateField(verbose_name="Date")
    start_time = models.TimeField(verbose_name="Heure de début")
    end_time = models.TimeField(verbose_name="Heure de fin")
    room = models.CharField(max_length=50, verbose_name="Salle")
    total_marks = models.IntegerField(default=100, verbose_name="Note totale")
    passing_marks = models.IntegerField(default=50, verbose_name="Note de passage")
    description = models.TextField(blank=True, verbose_name="Description")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} - {self.subject.name}"
    
    @property
    def is_past(self):
        """Vérifie si l'examen est passé"""
        from django.utils import timezone
        import datetime
        exam_datetime = datetime.datetime.combine(self.date, self.start_time)
        return exam_datetime < timezone.now()
    
    class Meta:
        verbose_name = "Examen"
        verbose_name_plural = "Examens"
        ordering = ['-date', 'start_time']


class Result(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='results', verbose_name="Examen")
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='results', verbose_name="Étudiant")
    marks_obtained = models.FloatField(verbose_name="Note obtenue")
    remarks = models.TextField(blank=True, verbose_name="Remarques")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.student.first_name} {self.student.last_name} - {self.exam.name}"
    
    @property
    def percentage(self):
        """Calcule le pourcentage"""
        if self.exam.total_marks > 0:
            return (self.marks_obtained / self.exam.total_marks) * 100
        return 0
    
    @property
    def is_passed(self):
        """Vérifie si l'étudiant a réussi"""
        return self.marks_obtained >= self.exam.passing_marks
    
    class Meta:
        verbose_name = "Résultat"
        verbose_name_plural = "Résultats"
        unique_together = ['exam', 'student']
        ordering = ['-exam__date']