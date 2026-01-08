import streamlit as st
import sys
import os
from streamlit_autorefresh import st_autorefresh # Nécessaire pour le point #5 du projet

# 1. FIX DES IMPORTS
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

# 2. CONFIGURATION DE LA PAGE (Doit être la toute première commande Streamlit)
st.set_page_config(page_title="Plateforme Quant", layout="wide")

# 3. RAFRAÎCHISSEMENT AUTOMATIQUE (Exigence #5 : toutes les 5 minutes)
# 300 000 ms = 5 minutes
st_autorefresh(interval=300000, key="datarefresh") 

# 4. IMPORTS DES MODULES
try:
    from single_asset import run_quant_a
    from portfolio import run_quant_b
except ImportError as e:
    st.error(f"Erreur d'importation : {e}. Vérifiez que les noms de fichiers sont corrects.")

# 5. NAVIGATION SIDEBAR
st.sidebar.title("🚀 Navigation")
page = st.sidebar.radio("Choisir un module", ["Accueil", "Analyse Mono-Actif (A)", "Gestion Portefeuille (B)"])

# 6. LOGIQUE D'AFFICHAGE
if page == "Accueil":
    st.title("📊 Bienvenue sur votre Plateforme Finance")
    st.markdown("""
    Cette plateforme regroupe vos outils d'analyse quantitative :
    * **Module A** : Analyse d'un actif unique et backtesting. [cite: 31, 33]
    * **Module B** : Gestion de portefeuille multi-actifs et corrélations. [cite: 40, 42]
    """)
    st.info("Utilisez le menu à gauche pour naviguer.")

elif page == "Analyse Mono-Actif (A)":
    # On vérifie si la fonction a bien été importée avant de l'appeler
    if 'run_quant_a' in locals() or 'run_quant_a' in globals():
        run_quant_a()
    else:
        st.error("Le module A n'a pas pu être chargé.")

elif page == "Gestion Portefeuille (B)":
    if 'run_quant_b' in locals() or 'run_quant_b' in globals():
        run_quant_b()
    else:
        st.error("Le module B n'a pas pu être chargé.")
