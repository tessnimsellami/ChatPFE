import os
import json
import difflib
from sklearn.svm import LinearSVC
from sklearn.feature_extraction.text import CountVectorizer


# Chemin d'accès au répertoire contenant les données
data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')

# Charger les fichiers JSON avec le bon encodage
with open(os.path.join(data_dir, 'quest_resp.json'), 'r', encoding='utf-8') as f:
    intents_data = json.load(f)


with open(os.path.join(data_dir, 'info_Encadrant.json'), 'r', encoding='utf-8') as f:
    encadrants_data = json.load(f)

with open(os.path.join(data_dir, 'info_société.json'), 'r', encoding='utf-8') as f:
    societes_data = json.load(f)

with open(os.path.join(data_dir, 'info_Stage.json'), 'r', encoding='utf-8') as f:
    stages_data = json.load(f)
    
with open(os.path.join(data_dir, 'dic.json'), 'r', encoding='utf-8') as f:
    dic_data = json.load(f)
    
    
# Préparer les données pour le classificateur
X = []
y = []

for intent in intents_data['intents']:
    tag = intent['tag']
    patterns = intent['patterns']
    responses = intent['responses']
    for pattern in patterns:
        X.append(pattern)
        y.append(tag)

# Vectoriser les phrases
vectorizer = CountVectorizer()
X_vectorized = vectorizer.fit_transform(X)

# Entraîner le classificateur
classifier = LinearSVC(dual='auto')
classifier.fit(X_vectorized, y)

# Fonction pour prédire l'intention et corriger l'orthographe en utilisant le dictionnaire
def correct_spelling(question, dictionary):
    words = question.split()
    corrected_words = []
    for word in words:
        if word.lower() in dictionary:
            corrected_words.append(word)
        else:
            closest_match = difflib.get_close_matches(word, dictionary.keys(), n=1)
            if closest_match:
                corrected_words.append(closest_match[0])
            else:
                corrected_words.append(word)
    return ' '.join(corrected_words)

# Fonction pour remplacer les mots par leurs synonymes
def replace_with_synonyms(question, dic_data):
    words = question.split()
    new_words = []
    for word in words:
        if word.lower() in dic_data:
            new_words.append(dic_data[word.lower()][0]) # Remplacer par le premier synonyme trouvé
        else:
            new_words.append(word)
    return ' '.join(new_words)

# Fonction pour prédire l'intention
def predict_intent(question):
    # Correction d'orthographe
    question = correct_spelling(question, vectorizer.vocabulary_)
    # Remplacement de synonymes (ya rabi sahel)
    question = replace_with_synonyms(question, dic_data)
    # Vectorisation et prédiction
    question_vectorized = vectorizer.transform([question])
    return classifier.predict(question_vectorized)[0]


# Fonctions de traitement pour chaque intention
def handle_hallo():
    intent_data = next((intent for intent in intents_data['intents'] if intent['tag'] == "hallo"), None)
    if intent_data:
        responses = intent_data['responses']
        return "\n".join(responses)
    return "Je ne trouve pas cette information."


def handel_a_plus():
    intent_data = next((intent for intent in intents_data['intents'] if intent['tag'] == "a plus"), None)
    if intent_data:
        responses = intent_data['responses']
        return "\n".join(responses)
    return "Je ne trouve pas cette information."


def handel_remerciment():
    intent_data = next((intent for intent in intents_data['intents'] if intent['tag'] == "remerciment"), None)
    if intent_data:
        responses = intent_data['responses']
        return "\n".join(responses)
    return "Je ne trouve pas cette information."


def handel_option():
    intent_data = next((intent for intent in intents_data['intents'] if intent['tag'] == "option"), None)
    if intent_data:
        responses = intent_data['responses']
        return "\n".join(responses)
    return "Je ne trouve pas cette information."


def handel_Identitée():
    intent_data = next((intent for intent in intents_data['intents'] if intent['tag'] == "Identitée"), None)
    if intent_data:
        responses = intent_data['responses']
        return "\n".join(responses)
    return "Je ne trouve pas cette information."


def handel_quoi():
    intent_data = next((intent for intent in intents_data['intents'] if intent['tag'] == "quoi"), None)
    if intent_data:
        responses = intent_data['responses']
        return "\n".join(responses)
    return "Je ne trouve pas cette information."


