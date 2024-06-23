from django.shortcuts import render
from django.http import JsonResponse
from .Chat_Enca import get_response 
    
    
def chat_encadrant(request):
    return render(request, 'ChatPFE/chatEncadrant.html')

def get_response_enca(request):
    user_question = request.GET.get('userQuestion', '')
    print("Question utilisateur : ", user_question)  # Ligne de débogage
    response_text = get_response(user_question)  # Appelez la fonction get_response définie 9bal
    print("Réponse générée : ", response_text)  # Ligne de débogage
    return JsonResponse({'response': response_text})

