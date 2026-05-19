import streamlit as st
import pandas as pd

st.set_page_config(page_title="Padel Palooza", layout="wide")

st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] { background-color: #000000; }
    input[aria-label="Score 1"], input[aria-label="Score 2"] {
        background-color: #FF0000 !important; color: #FFFFFF !important;
        font-weight: bold !important; text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

if "matches" not in st.session_state:
    st.session_state["matches"] = [
        {"Group": "Group A", "Wave": "W1", "Time": "16:30", "Court": "3", "Team 1": "Stu/Niall", "Score 1": 0, "Team 2": "Eric/Dermo", "Score 2": 0},
        {"Group": "Group A", "Wave": "W1", "Time": "16:30", "Court": "4", "Team 1": "Richie/Steve", "Score 1": 0, "Team 2": "Jason/Wonka", "Score 2": 0},
        {"Group": "Group A", "Wave": "W2", "Time": "16:55", "Court": "3", "Team 1": "Stu/Niall", "Score 1": 0, "Team 2": "Jason/Wonka", "Score 2": 0},
        {"Group": "Group A", "Wave": "W3", "Time": "17:20", "Court": "3", "Team 1": "Richie/Steve", "Score 1": 0, "Team 2": "Eric/Dermo", "Score 2": 0},
        {"Group": "Group A", "Wave": "W3", "Time": "17:20", "Court": "4", "Team 1": "Eric/Dermo", "Score 1": 0, "Team 2": "Jason/Wonka", "Score 2": 0},
        {"Group": "Group A", "Wave": "W4", "Time": "17:45", "Court": "3", "Team 1": "Stu/Niall", "Score 1": 0, "Team 2": "Richie/Steve", "Score 2": 0},
        {"Group": "Group B", "Wave": "W1", "Time": "16:30", "Court": "5", "Team 1": "Jamie/Kevin", "Score 1": 0, "Team 2": "Neil/Tom", "Score 2": 0},
        {"Group": "Group B", "Wave": "W2", "Time": "16:55", "Court": "4", "Team 1": "Simon/Cillian", "Score 1": 0, "Team 2": "Gerry/Rob", "Score 2": 0},
        {"Group": "Group B", "Wave": "W2", "Time": "16:55", "Court": "5", "Team 1": "Jamie/Kevin", "Score 1": 0, "Team 2": "Gerry/Rob", "Score 2": 0},
        {"Group": "Group B", "Wave": "W3", "Time": "17:20", "Court": "4", "Team 1": "Simon/Cillian", "Score 1": 0, "Team 2": "Neil/Tom", "Score 2": 0},
        {"Group": "Group B", "Wave": "W4", "Time": "17:45", "Court": "5", "Team 1": "Neil/Tom", "Score 1": 0, "Team 2": "Gerry/Rob", "Score 2": 0},
        {"Group": "Group B", "Wave": "W4", "Time": "17:45", "Court": "5", "Team 1": "Jamie/Kevin", "Score 1": 0, "Team 2": "Simon/Cillian", "Score 2": 0},
        {"Group": "Knockout", "Wave": "W5", "Time": "18:10", "Court": "3", "Phase": "Semi Final 1", "Team 1": "TBD", "Score 1": 0, "Team 2": "TBD", "Score 2": 0},
        {"Group": "Knockout", "Wave": "W5", "Time": "18:10", "Court": "4", "Phase": "Semi Final 2", "Team 1": "TBD", "Score 1": 0, "Team 2": "TBD", "Score 2": 0},
        {"Group": "Knockout", "Wave": "W5", "Time": "18:10", "Court": "5", "Phase": "Semi Final 3", "Team 1": "TBD", "Score 1": 0, "Team 2": "TBD", "Score 2": 0},
        {"Group": "Knockout", "Wave": "W6", "Time": "18:35", "Court": "3", "Phase": "Semi Final 4", "Team 1": "TBD", "Score 1": 0, "Team 2": "TBD", "Score 2": 0},
        {"Group": "Finals", "Wave": "W6", "Time": "18:35", "Court": "4", "Phase": "Shit the Bed Cup", "Team 1": "TBD", "Score 1": 0, "Team 2": "TBD", "Score 2": 0},
        {"Group": "Finals", "Wave": "W6", "Time": "18:35", "Court": "5", "Phase": "Shart in your pants Cup", "Team 1": "TBD", "Score 1": 0, "Team 2": "TBD", "Score 2": 0},
        {"Group": "Finals", "Wave": "W7", "Time": "19:00", "Court": "3", "Phase": "Shitstain Cup", "Team 1": "TBD", "Score 1": 0, "Team 2": "TBD", "Score 2": 0},
        {"Group": "Finals", "Wave": "W8", "Time": "19:05", "Court": "4", "Phase": "Champions Cup", "Team 1": "TBD", "Score 1": 0, "Team 2": "TBD", "Score 2": 0}
    ]

def get_standings(g):
    d = [m for m in st.session_state["matches"] if m["Group"] == g]
    r = {}
    for m in d:
        t1, t2 = m["Team 1"], m["Team 2"]
        try: s1, s2 = int(m.get("Score 1", 0)), int(m.get("Score 2", 0))
        except: s1, s2 = 0, 0
        for t in [t1, t2]: r.setdefault(t, {"W": 0, "P": 0})
        r[t1]["P"] += s1; r[t2]["P"] += s2
        if s1 > s2: r
