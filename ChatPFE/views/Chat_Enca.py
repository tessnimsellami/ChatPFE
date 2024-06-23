import os
import json
import difflib
from sklearn.svm import LinearSVC
from sklearn.feature_extraction.text import CountVectorizer


# Chemin d'accès au répertoire contenant les données
data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')

# Charger les fichiers JSON avec le bon encodage
with open(os.path.join(data_dir, 'quest_resp_enca.json'), 'r', encoding='utf-8') as f:
    intents_data = json.load(f)


with open(os.path.join(data_dir, 'info_Etudiant.json'), 'r', encoding='utf-8') as f:
    etudiants_data = json.load(f)

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
    # Remplacement de synonymes
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


def handle_moyenne(question, responses):
    etudiants = extract_etudiants(question)
    etudiants1 = extract_etudiants1(question)
    final_responses = []

    if etudiants:
        for etudiant in etudiants:
            prenom, nom = etudiant
            etudiant_info = find_etudiant_info(prenom, nom)
            if etudiant_info:
                moyenne_etudiant = etudiant_info.get('moyenne', 'non renseignée')
                if moyenne_etudiant != 'non renseignée':
                    moyenne_etudiant = str(moyenne_etudiant)  # Convert to string if it's not already
                    for response in responses:
                        final_responses.append(response.replace('[FULL_NAME]', f"{prenom} {nom}").replace('[MOYENNE]', moyenne_etudiant))
    elif etudiants1:
        for etudiant in etudiants1:
            etudiant_info = find_etudiant_info1(etudiant)
            if etudiant_info:
                moyenne_etudiant = etudiant_info.get('moyenne', 'non renseignée')
                if moyenne_etudiant != 'non renseignée':
                    moyenne_etudiant = str(moyenne_etudiant)  # Convert to string if it's not already
                    for response in responses:
                        final_responses.append(response.replace('[FULL_NAME]', etudiant[0] + " " + etudiant[1]).replace('[MOYENNE]', moyenne_etudiant))
                        
    if final_responses:
        return "\n".join(final_responses)
    return "Je ne trouve pas cette information."


def handle_ville(question, responses):
    etudiants = extract_etudiants(question)
    etudiants1 = extract_etudiants1(question)
    societes = extract_societes(question)
    final_responses = []

    if etudiants:
        for etudiant in etudiants:
            prenom, nom = etudiant
            etudiant_info = find_etudiant_info(prenom, nom)
            if etudiant_info:
                ville_etudiant = etudiant_info.get('ville', 'non renseignée')
                if ville_etudiant != 'non renseignée':
                    for response in responses:
                        final_responses.append(response.replace('[FULL_NAME]', f"{prenom} {nom}").replace('[VILLE]', ville_etudiant))
    elif etudiants1:
        for etudiant in etudiants1:
            etudiant_info = find_etudiant_info1(etudiant)
            if etudiant_info:
                ville_etudiant = etudiant_info.get('ville', 'non renseignée')
                if ville_etudiant != 'non renseignée':
                    for response in responses:
                        final_responses.append(response.replace('[FULL_NAME]', etudiant[0] + " " + etudiant[1]).replace('[VILLE]', ville_etudiant))
    
    elif societes:                
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
    etudiants = extract_etudiants(question)
    etudiants1 = extract_etudiants1(question)
    societes = extract_societes(question)
    final_responses = []
    
    if etudiants:
        for etudiant in etudiants:
            prenom, nom = etudiant
            etudiant_info = find_etudiant_info(prenom, nom)
            if etudiant_info:
                telephone_etudiant = etudiant_info.get('telephone', 'non renseignée')
                if telephone_etudiant != 'non renseignée':
                    for response in responses:
                        final_responses.append(response.replace('[FULL_NAME]', f"{prenom} {nom}").replace('[TELEPHONE]', telephone_etudiant))
    elif etudiants1:
        for etudiant in etudiants1:
            etudiant_info = find_etudiant_info1(etudiant)
            if etudiant_info:
                telephone_etudiant = etudiant_info.get('telephone', 'non renseignée')
                if telephone_etudiant != 'non renseignée':
                    for response in responses:
                        final_responses.append(response.replace('[FULL_NAME]', etudiant[0] + " " + etudiant[1]).replace('[TELEPHONE]', telephone_etudiant))
                        
    elif societes:
        for societe in societes:
            societe_info = find_societe_info(societe)
            if societe_info:
                for response in responses:
                    final_responses.append(response.replace('[FULL_NAME]', societe).replace('[TELEPHONE]', societe_info.get('telephone', 'non renseigné')))
    
    if final_responses:
        return "\n".join(final_responses)
    return "Je ne trouve pas cette information."



