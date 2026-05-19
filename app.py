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
    </style>
""", unsafe_allow_html=True)

if "matches" not in st.session_state:
    st.session_state["matches"] = [
        # Group A
        {"Group": "Group A", "Time": "16:30", "Team 1": "Stu/Niall", "Score 1": 0, "Team 2": "Eric/Dermo", "Score 2": 0},
        {"Group": "Group A", "Time": "16:30", "Team 1": "Richie/Steve", "Score 1": 0, "Team 2": "Jason/Wonka", "Score 2": 0},
        {"Group": "Group A", "Time": "16:55", "Team 1": "Stu/Niall", "Score 1": 0, "Team 2": "Jason/Wonka", "Score 2": 0},
        {"Group": "Group A", "Time": "17:20", "Team 1": "Richie/Steve", "Score 1": 0, "Team 2": "Eric/Dermo", "Score 2": 0},
        {"Group": "Group A", "Time": "17:20", "Team 1": "Eric/Dermo", "Score 1": 0, "Team 2": "Jason/Wonka", "Score 2": 0},
        {"Group": "Group A", "Time": "17:45", "Team 1": "Stu/Niall", "Score 1": 0, "Team 2": "Richie/Steve", "Score 2": 0},
        # Group B
        {"Group": "Group B", "Time": "16:30", "Team 1": "Jamie/Kevin", "Score 1": 0, "Team 2": "Neil/Tom", "Score 2": 0},
        {"Group": "Group B", "Time": "16:55", "Team 1": "Simon/Cillian", "Score 1": 0, "Team 2": "Gerry/Rob", "Score 2": 0},
        {"Group": "Group B", "Time": "16:55", "Team 1": "Jamie/Kevin", "Score 1": 0, "Team 2": "Gerry/Rob", "Score 2": 0},
        {"Group": "Group B", "Time": "17:20", "Team 1": "Simon/Cillian", "Score 1": 0, "Team 2": "Neil/Tom", "Score 2": 0},
        {"Group": "Group B", "Time": "17:45", "Team 1": "Neil/Tom", "Score 1": 0, "Team 2": "Gerry/Rob", "Score 2": 0},
        {"Group": "Group B", "Time": "17:45", "Team 1": "Jamie/Kevin", "Score 1": 0, "Team 2": "Simon/Cillian", "Score 2": 0},
        # Knockout
        {"Group": "Knockout", "Phase": "Semi 1", "Team 1": "TBD", "Score 1": 0, "Team 2": "TBD", "Score 2": 0},
        {"Group": "Knockout", "Phase": "Semi 2", "Team 1": "TBD", "Score 1": 0, "Team 2": "TBD", "Score 2": 0},
        {"Group": "Knockout", "Phase": "Semi 3", "Team 1": "TBD", "Score 1": 0, "Team 2": "TBD", "Score 2": 0},
        {"Group": "Knockout", "Phase": "Semi 4", "Team 1": "TBD", "Score 1": 0, "Team 2": "TBD", "Score 2": 0},
        # Finals
        {"Group": "Finals", "Phase": "Shit the Bed", "Team 1": "TBD", "Score 1": 0, "Team 2": "TBD", "Score 2": 0},
        {"Group": "Finals", "Phase": "Shart in your pants", "Team 1": "TBD", "Score 1": 0, "Team 2": "TBD", "Score 2": 0},
        {"Group": "Finals", "Phase": "Shitstain", "Team 1": "TBD", "Score 1": 0, "Team 2": "TBD", "Score 2": 0},
        {"Group": "Finals", "Phase": "Champions", "Team 1": "TBD", "Score 1": 0, "Team 2": "TBD", "Score 2": 0}
    ]

def update_scores(key, full_df):
    delta = st.session_state[key]
    if "edited_rows" in delta:
        for idx, up in delta["edited_rows"].items():
            row = full_df.iloc[int(idx)]
            for m in st.session_state["matches"]:
                # Matches by Team 1/Team 2 pair and Group to ensure unique identification
                if m["Group"] == row["Group"] and m["Team 1"] == row["Team 1"] and m["Team 2"] == row["Team 2"]:
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

for section in ["Group A", "Group B", "Knockout", "Finals"]:
    st.subheader(f"📊 {section}")
    sub = df[df["Group"] == section]
    st.data_editor(sub, key=f"e_{section}", hide_index=True, use_container_width=True, 
                   on_change=update_scores, args=(f"e_{section}", sub))
    if "Group" in section:
        st.dataframe(get_standings(section), hide_index=True, use_container_width=True)