def handel_insult():
    intent_data = next((intent for intent in intents_data['intents'] if intent['tag'] == "insult"), None)
    if intent_data:
        responses = intent_data['responses']
        return "\n".join(responses)
    return "Je ne trouve pas cette information."


def handel_activité():
    intent_data = next((intent for intent in intents_data['intents'] if intent['tag'] == "activité"), None)
    if intent_data:
        responses = intent_data['responses']
        return "\n".join(responses)
    return "Je ne trouve pas cette information."


def handel_exclaim():
    intent_data = next((intent for intent in intents_data['intents'] if intent['tag'] == "exclaim"), None)
    if intent_data:
        responses = intent_data['responses']
        return "\n".join(responses)
    return "Je ne trouve pas cette information."


def handel_appreciation():
    intent_data = next((intent for intent in intents_data['intents'] if intent['tag'] == "appreciation"), None)
    if intent_data:
        responses = intent_data['responses']
        return "\n".join(responses)
    return "Je ne trouve pas cette information."


def handel_sympatique():
    intent_data = next((intent for intent in intents_data['intents'] if intent['tag'] == "sympatique"), None)
    if intent_data:
        responses = intent_data['responses']
        return "\n".join(responses)
    return "Je ne trouve pas cette information."


def handel_non():
    intent_data = next((intent for intent in intents_data['intents'] if intent['tag'] == "non"), None)
    if intent_data:
        responses = intent_data['responses']
        return "\n".join(responses)
    return "Je ne trouve pas cette information."


def handel_greetreply():
    intent_data = next((intent for intent in intents_data['intents'] if intent['tag'] == "greetreply"), None)
    if intent_data:
        responses = intent_data['responses']
        return "\n".join(responses)
    return "Je ne trouve pas cette information."


def handel_suggestion():
    intent_data = next((intent for intent in intents_data['intents'] if intent['tag'] == "suggestion"), None)
    if intent_data:
        responses = intent_data['responses']
        return "\n".join(responses)
    return "Je ne trouve pas cette information."


def handle_ville(question, responses):
    encadrants = extract_encadrants(question)
    encadrants1 = extract_encadrants1(question)
    societes = extract_societes(question)
    final_responses = []

    if encadrants:
        for encadrant in encadrants:
            prenom, nom = encadrant
            encadrant_info = find_encadrant_info(prenom, nom)
            if encadrant_info:
                ville_encadrant = encadrant_info.get('ville', 'non renseignée')
                if ville_encadrant != 'non renseignée':
                    for response in responses:
                        final_responses.append(response.replace('[FULL_NAME]', f"{prenom} {nom}").replace('[VILLE]', ville_encadrant))
    elif encadrants1:
        for encadrant in encadrants1:
            encadrant_info = find_encadrant_info1(encadrant)
            if encadrant_info:
                ville_encadrant = encadrant_info.get('ville', 'non renseignée')
                if ville_encadrant != 'non renseignée':
                    for response in responses:
                        final_responses.append(response.replace('[FULL_NAME]', encadrant[0] + " " + encadrant[1]).replace('[VILLE]', ville_encadrant))
                        
    for societe in societes:
        societe_info = find_societe_info(societe)
        if societe_info:
            ville_societe = societe_info.get('localisation', 'non renseignée')
            if ville_societe != 'non renseignée':
                for response in responses:
                    final_responses.append(response.replace('[FULL_NAME]', societe).replace('[VILLE]', ville_societe))

    if final_responses:
        return "\n".join(final_responses)
    return "Je ne trouve pas cette information."


def handle_telephone(question, responses):
    societes = extract_societes(question)
    final_responses = []
    if societes:
        for societe in societes:
            societe_info = find_societe_info(societe)
            if societe_info:
                for response in responses:
                    final_responses.append(response.replace('[SOCIETE]', societe).replace('[TELEPHONE]', societe_info.get('telephone', 'non renseigné')))
    if final_responses:
        return "\n".join(final_responses)
    return "Je ne trouve pas cette information."