def handle_email(question, responses):
    etudiants = extract_etudiants(question)
    etudiants1 = extract_etudiants1(question)
    societes = extract_societes(question)
    final_responses = []
    
    if etudiants:
        for etudiant in etudiants:
            prenom, nom = etudiant
            etudiant_info = find_etudiant_info(prenom, nom)
            if etudiant_info:
                for response in responses:
                    final_responses.append(response.replace('[FULL_NAME]', f"{prenom} {nom}").replace('[EMAIL]', etudiant_info.get('email', 'non renseignée')))
    elif etudiants1:
        for etudiant in etudiants1:
            etudiant_info = find_etudiant_info1(etudiant)
            if etudiant_info:
                for response in responses:
                    final_responses.append(response.replace('[FULL_NAME]', etudiant[0] + " " + etudiant[1]).replace('[EMAIL]', etudiant_info.get('email', 'non renseignée')))
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
    etudiants = extract_etudiants(question)
    etudiants1 = extract_etudiants1(question)
    societes = extract_societes(question)
    final_responses = []
    
    if etudiants:
        for etudiant in etudiants:
            prenom, nom = etudiant
            etudiant_info = find_etudiant_info(prenom, nom)
            if etudiant_info:
                link = etudiant_info.get('linkedin', 'non renseigné')
                if link == "":
                    for response in responses:
                        final_responses.append(response.replace('[FULL_NAME]', f"{prenom} {nom}").replace('[LINKEDIN]', "introuvable"))
                else :
                    for response in responses:
                        final_responses.append(response.replace('[FULL_NAME]', f"{prenom} {nom}").replace('[LINKEDIN]', etudiant_info.get('linkedin', 'non renseigné')))
    elif etudiants1:
        for etudiant in etudiants1:
            etudiant_info = find_etudiant_info1(etudiant)
            if etudiant_info:
                link = etudiant_info.get('linkedin', 'non renseigné')
                if link == "":
                    for response in responses:
                        final_responses.append(response.replace('[FULL_NAME]', etudiant[0] + " " + etudiant[1]).replace('[LINKEDIN]', "introuvable"))
                else :
                    for response in responses:
                        final_responses.append(response.replace('[FULL_NAME]', etudiant[0] + " " + etudiant[1]).replace('[LINKEDIN]', etudiant_info.get('linkedin', 'non renseigné')))
    elif societes:
        for societe in societes:
            societe_info = find_societe_info(societe)
            if societe_info:
                link = societe_info.get('linkedin', 'non renseigné')
                if link == "":
                    for response in responses:
                        final_responses.append(response.replace('[FULL_NAME]', societe).replace('[LINKEDIN]', "introuvable"))
                else :
                    for response in responses:
                        final_responses.append(response.replace('[FULL_NAME]', societe).replace('[LINKEDIN]', societe_info.get('linkedin', 'non renseigné')))
    if final_responses:
        return "\n".join(final_responses)
    return "Je ne trouve pas cette information."


def handle_preference(question, responses):
    etudiants = extract_etudiants(question)
    etudiants1 = extract_etudiants1(question)
    final_responses = []
    
    if etudiants:
        for etudiant in etudiants:
            prenom, nom = etudiant
            etudiant_info = find_etudiant_info(prenom, nom)
            if etudiant_info:
                for response in responses:
                    final_responses.append(response.replace('[FULL_NAME]', f"{prenom} {nom}").replace('[PREFERENCE]', etudiant_info.get('préférence', 'non renseignée')))
    elif etudiants1:
        for etudiant in etudiants1:
            etudiant_info = find_etudiant_info1(etudiant)
            if etudiant_info:
                for response in responses:
                    final_responses.append(response.replace('[FULL_NAME]', etudiant[0] + " " + etudiant[1]).replace('[PREFERENCE]', etudiant_info.get('préférence', 'non renseignée')))
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
    etudiants = extract_etudiants(question)
    etudiants1 = extract_etudiants1(question)
    societes = extract_societes(question)
    final_responses = []
    
    if etudiants:
        for etudiant in etudiants:
            prenom, nom = etudiant
            etudiant_info = find_etudiant_info(prenom, nom)
            if etudiant_info:
                for response in responses:
                    final_responses.append(response.replace('[FULL_NAME]', f"{prenom} {nom}").replace('[SPECIALITE]', etudiant_info.get('specialite', 'non renseignée')))
    elif etudiants1:
        for etudiant in etudiants1:
            etudiant_info = find_etudiant_info1(etudiant)
            if etudiant_info:
                for response in responses:
                    final_responses.append(response.replace('[FULL_NAME]', etudiant[0] + " " + etudiant[1]).replace('[SPECIALITE]', etudiant_info.get('specialite', 'non renseignée')))
    elif societes:
        for societe in societes:
            societe_info = find_societe_info(societe)
            if societe_info:
                for response in responses:
                    final_responses.append(response.replace('[FULL_NAME]', societe).replace('[SPECIALITE]', societe_info.get('domaine', 'non renseigné')))
    
    if final_responses:
        return "\n".join(final_responses)
    return "Je ne trouve pas cette information."

