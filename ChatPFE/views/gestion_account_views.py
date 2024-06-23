from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from ChatPFE.models import Etudiant, Encadrant, Responsable
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import os
import json
from django.urls import reverse
from django.http import HttpResponseRedirect


# Chemin d'accès au répertoire contenant les données
data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')

# Charger les données des fichiers JSON
with open(os.path.join(data_dir, 'info_Encadrant.json'), 'r', encoding='utf-8') as file:
    data_enca = json.load(file)
    encadrant = data_enca.get('Encadrant', [])
    
with open(os.path.join(data_dir, 'info_Etudiant.json'), 'r', encoding='utf-8') as file:
    data_etud = json.load(file)
    etudiants = data_etud.get('Etudiant', [])
        
        
def gérer_profil(request):
    return render(request, 'ChatPFE/GérerProfil.html')

def gérer_étudiant(request):
    return render(request, 'ChatPFE/GérerEtudiant.html')

def gérer_encadrant(request):
    return render(request, 'ChatPFE/GérerEncadrant.html')

def list_resp_ad(request):
    return render(request, 'ChatPFE/GérerRespAd.html')


def list_etudiants(request):
    etudiants = Etudiant.objects.all()
    return render(request, 'ChatPFE/GérerEtudiant.html', {'etudiants': etudiants})

def delete_etudiant(request, cin_etud):
    etudiant = get_object_or_404(Etudiant, cin_etud=cin_etud)
    etudiant.delete()
    return redirect('list_etudiants')

def delete_all_etudiants(request):
    Etudiant.objects.all().delete()
    return redirect('list_etudiants')

def mod_etudiant(request, cin_etud):
    etudiant = get_object_or_404(Etudiant, cin_etud=cin_etud)
    if request.method == "POST":
        # Assurez-vous de valider et sauvegarder les données correctement
        password_etud = request.POST.get('password_etud')
        
        # Utilisation de make_password pour hacher le mot de passe avant de le sauvegarder
        etudiant.password_etud = make_password(password_etud)
        
        etudiant.save()
        return redirect('list_etudiants')
    return render(request, 'ChatPFE/mod_etudiant.html', {'etudiant': etudiant})


def list_encadrants(request):
    encadrants = Encadrant.objects.all()
    return render(request, 'ChatPFE/GérerEncadrant.html', {'encadrants': encadrants})

def delete_encadrant(request, cin_enca):
    encadrant = get_object_or_404(Encadrant, cin_enca=cin_enca)
    encadrant.delete()
    return redirect('list_encadrants')

def delete_all_encadrants(request):
    Encadrant.objects.all().delete()
    return redirect('list_encadrants')

def mod_encadrant(request, cin_enca):
    encadrant = get_object_or_404(Encadrant, cin_enca=cin_enca)
    if request.method == "POST":
        # Assurez-vous de valider et sauvegarder les données correctement
        password_enca = request.POST.get('password_enca')
        
        # Utilisation de make_password pour hacher le mot de passe avant de le sauvegarder
        encadrant.password_enca = make_password(password_enca)
        
        encadrant.save()
        return redirect('list_encadrants')
    return render(request, 'ChatPFE/mod_encadrant.html', {'encadrant': encadrant})

def list_resp_ad(request):
    # Filter responsables to only include those with the role 'responsable administratif'
    responsables = Responsable.objects.filter(role='responsable administratif')

    return render(request, 'ChatPFE/GérerRespAd.html', {'responsables': responsables})


def mod_resp_ad(request, cin):
    responsable = get_object_or_404(Responsable, cin=cin)
    if request.method == "POST":
        # Assurez-vous de valider et sauvegarder les données correctement
        password = request.POST.get('password')
        
        # Utilisation de make_password pour hacher le mot de passe avant de le sauvegarder
        responsable.password = make_password(password)
        
        responsable.save()
        return redirect('list_resp_ad')
    return render(request, 'ChatPFE/mod_resp_ad.html', {'responsable': responsable})


