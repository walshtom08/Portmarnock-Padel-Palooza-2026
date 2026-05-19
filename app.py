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

# --- INITIALIZATION ---
if "matches" not in st.session_state:
    st.session_state["matches"] = [
        {"Group": "Group A", "Wave": "W1", "Time": "16:30", "Team 1": "Stu/Niall", "Score 1": 0, "Team 2": "Eric/Dermo", "Score 2": 0},
        {"Group": "Group A", "Wave": "W1", "Time": "16:30", "Team 1": "Richie/Steve", "Score 1": 0, "Team 2": "Jason/Wonka", "Score 2": 0},
        {"Group": "Knockout", "Wave": "W5", "Phase": "Semi 1", "Team 1": "TBD", "Score 1": 0, "Team 2": "TBD", "Score 2": 0},
        {"Group": "Finals", "Wave": "W8", "Phase": "Champions Cup", "Team 1": "TBD", "Score 1": 0, "Team 2": "TBD", "Score 2": 0}
    ]

# --- FUNCTIONS ---
def update_scores(key, full_df):
    delta = st.session_state[key]
    if "edited_rows" in delta:
        for idx, up in delta["edited_rows"].items():
            # Get row from the full df based on original index
            original_row = full_df.iloc[int(idx)]
            for m in st.session_state["matches"]:
                # Match based on Team 1 and Time to identify the record
                if m["Team 1"] == original_row["Team 1"] and m["Time"] == original_row["Time"]:
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

# --- UI ---
st.title("🎾 Padel Palooza")
df = pd.DataFrame(st.session_state["matches"])

for section in ["Group A", "Group B", "Knockout", "Finals"]:
    st.subheader(f"📊 {section}")
    # Show subset but keep access to original full dataframe for indexing
    sub = df[df["Group"] == section].drop(columns=["Group"])
    
    st.data_editor(
        sub, key=f"e_{section}", hide_index=True, use_container_width=True, 
        on_change=update_scores, args=(f"e_{section}", df[df["Group"] == section])
    )
    
    if "Group" in section:
        st.dataframe(get_standings(section), hide_index=True, use_container_width=True)
