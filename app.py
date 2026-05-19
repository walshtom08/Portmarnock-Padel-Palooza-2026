import streamlit as st
import pandas as pd

st.set_page_config(page_title="Padel Palooza", layout="wide")

# CSS: Optimizing for Mobile
st.markdown("""
    <style>
    /* Compact everything for mobile */
    [data-testid="stAppViewContainer"] { background-color: #000000; }
    .stApp { padding-left: 5px !important; padding-right: 5px !important; }
    
    /* Make score inputs stand out on phone */
    input[aria-label="Score 1"], input[aria-label="Score 2"] {
        background-color: #FFFF00 !important; 
        color: #000000 !important;
        font-weight: bold !important;
        text-align: center;
    }
    /* Force table cells to be tight */
    .stDataEditor { width: 100% !important; }
    </style>
""", unsafe_allow_html=True)

# [Matches initialization as before]
if "matches" not in st.session_state:
    st.session_state["matches"] = [
        {"Group": "Group A", "Wave": "W1", "Time": "16:30", "Team 1": "Stu/Niall", "Score 1": 0, "Team 2": "Eric/Dermo", "Score 2": 0},
        {"Group": "Group A", "Wave": "W1", "Time": "16:30", "Team 1": "Richie/Steve", "Score 1": 0, "Team 2": "Jason/Wonka", "Score 2": 0},
        {"Group": "Group B", "Wave": "W1", "Time": "16:30", "Team 1": "Jamie/Kevin", "Score 1": 0, "Team 2": "Neil/Tom", "Score 2": 0},
        {"Group": "Group B", "Wave": "W2", "Time": "16:55", "Team 1": "Simon/Cillian", "Score 1": 0, "Team 2": "Gerry/Rob", "Score 2": 0},
    ]

# [Keep your existing get_standings and update_scores functions here]

# UI - Optimized for narrow screens
st.title("🎾 Padel Palooza")

col_config = {
    "Wave": st.column_config.TextColumn(width="small"),
    "Time": st.column_config.TextColumn(width="small"),
    "Score 1": st.column_config.NumberColumn(width="small"),
    "Score 2": st.column_config.NumberColumn(width="small"),
}

df = pd.DataFrame(st.session_state["matches"])

for g in ["Group A", "Group B"]:
    st.subheader(f"📊 {g}")
    sub = df[df["Group"] == g].drop(columns=["Group"], errors="ignore")
    # For iPhone: Use data_editor to allow rapid editing
    st.data_editor(sub, key=f"e_{g}", hide_index=True, use_container_width=True, 
                   column_config=col_config, on_change=update_scores, args=(f"e_{g}", sub))

st.write("---")
# Add a simple refresh button for mobile
if st.button("🔄 Refresh View"):
    st.rerun()
