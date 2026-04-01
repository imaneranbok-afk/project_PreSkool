# faculty/models.py
from django.db import models

# ========== Modèle Teacher ==========
class Teacher(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Masculin'),
        ('Female', 'Féminin'),
    ]
    
    first_name = models.CharField(max_length=100, verbose_name="Prénom")
    last_name = models.CharField(max_length=100, verbose_name="Nom")
    teacher_id = models.CharField(max_length=20, unique=True, verbose_name="Matricule")
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, verbose_name="Genre")
    date_of_birth = models.DateField(verbose_name="Date de naissance")
    hire_date = models.DateField(verbose_name="Date d'embauche")
    email = models.EmailField(unique=True, verbose_name="Email")
    phone = models.CharField(max_length=15, verbose_name="Téléphone")
    address = models.TextField(blank=True, verbose_name="Adresse")
    qualification = models.CharField(max_length=200, verbose_name="Qualification")
    specialization = models.CharField(max_length=200, verbose_name="Spécialisation")
    is_active = models.BooleanField(default=True, verbose_name="Actif")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.teacher_id})"
    
    class Meta:
        verbose_name = "Enseignant"
        verbose_name_plural = "Enseignants"
        ordering = ['last_name', 'first_name']


# ========== Modèle Department ==========
class Department(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Nom du département")
    code = models.CharField(max_length=20, unique=True, verbose_name="Code")
    description = models.TextField(blank=True, verbose_name="Description")
    head = models.OneToOneField(
        Teacher,  # Maintenant Teacher est défini avant, donc pas d'erreur
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='headed_department', 
        verbose_name="Chef de département"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Département"
        verbose_name_plural = "Départements"
        ordering = ['name']


# ========== Modèle Subject (Matière) ==========
class Subject(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nom de la matière")
    code = models.CharField(max_length=20, unique=True, verbose_name="Code")
    description = models.TextField(blank=True, verbose_name="Description")
    department = models.ForeignKey(
        Department, 
        on_delete=models.CASCADE, 
        related_name='subjects', 
        verbose_name="Département"
    )
    teacher = models.ForeignKey(
        Teacher, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='subjects', 
        verbose_name="Enseignant"
    )
    credits = models.IntegerField(default=3, verbose_name="Crédits")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} ({self.code})"
    
    class Meta:
        verbose_name = "Matière"
        verbose_name_plural = "Matières"
        ordering = ['name']



class Subject(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nom de la matière")
    code = models.CharField(max_length=20, unique=True, verbose_name="Code")
    description = models.TextField(blank=True, verbose_name="Description")
    department = models.ForeignKey(
        Department, 
        on_delete=models.CASCADE, 
        related_name='subjects', 
        verbose_name="Département"
    )
    teacher = models.ForeignKey(
        Teacher, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='subjects', 
        verbose_name="Enseignant"
    )
    credits = models.IntegerField(default=3, verbose_name="Crédits")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} ({self.code})"
    
    class Meta:
        verbose_name = "Matière"
        verbose_name_plural = "Matières"
        ordering = ['name']