from django.shortcuts import render, redirect
import os
import json
from django.http import JsonResponse, HttpResponse

# Chemin d'accès au répertoire contenant les données
data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')

# Charger les données des fichiers JSON
with open(os.path.join(data_dir, 'info_Encadrant.json'), 'r', encoding='utf-8') as file:
    data_enca = json.load(file)
    encadrant = data_enca.get('Encadrant', [])
    
with open(os.path.join(data_dir, 'info_Etudiant.json'), 'r', encoding='utf-8') as file:
    data_etud = json.load(file)
    etudiants = data_etud.get('Etudiant', [])

with open(os.path.join(data_dir, 'info_société.json'), 'r', encoding='utf-8') as file:
        data_soc = json.load(file)
        sociétés = data_soc.get('Société', [])
        

def profil_resp_ad(request):
    # Votre logique pour le reste de la vue
    return render(request, 'ChatPFE/profil_resp_ad.html')

def profil_resp(request):
    return render(request, 'ChatPFE/profil_resp.html')

def gérer_info_étudiant(request):
    # Charger les données des fichiers JSON
    with open(os.path.join(data_dir, 'info_Etudiant.json'), 'r', encoding='utf-8') as file:
        data_etud = json.load(file)
        etudiants = data_etud.get('Etudiant', [])
    return render(request, 'ChatPFE/GérerinfoEtudiant.html', {'etudiants': etudiants})


def gérer_info_encadrant(request):
    # Charger les données des fichiers JSON
    with open(os.path.join(data_dir, 'info_Encadrant.json'), 'r', encoding='utf-8') as file:
        data_enca = json.load(file)
        encadrants = data_enca.get('Encadrant', [])
    return render(request, 'ChatPFE/GérerinfoEncadrant.html', {'encadrants': encadrants})


def gérer_info_société(request):
    with open(os.path.join(data_dir, 'info_société.json'), 'r', encoding='utf-8') as file:
        data_soc = json.load(file)
        sociétés = data_soc.get('Société', [])
    return render(request, 'ChatPFE/GérerinfoSociété.html', {'sociétés': sociétés})


def gérer_info_stage(request):
    with open(os.path.join(data_dir, 'info_stage.json'), 'r', encoding='utf-8') as file:
        data_sta = json.load(file)
        stages = data_sta.get('Stage', [])
    return render(request, 'ChatPFE/GérerinfoStage.html', {'stages': stages})


def ajouter_info_étudiant(request):
    return render(request, 'ChatPFE/AjouterinfoEtudiant.html')

def enregistrer_info_étudiant(request):
    if request.method == 'POST':
        # Charger les données des étudiants existants
        with open(os.path.join(data_dir, 'info_Etudiant.json'), 'r', encoding='utf-8') as file:
            data_etud = json.load(file)
            etudiants = data_etud.get('Etudiant', [])
        with open(os.path.join(data_dir, 'info_société.json'), 'r', encoding='utf-8') as file:
            data_soc = json.load(file)
            sociétés = data_soc.get('Société', [])
        # Récupérer les données du formulaire
        cin = request.POST.get('cin')
        nom = request.POST.get('nom')
        prenom = request.POST.get('prenom')
        moyenne = request.POST.get('moyenne')
        ville = request.POST.get('ville')
        niveau = request.POST.get('niveau')
        telephone = request.POST.get('telephone')
        email = request.POST.get('email')
        linkedin = request.POST.get('linkedin', '')
        préférence = request.POST.get('préférence', '')

        # Ajouter les nouvelles informations à la liste des étudiants
        new_student = {
            'cin': cin,
            'nom': nom,
            'prenom': prenom,
            'moyenne': float(moyenne),
            'ville': ville,
            'niveau': niveau,
            'telephone': telephone,
            'email': email,
            'linkedin': linkedin,
            'préférence': préférence
        }
        etudiants.append(new_student)

        # Sauvegarder les données dans le fichier JSON
        data_etud['Etudiant'] = etudiants
        with open(os.path.join(data_dir, 'info_Etudiant.json'), 'w', encoding='utf-8') as file:
            json.dump(data_etud, file, indent=4, ensure_ascii=False)
            
        return render(request, 'ChatPFE/AjouterinfoEtudiant.html')

    return render(request, 'ChatPFE/AjouterinfoEtudiant.html')


