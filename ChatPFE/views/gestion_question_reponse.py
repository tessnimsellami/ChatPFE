from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.http import HttpResponseNotAllowed
import os
import json
from django.views.decorators.csrf import csrf_exempt

# Chemin d'accès au répertoire contenant les données
data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')


def load_intents():
     with open(os.path.join(data_dir, 'quest_resp.json'), 'r', encoding='utf-8') as file:
        return json.load(file)

def save_intents(intents):
    with open(os.path.join(data_dir, 'quest_resp.json'), 'w', encoding='utf-8') as file:
        json.dump(intents, file, indent=4)

def gérer_ques_resp_et(request):
    with open(os.path.join(data_dir, 'quest_resp.json'), 'r', encoding='utf-8') as file:
        data = json.load(file)
        intents = data['intents']
    return render(request, 'ChatPFE/GérerQuestionsRéponses.html', {'intents': intents})


def ajouter_question_reponse(request):
    if request.method == 'GET':
        return render(request, 'ChatPFE/ajouter_question_reponse.html')

    elif request.method == 'POST':
        tag = request.POST.get('tag')
        new_question = request.POST.get('new_question')

        # Load existing intents from data source
        with open(os.path.join(data_dir, 'quest_resp.json'), 'r', encoding='utf-8') as file:
            data = json.load(file)
            intents = data['intents']

            # Find the intent by tag
            intent = next((intent for intent in intents if intent['tag'] == tag), None)

            if intent:
                # Add the new question to the intent
                if 'patterns' in intent:
                    intent['patterns'].append(new_question)
                else:
                    intent['patterns'] = [new_question]

                # Save updated intents back to data source
                with open(os.path.join(data_dir, 'quest_resp.json'), 'w', encoding='utf-8') as file:
                    json.dump(data, file, ensure_ascii=False, indent=4)

                # Redirect to view intent details or list of intents
                return redirect('gérer_ques_resp_et')  # Assuming you have a gérer_ques_resp_et view that accepts 'tag'

            else:
                # Handle if intent with given tag doesn't exist
                return HttpResponseNotAllowed(['GET', 'POST'])

    # Handle other cases if needed
    return HttpResponseNotAllowed(['GET', 'POST'])




def modifier_question_reponse(request):
    if request.method == 'POST':
        tag = request.POST.get('tag')
        intents = load_intents()
        intent_data = next((intent for intent in intents['intents'] if intent['tag'] == tag), None)
        if intent_data:
            return render(request, 'ChatPFE/modifier_question_reponse.html', {'intent': intent_data})
        return redirect('gérer_ques_resp_et')

    return render(request, 'ChatPFE/modifier_question_reponse.html')
        
    
def gérer_ques_resp_en(request):
    with open(os.path.join(data_dir, 'quest_resp_enca.json'), 'r', encoding='utf-8') as file:
        data = json.load(file)
        intents = data['intents']
    return render(request, 'ChatPFE/GérerQuestionsRéponses_en.html', {'intents': intents})