def handle_email(question, responses):
    encadrants = extract_encadrants(question)
    encadrants1 = extract_encadrants1(question)
    societes = extract_societes(question)
    final_responses = []
    
    if encadrants:
        for encadrant in encadrants:
            prenom, nom = encadrant
            encadrant_info = find_encadrant_info(prenom, nom)
            if encadrant_info:
                for response in responses:
                    final_responses.append(response.replace('[FULL_NAME]', f"{prenom} {nom}").replace('[EMAIL]', encadrant_info.get('email', 'non renseignée')))
    elif encadrants1:
        for encadrant in encadrants1:
            encadrant_info = find_encadrant_info1(encadrant)
            if encadrant_info:
                for response in responses:
                    final_responses.append(response.replace('[FULL_NAME]', encadrant[0] + " " + encadrant[1]).replace('[EMAIL]', encadrant_info.get('email', 'non renseignée')))
    elif societes:
        for societe in societes:
            societe_info = find_societe_info(societe)
            if societe_info:
                for response in responses:
                    final_responses.append(response.replace('[FULL_NAME]', societe).replace('[EMAIL]', societe_info.get('email', 'non renseigné')))
    
    if final_responses:
        return "\n".join(final_responses)
    return "Je ne trouve pas cette information."

def handle_linkedin(question, responses):
    societes = extract_societes(question)
    final_responses = []
    
    if societes:
        for societe in societes:
            societe_info = find_societe_info(societe)
            if societe_info:
                link = societe_info.get('linkedin', 'non renseigné')
                if link == "":
                    for response in responses:
                        return response.replace('[SOCIETE]', societe).replace('[LINKEDIN]', "introuvable")
                else :
                    for response in responses:
                        final_responses.append(response.replace('[SOCIETE]', societe).replace('[LINKEDIN]', societe_info.get('linkedin', 'non renseigné')))
    if final_responses:
        return "\n".join(final_responses)
    return "Je ne trouve pas cette information."

def handle_description_stage(question, responses):
    domaines = extract_domaines(question)
    final_responses = []
    
    if domaines:
        for domaine in domaines:
            stage_infos = find_stage_info_by_domaine(domaine)
            if stage_infos:
                for stage_info in stage_infos:
                    for response in responses:
                        final_responses.append(response.replace('[DOMAINE]', domaine).replace('[ID_SUJET]', stage_info.get('id_sujet')).replace('[DESCRIPTION]', stage_info.get('description')))
    if final_responses:
        return "\n".join(final_responses)
    return "Je ne trouve pas cette information." 

def handle_societe_stage(question, responses):
    ids = extract_ids(question)
    final_responses = []
    
    if ids:
        for id in ids:
            stage_info = find_stage_info_by_id(id)
            if stage_info:
                for response in responses:
                    final_responses.append(response.replace('[ID_SUJET]', id).replace('[SOCIETE]', stage_info.get('société', 'non renseignée')))
    if final_responses:
        return "\n".join(final_responses)
    return "Je ne trouve pas cette information."

def handle_specialite(question, responses):
    encadrants = extract_encadrants(question)
    encadrants1 = extract_encadrants1(question)
    societes = extract_societes(question)
    final_responses = []
    
    if encadrants:
        for encadrant in encadrants:
            prenom, nom = encadrant
            encadrant_info = find_encadrant_info(prenom, nom)
            if encadrant_info:
                for response in responses:
                    final_responses.append(response.replace('[FULL_NAME]', f"{prenom} {nom}").replace('[SPECIALITE]', encadrant_info.get('spécialité', 'non renseignée')))
    elif encadrants1:
        for encadrant in encadrants1:
            encadrant_info = find_encadrant_info1(encadrant)
            if encadrant_info:
                for response in responses:
                    final_responses.append(response.replace('[FULL_NAME]', encadrant[0] + " " + encadrant[1]).replace('[SPECIALITE]', encadrant_info.get('spécialité', 'non renseignée')))
    elif societes:
        for societe in societes:
            societe_info = find_societe_info(societe)
            if societe_info:
                for response in responses:
                    final_responses.append(response.replace('[FULL_NAME]', societe).replace('[SPECIALITE]', societe_info.get('domaine', 'non renseigné')))
    
    if final_responses:
        return "\n".join(final_responses)
    return "Je ne trouve pas cette information."


def handle_encadrant_stage(question, responses):
    ids = extract_ids(question)
    if ids:
        for id in ids:
            stage_info = find_stage_info_by_id(id)
            if stage_info:
                for response in responses:
                    return response.replace('[ID_SUJET]', id).replace('[FULL_NAME]', stage_info.get('encadrant', 'non renseigné'))
    return "Je ne trouve pas cette information."

