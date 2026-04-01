# holidays/models.py
from django.db import models

class Holiday(models.Model):
    name = models.CharField(max_length=200, verbose_name="Nom du congé")
    start_date = models.DateField(verbose_name="Date de début")
    end_date = models.DateField(verbose_name="Date de fin")
    description = models.TextField(blank=True, verbose_name="Description")
    is_active = models.BooleanField(default=True, verbose_name="Actif")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    @property
    def duration(self):
        """Calcule la durée du congé en jours"""
        return (self.end_date - self.start_date).days + 1
    
    class Meta:
        verbose_name = "Jour férié"
        verbose_name_plural = "Jours fériés"
        ordering = ['start_date']