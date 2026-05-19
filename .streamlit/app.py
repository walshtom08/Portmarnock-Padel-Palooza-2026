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
    div[data-baseweb="popover"] {
        background-color: #111111 !important;
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
st.write("Enter scores below. Updates sync instantly for everyone!")

# --- DATA INITIALIZATION ---
# Raw match schedule from your file
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

# Establish multi-user persistent cloud storage using Streamlit's built-in key-value connection
try:
    conn = st.connection("cache", type="dict")
except Exception:
    # Fallback to local session state if cloud context isn't fully ready yet
    conn = st.session_state

if "matches" not in conn:
    conn["matches"] = initial_matches

matches = conn["matches"]

# --- SIDEBAR: SCORE INPUT ---
st.sidebar.header("🏆 Update Match Scores")
match_options = {f"{m['Wave']} - {m['Phase']} ({m['Team 1']} v {m['Team 2']})": m['ID'] for m in matches}
selected_match_label = st.sidebar.selectbox("Select Match to Score", list(match_options.keys()))
selected_id = match_options[selected_match_label]

# Find selected match data
match_idx = next(i for i, m in enumerate(matches) if m["ID"] == selected_id)
current_match = matches[match_idx]

st.sidebar.write(f"**Court:** {current_match['Court']} | **Time:** {current_match['Time']}")
s1 = st.sidebar.number_input(f"Score for: {current_match['Team 1']}", min_value=0, value=int(current_match['Score 1']), step=1)
s2 = st.sidebar.number_input(f"Score for: {current_match['Team 2']}", min_value=0, value=int(current_match['Score 2']), step=1)

if st.sidebar.button("Save & Sync Score"):
    matches[match_idx]["Score 1"] = s1
    matches[match_idx]["Score 2"] = s2
    conn["matches"] = matches
    st.sidebar.success("Scores uploaded successfully!")
    st.rerun()

# --- MAIN DISPLAY TABLES ---
df = pd.DataFrame(matches)

st.header("📊 Group A Fixtures")
df_a = df[df["Group"] == "Group A"][["Wave", "Phase", "Time", "Court", "Team 1", "Score 1", "Team 2", "Score 2"]]
st.dataframe(df_a, use_container_width=True, hide_index=True)

st.header("📊 Group B Fixtures")
df_b = df[df["Group"] == "Group B"][["Wave", "Phase", "Time", "Court", "Team 1", "Score 1", "Team 2", "Score 2"]]
st.dataframe(df_b, use_container_width=True, hide_index=True)

st.header("⚔️ Knockout Stage")
df_ko = df[df["Group"] == "Knockout"][["Wave", "Phase", "Time", "Court", "Team 1", "Score 1", "Team 2", "Score 2"]]
st.dataframe(df_ko, use_container_width=True, hide_index=True)

st.header("🏆 The Finals")
df_f = df[df["Group"] == "Finals"][["Wave", "Phase", "Time", "Court", "Team 1", "Score 1", "Team 2", "Score 2"]]
st.dataframe(df_f, use_container_width=True, hide_index=True)
