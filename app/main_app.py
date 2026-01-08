import streamlit as st
import sys
import os

# 1. FIX DES IMPORTS
# On récupère le chemin absolu du dossier /app pour éviter les erreurs de module
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

# 2. IMPORTS DES MODULES (Vérifie bien que les fichiers existent dans /app)
try:
    from single_asset import run_quant_a
    from quant_b import run_quant_b
except ImportError as e:
    st.error(f"Erreur d'importation : {e}")

# 3. CONFIGURATION DE LA PAGE
st.set_page_config(page_title="Plateforme Quant", layout="wide")

# 4. NAVIGATION SIDEBAR
st.sidebar.title("🚀 Navigation")
page = st.sidebar.radio("Choisir un module", ["Accueil", "Analyse Mono-Actif (A)", "Gestion Portefeuille (B)"])

# 5. LOGIQUE D'AFFICHAGE
if page == "Accueil":
    st.title("📊 Bienvenue sur votre Plateforme Finance")
    st.markdown("""
    Cette plateforme regroupe vos outils d'analyse quantitative :
    * **Module A** : Analyse d'un actif unique et backtesting.
    * **Module B** : Gestion de portefeuille multi-actifs et corrélations.
    """)
    st.info("Utilisez le menu à gauche pour naviguer.")

elif page == "Analyse Mono-Actif (A)":
    run_quant_a()

elif page == "Gestion Portefeuille (B)":
    run_quant_b()
