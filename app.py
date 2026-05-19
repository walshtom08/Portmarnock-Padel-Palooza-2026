import streamlit as st
import pandas as pd

# Set up page config
st.set_page_config(page_title="Portmarnock Padel Palooza", layout="wide")

# Fixed CSS: Style text and background without breaking the table canvases
st.markdown("""
    <style>
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #000000 !important;
        color: #FFFF00 !important;
    }
    h1, h2, h3, h4, p, span, label {
        color: #FFFF00 !important;
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
st.write("Type scores directly into the tables below. Click 'Save & Sync Tournament Changes' at the bottom to lock them in!")

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
    {"ID": "F4", "Group": "Finals", "Wave": "
