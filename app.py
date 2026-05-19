import streamlit as st
import pandas as pd

st.set_page_config(page_title="Portmarnock Padel Palooza", layout="wide")

# CSS to make the score cells stand out clearly
st.markdown("""
    <style>
    html, body, [data-testid="stAppViewContainer"] { background-color: #000000 !important; color: #FFFF00 !important; }
    
    /* Target the score cells in the data_editor */
    [data-testid="stDataEditor"] td:has(div[data-testid="stNumberInput"]) {
        background-color: #550055 !important; /* Deep Purple highlight for cells */
    }
    input[aria-label="Score 1"], input[aria-label="Score 2"] {
        background-color: #FF00FF !important; /* Magenta background for the input */
        color: #FFFFFF !important;
        font-weight: bold !important;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize Session State
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
        {"Group": "Knockout", "Wave": "W5", "Time": "18:10", "Court": "3", "Phase": "Semi Final 1", "Team 1": "G1 3rd", "Score 1": 0, "Team 2": "G2 4th", "Score 2": 0},
        {"Group": "Knockout", "Wave": "W5", "Time": "18:10", "Court": "4", "Phase": "Semi Final 2", "Team 1": "G1 4th", "Score 1": 0, "Team 2": "G2 3rd", "Score 2": 0},
        {"Group": "Knockout", "Wave": "W5", "Time": "18:10", "Court": "5", "Phase": "Semi Final 3", "Team 1": "G1 1st", "Score 1": 0, "Team 2": "G2 2nd", "Score 2": 0},
        {"Group": "Knockout", "Wave": "W6", "Time": "18:35", "Court": "3", "Phase": "Semi Final 4", "Team 1": "G1 2nd", "Score 1": 0, "Team 2": "G2 1st", "Score 2": 0},
        {"Group": "Finals", "Wave": "W6", "Time": "18:35", "Court": "4", "Phase": "Shit the Bed Cup", "Team 1": "L-SF1", "Score 1": 0, "Team 2": "L-SF2", "Score 2": 0},
        {"Group": "Finals", "Wave": "W6", "Time": "18:35", "Court": "5", "Phase": "Shart in your pants Cup", "Team 1": "W-SF1", "Score 1": 0, "Team 2": "W-SF2", "Score 2": 0},
        {"Group": "Finals", "Wave": "W7", "Time": "19:00", "Court": "3", "Phase": "Shitstain Cup", "Team 1": "L-SF3", "Score 1": 0, "Team 2": "L-SF4", "Score 2": 0},
        {"Group": "Finals", "Wave": "W8", "Time": "19:05", "Court": "4", "Phase": "Champions Cup", "Team 1": "W-SF3", "Score 1": 0, "Team 2": "W-SF4", "Score 2": 0}
    ]

# Define narrow column configuration
col_config = {
    "Wave": st.column_config.TextColumn(width="small"),
    "Time": st.column_config.TextColumn(width="small"),
    "Court": st.column_config.TextColumn(width="small"),
    "Score 1": st.column_config.NumberColumn(width="small"),
    "Score 2": st.column_config.NumberColumn(width="small"),
}

# Standings and update functions remain same...
def get_standings(group):
    data = [m for m in st.session_state["matches"] if m["Group"] == group]
    teams = set([m["Team 1"] for m in data] + [m["Team 2"] for m in data])
    res = {t: {"Wins": 0, "Pts": 0} for t in teams}
    for m in data:
        t1, t2, s1, s2 = m["Team 1"], m["Team 2"], int(m["Score 1"]), int(m["Score 2"])
        res[t1]["Pts"] += s1; res[t2]["Pts"] += s2
        if s1 > s2: res[t1]["Wins"] += 1
        elif s2 > s1: res[t2]["Wins"] += 1
    rows = [{"Team": t, "Match Points": v["Wins"] * 2, "Points Scored": v["Pts"] + (100 if v["Wins"] == 3 else 0)} for t, v in res.items()]
    return pd.DataFrame(rows).sort_values(["Match Points", "Points Scored"], ascending=False).reset_index(drop=True)

def update_scores(key, df):
    delta = st.session_state[key]
    if "edited_rows" in delta:
        for idx, up in delta["edited_rows"].items():
            match_row = df.iloc[int(idx)]
            for m in st.session_state["matches"]:
                if m.get("Group") == match_row["Group"] and m.get("Team 1") == match_row["Team 1"] and m.get("Time") == match_row["Time"]:
                    m.update(up)

# --- UI ---
st.title("🎾 Portmarnock Padel Palooza 🎾")
df = pd.DataFrame(st.session_state["matches"])

for g in ["Group A", "Group B"]:
    st.header(f"📊 {g} Fixtures")
    sub = df[df["Group"] == g].drop(columns=["Group", "Phase"], errors="ignore")
    st.data_editor(sub, key=f"e_{g}", hide_index=True, use_container_width=True, column_config=col_config, on_change=update_scores, args=(f"e_{g}", sub))
    st.subheader(f"🏆 {g} Standings")
    st.dataframe(get_standings(g), hide_index=True, use_container_width=True)

for section in ["Knockout", "Finals"]:
    st.header(f"⚔️ {section} Stage")
    sub = df[df["Group"] == section].drop(columns=["Group"], errors="ignore")
    st.data_editor(sub, key=f"e_{section}", hide_index=True, use_container_width=True, column_config=col_config, on_change=update_scores, args=(f"e_{section}", sub))