def consulter_info_étudiant(request, cin):
    with open(os.path.join(data_dir, 'info_Etudiant.json'), 'r', encoding='utf-8') as file:
            data_etud = json.load(file)
            etudiants = data_etud.get('Etudiant', [])
    etudiant = None
    for e in etudiants:
        if e['cin'] == cin:
            etudiant = e
            break
    return render(request, 'ChatPFE/ConsulterinfoEtudiant.html', {'etudiant': etudiant})


def modifier_info_étudiant(request, cin):
    with open(os.path.join(data_dir, 'info_Etudiant.json'), 'r', encoding='utf-8') as file:
            data_etud = json.load(file)
            etudiants = data_etud.get('Etudiant', [])
    etudiant = None
    for e in etudiants:
        if e['cin'] == cin:
            etudiant = e
            break
    return render(request, 'ChatPFE/ModifierinfoEtudiant.html', {'etudiant': etudiant})

def modifier_email(request):
    if request.method == 'POST':
        nouveau_email = request.POST.get('nouveau_email')
        cin = request.POST.get('cin')
        for etudiant in etudiants:
            if etudiant['cin'] == cin:
                etudiant['email'] = nouveau_email
                with open(os.path.join(data_dir, 'info_Etudiant.json'), 'w') as file:
                    json.dump(data_etud, file, indent=4)
                return redirect('consulter_info_étudiant', cin=cin)
    return JsonResponse({'error': 'Invalid request'})

def modifier_téléphone(request):
    if request.method == 'POST':
        nouveau_téléphone = request.POST.get('nouveau_téléphone')
        cin = request.POST.get('cin')
        for etudiant in etudiants:
            if etudiant['cin'] == cin:
                etudiant['telephone'] = nouveau_téléphone
                with open(os.path.join(data_dir, 'info_Etudiant.json'), 'w', encoding='utf-8') as file:
                    json.dump(data_etud, file, indent=4)
                return redirect('consulter_info_étudiant', cin=cin)
    return JsonResponse({'error': 'Invalid request'})


def supprimer_info_étudiant(request, cin):
    if request.method == 'POST':
        # Charger les données des fichiers JSON
        with open(os.path.join(data_dir, 'info_Etudiant.json'), 'r', encoding='utf-8') as file:
            data_etud = json.load(file)

        etudiants = data_etud.get('Etudiant', [])
        etudiants = [etudiant for etudiant in etudiants if etudiant['cin'] != cin]
        data_etud['Etudiant'] = etudiants

        # Sauvegarder les données dans les fichiers JSON
        with open(os.path.join(data_dir, 'info_Etudiant.json'), 'w', encoding='utf-8') as file:
            json.dump(data_etud, file, indent=4, ensure_ascii=False)

        return redirect('gérer_info_étudiant')  # Redirection vers la page de gestion des étudiants


def rechercher_info_étudiant(request):
    with open(os.path.join(data_dir, 'info_Etudiant.json'), 'r', encoding='utf-8') as file:
        data_etud = json.load(file)
        etudiants = data_etud.get('Etudiant', [])

    if 'search_query' in request.GET:
        search_query = request.GET['search_query'].lower()
        search_results = []

        for etudiant in etudiants:
            full_name = f"{etudiant['nom'].lower()} {etudiant['prenom'].lower()}"
            reverse_full_name = f"{etudiant['prenom'].lower()} {etudiant['nom'].lower()}"
            if (search_query in etudiant['nom'].lower() or
                search_query in etudiant['prenom'].lower() or
                search_query in etudiant['cin'].lower() or
                search_query in full_name or
                search_query in reverse_full_name):
                search_results.append(etudiant)

        context = {'search_results': search_results}
        return render(request, 'ChatPFE/GérerinfoEtudiant.html', context)

    return render(request, 'ChatPFE/GérerinfoEtudiant.html')


def supprimer_tous_les_étudiants(request):
    if request.method == 'POST':
        # Charger les données des fichiers JSON
        with open(os.path.join(data_dir, 'info_Etudiant.json'), 'r', encoding='utf-8') as file:
            data_etud = json.load(file)

        # Vider la liste des étudiants
        data_etud['Etudiant'] = []

        # Sauvegarder les données dans les fichiers JSON
        with open(os.path.join(data_dir, 'info_Etudiant.json'), 'w', encoding='utf-8') as file:
            json.dump(data_etud, file, indent=4, ensure_ascii=False)

        return redirect('gérer_info_étudiant')  # Redirection vers la page de gestion des étudiants

