import streamlit as st
import sys
import os

# Ajoute le dossier app au chemin pour que les imports fonctionnent
sys.path.append(os.path.dirname(__file__))

# Import des fonctions depuis vos fichiers respectifs
from single_asset import run_quant_a
from portfolio import run_quant_b

st.set_page_config(page_title="Plateforme Quant", layout="wide")

st.sidebar.title("Navigation")
page = st.sidebar.radio("Choisir un module", ["Accueil", "Analyse Mono-Actif (A)", "Gestion Portefeuille (B)"])

if page == "Accueil":
    st.title("Bienvenue sur votre Plateforme Finance")
    st.write("Utilisez le menu à gauche pour naviguer entre les outils d'analyse.")
elif page == "Analyse Mono-Actif (A)":
    run_quant_a()
elif page == "Gestion Portefeuille (B)":
    run_quant_b()
