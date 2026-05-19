import streamlit as st
import pandas as pd

st.set_page_config(page_title="Portmarnock Padel Palooza", layout="wide")

# CSS to make the scores stand out and adjust input styles
st.markdown("""
    <style>
    /* Dark theme overrides */
    html, body, [data-testid="stAppViewContainer"] { background-color: #000000 !important; color: #FFFF00 !important; }
    
    /* Highlight the score input fields */
    input[aria-label="Score 1"], input[aria-label="Score 2"] {
        background-color: #FF00FF !important; /* Magenta highlight */
        color: #FFFFFF !important;
        font-weight: bold !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🎾 Portmarnock Padel Palooza 🎾")

# ... (Keep your session_state definition as it was in the previous step) ...

def get_standings(group):
    # ... (Keep your existing standings logic) ...
    pass

def update_scores(key, df):
    # ... (Keep your existing update logic) ...
    pass

# Helper to define column configuration (Widths)
def get_col_config():
    return {
        "Wave": st.column_config.TextColumn("Wave", width="small"),
        "Time": st.column_config.TextColumn("Time", width="small"),
        "Court": st.column_config.TextColumn("Court", width="small"),
        "Score 1": st.column_config.NumberColumn("Score 1", width="small"),
        "Score 2": st.column_config.NumberColumn("Score 2", width="small"),
    }

# --- UI with column configuration ---
df = pd.DataFrame(st.session_state["matches"])

for g in ["Group A", "Group B"]:
    st.header(f"📊 {g} Fixtures")
    sub = df[df["Group"] == g].drop(columns=["Group", "Phase"], errors="ignore")
    
    st.data_editor(
        sub, 
        key=f"e_{g}", 
        hide_index=True, 
        use_container_width=True, 
        column_config=get_col_config(),
        on_change=update_scores, 
        args=(f"e_{g}", sub)
    )
    st.subheader(f"🏆 {g} Standings")
    st.dataframe(get_standings(g), hide_index=True, use_container_width=True)

# Repeat column_config for Knockout/Finals similarly