def handle_etudiant_stage(question, responses):
    ids = extract_ids(question)
    final_responses = []
    
    if ids:
        for id in ids:
            stage_info = find_stage_info_by_id(id)
            if stage_info:
                for response in responses:
                    final_responses.append(response.replace('[ID_SUJET]', id).replace('[FULL_NAME]', stage_info.get('etudiant', 'non renseigné')))
    if final_responses:
        return "\n".join(final_responses)
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

def handle_experience_etudiant(question, responses):
    etudiants = extract_etudiants(question)
    etudiants1 = extract_etudiants1(question)
    final_responses = []
    
    if etudiants:
        for etudiant in etudiants:
            prenom, nom = etudiant
            etudiant_info = find_etudiant_info(prenom, nom)
            if etudiant_info:
                experience = str(etudiant_info.get('experience', 'non renseignée'))  # Convertir en str
                for response in responses:
                    final_responses.append(response.replace('[FULL_NAME]', f"{prenom} {nom}").replace('[EXPERIENCE]', experience))
    elif etudiants1:
        for etudiant in etudiants1:
            etudiant_info = find_etudiant_info1(etudiant)
            if etudiant_info:
                experience = str(etudiant_info.get('experience', 'non renseignée'))  # Convertir en str
                for response in responses:
                    final_responses.append(response.replace('[FULL_NAME]', etudiant[0] + " " + etudiant[1]).replace('[EXPERIENCE]', experience))
                    
    if final_responses:
        return "\n".join(final_responses)
    return "Je ne trouve pas cette information."



def handle_niveaux_etudiant(question, responses):
    etudiants = extract_etudiants(question)
    etudiants1 = extract_etudiants1(question)
    final_responses = []
    
    if etudiants:
        for etudiant in etudiants:
            prenom, nom = etudiant
            etudiant_info = find_etudiant_info(prenom, nom)
            if etudiant_info:
                for response in responses:
                    final_responses.append(response.replace('[FULL_NAME]', f"{prenom} {nom}").replace('[NIVEAU]', etudiant_info.get('niveau', 'non renseignés')))
    elif etudiants1:
        for etudiant in etudiants1:
            etudiant_info = find_etudiant_info1(etudiant)
            if etudiant_info:
                for response in responses:
                    final_responses.append(response.replace('[FULL_NAME]', etudiant[0] + " " + etudiant[1]).replace('[NIVEAU]', etudiant_info.get('niveau', 'non renseignés')))
                
    if final_responses:
        return "\n".join(final_responses)
    return "Je ne trouve pas cette information."

def handle_proposition_etudiant(question, responses):
    specialites = extract_specialites(question)
    if specialites:
        final_response = ""
        for specialite in specialites:
            etudiants_matching = find_etudiants_by_specialite(specialite)
            if etudiants_matching:
                for etudiant_info in etudiants_matching:
                    prenom = etudiant_info['prenom']
                    nom = etudiant_info['nom']
                    for response in responses:
                        final_response += response.replace('[FULL_NAME]', f"{prenom} {nom}").replace('[SPECIALITE]', etudiant_info.get('specialite', 'non renseignées')) + "\n"
            else:
                final_response = "Je ne trouve pas d'etudiant avec cette spécialité."
        return final_response.strip()
    return "Je ne trouve pas cette information."



def handle_localisation_etudiant(question, responses):
    villes_question = extract_ville(question)
    final_response = ""

    for etudiant_info in etudiants_data['Etudiant']:
        prenom = etudiant_info['prenom']
        nom = etudiant_info['nom']
        ville_etudiant = etudiant_info.get('ville', 'non renseignée')

        if any(ville_etudiant.lower() == ville.lower() for ville in villes_question):
            for response in responses:
                final_response += response.replace('[FULL_NAME]', f"{prenom} {nom}").replace('[VILLE]', ville_etudiant) + "\n"

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