def ajouter_info_encadrant(request):
    return render(request, 'ChatPFE/AjouterinfoEncadrant.html')

def enregistrer_info_encadrant(request):
    if request.method == 'POST':
        # Charger les données des encadrant existants
        with open(os.path.join(data_dir, 'info_Encadrant.json'), 'r', encoding='utf-8') as file:
            data_enca = json.load(file)
            encadrants = data_enca.get('Encadrant', [])
            
        # Récupérer les données du formulaire
        cin = request.POST.get('cin')
        nom = request.POST.get('nom')
        prenom = request.POST.get('prenom')
        spécialité = request.POST.get('spécialité')
        expérience = request.POST.get('expérience')
        ville = request.POST.get('ville')
        email = request.POST.get('email')
        quota = request.POST.get('quota')

        # Ajouter les nouvelles informations à la liste des encadrant
        new_encadrant = {
            'cin': cin,
            'nom': nom,
            'prenom': prenom,
            'spécialité': spécialité,
            'expérience': expérience,
            'ville': ville,
            'email': email,
            'quota': int(quota),
        }
        encadrants.append(new_encadrant)

        # Sauvegarder les données dans le fichier JSON
        data_enca['Encadrant'] = encadrants
        with open(os.path.join(data_dir, 'info_Encadrant.json'), 'w', encoding='utf-8') as file:
            json.dump(data_enca, file, indent=4, ensure_ascii=False)
            
        return render(request, 'ChatPFE/AjouterinfoEncadrant.html')

    return render(request, 'ChatPFE/AjouterinfoEncadrant.html')

def consulter_info_encadrant(request, cin):
    with open(os.path.join(data_dir, 'info_Encadrant.json'), 'r', encoding='utf-8') as file:
            data_enca = json.load(file)
            encadrants = data_enca.get('Encadrant', [])
    encadrant = None
    for en in encadrants:
        if en['cin'] == cin:
            encadrant = en
            break
    return render(request, 'ChatPFE/ConsulterinfoEncadrant.html', {'encadrant': encadrant})

def modifier_info_encadrant(request, cin):
    pass

def supprimer_info_encadrant(request, cin):
    if request.method == 'POST':
        # Charger les données des fichiers JSON
        with open(os.path.join(data_dir, 'info_Encadrant.json'), 'r', encoding='utf-8') as file:
            data_enca = json.load(file)

        encadrants = data_enca.get('Encadrant', [])
        encadrants = [encadrant for encadrant in encadrants if encadrant['cin'] != cin]
        data_enca['Encadrant'] = encadrants

        # Sauvegarder les données dans les fichiers JSON
        with open(os.path.join(data_dir, 'info_Encadrant.json'), 'w', encoding='utf-8') as file:
            json.dump(data_enca, file, indent=4, ensure_ascii=False)

        return redirect('gérer_info_encadrant')  # Redirection vers la page de gestion des encadrants

def ajouter_info_société(request):
    return render(request, 'ChatPFE/AjouterinfoSociété.html')

def enregistrer_info_société(request):
    if request.method == 'POST':
        # Charger les données des étudiants existants
        with open(os.path.join(data_dir, 'info_société.json'), 'r', encoding='utf-8') as file:
            data_soc = json.load(file)
            sociétés = data_soc.get('Société', [])
            
        # Récupérer les données du formulaire
        matricule = request.POST.get('matricule')
        nom = request.POST.get('nom')
        localisation = request.POST.get('localisation')
        domaine = request.POST.get('domaine')
        telephone = request.POST.get('telephone')
        email = request.POST.get('email')
        linkedin = request.POST.get('linkedin', '')
        mode_travail = request.POST.get('mode_travail', '')

        # Ajouter les nouvelles informations à la liste des sociétés
        new_société = {
            'matricule': matricule,
            'nom': nom,
            'localisation': localisation,
            'domaine': domaine,
            'telephone': telephone,
            'email': email,
            'linkedin': linkedin,
            'mode_travail': mode_travail
        }
        sociétés.append(new_société)

        # Sauvegarder les données dans le fichier JSON
        data_soc['Société'] = sociétés
        with open(os.path.join(data_dir, 'info_société.json'), 'w', encoding='utf-8') as file:
            json.dump(data_soc, file, indent=4, ensure_ascii=False)
            
        return render(request, 'ChatPFE/AjouterinfoSociété.html')

    return render(request, 'ChatPFE/AjouterinfoSociété.html')

