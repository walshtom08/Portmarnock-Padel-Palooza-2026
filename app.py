import streamlit as st
import pandas as pd

st.set_page_config(page_title="Padel Palooza", layout="wide")

st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] { background-color: #000000; }
    input[aria-label="Score 1"], input[aria-label="Score 2"] {
        background-color: #FF0000 !important; 
        color: #FFFFFF !important;
        font-weight: bold !important;
        text-align: center;
    }
    .stDataEditor { width: 100% !important; }
    </style>
""", unsafe_allow_html=True)

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
        # Knockout
        {"Group": "Knockout", "Wave": "W5", "Time": "18:10", "Court": "3", "Phase": "Semi 1", "Team 1": "TBD", "Score 1": 0, "Team 2": "TBD", "Score 2": 0},
        {"Group": "Knockout", "Wave": "W5", "Time": "18:10", "Court": "4", "Phase": "Semi 2", "Team 1": "TBD", "Score 1": 0, "Team 2": "TBD", "Score 2": 0},
        {"Group": "Knockout", "Wave": "W5", "Time": "18:10", "Court": "5", "Phase": "Semi 3", "Team 1": "TBD", "Score 1": 0, "Team 2": "TBD", "Score 2": 0},
        {"Group": "Knockout", "Wave": "W6", "Time": "18:35", "Court": "3", "Phase": "Semi 4", "Team 1": "TBD", "Score 1": 0, "Team 2": "TBD", "Score 2": 0},
        # Finals
        {"Group": "Finals", "Wave": "W6", "Time": "18:35", "Court": "4", "Phase": "Shit the Bed", "Team 1": "TBD", "Score 1": 0, "Team 2": "TBD", "Score 2": 0},
        {"Group": "Finals", "Wave": "W6", "Time": "18:35", "Court": "5", "Phase": "Shart in your pants", "Team 1": "TBD", "Score 1": 0, "Team 2": "TBD", "Score 2": 0},
        {"Group": "Finals", "Wave": "W7", "Time": "19:00", "Court": "3", "Phase": "Shitstain", "Team 1": "TBD", "Score 1": 0, "Team 2": "TBD", "Score 2": 0},
        {"Group": "Finals", "Wave": "W8", "Time": "19:05", "Court": "4", "Phase": "Champions", "Team 1": "TBD", "Score 1": 0, "Team 2": "TBD", "Score 2": 0}
    ]

def update_scores(key, full_df):
    delta = st.session_state[key]
    if "edited_rows" in delta:
        for idx, up in delta["edited_rows"].items():
            row = full_df.iloc[int(idx)]
            for m in st.session_state["matches"]:
                # Matches by unique combination of Group, Time, and Team 1
                if m["Group"] == row["Group"] and m["Time"] == row["Time"] and m["Team 1"] == row["Team 1"]:
                    m.update(up)

def get_standings(group):
    data = [m for m in st.session_state["matches"] if m["Group"] == group]
    res = {}
    for m in data:
        t1, t2 = m["Team 1"], m["Team 2"]
        s1 = int(m.get("Score 1", 0)); s2 = int(m.get("Score 2", 0))
        for t in [t1, t2]: res.setdefault(t, {"Wins": 0, "Pts": 0})
        res[t1]["Pts"] += s1; res[t2]["Pts"] += s2
        if s1 > s2: res[t1]["Wins"] += 1
        elif s2 > s1: res[t2]["Wins"] += 1
    rows = [{"Team": t, "Match Points": v["Wins"] * 2, "Points Scored": v["Pts"]} for t, v in res.items()]
    return pd.DataFrame(rows).sort_values(["Match Points", "Points Scored"], ascending=False)

st.title("🎾 Padel Palooza")
df = pd.DataFrame(st.session_state["matches"])

# Configuration to keep columns small
col_config = {
    "Wave": st.column_config.TextColumn(width="small"),
    "Time": st.column_config.TextColumn(width="small"),
    "Court": st.column_config.TextColumn(width="small"),
    "Score 1": st.column_config.NumberColumn(width="small"),
    "Score 2": st.column_config.NumberColumn(width="small"),
}
