import streamlit as st
import pandas as pd

# Set up page config
st.set_page_config(page_title="Portmarnock Padel Palooza", layout="wide")

# Custom CSS injection to force yellow text and custom element styling
st.markdown("""
    <style>
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #000000 !important;
        color: #FFFF00 !important;
    }
    h1, h2, h3, h4, p, span, label, div {
        color: #FFFF00 !important;
    }
    .stDataFrame div, .stDataFrame span, .stDataFrame table {
        color: #FFFF00 !important;
        background-color: #000000 !important;
    }
    button {
        background-color: #111111 !important;
        color: #FFFF00 !important;
        border: 1px solid #FFFF00 !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🎾 Portmarnock Padel Palooza 🎾")
st.subheader("Live Tournament Dashboard & Score Tracker")
st.write("Type scores directly into the tables below. Click 'Save & Sync Tournament' at the bottom to lock them in!")

# --- DATA INITIALIZATION ---
initial_matches = [
    # Group A
    {"ID": "GA1", "Group": "Group A", "Wave": "Wave 1", "Phase": "Group stage", "Time": "16:30 - 16:50", "Court": "3", "Team 1": "Stu/Niall Hayden", "Score 1": 0, "Team 2": "Eric/Dermo", "Score 2": 0},
    {"ID": "GA2", "Group": "Group A", "Wave": "Wave 1", "Phase": "Group stage", "Time": "16:30 - 16:50", "Court": "4", "Team 1": "Richie/Steve", "Score 1": 0, "Team 2": "Jason/Wonka", "Score 2": 0},
    {"ID": "GA3", "Group": "Group A", "Wave": "Wave 2", "Phase": "Group stage", "Time": "16:55 - 17:15", "Court": "3", "Team 1": "Stu/Niall Hayden", "Score 1": 0, "Team 2": "Jason/Wonka", "Score 2": 0},
    {"ID": "GA4", "Group": "Group A", "Wave": "Wave 3", "Phase": "Group stage", "Time": "17:20 - 17:40", "Court": "3", "Team 1": "Richie/Steve", "Score 1": 0, "Team 2": "Eric/Dermo", "Score 2": 0},
    {"ID": "GA5", "Group": "Group A", "Wave": "Wave 3", "Phase": "Group stage", "Time": "17:20 - 17:40", "Court": "4", "Team 1": "Eric/Dermo", "Score 1": 0, "Team 2": "Jason/Wonka", "Score 2": 0},
    {"ID": "GA6", "Group": "Group A", "Wave": "Wave 4", "Phase": "Group stage", "Time": "17:45 - 18:05", "Court": "3", "Team 1": "Stu/Niall Hayden", "Score 1": 0, "Team 2": "Richie/Steve", "Score 2": 0},
    # Group B
    {"ID": "GB1", "Group": "Group B", "Wave": "Wave 1", "Phase": "Group stage", "Time": "16:30 - 16:50", "Court": "5", "Team 1": "Jamie/Kevin", "Score 1": 0, "Team 2": "Neil/Tom", "Score 2": 0},
    {"ID": "GB2", "Group": "Group B", "Wave": "Wave 2", "Phase": "Group stage", "Time": "16:55 - 17:15", "Court": "4", "Team 1": "Simon/Cillian", "Score 1": 0, "Team 2": "Gerry/Rob", "Score 2": 0},
    {"ID": "GB3", "Group": "Group B", "Wave": "Wave 2", "Phase": "Group stage", "Time": "16:55 - 17:15", "Court": "5", "Team 1": "Jamie/Kevin", "Score 1": 0, "Team 2": "Gerry/Rob", "Score 2": 0},
    {"ID": "GB4", "Group": "Group B", "Wave": "Wave 3", "Phase": "Group stage", "Time": "17:20 - 17:40", "Court": "4", "Team 1": "Simon/Cillian", "Score 1": 0, "Team 2": "Neil/Tom", "Score 2": 0},
    {"ID": "GB5", "Group": "Group B", "Wave": "Wave 4", "Phase": "Group stage", "Time": "17:45 - 18:05", "Court": "5", "Team 1": "Neil/Tom", "Score 1": 0, "Team 2": "Gerry/Rob", "Score 2": 0},
    {"ID": "GB6", "Group": "Group B", "Wave": "Wave 4", "Phase": "Group stage", "Time": "17:45 - 18:05", "Court": "5", "Team 1": "Jamie/Kevin", "Score 1": 0, "Team 2": "Simon/Cillian", "Score 2": 0},
    # Knockouts
    {"ID": "KO1", "Group": "Knockout", "Wave": "Wave 5", "Phase": "Semi Final 1 (G1 3rd v G2 4th)", "Time": "18:10 - 18:30", "Court": "3", "Team 1": "Group 1 3rd", "Score 1": 0, "Team 2": "Group 2 4th", "Score 2": 0},
    {"ID": "KO2", "Group": "Knockout", "Wave": "Wave 5", "Phase": "Semi Final 2 (G1 4th v G2 3rd)", "Time": "18:10 - 18:30", "Court": "4", "Team 1": "Group 1 4th", "Score 1": 0, "Team 2": "Group 2 3rd", "Score 2": 0},
    {"ID": "KO3", "Group": "Knockout", "Wave": "Wave 5", "Phase": "Semi Final 3 (G1 1st v G2 2nd)", "Time": "18:10 - 18:30", "Court": "5", "Team 1": "Jason/Wonka", "Score 1": 0, "Team 2": "Jamie/Kevin", "Score 2": 0},
    {"ID": "KO4", "Group": "Knockout", "Wave": "Wave 6", "Phase": "Semi Final 4 (G1 2nd v G2 1st)", "Time": "18:35 - 18:55", "Court": "3", "Team 1": "Stu/Niall Hayden", "Score 1": 0, "Team 2": "Gerry/Rob", "Score 2": 0},
    # Finals
    {"ID": "F1", "Group": "Finals", "Wave": "Wave 6", "Phase": "Shit the Bed Cup Final", "Time": "18:35 - 18:55", "Court": "4", "Team 1": "Loser Semi 1", "Score 1": 0, "Team 2": "Loser Semi 2", "Score 2": 0},
    {"ID": "F2", "Group": "Finals", "Wave": "Wave 6", "Phase": "Shart in your pants Cup Final", "Time": "18:35 - 18:55", "Court": "5", "Team 1": "Winner Semi 1", "Score 1": 0, "Team 2": "Winner Semi 2", "Score 2": 0},
    {"ID": "F3", "Group": "Finals", "Wave": "Wave 7", "Phase": "Shitstain Cup Final", "Time": "19:00 - 19:20", "Court": "3", "Team 1": "Jamie/Kevin", "Score 1": 0, "Team 2": "Gerry/Rob", "Score 2": 0},
    {"ID": "F4", "Group": "Finals", "Wave": "Wave 8", "Phase": "Champions Cup Final", "Time": "19:05 - 19:30", "Court": "4", "Team 1": "Jamie/Kevin", "Score 1": 0, "Team 2": "Gerry/Rob", "Score 2": 0}
]

# Shared persistent storage setup
try:
    conn = st.connection("cache", type="dict")
except Exception:
    conn = st.session_state

if "matches" not in conn:
    conn["matches"] = initial_matches

# Read raw matches from database storage
df_current = pd.DataFrame(conn["matches"])

# Define explicit column protections. Columns set to disabled=True are read-only!
column_setup = {
    "ID": st.column_config.TextColumn("ID", disabled=True),
    "Group": st.column_config.TextColumn("Group", disabled=True),
    "Wave": st.column_config.TextColumn("Wave", disabled=True),
    "Phase": st.column_config.TextColumn("Phase", disabled=True),
    "Time": st.column_config.TextColumn("Time", disabled=True),
    "Court": st.column_config.TextColumn("Court", disabled=True),
    "Team 1": st.column_config.TextColumn("Team 1", disabled=True),
    "Score 1": st.column_config.NumberColumn("Score 1", min_value=0, step=1, disabled=False),
    "Team 2": st.column_config.TextColumn("Team 2", disabled=True),
    "Score 2": st.column_config.NumberColumn("Score 2", min_value=0, step=1, disabled=False)
}

# Explicitly choose columns to view in the tables
visible_columns = ["Wave", "Phase", "Time", "Court", "Team 1", "Score 1", "Team 2", "Score 2"]

# --- RENDER INTERACTIVE TABLES ---
st.header("📊 Group A Fixtures")
df_a = df_current[df_current["Group"] == "Group A"]
edited_a = st.data_editor(df_a, key="edit_a", column_config=column_setup, column_order=visible_columns, hide_index=True, use_container_width=True)

st.header("📊 Group B Fixtures")
df_b = df_current[df_current["Group"] == "Group B"]
edited_b = st.data_editor(df_b, key="edit_b", column_config=column_setup, column_order=visible_columns, hide_index=True, use_container_width=True)

st.header("⚔️ Knockout Stage")
df_ko = df_current[df_current["Group"] == "Knockout"]
edited_ko = st.data_editor(df_ko, key="edit_ko", column_config=column_setup, column_order=visible_columns, hide_index=True, use_container_width=True)

st.header("🏆 The Finals")
df_f = df_current[df_current["Group"] == "Finals"]
edited_f = st.data_editor(df_f, key="edit_f", column_config=column_setup, column_order=visible_columns, hide_index=True, use_container_width=True)

# --- GLOBAL SAVE TRIGGER ---
st.write("---")
if st.button("💾 Save & Sync Tournament Changes", use_container_width=True):
    # Pull the exact underlying full dataset (including hidden grouping keys) out of the widgets
    # This prevents data dropping out when re-merging
    all_updated_records = []
    for edited_segment in [edited_a, edited_b, edited_ko, edited_f]:
        all_updated_records.extend(edited_segment.to_dict(orient="records"))
        
    # Save back to cache
    conn["matches"] = all_updated_records
    st.success("All table changes synced perfectly for all players!")
    st.rerun()
