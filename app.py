import streamlit as st
import pandas as pd

st.set_page_config(page_title="Portmarnock Padel Palooza", layout="wide")

st.markdown("""
    <style>
    html, body, [data-testid="stAppViewContainer"] { background-color: #000000 !important; color: #FFFF00 !important; }
    h1, h2, h3, h4, p, span, label { color: #FFFF00 !important; }
    </style>
""", unsafe_allow_html=True)

st.title("🎾 Portmarnock Padel Palooza 🎾")

if "matches" not in st.session_state:
    st.session_state["matches"] = [
        # Group A
        {"Group": "Group A", "Wave": "W1", "Time": "16:30", "Court": "3", "Team 1": "Stu/Niall", "Score 1": 0, "Team 2": "Eric/Dermo", "Score 2": 0},
        {"Group": "Group A", "Wave": "W1", "Time": "16:30", "Court": "4", "Team 1": "Richie/Steve", "Score 1": 0, "Team 2": "Jason/Wonka", "Score 2": 0},
        {"Group": "Group A", "Wave": "W2", "Time": "16:55", "Court": "3", "Team 1": "Stu/Niall", "Score 1": 0, "Team 2": "Jason/Wonka", "Score 2": 0},
        {"Group": "Group A", "Wave": "W3", "Time": "17:20", "Court": "3", "Team 1": "Richie/Steve", "Score 1": 0, "Team 2": "Eric/Dermo", "Score 2": 0},
        {"Group": "Group A", "Wave": "W3", "Time": "17:20", "Court": "4", "Team 1": "Eric/Dermo", "Score 1": 0, "Team 2": "Jason/Wonka", "Score 2": 0},
        {"Group": "Group A", "Wave": "W4", "Time": "17:45", "Court": "3", "Team 1": "Stu/Niall", "Score 1": 0, "Team 2": "Richie/Steve", "Score 2": 0},
        # Group B
        {"Group": "Group B", "Wave": "W1", "Time": "16:30", "Court": "5", "Team 1": "Jamie/Kevin", "Score 1": 0, "Team 2": "Neil/Tom", "Score 2": 0},
        {"Group": "Group B", "Wave": "W2", "Time": "16:55", "Court": "4", "Team 1": "Simon/Cillian", "Score 1": 0, "Team 2": "Gerry/Rob", "Score 2": 0},
        {"Group": "Group B", "Wave": "W2", "Time": "16:55", "Court": "5", "Team 1": "Jamie/Kevin", "Score 1": 0, "Team 2": "Gerry/Rob", "Score 2": 0},
        {"Group": "Group B", "Wave": "W3", "Time": "17:20", "Court": "4", "Team 1": "Simon/Cillian", "Score 1": 0, "Team 2": "Neil/Tom", "Score 2": 0},
        {"Group": "Group B", "Wave": "W4", "Time": "17:45", "Court": "5", "Team 1": "Neil/Tom", "Score 1": 0, "Team 2": "Gerry/Rob", "Score 2": 0},
        {"Group": "Group B", "Wave": "W4", "Time": "17:45", "Court": "5", "Team 1": "Jamie/Kevin", "Score 1": 0, "Team 2": "Simon/Cillian", "Score 2": 0},
        # Semis
        {"Group": "Knockout", "Wave": "W5", "Time": "18:10", "Court": "3", "Phase": "Semi Final 1", "Team 1": "G1 3rd", "Score 1": 0, "Team 2": "G2 4th", "Score 2": 0},
        {"Group": "Knockout", "Wave": "W5", "Time": "18:10", "Court": "4", "Phase": "Semi Final 2", "Team 1": "G1 4th", "Score 1": 0, "Team 2": "G2 3rd", "Score 2": 0},
        {"Group": "Knockout", "Wave": "W5", "Time": "18:10", "Court": "5", "Phase": "Semi Final 3", "Team 1": "G1 1st", "Score 1": 0, "Team 2": "G2 2nd", "Score 2": 0},
        {"Group": "Knockout", "Wave": "W6", "Time": "18:35", "Court": "3", "Phase": "Semi Final 4", "Team 1": "G1 2nd", "Score 1": 0, "Team 2": "G2 1st", "Score 2": 0},
        # Finals
        {"Group": "Finals", "Wave": "W6", "Time": "18:35", "Court": "4", "Phase": "Shit the Bed Cup", "Team 1": "L-SF1", "Score 1": 0, "Team 2": "L-SF2", "Score 2": 0},
        {"Group": "Finals", "Wave": "W6", "Time": "18:35", "Court": "5", "Phase": "Shart in your pants Cup", "Team 1": "W-SF1", "Score 1": 0, "Team 2": "W-SF2", "Score 2": 0},
        {"Group": "Finals", "Wave": "W7", "Time": "19:00
