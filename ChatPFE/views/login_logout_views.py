import os
import json
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password, make_password
from ChatPFE.models import Responsable, Verification_Code, Encadrant, Etudiant
from django.http import HttpResponse
from django.contrib.auth import logout as django_logout
from django.urls import reverse
from django.http import HttpResponseRedirect

# Chemin d'accès au répertoire contenant les données
data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')


# Charger les données des fichiers JSON
with open(os.path.join(data_dir, 'info_Encadrant.json'), 'r', encoding='utf-8') as file:
    data_enca = json.load(file)
    
with open(os.path.join(data_dir, 'info_Etudiant.json'), 'r', encoding='utf-8') as file:
    data_etud = json.load(file)
    
    
def index(request):
    return render(request, 'ChatPFE/index.html')

def responsable(request):
    return render(request, 'ChatPFE/responsable.html')

def login(request):
    if request.method == 'POST':
        cin = request.POST.get('cin')
        password = request.POST.get('password')
        role = request.POST.get('role')  # Retrieve the role field value

        try:
            responsable = Responsable.objects.get(cin=cin)
            if check_password(password, responsable.password):
                if responsable.role == role:  # Verify that the role matches
                    # Password and role correct, log the user in
                    request.session['cin'] = responsable.cin  # Example of using session
                    if role == 'responsable administratif':
                        return render(request, 'ChatPFE/profil_resp_ad.html')
                    elif role == 'responsable':
                        return render(request, 'ChatPFE/profil_resp.html')
                else:
                    # Role does not match
                    return render(request, 'ChatPFE/responsable.html', {'error': 'Role incorrect pour ce CIN.'})
            else:
                # Incorrect password
                return render(request, 'ChatPFE/responsable.html', {'error': 'CIN ou mot de passe incorrect.'})
        except Responsable.DoesNotExist:
            # No user found with this CIN
            return render(request, 'ChatPFE/responsable.html', {'error': 'CIN ou mot de passe incorrect.'})
    else:
        return render(request, 'ChatPFE/responsable.html')
   
def signup(request):
    if request.method == 'POST':
        cin = request.POST.get('cin')
        nom = request.POST.get('nom')
        prenom = request.POST.get('prenom')
        password = request.POST.get('password')
        role = request.POST.get('role')
        verification_code = request.POST.get('verification_code')

        # Vérifier si un utilisateur avec ce CIN existe déjà
        if Responsable.objects.filter(cin=cin).exists():
            return render(request, 'ChatPFE/responsable.html', {'error': 'Un utilisateur avec ce CIN existe déjà.'})

        # Vérifier si un utilisateur avec le rôle 'responsable' existe déjà
        if role == 'responsable' and Responsable.objects.filter(role='responsable').exists():
            return render(request, 'ChatPFE/responsable.html', {'error': 'Un autre utilisateur avec le rôle responsable existe déjà.'})

        # Si le rôle est 'responsable administratif', vérifier le code de validation
        if role == 'responsable administratif':
            if not verification_code:
                # Si le code de vérification n'est pas fourni, vérifier si le CIN est dans Verification_Code
                if Verification_Code.objects.filter(cin_verification=cin).exists():
                    return render(request, 'ChatPFE/responsable.html', {
                        'cin': cin,
                        'nom': nom,
                        'prenom': prenom,
                        'password': password,
                        'role': role,
                        'show_verification': True,
                        'error': None
                    })
                else:
                    return render(request, 'ChatPFE/responsable.html', {'error': 'CIN introuvable dans la table de vérification.'})
            else:
                try:
                    verification_entry = Verification_Code.objects.get(cin_verification=cin, code=verification_code)
                    verification_entry.delete()
                except Verification_Code.DoesNotExist:
                    return render(request, 'ChatPFE/responsable.html', {'error': 'Le code de vérification est invalide ou le CIN est incorrect.'})

        # Créer un nouvel utilisateur
        hashed_password = make_password(password)
        Responsable.objects.create(cin=cin, nom=nom, prenom=prenom, password=hashed_password, role=role)
        return redirect('login')  # Rediriger vers la page de connexion

    else:
        return render(request, 'ChatPFE/responsable.html')
   
def utilisateur(request):
    return render(request, 'ChatPFE/utilisateur.html')

data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')

def load_json_data(file_name):
    file_path = os.path.join(data_dir, file_name)
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    return None

def save_json_data(data, file_name):
    file_path = os.path.join(data_dir, file_name)
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)
        
        
def login_e(request):
    if request.method == 'POST':
        cin = request.POST.get('cin')
        password = request.POST.get('password')
        user_type = request.POST.get('user_type')
        
        try:
            if user_type == 'etudiant':
                etudiant = Etudiant.objects.get(cin_etud=cin)
                if check_password(password, etudiant.password_etud):
                    request.session['connected_cin'] = cin  # Stocker le CIN en session
                    return redirect('chat_etudiant')
                else:
                    return render(request, 'ChatPFE/utilisateur.html', {'error': 'CIN ou mot de passe incorrect.'})
            
            elif user_type == 'encadrant':
                encadrant = Encadrant.objects.get(cin_enca=cin)
                if check_password(password, encadrant.password_enca):
                    request.session['connected_cin'] = cin  # Stocker le CIN en session
                    return redirect('chat_encadrant')
                else:
                    return render(request, 'ChatPFE/utilisateur.html', {'error': 'CIN ou mot de passe incorrect.'})
        
        except (Etudiant.DoesNotExist, Encadrant.DoesNotExist):
            return render(request, 'ChatPFE/utilisateur.html', {'error': 'CIN ou mot de passe incorrect.'})

    else:
        return render(request, 'ChatPFE/utilisateur.html')






def signup_e(request):
    if request.method == 'POST':
        cin = request.POST.get('cin')
        password = request.POST.get('password')
        user_type = request.POST.get('user_type')

        if user_type == 'etudiant':
            if cin not in [etudiant['cin'] for etudiant in data_etud['Etudiant']]:
                return render(request, 'ChatPFE/utilisateur.html', {'error': 'CIN non autorisé à créer un compte.'})
            hashed_password = make_password(password)
            Etudiant.objects.create(cin_etud=cin, password_etud=hashed_password)
        elif user_type == 'encadrant':
            if cin not in [encadrant['cin'] for encadrant in data_enca['Encadrant']]:
                return render(request, 'ChatPFE/utilisateur.html', {'error': 'CIN non autorisé à créer un compte.'})
            hashed_password = make_password(password)
            Encadrant.objects.create(cin_enca=cin, password_enca=hashed_password)
        
        return redirect('login_e')  # Rediriger vers la page de connexion

    else:
        return render(request, 'ChatPFE/utilisateur.html')
    

def logout(request):
    # Effacer les données de session de l'utilisateur
    django_logout(request)
    # Rediriger vers la page de connexion
    return redirect('ChatPFE')