import streamlit as st
import pandas as pd

st.set_page_config(page_title="Padel Palooza", layout="wide")

# CSS: Highlighting scores and mobile compacting
st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] { background-color: #000000; }
    input[aria-label="Score 1"], input[aria-label="Score 2"] {
        background-color: #FFFF00 !important; 
        color: #000000 !important;
        font-weight: bold !important;
    }
    .stDataEditor { width: 100% !important; }
    </style>
""", unsafe_allow_html=True)

# --- FUNCTIONS (Defined first) ---
def get_standings(group):
    data = [m for m in st.session_state["matches"] if m["Group"] == group]
    teams = set([m["Team 1"] for m in data] + [m["Team 2"] for m in data])
    res = {t: {"Wins": 0, "Pts": 0} for t in teams}
    for m in data:
        s1 = int(m["Score 1"]) if m["Score 1"] else 0
        s2 = int(m["Score 2"]) if m["Score 2"] else 0
        res[m["Team 1"]]["Pts"] += s1
        res[m["Team 2"]]["Pts"] += s2
        if s1 > s2: res[m["Team 1"]]["Wins"] += 1
        elif s2 > s1: res[m["Team 2"]]["Wins"] += 1
    rows = [{"Team": t, "Pts": v["Wins"] * 2} for t, v in res.items()]
    return pd.DataFrame(rows).sort_values("Pts", ascending=False)

def update_scores(key, df):
    delta = st.session_state[key]
    if "edited_rows" in delta:
        for idx, up in delta["edited_rows"].items():
            match_row = df.iloc[int(idx)]
            for m in st.session_state["matches"]:
                if m.get("Group") == match_row["Group"] and m.get("Team 1") == match_row["Team 1"] and m.get("Time") == match_row["Time"]:
                    m.update(up)

# --- INITIALIZATION ---
if "matches" not in st.session_state:
    st.session_state["matches"] = [
        {"Group": "Group A", "Wave": "W1", "Time": "16:30", "Team 1": "Stu/Niall", "Score 1": 0, "Team 2": "Eric/Dermo", "Score 2": 0},
        {"Group": "Group A", "Wave": "W1", "Time": "16:30", "Team 1": "Richie/Steve", "Score 1": 0, "Team 2": "Jason/Wonka", "Score 2": 0},
        {"Group": "Group B", "Wave": "W1", "Time": "16:30", "Team 1": "Jamie/Kevin", "Score 1": 0, "Team 2": "Neil/Tom", "Score 2": 0},
        {"Group": "Group B", "Wave": "W2", "Time": "16:55", "Team 1": "Simon/Cillian", "Score 1": 0, "Team 2": "Gerry/Rob", "Score 2": 0},
    ]

# --- UI ---
st.title("🎾 Padel Palooza")

col_config = {
    "Wave": st.column_config.TextColumn(width="small"),
    "Time": st.column_config.TextColumn(width="small"),
    "Score 1": st.column_config.NumberColumn(width="small"),
    "Score 2": st.column_config.NumberColumn(width="small"),
}

df = pd.DataFrame(st.session_state["matches"])

for g in ["Group A", "Group B"]:
    st.subheader(f"📊 {g}")
    sub = df[df["Group"] == g].drop(columns=["Group"], errors="ignore")
    st.data_editor(sub, key=f"e_{g}", hide_index=True, use_container_width=True, 
                   column_config=col_config, on_change=update_scores, args=(f"e_{g}", sub))
    st.dataframe(get_standings(g), hide_index=True, use_container_width=True)

if st.button("Refresh Results"):
    st.rerun()
