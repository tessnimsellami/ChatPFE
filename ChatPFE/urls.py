"""
URL configuration for ChatPFE project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
#from django.contrib.auth import
from .views import discussion_views_encadrant, discussion_views_etudiant, gestion_account_views, gestion_information_views, gestion_question_reponse, login_logout_views
from ChatPFE.views.login_logout_views import login, logout, signup, login_e, signup_e
from ChatPFE.views.gestion_information_views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login_logout_views.index, name='ChatPFE'),
    path('chatEncadrant/', discussion_views_encadrant.chat_encadrant, name='chat_encadrant'),
    path('chatEtudiant/', discussion_views_etudiant.chat_etudiant, name='chat_etudiant'),
    
    path('responsable/', login_logout_views.responsable, name='responsable'),
    path('login/', login_logout_views.login, name='login'),
    path('signup/', login_logout_views.signup, name='signup'),
    path('utilisateur/', login_logout_views.utilisateur, name='utilisateur'),
    path('login_e/', login_logout_views.login_e, name='login_e'),
    path('signup_e/', login_logout_views.signup_e, name='signup_e'),
    
    path('profil_resp_ad/', gestion_information_views.profil_resp_ad, name='profil_resp_ad'),
    path('profil_resp/', gestion_information_views.profil_resp, name='profil_resp'),
    path('logout/', login_logout_views.logout, name='logout'),
    
    path('gérer_info_étudian/', gestion_information_views.gérer_info_étudiant, name='gérer_info_étudiant'),
    path('gérer_info_encadrant/', gestion_information_views.gérer_info_encadrant, name='gérer_info_encadrant'),
    path('gérer_info_société/', gestion_information_views.gérer_info_société, name='gérer_info_société'),
    path('gérer_info_stage/', gestion_information_views.gérer_info_stage, name='gérer_info_stage'),
    path('gérer_profil/', gestion_account_views.gérer_profil, name='gérer_profil'),
    
    path('AjouterinfoEtudiant/', gestion_information_views.ajouter_info_étudiant, name='ajouter_info_étudiant'),
    path('enregistrer_info_étudiant/', gestion_information_views.enregistrer_info_étudiant, name='enregistrer_info_étudiant'),
    path('ConsulterinfoEtudiant/<str:cin>/', gestion_information_views.consulter_info_étudiant, name='consulter_info_étudiant'),
    path('ModifierinfoEtudiant/<str:cin>/', gestion_information_views.modifier_info_étudiant, name='modifier_info_étudiant'),
    path('supprimer_info_étudiant/<str:cin>/', gestion_information_views.supprimer_info_étudiant, name='supprimer_info_étudiant'),
    path('supprimer_tous_les_étudiants/', gestion_information_views.supprimer_tous_les_étudiants, name='supprimer_tous_les_étudiants'),
    
    path('rechercher_info_étudiant/', gestion_information_views.rechercher_info_étudiant, name='rechercher_info_étudiant'),
    
    path("modifier_email/", gestion_information_views.modifier_email, name="modifier_email"),
    path("modifier_téléphone/", gestion_information_views.modifier_téléphone, name="modifier_téléphone"),
    
    path('AjouterinfoEncadrant/', gestion_information_views.ajouter_info_encadrant, name='ajouter_info_encadrant'),
    path('enregistrer_info_encadrant/', gestion_information_views.enregistrer_info_encadrant, name='enregistrer_info_encadrant'),
    path('ConsulterinfoEncadrant/<str:cin>/', gestion_information_views.consulter_info_encadrant, name='consulter_info_encadrant'),
    path('ModifierinfoEncadrant/<str:cin>/', gestion_information_views.modifier_info_encadrant, name='modifier_info_encadrant'),
    path('supprimer_info_encadrant/<str:cin>/', gestion_information_views.supprimer_info_encadrant, name='supprimer_info_encadrant'),
    
    path('AjouterinfoSociété/', gestion_information_views.ajouter_info_société, name='ajouter_info_société'),
    path('enregistrer_info_société/', gestion_information_views.enregistrer_info_société, name='enregistrer_info_société'),
    path('ConsulterinfoSociété/<str:matricule>/', gestion_information_views.consulter_info_société, name='consulter_info_société'),
    path('ModifierinfoSociété/<str:matricule>/', gestion_information_views.modifier_info_société, name='modifier_info_société'),
    path('supprimer_info_société/<str:matricule>/', gestion_information_views.supprimer_info_société, name='supprimer_info_société'),
    
    path('AjouterinfoStage/', gestion_information_views.ajouter_info_stage, name='ajouter_info_stage'),
    path('enregistrer_info_stage/', gestion_information_views.enregistrer_info_stage, name='enregistrer_info_stage'),
    path('ConsulterinfoStage/<str:ID_Sujet>/', gestion_information_views.consulter_info_stage, name='consulter_info_stage'),
    path('ModifierinfoStage/<str:ID_Sujet>/', gestion_information_views.modifier_info_stage, name='modifier_info_stage'),
    path('supprimer_info_stage/<str:ID_Sujet>/', gestion_information_views.supprimer_info_stage, name='supprimer_info_stage'),
    
    path('gérer_étudiant/', gestion_account_views.list_etudiants, name='list_etudiants'),
    path('gérer_encadrant/', gestion_account_views.list_encadrants, name='list_encadrants'),
    path('gérer_resp_adm/', gestion_account_views.list_resp_ad, name='list_resp_ad'),
    path('gérer_ques_resp_et/', gestion_question_reponse.gérer_ques_resp_et, name='gérer_ques_resp_et'),
    path('gérer_ques_resp_en/', gestion_question_reponse.gérer_ques_resp_en, name='gérer_ques_resp_en'),
    
    
    path('ChatPFE/getResponseEnca/', discussion_views_encadrant.get_response_enca, name='get_response_enca'),
    path('ChatPFE/getResponseEtud/', discussion_views_etudiant.get_response_etud, name='get_response_etud'),
    
    
    
    path('delete_enca/<str:cin_enca>/', gestion_account_views.delete_encadrant, name='delete_encadrant'),
    path('delete_all_enca/', gestion_account_views.delete_all_encadrants, name='delete_all_encadrants'),
    path('edit_enca/<str:cin_enca>/', gestion_account_views.mod_encadrant, name='mod_encadrant'),
    
    path('delete/<str:cin_etud>/', gestion_account_views.delete_etudiant, name='delete_etudiant'),
    path('delete_all/', gestion_account_views.delete_all_etudiants, name='delete_all_etudiants'),
    path('edit/<str:cin_etud>/', gestion_account_views.mod_etudiant, name='mod_etudiant'),
    
    path('delete_resp/<str:cin>/', gestion_account_views.delete_responsable, name='delete_responsable'),
    path('edit_resp_ad/<int:cin>/', gestion_account_views.mod_resp_ad, name='mod_resp_ad'),
    
    path('ajouter_question_reponse/', gestion_question_reponse.ajouter_question_reponse, name='ajouter_question_reponse'),
    path('modifier_question_reponse/', gestion_question_reponse.modifier_question_reponse, name='modifier_question_reponse'),

    path('modification_mot_de_passe/', gestion_account_views.modification_mot_de_passe, name='modification_mot_de_passe'),
    path('modification_mot_de_passe_et/', gestion_account_views.modification_mot_de_passe_et, name='modification_mot_de_passe_et'),
    
    path('modification_num_et/', gestion_account_views.modification_num_et, name='modification_num_et'),
    
]