def delete_responsable(request, cin):
    responsable = get_object_or_404(Responsable, cin=cin)
    responsable.delete()
    return redirect('list_resp_ad')


def modification_mot_de_passe(request):
    if request.method == 'POST':
        new_password1 = request.POST.get('new_password1')
        new_password2 = request.POST.get('new_password2')

        if new_password1 and new_password2:
            if new_password1 == new_password2:
                # Assurez-vous que le responsable est correctement identifié
                if 'cin' in request.session:
                    try:
                        responsable = Responsable.objects.get(cin=request.session['cin'])
                        responsable.password = make_password(new_password1)
                        responsable.save()
                        return redirect('profil_resp')  # Rediriger vers la page de profil ou une autre page appropriée
                    except Responsable.DoesNotExist:
                        return render(request, 'ChatPFE/modification_mot_de_passe.html', {'error': 'Utilisateur non trouvé'})
                else:
                    return render(request, 'ChatPFE/modification_mot_de_passe.html', {'error': 'Session non valide'})
            else:
                return render(request, 'ChatPFE/modification_mot_de_passe.html', {'error': 'Les mots de passe ne correspondent pas'})
        else:
            return render(request, 'ChatPFE/modification_mot_de_passe.html', {'error': 'Veuillez remplir tous les champs'})
    
    return render(request, 'ChatPFE/modification_mot_de_passe.html')


def modification_mot_de_passe_et(request):
    if request.method == 'POST':
        new_password1 = request.POST.get('new_password1')
        new_password2 = request.POST.get('new_password2')

        if new_password1 and new_password2:
            if new_password1 == new_password2:
                # Vérifiez si l'étudiant est correctement identifié via la session
                if 'cin' in request.session:
                    try:
                        etudiant = Etudiant.objects.get(cin_etud=request.session['cin'])
                        etudiant.password_etud = make_password(new_password1)
                        etudiant.save()
                        return redirect('chat_etudiant')  # Rediriger vers la page de chat étudiant ou autre page appropriée
                    except Etudiant.DoesNotExist:
                        return render(request, 'ChatPFE/modification_mot_de_passe_et.html', {'error': 'Utilisateur non trouvé'})
                else:
                    return render(request, 'ChatPFE/modification_mot_de_passe_et.html', {'error': 'Session non valide'})
            else:
                return render(request, 'ChatPFE/modification_mot_de_passe_et.html', {'error': 'Les mots de passe ne correspondent pas'})
        else:
            return render(request, 'ChatPFE/modification_mot_de_passe_et.html', {'error': 'Veuillez remplir tous les champs'})
    
    return render(request, 'ChatPFE/modification_mot_de_passe_et.html')


from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
import os
import json

# Chemin d'accès au répertoire contenant les données
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


def modification_num_et(request):
    if request.method == 'POST':
        new_phone_number = request.POST.get('new_phone_number')
        cin_to_update = request.session.get('connected_cin')

        if not new_phone_number or not cin_to_update:
            return render(request, 'ChatPFE/modification_num_et.html', {'error': 'Numéro de téléphone ou CIN manquant.'})

        # Charger les données des étudiants depuis le fichier JSON
        data_etud = load_json_data('info_Etudiant.json')

        if data_etud is not None:
            # Mettre à jour le numéro de téléphone de l'étudiant
            for etudiant in data_etud.get("Etudiant", []):
                if etudiant.get("cin") == cin_to_update:
                    etudiant["telephone"] = new_phone_number
                    break

            # Sauvegarder les données mises à jour dans le fichier JSON
            save_json_data(data_etud, 'info_Etudiant.json')
            return HttpResponseRedirect(reverse('chat_etudiant'))  # Redirection après la mise à jour

        else:
            return render(request, 'ChatPFE/modification_num_et.html', {'error': 'Erreur lors du chargement des données'})

    return render(request, 'ChatPFE/modification_num_et.html')