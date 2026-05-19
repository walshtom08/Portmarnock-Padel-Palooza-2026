import streamlit as st
import pandas as pd

st.set_page_config(page_title="Portmarnock Padel Palooza", layout="wide")

# CSS to keep the dark theme
st.markdown("""
    <style>
    html, body, [data-testid="stAppViewContainer"] { background-color: #000000 !important; color: #FFFF00 !important; }
    h1, h2, h3, h4, p, span, label { color: #FFFF00 !important; }
    </style>
""", unsafe_allow_html=True)

st.title("🎾 Portmarnock Padel Palooza 🎾")

# Initialize Session State with full match list
if "matches" not in st.session_state:
    st.session_state["matches"] = [
        {"Group": "Group A", "Wave": "W1", "Team 1": "Stu/Niall", "Score 1": 0, "Team 2": "Eric/Dermo", "Score 2": 0},
        {"Group": "Group A", "Wave": "W1", "Team 1": "Richie/Steve", "Score 1": 0, "Team 2": "Jason/Wonka", "Score 2": 0},
        {"Group": "Group B", "Wave": "W1", "Team 1": "Jamie/Kevin", "Score 1": 0, "Team 2": "Neil/Tom", "Score 2": 0},
        {"Group": "Group B", "Wave": "W2", "Team 1": "Simon/Cillian", "Score 1": 0, "Team 2": "Gerry/Rob", "Score 2": 0},
        {"Group": "Knockout", "Phase": "Semi 1 (A1 v B2)", "Team 1": "TBD", "Score 1": 0, "Team 2": "TBD", "Score 2": 0},
        {"Group": "Knockout", "Phase": "Semi 2 (A2 v B1)", "Team 1": "TBD", "Score 1": 0, "Team 2": "TBD", "Score 2": 0},
        {"Group": "Finals", "Phase": "Champions Final", "Team 1": "Winner S1", "Score 1": 0, "Team 2": "Winner S2", "Score 2": 0}
    ]

def get_standings(group):
    data = [m for m in st.session_state["matches"] if m["Group"] == group]
    res = {}
    for m in data:
        t1, t2, s1, s2 = m["Team 1"], m["Team 2"], int(m["Score 1"]), int(m["Score 2"])
        for t in [t1, t2]: res.setdefault(t, {"Wins": 0, "Pts": 0})
        res[t1]["Pts"] += s1; res[t2]["Pts"] += s2
        if s1 > s2: res[t1]["Wins"] += 1
        elif s2 > s1: res[t2]["Wins"] += 1
    
    rows = [{"Team": t, "Match Points": v["Wins"] * 2, "Points Scored": v["Pts"] + (100 if v["Wins"] == 3 else 0)} for t, v in res.items()]
    return pd.DataFrame(rows).sort_values(["Match Points", "Points Scored"], ascending=False).reset_index(drop=True)

def update_bracket():
    s_a = get_standings("Group A")
    s_b = get_standings("Group B")
    
    # Map standings to Knockout table
    for m in st.session_state["matches"]:
        if m.get("Phase") == "Semi 1 (A1 v B2)":
            if len(s_a) > 0: m["Team 1"] = s_a.iloc[0]["Team"]
            if len(s_b) > 1: m["Team 2"] = s_b.iloc[1]["Team"]
        if m.get("Phase") == "Semi 2 (A2 v B1)":
            if len(s_a) > 1: m["Team 1"] = s_a.iloc[1]["Team"]
            if len(s_b) > 0: m["Team 2"] = s_b.iloc[0]["Team"]

def update_scores(key, df):
    delta = st.session_state[key]
    if "edited_rows" in delta:
        for idx, up in delta["edited_rows"].items():
            # Update the specific match row in session state
            match_row = df.iloc[int(idx)]
            for m in st.session_state["matches"]:
                # Matches are identified by Group and Wave/Phase
                if m.get("Group") == match_row["Group"] and (m.get("Wave") == match_row.get("Wave") or m.get("Phase") == match_row.get("Phase")):
                    m.update(up)
    update_bracket()

# --- UI ---
df = pd.DataFrame(st.session_state["matches"])

for g in ["Group A", "Group B"]:
    st.header(f"📊 {g} Fixtures")
    sub = df[df["Group"] == g].drop(columns=["Group", "Phase"], errors="ignore")
    st.data_editor(sub, key=f"e_{g}", hide_index=True, use_container_width=True, on_change=update_scores, args=(f"e_{g}", sub))
    st.dataframe(get_standings(g), hide_index=True, use_container_width=True)

st.header("⚔️ Knockout Stage")
sub_ko = df[df["Group"] == "Knockout"].drop(columns=["Group", "Wave"], errors="ignore")
st.data_editor(sub_ko, key="e_ko", hide_index=True, use_container_width=True, on_change=update_scores, args=("e_ko", sub_ko))