def handle_remarque_stage(question, responses):
    ids = extract_ids(question)
    final_responses = []
    
    if ids:
        for id in ids:
            stage_info = find_stage_info_by_id(id)
            if stage_info:
                for response in responses:
                    final_responses.append(response.replace('[ID_SUJET]', id).replace('[REMARQUE]', stage_info.get('remarque', 'non renseignée')))
    if final_responses:
        return "\n".join(final_responses)
    return "Je ne trouve pas cette information." 

def handle_mode_travail_societe(question, responses):
    societes = extract_societes(question)
    if societes:
        for societe in societes:
            societe_info = find_societe_info(societe)
            if societe_info:
                for response in responses:
                    return response.replace('[SOCIETE]', societe).replace('[MODE_TRAVAIL]', societe_info.get('mode_travail', 'non renseigné'))
    return "Je ne trouve pas cette information."

def handle_experience_encadrant(question, responses):
    encadrants = extract_encadrants(question)
    encadrants1 = extract_encadrants1(question)
    final_responses = []
    
    if encadrants:
        for encadrant in encadrants:
            prenom, nom = encadrant
            encadrant_info = find_encadrant_info(prenom, nom)
            if encadrant_info:
                experience = str(encadrant_info.get('expérience', 'non renseignée'))  # Convertir en str
                for response in responses:
                    final_responses.append(response.replace('[FULL_NAME]', f"{prenom} {nom}").replace('[EXPERIENCE]', experience))
    elif encadrants1:
        for encadrant in encadrants1:
            encadrant_info = find_encadrant_info1(encadrant)
            if encadrant_info:
                experience = str(encadrant_info.get('expérience', 'non renseignée'))  # Convertir en str
                for response in responses:
                    final_responses.append(response.replace('[FULL_NAME]', encadrant[0] + " " + encadrant[1]).replace('[EXPERIENCE]', experience))
                    
    if final_responses:
        return "\n".join(final_responses)
    return "Je ne trouve pas cette information."

def handle_quota_encadrant(question, responses):
    encadrants = extract_encadrants(question)
    encadrants1 = extract_encadrants1(question)
    final_response = ""
    
    if encadrants:
        for encadrant in encadrants:
            prenom, nom = encadrant
            encadrant_info = find_encadrant_info(prenom, nom)
            if encadrant_info:
                quota = str(encadrant_info.get('quota', 'non renseigné'))  # Convertir en str
                for response in responses:
                    final_response += response.replace('[FULL_NAME]', f"{prenom} {nom}").replace('[QUOTA]', quota) + "\n"
                    
    elif encadrants1:
        for encadrant in encadrants1:
            encadrant_info = find_encadrant_info1(encadrant)
            if encadrant_info:
                quota = str(encadrant_info.get('quota', 'non renseigné'))  # Convertir en str
                for response in responses:
                    final_response += response.replace('[FULL_NAME]', encadrant[0] + " " + encadrant[1]).replace('[QUOTA]', quota) + "\n"

    if final_response:
        return final_response.strip()

    return "Je ne trouve pas cette information."


def handle_niveaux_encadrant(question, responses):
    encadrants = extract_encadrants(question)
    encadrants1 = extract_encadrants1(question)
    final_responses = []
    
    if encadrants:
        for encadrant in encadrants:
            prenom, nom = encadrant
            encadrant_info = find_encadrant_info(prenom, nom)
            if encadrant_info:
                niv = encadrant_info.get('niveau', 'non renseignés')
                if niv == "Licence":
                    for response in responses:
                        final_responses.append(response.replace('[FULL_NAME]', f"{prenom} {nom}").replace('[NIVEAU]', niv))
                else:
                    for response in responses:
                        final_responses.append(response.replace('[FULL_NAME]', f"{prenom} {nom}").replace('[NIVEAU]', "licence et de master"))
    elif encadrants1:
        for encadrant in encadrants1:
            encadrant_info = find_encadrant_info1(encadrant)
            if encadrant_info:
                niv = encadrant_info.get('niveau', 'non renseignés')
                if niv == "Licence":
                    for response in responses:
                        final_responses.append(response.replace('[FULL_NAME]', encadrant[0] + " " + encadrant[1]).replace('[NIVEAU]', niv))
                else:
                    for response in responses:
                        final_responses.append(response.replace('[FULL_NAME]', encadrant[0] + " " + encadrant[1]).replace('[NIVEAU]', "licence et de master"))
                    
    if final_responses:
        return "\n".join(final_responses)
    return "Je ne trouve pas cette information."

