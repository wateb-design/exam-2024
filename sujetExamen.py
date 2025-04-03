import streamlit as st
import random

# Simuler une base de données d’utilisateurs (nom d'utilisateur : mot de passe)
users = {"eleve1": "pass123", "eleve2": "bac2025"}

# Suivi des scores
def get_score():
    if "score" not in st.session_state:
        st.session_state["score"] = {}
    return st.session_state["score"]

# QCM de mathématiques, informatique et anglais
qcm_data = {
    "maths": [
        {"question": "Quel est le résultat de 2x + 3 = 7 ?", "options": ["x=2", "x=3", "x=4"], "answer": "x=2"},
        {"question": "La dérivée de x^2 est ?", "options": ["2x", "x^2", "x"], "answer": "2x"},
        {"question": "Quel est le résultat de 5 + 7 * 2 ?", "options": ["24", "19", "17"], "answer": "19"},
        {"question": "L'intégrale de 1/x dx est ?", "options": ["ln(x)", "x", "x^2/2"], "answer": "ln(x)"},
        {"question": "Quelle est la formule du périmètre d'un cercle ?", "options": ["πr^2", "2πr", "r^2"], "answer": "2πr"}
    ],
    "informatique": [
        {"question": "Quel est le langage utilisé pour le développement web front-end ?", "options": ["Python", "HTML", "Java"], "answer": "HTML"},
        {"question": "Que signifie CSS ?", "options": ["Cascading Style Sheets", "Computer Style Syntax", "Centralized System Software"], "answer": "Cascading Style Sheets"},
        {"question": "Quelle est la principale fonction de JavaScript ?", "options": ["Mise en page", "Interaction utilisateur", "Gestion des bases de données"], "answer": "Interaction utilisateur"},
        {"question": "Quel est le type de base de données le plus couramment utilisé ?", "options": ["SQL", "NoSQL", "XML"], "answer": "SQL"},
        {"question": "Que signifie HTTP ?", "options": ["HyperText Transfer Protocol", "Hyperlink Text Transmission Protocol", "High Transfer Text Protocol"], "answer": "HyperText Transfer Protocol"}
    ],
    "anglais": [
        {"question": "Comment dit-on 'chien' en anglais ?", "options": ["Dog", "Cat", "Horse"], "answer": "Dog"},
        {"question": "Quelle est la traduction de 'maison' en anglais ?", "options": ["House", "Car", "Tree"], "answer": "House"},
        {"question": "Comment traduit-on 'ordinateur' en anglais ?", "options": ["Computer", "Tablet", "Phone"], "answer": "Computer"},
        {"question": "Quel est le synonyme de 'big' en anglais ?", "options": ["Small", "Large", "Tiny"], "answer": "Large"},
        {"question": "Quelle est la forme correcte du verbe 'to be' au passé pour 'he' ?", "options": ["Was", "Were", "Be"], "answer": "Was"}
    ]
}

# Authentification
def login():
    st.title("Connexion")
    username = st.text_input("Nom d'utilisateur")
    password = st.text_input("Mot de passe", type="password")
    if st.button("Se connecter"):
        if username in users and users[username] == password:
            st.session_state["authenticated"] = True
            st.session_state["username"] = username
            st.success("Connexion réussie !")
        else:
            st.error("Identifiants incorrects")

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    login()
else:
    st.sidebar.button("Se déconnecter", on_click=lambda: st.session_state.update({"authenticated": False}))
    st.title("Préparation au Bac - QCM")
    subject = st.selectbox("Choisissez une matière", ["maths", "informatique", "anglais"])
    
    if subject:
        questions = random.sample(qcm_data[subject], len(qcm_data[subject]))  # Mélanger les questions
        score = 0
        responses = []
        
        for i, q in enumerate(questions):
            st.subheader(f"Q{i+1}: {q['question']}")
            choice = st.radio("", q["options"], key=f"q{i}")
            responses.append((q, choice))
        
        if st.button("Valider les réponses"):
            for q, choice in responses:
                if choice == q["answer"]:
                    score += 1
            st.success(f"Votre score : {score}/{len(questions)}")
            
            # Mettre à jour le score de l'utilisateur
            scores = get_score()
            username = st.session_state["username"]
            if username not in scores:
                scores[username] = {}
            scores[username][subject] = score
            st.write("## Suivi de vos scores")
            for matiere, sc in scores[username].items():
                st.write(f"**{matiere.capitalize()}** : {sc}/{len(qcm_data[matiere])}")
            
            st.subheader("Correction")
            for q, choice in responses:
                st.write(f"**{q['question']}**")
                st.write(f"✅ Réponse correcte : {q['answer']}")
                st.write(f"📝 Votre réponse : {choice}")
                st.write("---")

