from django.shortcuts import render
from django.http import JsonResponse
from .Chat_Etud import get_response 
from django.shortcuts import render, get_object_or_404



def chat_etudiant(request):
    cin = request.session.get('connected_cin')
    print(f"Utilisateur connecté avec CIN : {cin}")
    return render(request, 'ChatPFE/chatEtudiant.html')
    



def get_response_etud(request):
    user_question = request.GET.get('userQuestion', '')
    print("Question utilisateur : ", user_question)  # Ligne de débogage
    response_text = get_response(user_question)  # Appelez la fonction get_response définie 9bal
    print("Réponse générée : ", response_text)  # Ligne de débogage
    return JsonResponse({'response': response_text})