def handle_proposition_encadrant(question, responses):
    specialites = extract_specialites(question)
    if specialites:
        final_response = ""
        for specialite in specialites:
            encadrants_matching = find_encadrants_by_specialite(specialite)
            if encadrants_matching:
                for encadrant_info in encadrants_matching:
                    prenom = encadrant_info['prenom']
                    nom = encadrant_info['nom']
                    for response in responses:
                        final_response += response.replace('[FULL_NAME]', f"{prenom} {nom}").replace('[SPECIALITE]', encadrant_info.get('spécialité', 'non renseignées')) + "\n"
            else:
                final_response = "Je ne trouve pas d'encadrant avec cette spécialité."
        return final_response.strip()
    return "Je ne trouve pas cette information."




def handle_disponibilite_encadrant(question, responses):
    final_response = ""
    n=0
    for encadrant_info in encadrants_data['Encadrant']:
        prenom = encadrant_info['prenom']
        nom = encadrant_info['nom']
        quota = int(encadrant_info.get('quota', 0))
        if quota < 5:
            n=+1
            for response in responses:
                final_response += response.replace('[FULL_NAME]', f"{prenom} {nom}" + " ") + "\n"
    if n == 0:
        final_response += response.replace('[FULL_NAME]', "Aucun encadrant n'est ").replace('[NOM]', nom) + "\n"

    if final_response:
        return final_response.strip()
    
    return "Je ne trouve pas cette information."


def handle_localisation_encadrant(question, responses):
    villes_question = extract_ville(question)
    final_response = ""

    for encadrant_info in encadrants_data['Encadrant']:
        prenom = encadrant_info['prenom']
        nom = encadrant_info['nom']
        ville_encadrant = encadrant_info.get('ville', 'non renseignée')

        if any(ville_encadrant.lower() == ville.lower() for ville in villes_question):
            for response in responses:
                final_response += response.replace('[FULL_NAME]', f"{prenom} {nom}").replace('[VILLE]', ville_encadrant) + "\n"

    if final_response:
        return final_response.strip()

    return "Je ne trouve pas cette information."

def handle_societe_domaine(question, responses):
    domaines = extract_domaines(question)
    final_response = ""
    
    for societe_info in societes_data['Société']:
        soc = societe_info['nom']
        domaine = societe_info.get('domaine', 'non renseigné')
        
        if any(domaine.lower() == d.lower() for d in domaines):
            for response in responses:
                final_response += response.replace('[DOMAINE]', domaine).replace('[SOCIETES]', soc) + "\n"
    
    if final_response:
        return final_response.strip()

    return "Je ne trouve pas cette information."


def handle_societe_mode(question, responses):
    modes = extract_mode(question)
    final_response = ""
    
    if modes:
        for mode_travail in modes:
            societe_info = find_societe_info_by_mode(mode_travail)
            if societe_info:
                for response in responses:
                    final_response += response.replace('[MODE]', mode_travail).replace('[SOCIETES]', societe_info.get('nom', 'non renseigné'))
    if final_response:
        return final_response.strip()

    return "Je ne trouve pas cette information."

def handle_societe_mode(question, responses):
    mode_question = extract_mode(question)
    final_response = ""

    for societe_info in societes_data['Société']:
        mode_soc = societe_info.get('mode_travail', 'non renseignée')

        if any(mode_soc.lower() == mode_travail.lower() for mode_travail in mode_question):
            for response in responses:
                final_response += response.replace('[MODE]', mode_soc).replace('[SOCIETES]', societe_info.get('nom', 'non renseigné')) + "\n"

    if final_response:
        return final_response.strip()

    return "Je ne trouve pas cette information."

def handle_comparaison_experience(question, responses):
    encadrants = extract_encadrants(question)
    encadrants1 = extract_encadrants1(question)
    
    if not encadrants and not encadrants1:
        return "Aucun étudiant trouvé dans la question."
    
    plus_exp = None
    meilleure_exp = -1
    encadrant_info = []
    
    for encadrant in encadrants:
        prenom, nom = encadrant
        info = find_encadrant_info(prenom, nom)
        if info:
            encadrant_info.append(info)
        
    for encadrant in encadrants1:
        info = find_encadrant_info1(encadrant)
        if info:
            encadrant_info.append(info)
        
    for info in encadrant_info:
        if info:
            expérience = int(info['expérience'])
            if expérience > meilleure_exp:
                meilleure_exp = expérience
                plus_exp = info
    
    if plus_exp:
        response = f"C'est {plus_exp['prenom']} {plus_exp['nom']} : {meilleure_exp}."
        return response
    
    return "Impossible de déterminer l'étudiant avec la meilleure moyenne."




