import streamlit as st
import sys
import os
from streamlit_autorefresh import st_autorefresh  # Required for project requirement #5

# 1. FIX IMPORT PATHS
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

# 2. PAGE CONFIGURATION (Must be the very first Streamlit command)
st.set_page_config(page_title="Quant Platform", layout="wide")

# 3. AUTO-REFRESH (Requirement #5: every 5 minutes)
# 300,000 ms = 5 minutes
st_autorefresh(interval=300_000, key="datarefresh")

# 4. MODULE IMPORTS
try:
    from single_asset import run_quant_a
    from portfolio import run_quant_b
except ImportError as e:
    st.error(
        f"Import error: {e}. Please check that file names are correct."
    )

# 5. SIDEBAR NAVIGATION
st.sidebar.title("🚀 Navigation")
page = st.sidebar.radio(
    "Choose a module",
    ["Home", "Single Asset Analysis (A)", "Portfolio Management (B)"]
)

# 6. DISPLAY LOGIC
if page == "Home":
    st.title("📊 Welcome to Your Quant Finance Platform")
    st.markdown("""
    This platform brings together your quantitative analysis tools:
    * **Module A**: Single asset analysis and backtesting.
    * **Module B**: Multi-asset portfolio management and correlation analysis.
    """)
    st.info("Use the menu on the left to navigate.")

elif page == "Single Asset Analysis (A)":
    # Check that the function was correctly imported before calling it
    if 'run_quant_a' in locals() or 'run_quant_a' in globals():
        run_quant_a()
    else:
        st.error("Module A could not be loaded.")

elif page == "Portfolio Management (B)":
    if 'run_quant_b' in locals() or 'run_quant_b' in globals():
        run_quant_b()
    else:
        st.error("Module B could not be loaded.")
