import streamlit as st
import pandas as pd

st.set_page_config(page_title="Portmarnock Padel Palooza", layout="wide")

st.markdown("""
    <style>
    html, body, [data-testid="stAppViewContainer"] { background-color: #000000 !important; color: #FFFF00 !important; }
    h1, h2, h3, h4, p, span, label { color: #FFFF00 !important; }
    button { background-color: #111111 !important; color: #FFFF00 !important; border: 1px solid #FFFF00 !important; }
    </style>
""", unsafe_allow_html=True)

st.title("🎾 Portmarnock Padel Palooza 🎾")

# Initialize Data
if "matches" not in st.session_state:
    st.session_state["matches"] = [
        {"ID": "GA1", "Group": "Group A", "Wave": "Wave 1", "Phase": "Group stage", "Time": "16:30", "Court": "3", "Team 1": "Stu/Niall Hayden", "Score 1": 0, "Team 2": "Eric/Dermo", "Score 2": 0},
        {"ID": "GA2", "Group": "Group A", "Wave": "Wave 1", "Phase": "Group stage", "Time": "16:30", "Court": "4", "Team 1": "Richie/Steve", "Score 1": 0, "Team 2": "Jason/Wonka", "Score 2": 0},
        {"ID": "GA3", "Group": "Group A", "Wave": "Wave 2", "Phase": "Group stage", "Time": "16:55", "Court": "3", "Team 1": "Stu/Niall Hayden", "Score 1": 0, "Team 2": "Jason/Wonka", "Score 2": 0},
        {"ID": "GB1", "Group": "Group B", "Wave": "Wave 1", "Phase": "Group stage", "Time": "16:30", "Court": "5", "Team 1": "Jamie/Kevin", "Score 1": 0, "Team 2": "Neil/Tom", "Score 2": 0},
        {"ID": "GB2", "Group": "Group B", "Wave": "Wave 2", "Phase": "Group stage", "Time": "16:55", "Court": "4", "Team 1": "Simon/Cillian", "Score 1": 0, "Team 2": "Gerry/Rob", "Score 2": 0}
        # Add your other matches here similarly...
    ]

def update_scores(key_name, df):
    delta = st.session_state[key_name]
    if "edited_rows" in delta:
        for idx, updates in delta["edited_rows"].items():
            match_id = df.iloc[int(idx)]["ID"]
            for m in st.session_state["matches"]:
                if m["ID"] == match_id:
                    m.update(updates)

def calc_standings(group):
    data = [m for m in st.session_state["matches"] if m["Group"] == group]
    teams = set([m["Team 1"] for m in data] + [m["Team 2"] for m in data])
    results = {t: {"Wins": 0, "Points": 0} for t in teams}
    for m in data:
        s1, s2 = int(m["Score 1"]), int(m["Score 2"])
        results[m["Team 1"]]["Points"] += s1
        results[m["Team 2"]]["Points"] += s2
        if s1 > s2: results[m["Team 1"]]["Wins"] += 1
        elif s2 > s1: results[m["Team 2"]]["Wins"] += 1
    
    rows = []
    for t, v in results.items():
        score = v["Points"] + (100 if v["Wins"] == 3 else 0)
        rows.append({"Team": t, "Wins": v["Wins"], "Total": score})
    return pd.DataFrame(rows).sort_values("Total", ascending=False)

# Display
df = pd.DataFrame(st.session_state["matches"])
for group in ["Group A", "Group B"]:
    st.header(f"📊 {group} Fixtures")
    sub = df[df["Group"] == group].reset_index(drop=True)
    st.data_editor(sub, key=f"edit_{group}", hide_index=True, use_container_width=True, 
                   on_change=update_scores, args=(f"edit_{group}", sub))
    st.subheader(f"🏆 {group} Standings")
    st.dataframe(calc_standings(group), hide_index=True, use_container_width=True)