def handle_comparaison_sujet(question, responses):
    sujets = extract_ids(question)
    if sujets and len(sujets) == 2:
        sujet1_info = find_stage_info_by_id(sujets[0])
        sujet2_info = find_stage_info_by_id(sujets[1])
        if sujet1_info and sujet2_info:
            domaine1 = sujet1_info.get('domaine', '')
            domaine2 = sujet2_info.get('domaine', '')
            if domaine1 == domaine2:
                return responses[0].replace('[ID_SUJET1]', sujets[0]).replace('[ID_SUJET2]', sujets[1])
            else:
                return responses[1].replace('[ID_SUJET1]', sujets[0]).replace('[ID_SUJET2]', sujets[1])
    return "Je ne trouve pas cette information."

def handle_sout_rmq(question, responses):
    sujet_ids = extract_ids(question)
    final_responses = []
    
    if sujet_ids:
        for id_sujet in sujet_ids:
            sujet_info = find_stage_info_by_id(id_sujet)
            if sujet_info:
                remarques = sujet_info.get('remarque_sout', 'Aucune remarque de soutien trouvée')
                # Si remarques est une liste, on les transforme en chaîne de caractères
                if isinstance(remarques, list):
                    remarques = "; ".join(remarques)
                for response in responses:
                    final_responses.append(response.replace('[ID_SUJET]', id_sujet).replace('[REMARQUES]', remarques))
                return "\n".join(final_responses)
    
    return "Je ne trouve pas cette information."



def extract_societes(question):
    societes = []
    for societe in societes_data['Société']:
        if societe['nom'].lower() in question.lower():
            societes.append(societe['nom'])
    return societes

def extract_domaines(question):
    domaines = []
    for stage in stages_data['Stage']:
        domaine = stage['domaine'].lower()
        if domaine in question.lower():
            domaines.append(domaine)
    return list(set(domaines))  # Pour éviter les doublons

def extract_mode(question):
    modes = []
    for Societe in societes_data['Société']:
        if Societe['mode_travail'].lower() in question.lower():
            modes.append(Societe['mode_travail'])
    return modes

def extract_specialites(question):
    specialites = []
    for encadrant in encadrants_data['Encadrant']:
        if encadrant['spécialité'].lower() in question.lower():
            specialites.append(encadrant['spécialité'])
    return specialites

def extract_ids(question):
    ids = []
    for stage in stages_data['Stage']:
        if stage['id_sujet'].lower() in question.lower():
            ids.append(stage['id_sujet'])
    return ids

def extract_encadrants(question):
    encadrants = []
    question_words = question.lower().split()
    
    for encadrant in encadrants_data['Encadrant']:
        prenom = encadrant['prenom'].lower()
        nom = encadrant['nom'].lower()
        
        # Utiliser difflib pour trouver les correspondances les plus proches
        prenom_match = difflib.get_close_matches(prenom, question_words, n=1, cutoff=0.7)
        nom_match = difflib.get_close_matches(nom, question_words, n=1, cutoff=0.7)
        
        if prenom_match and nom_match:
            encadrants.append((encadrant['prenom'], encadrant['nom']))
    
    return encadrants



def extract_encadrants1(question):
    encadrants1 = []
    question_words = question.lower().split()
    
    for encadrant in encadrants_data['Encadrant']:
        prenom = encadrant['prenom'].lower()
        nom = encadrant['nom'].lower()
        
        # Utiliser difflib pour trouver les correspondances les plus proches
        prenom_match = difflib.get_close_matches(prenom, question_words, n=1, cutoff=0.7)
        nom_match = difflib.get_close_matches(nom, question_words, n=1, cutoff=0.7)
        
        if prenom_match or nom_match:
            encadrants1.append((encadrant['prenom'], encadrant['nom']))
    
    return encadrants1


def extract_ville(question):
    villes = []
    for encadrant in encadrants_data['Encadrant']:
        if encadrant['ville'].lower() in question.lower():
            villes.append(encadrant['ville'])
    return villes
    

# Fonctions de recherche dans les données