def consulter_info_société(request, matricule):
    with open(os.path.join(data_dir, 'info_société.json'), 'r', encoding='utf-8') as file:
            data_soc = json.load(file)
            sociétés = data_soc.get('Société', [])     
    société = None
    for s in sociétés:
        if s['matricule'] == matricule:
            société = s
            break
    return render(request, 'ChatPFE/ConsulterinfoSociété.html', {'société': société})

def modifier_info_société(request, matricule):
    pass

def supprimer_info_société(request, matricule):
    if request.method == 'POST':
        # Charger les données des fichiers JSON
        with open(os.path.join(data_dir, 'info_société.json'), 'r', encoding='utf-8') as file:
            data_soc = json.load(file)

        sociétés = data_soc.get('Société', [])
        sociétés = [société for société in sociétés if société['matricule'] != matricule]
        data_soc['Société'] = sociétés

        # Sauvegarder les données dans les fichiers JSON
        with open(os.path.join(data_dir, 'info_société.json'), 'w', encoding='utf-8') as file:
            json.dump(data_soc, file, indent=4, ensure_ascii=False)

        return redirect('gérer_info_société')  # Redirection vers la page de gestion des étudiants


def ajouter_info_stage(request):
    return render(request, 'ChatPFE/AjouterinfoStage.html')

def enregistrer_info_stage(request):
    if request.method == 'POST':
        # Charger les données des étudiants existants
        with open(os.path.join(data_dir, 'info_stage.json'), 'r', encoding='utf-8') as file:
            data_sta = json.load(file)
            stages = data_sta.get('Stage', [])
            
        # Récupérer les données du formulaire
        ID_Sujet = request.POST.get('ID_Sujet')
        description = request.POST.get('description')
        domaine = request.POST.get('domaine')
        société = request.POST.get('société')
        encadrant = request.POST.get('encadrant')
        remarque = request.POST.get('remarque', '')
        remarque_sout = request.POST.get('remarque_sout', '')

        # Ajouter les nouvelles informations à la liste des sociétés
        new_stage = {
            'ID_Sujet': ID_Sujet,
            'description': description,
            'domaine': domaine,
            'société': société,
            'encadrant': encadrant,
            'remarque': remarque,
            'remarque_sout': remarque_sout
        }
        stages.append(new_stage)

        # Sauvegarder les données dans le fichier JSON
        data_sta['Stage'] = stages
        with open(os.path.join(data_dir, 'info_stage.json'), 'w', encoding='utf-8') as file:
            json.dump(data_sta, file, indent=4, ensure_ascii=False)
            
        return render(request, 'ChatPFE/AjouterinfoStage.html')

    return render(request, 'ChatPFE/AjouterinfoStage.html')

def consulter_info_stage(request, ID_Sujet):
    with open(os.path.join(data_dir, 'info_stage.json'), 'r', encoding='utf-8') as file:
            data_sta = json.load(file)
            stages = data_sta.get('Stage', [])     
    stage = None
    for st in stages:
        if st['ID_Sujet'] == ID_Sujet:
            stage = st
            break
    return render(request, 'ChatPFE/ConsulterinfoStage.html', {'stage': stage})

def modifier_info_stage(request, ID_Sujet):
    pass

def supprimer_info_stage(request, ID_Sujet):
    if request.method == 'POST':
        # Charger les données des fichiers JSON
        with open(os.path.join(data_dir, 'info_stage.json'), 'r', encoding='utf-8') as file:
            data_sta = json.load(file)

        stages = data_sta.get('Stage', [])
        stages = [stage for stage in stages if stage['ID_Sujet'] != ID_Sujet]
        data_sta['Stage'] = stages

        # Sauvegarder les données dans les fichiers JSON
        with open(os.path.join(data_dir, 'info_stage.json'), 'w', encoding='utf-8') as file:
            json.dump(data_sta, file, indent=4, ensure_ascii=False)

        return redirect('gérer_info_stage')  # Redirection vers la page de gestion des étudiants