def handle_comparaison_etudiant(question, responses):
    etudiants = extract_etudiants(question)
    etudiants1 = extract_etudiants1(question)
    
    if not etudiants and not etudiants1:
        return "Aucun étudiant trouvé dans la question."
    
    meilleur_etudiant = None
    meilleure_moyenne = -1
    etudiant_info = []
    
    for etudiant in etudiants:
        prenom, nom = etudiant
        info = find_etudiant_info(prenom, nom)
        if info:
            etudiant_info.append(info)
        
    for etudiant in etudiants1:
        info = find_etudiant_info1(etudiant)
        if info:
            etudiant_info.append(info)
        
    for info in etudiant_info:
        if info:
            moyenne = info['moyenne']
            if moyenne > meilleure_moyenne:
                meilleure_moyenne = moyenne
                meilleur_etudiant = info
    
    if meilleur_etudiant:
        response = f"L'étudiant avec la meilleure moyenne est {meilleur_etudiant['prenom']} {meilleur_etudiant['nom']} avec une moyenne de {meilleure_moyenne}."
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
    for etudiant in etudiants_data['Etudiant']:
        if etudiant['specialite'].lower() in question.lower():
            specialites.append(etudiant['specialite'])
    return specialites

def extract_ids(question):
    ids = []
    for stage in stages_data['Stage']:
        if stage['id_sujet'].lower() in question.lower():
            ids.append(stage['id_sujet'])
    return ids

def extract_etudiants(question):
    etudiants = []
    question_words = question.lower().split()
    
    for etudiant in etudiants_data['Etudiant']:
        prenom = etudiant['prenom'].lower()
        nom = etudiant['nom'].lower()
        
        # Utiliser difflib pour trouver les correspondances les plus proches
        prenom_match = difflib.get_close_matches(prenom, question_words, n=1, cutoff=0.7)
        nom_match = difflib.get_close_matches(nom, question_words, n=1, cutoff=0.7)
        
        if prenom_match and nom_match:
            etudiants.append((etudiant['prenom'], etudiant['nom']))
    
    return etudiants



def extract_etudiants1(question):
    etudiants1 = []
    question_words = question.lower().split()
    
    for etudiant in etudiants_data['Etudiant']:
        prenom = etudiant['prenom'].lower()
        nom = etudiant['nom'].lower()
        
        # Utiliser difflib pour trouver les correspondances les plus proches
        prenom_match = difflib.get_close_matches(prenom, question_words, n=1, cutoff=0.7)
        nom_match = difflib.get_close_matches(nom, question_words, n=1, cutoff=0.7)
        
        if prenom_match or nom_match:
            etudiants1.append((etudiant['prenom'], etudiant['nom']))
    
    return etudiants1



def extract_ville(question):
    villes = []
    for etudiant in etudiants_data['Etudiant']:
        if etudiant['ville'].lower() in question.lower():
            villes.append(etudiant['ville'])
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

def find_societe_info_domaine(domaine):
    for societe in societes_data['Société']:
        if societe['domaine'].lower() == domaine.lower():
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

def find_etudiant_info(prenom, nom):
    for etudiant in etudiants_data['Etudiant']:
        if etudiant['prenom'].lower() == prenom.lower() and etudiant['nom'].lower() == nom.lower():
            return etudiant
    return None

def find_etudiant_info1(name):
    for etudiant in etudiants_data['Etudiant']:
        if etudiant['prenom'].lower() == name[0].lower() and etudiant['nom'].lower() == name[1].lower():
            return etudiant
    return None



def find_etudiants_by_specialite(specialite):
    matching_etudiants = []
    for etudiant in etudiants_data['Etudiant']:
        if etudiant['specialite'].lower() == specialite.lower():
            matching_etudiants.append(etudiant)
    return matching_etudiants

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
    elif intent == "remerciment":
        return handel_remerciment()
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
    elif intent == "moyenne":
        return handle_moyenne(question, responses)
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
    elif intent == "preference":
        return handle_preference(question, responses)
    elif intent == "societe_stage":
        return handle_societe_stage(question, responses)
    elif intent == "specialite":
        return handle_specialite(question, responses)
    elif intent == "etudiant_stage":
        return handle_etudiant_stage(question, responses)
    elif intent == "remarque_stage":
        return handle_remarque_stage(question, responses)
    elif intent == "mode_travail_societe":
        return handle_mode_travail_societe(question, responses)
    elif intent == "experience_etudiant":
        return handle_experience_etudiant(question, responses)
    elif intent == "niveau":
        return handle_niveaux_etudiant(question, responses)
    elif intent == "proposition_etudiant":
        return handle_proposition_etudiant(question, responses)
    elif intent == "localisation_etudiant":
        return handle_localisation_etudiant(question, responses)
    elif intent == "societe_domaine":
        return handle_societe_domaine(question, responses)
    elif intent == "comparaison_etudiant":
        return handle_comparaison_etudiant(question, responses)
    elif intent == "comparaison_sujet":
        return handle_comparaison_sujet(question, responses)
    elif intent == "sout_rmq":
        return handle_sout_rmq(question, responses)
    else:
        return "Je ne suis pas sûr de comprendre la question."