def find_societe_info(nom_societe):
    for societe in societes_data['Société']:
        if societe['nom'].lower() == nom_societe.lower():
            return societe
    return None

def find_societe_info_by_mode(mode_travail):
    for societe in societes_data['Société']:
        if societe['mode_travail'].lower() == mode_travail.lower():
            return societe
    return None

def find_stage_info_by_domaine(domaine):
    stages = []
    for stage in stages_data['Stage']:
        if stage['domaine'].lower() == domaine.lower():
            stages.append(stage)
    return stages

def find_stage_info_by_id(id_sujet):
    for stage in stages_data['Stage']:
        if stage['id_sujet'].lower() == id_sujet.lower():
            return stage
    return None

def find_encadrant_info(prenom, nom):
    for encadrant in encadrants_data['Encadrant']:
        if encadrant['prenom'].lower() == prenom.lower() and encadrant['nom'].lower() == nom.lower():
            return encadrant
    return None

def find_encadrant_info1(name):
    for encadrant in encadrants_data['Encadrant']:
        if encadrant['prenom'].lower() == name[0].lower() and encadrant['nom'].lower() == name[1].lower():
            return encadrant
    return None



def find_encadrants_by_specialite(specialite):
    matching_encadrants = []
    for encadrant in encadrants_data['Encadrant']:
        if encadrant['spécialité'].lower() == specialite.lower():
            matching_encadrants.append(encadrant)
    return matching_encadrants

# Fonction principale pour obtenir une réponse
def get_response(question):
    intent = predict_intent(question)
    print(f"Intent détecté: {intent}")  # Pour le débogage : affiche l'intention détectée

    responses = []
    for intent_data in intents_data['intents']:
        if intent_data['tag'] == intent:
            responses = intent_data['responses']
            break

    # Appel de la fonction appropriée pour gérer l'intention détectée
    if intent == "hallo":
        return handle_hallo()
    elif intent == "a plus":
        return handel_a_plus()
    elif intent == "option":
        return handel_option()
    elif intent == "Identitée":
        return handel_Identitée()
    elif intent == "quoi":
        return handel_quoi()
    elif intent == "insult":
        return handel_insult()
    elif intent == "activité":
        return handel_activité()
    elif intent == "remerciment":
        return handel_remerciment()
    elif intent == "exclaim":
        return handel_exclaim()
    elif intent == "appreciation":
        return handel_appreciation()
    elif intent == "sympatique":
        return handel_sympatique()
    elif intent == "non":
        return handel_non()
    elif intent == "greetreply":
        return handel_greetreply()
    elif intent == "suggestion":
        return handel_suggestion()
    elif intent == "ville":
        return handle_ville(question, responses)
    elif intent == "telephone":
        return handle_telephone(question, responses)
    elif intent == "email":
        return handle_email(question, responses)
    elif intent == "linkedin":
        return handle_linkedin(question, responses)
    elif intent == "description_stage":
        return handle_description_stage(question, responses)
    elif intent == "societe_stage":
        return handle_societe_stage(question, responses)
    elif intent == "specialite":
        return handle_specialite(question, responses)
    elif intent == "encadrant_stage":
        return handle_encadrant_stage(question, responses)
    elif intent == "remarque_stage":
        return handle_remarque_stage(question, responses)
    elif intent == "mode_travail_societe":
        return handle_mode_travail_societe(question, responses)
    elif intent == "experience_encadrant":
        return handle_experience_encadrant(question, responses)
    elif intent == "quota_encadrant":
        return handle_quota_encadrant(question, responses)
    elif intent == "niveaux_encadrant":
        return handle_niveaux_encadrant(question, responses)
    elif intent == "proposition_encadrant":
        return handle_proposition_encadrant(question, responses)
    elif intent == "disponibilite_encadrant":
        return handle_disponibilite_encadrant(question, responses)
    elif intent == "localisation_encadrant":
        return handle_localisation_encadrant(question, responses)
    elif intent == "societe_domaine":
        return handle_societe_domaine(question, responses)
    elif intent == "societe_mode":
        return handle_societe_mode(question, responses)
    elif intent == "comparaison_experience":
        return handle_comparaison_experience(question, responses)
    elif intent == "comparaison_sujet":
        return handle_comparaison_sujet(question, responses)
    elif intent == "sout_rmq":
        return handle_sout_rmq(question, responses)
    else:
        return "Je ne suis pas sûr de comprendre la question."
