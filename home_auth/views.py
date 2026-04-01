# home_auth/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import CustomUser

def register_view(request):
    if request.method == 'POST':
        # Récupérer les données du formulaire
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        role = request.POST.get('role')
        
        # Validation des champs
        if not all([first_name, last_name, username, email, password, password2, role]):
            messages.error(request, 'Tous les champs sont obligatoires')
            return redirect('register')
        
        # Vérifier que les mots de passe correspondent
        if password != password2:
            messages.error(request, 'Les mots de passe ne correspondent pas')
            return redirect('register')
        
        # Vérifier si l'utilisateur existe déjà
        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, 'Ce nom d\'utilisateur existe déjà')
            return redirect('register')
        
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'Cet email existe déjà')
            return redirect('register')
        
        # Créer l'utilisateur
        try:
            user = CustomUser.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            
            # Assigner le rôle
            if role == 'student':
                user.is_student = True
            elif role == 'teacher':
                user.is_teacher = True
            elif role == 'admin':
                user.is_admin = True
                user.is_staff = True
            else:
                user.is_student = True
            
            user.save()
            
            messages.success(request, f'Inscription réussie ! Bienvenue {first_name} {last_name}. Veuillez vous connecter.')
            return redirect('login')
            
        except Exception as e:
            messages.error(request, f'Erreur lors de l\'inscription: {str(e)}')
            return redirect('register')
    
    return render(request, 'authentication/register.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if not username or not password:
            messages.error(request, 'Veuillez remplir tous les champs')
            return redirect('login')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Bienvenue {user.first_name} {user.last_name}!')
            
            # Rediriger selon le rôle
            if user.is_admin:
                return redirect('admin_dashboard')
            elif user.is_teacher:
                return redirect('teacher_dashboard')
            else:
                return redirect('student_dashboard')
        else:
            messages.error(request, 'Nom d\'utilisateur ou mot de passe incorrect')
            return redirect('login')
    
    return render(request, 'authentication/login.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'Vous avez été déconnecté avec succès')
    return redirect('login')
def forgot_password_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        # Vérifier si l'email existe
        try:
            user = CustomUser.objects.get(email=email)
            # Ici vous pouvez envoyer un email de réinitialisation
            # Pour l'instant, on affiche juste un message
            messages.success(request, f'Un lien de réinitialisation a été envoyé à {email}')
            return redirect('login')
        except CustomUser.DoesNotExist:
            messages.error(request, 'Aucun compte associé à cet email')
            return redirect('forgot_password')
    
    return render(request, 'authentication/forgot-password.html')