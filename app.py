import streamlit as st
import pandas as pd

st.set_page_config(page_title="Portmarnock Padel Palooza", layout="wide")

# CSS
st.markdown("""
    <style>
    html, body, [data-testid="stAppViewContainer"] { background-color: #000000 !important; color: #FFFF00 !important; }
    h1, h2, h3, h4, p, span, label { color: #FFFF00 !important; }
    button { background-color: #111111 !important; color: #FFFF00 !important; border: 1px solid #FFFF00 !important; }
    </style>
""", unsafe_allow_html=True)

st.title("🎾 Portmarnock Padel Palooza 🎾")

# Data
if "matches" not in st.session_state:
    st.session_state["matches"] = [
        {"ID": "GA1", "Group": "Group A", "Wave": "W1", "Phase": "Group", "Time": "16:30", "Court": "3", "Team 1": "Stu/Niall", "Score 1": 0, "Team 2": "Eric/Dermo", "Score 2": 0},
        {"ID": "GA2", "Group": "Group A", "Wave": "W1", "Phase": "Group", "Time": "16:30", "Court": "4", "Team 1": "Richie/Steve", "Score 1": 0, "Team 2": "Jason/Wonka", "Score 2": 0},
        {"ID": "GA3", "Group": "Group A", "Wave": "W2", "Phase": "Group", "Time": "16:55", "Court": "3", "Team 1": "Stu/Niall", "Score 1": 0, "Team 2": "Jason/Wonka", "Score 2": 0},
        {"ID": "GA4", "Group": "Group A", "Wave": "W3", "Phase": "Group", "Time": "17:20", "Court": "3", "Team 1": "Richie/Steve", "Score 1": 0, "Team 2": "Eric/Dermo", "Score 2": 0},
        {"ID": "GA5", "Group": "Group A", "Wave": "W3", "Phase": "Group", "Time": "17:20", "Court": "4", "Team 1": "Eric/Dermo", "Score 1": 0, "Team 2": "Jason/Wonka", "Score 2": 0},
        {"ID": "GA6", "Group": "Group A", "Wave": "W4", "Phase": "Group", "Time": "17:45", "Court": "3", "Team 1": "Stu/Niall", "Score 1": 0, "Team 2": "Richie/Steve", "Score 2": 0},
        {"ID": "GB1", "Group": "Group B", "Wave": "W1", "Phase": "Group", "Time": "16:30", "Court": "5", "Team 1": "Jamie/Kevin", "Score 1": 0, "Team 2": "Neil/Tom", "Score 2": 0},
        {"ID": "GB2", "Group": "Group B", "Wave": "W2", "Phase": "Group", "Time": "16:55", "Court": "4", "Team 1": "Simon/Cillian", "Score 1": 0, "Team 2": "Gerry/Rob", "Score 2": 0},
        {"ID": "GB3", "Group": "Group B", "Wave": "W2", "Phase": "Group", "Time": "16:55", "Court": "5", "Team 1": "Jamie/Kevin", "Score 1": 0, "Team 2": "Gerry/Rob", "Score 2": 0},
        {"ID": "GB4", "Group": "Group B", "Wave": "W3", "Phase": "Group", "Time": "17:20", "Court": "4", "Team 1": "Simon/Cillian", "Score 1": 0, "Team 2": "Neil/Tom", "Score 2": 0},
        {"ID": "GB5", "Group": "Group B", "Wave": "W4", "Phase": "Group", "Time": "17:45", "Court": "5", "Team 1": "Neil/Tom", "Score 1": 0, "Team 2": "Gerry/Rob", "Score 2": 0},
        {"ID": "GB6", "Group": "Group B", "Wave": "W4", "Phase": "Group", "Time": "17:45", "Court": "5", "Team 1": "Jamie/Kevin", "Score 1": 0, "Team 2": "Simon/Cillian", "Score 2": 0}
    ]

def update_scores(key, df):
    delta = st.session_state[key]
    if "edited_rows" in delta:
        for idx, up in delta["edited_rows"].items():
            mid = df.iloc[int(idx)]["ID"]
            for m in st.session_state["matches"]:
                if m["ID"] == mid: m.update(up)

def get_standings(group):
    data = [m for m in st.session_state["matches"] if m["Group"] == group]
    teams = set([m["Team 1"] for m in data] + [m["Team 2"] for m in data])
    res = {t: {"Wins": 0, "Pts": 0} for t in teams}
    for m in data:
        s1, s2 = int(m["Score 1"]), int(m["Score 2"])
        res[m["Team 1"]]["Pts"] += s1
        res[m["Team 2"]]["Pts"] += s2
        if s1 > s2: res[m["Team 1"]]["Wins"] += 1
        elif s2 > s1: res[m["Team 2"]]["Wins"] += 1
    
    rows = []
    for t, v in res.items():
        rows.append({
            "Team": t, 
            "Match Points": v["Wins"] * 2, 
            "Points Scored": v["Pts"] + (100 if v["Wins"] == 3 else 0)
        })
    return pd.DataFrame(rows).sort_values("Match Points", ascending=False)

# UI
df = pd.DataFrame(st.session_state["matches"])
for g in ["Group A", "Group B"]:
    st.header(f"📊 {g} Fixtures")
    sub = df[df["Group"] == g].reset_index(drop=True)
    st.data_editor(sub, key=f"e_{g}", hide_index=True, use_container_width=True, 
                   on_change=update_scores, args=(f"e_{g}", sub))
    st.subheader(f"🏆 {g} Standings")
    st.dataframe(get_standings(g), hide_index=True, use_container_width=True)
