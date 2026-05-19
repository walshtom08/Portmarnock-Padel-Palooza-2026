import streamlit as st
import pandas as pd

# Set up page config
st.set_page_config(page_title="Portmarnock Padel Palooza", layout="centered")

# Custom CSS injection for stark high-contrast theme (Pitch black background, Pure yellow text)
st.markdown("""
    <style>
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        background-color: #000000 !important;
        color: #FFFF00 !important;
    }
    h1, h2, h3, h4, p, span, label, div {
        color: #FFFF00 !important;
    }
    /* Mobile Scorecard Blocks styling */
    .match-box {
        border: 2px solid #FFFF00;
        padding: 12px;
        border-radius: 8px;
        margin-bottom: 15px;
        background-color: #050505;
    }
    .match-meta {
        font-size: 13px;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 8px;
        border-bottom: 1px dict #FFFF00;
        padding-bottom: 4px;
    }
    /* Force individual input boxes to look correct */
    div[data-testid="stNumberInput"] input {
        color: #FFFF00 !important;
        background-color: #111111 !important;
        border: 1px solid #FFFF00 !important;
        font-size: 16px !important;
    }
    /* Global submit button configuration */
    .stButton>button {
        background-color: #111111 !important;
        color: #FFFF00 !important;
        border: 2px solid #FFFF00 !important;
        width: 100%;
        padding: 16px;
        font-weight: bold;
        font-size: 18px;
        margin-top: 20px;
        border-radius: 8px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🎾 PADEL PALOOZA 🎾")
st.write("📲 Scorecard View: Tap the score boxes directly from your phone on the courts. Scroll to the bottom to Save & Sync.")

# --- COMPREHENSIVE FIXTURE DATA REPAIR FROM SOURCE SHEET ---
initial_matches = [
    # Group A
    {"ID": "GA1", "Sec": "Group A", "Wave": "Wave 1", "Phase": "Group stage", "Time": "16:30 - 16:50", "Ct": "3", "Team 1": "Stu/Niall Hayden", "S1": 0, "Team 2": "Eric/Dermo", "S2": 0},
    {"ID": "GA2", "Sec": "Group A", "Wave": "Wave 1", "Phase": "Group stage", "Time": "16:30 - 16:50", "Ct": "4", "Team 1": "Richie/Steve", "S1": 0, "Team 2": "Jason/Wonka", "S2": 0},
    {"ID": "GA3", "Sec": "Group A", "Wave": "Wave 2", "Phase": "Group stage", "Time": "16:55 - 17:15", "Ct": "3", "Team 1": "Stu/Niall Hayden", "S1": 0, "Team 2": "Jason/Wonka", "S2": 0},
    {"ID": "GA4", "Sec": "Group A", "Wave": "Wave 3", "Phase": "Group stage", "Time": "17:20 - 17:40", "Ct": "3", "Team 1": "Richie/Steve", "S1": 0, "Team 2": "Eric/Dermo", "S2": 0},
    {"ID": "GA5", "Sec": "Group A", "Wave": "Wave 3", "Phase": "Group stage", "Time": "17:20 - 17:40", "Ct": "4", "Team 1": "Eric/Dermo", "S1": 0, "Team 2": "Jason/Wonka", "S2": 0},
    {"ID": "GA6", "Sec": "Group A", "Wave": "Wave 4", "Phase": "Group stage", "Time": "17:45 - 18:05", "Ct": "3", "Team 1": "Stu/Niall Hayden", "S1": 0, "Team 2": "Richie/Steve", "S2": 0},
    # Group B
    {"ID": "GB1", "Sec": "Group B", "Wave": "Wave 1", "Phase": "Group stage", "Time": "16:30 - 16:50", "Ct": "5", "Team 1": "Jamie/Kevin", "S1": 0, "Team 2": "Neil/Tom", "S2": 0},
    {"ID": "GB2", "Sec": "Group B", "Wave": "Wave 2", "Phase": "Group stage", "Time": "16:55 - 17:15", "Ct": "4", "Team 1": "Simon/Cillian", "S1": 0, "Team 2": "Gerry/Rob", "S2": 0},
    {"ID": "GB3", "Sec": "Group B", "Wave": "Wave 2", "Phase": "Group stage", "Time": "16:55 - 17:15", "Ct": "5", "Team 1": "Jamie/Kevin", "S1": 0, "Team 2": "Gerry/Rob", "S2": 0},
    {"ID": "GB4", "Sec": "Group B", "Wave": "Wave 3", "Phase": "Group stage", "Time": "17:20 - 17:40", "Ct": "4", "Team 1": "Simon/Cillian", "S1": 0, "Team 2": "Neil/Tom", "S2": 0},
    {"ID": "GB5", "Sec": "Group B", "Wave": "Wave 4", "Phase": "Group stage", "Time": "17:45 - 18:05", "Ct": "5", "Team 1": "Neil/Tom", "S1": 0, "Team 2": "Gerry/Rob", "S2": 0},
    {"ID": "GB6", "Sec": "Group B", "Wave": "Wave 4", "Phase": "Group stage", "Time": "17:45 - 18:05", "Ct": "5", "Team 1": "Jamie/Kevin", "S1": 0, "Team 2": "Simon/Cillian", "S2": 0},
    # Knockouts
    {"ID": "KO1", "Sec": "Knockouts", "Wave": "Wave 5", "Phase": "Semi final 1 (Group 1 3rd v Group 2 4th)", "Time": "18:10 - 18:30", "Ct": "3", "Team 1": "Group 1 3rd Place", "S1": 0, "Team 2": "Group 2 4th Place", "S2": 0},
    {"ID": "KO2", "Sec": "Knockouts", "Wave": "Wave 5", "Phase": "Semi final 2 (Group 1 4th v Group 2 3rd)", "Time": "18:10 - 18:30", "Ct": "4", "Team 1": "Group 1 4th Place", "S1": 0, "Team 2": "Group 2 3rd Place", "S2": 0},
    {"ID": "KO3", "Sec": "Knockouts", "Wave": "Wave 5", "Phase": "Semi final 3 (Group 1 1st v Group 2 2nd)", "Time": "18:10 - 18:30", "Ct": "5", "Team 1": "Group 1 1st Place", "S1": 0, "Team 2": "Group 2 2nd Place", "S2": 0},
    {"ID": "KO4", "Sec": "Knockouts", "Wave": "Wave 6", "Phase": "Semi final 4 (Group 1 2nd v Group 2 1st)", "Time": "18:35 - 18:55", "Ct": "3", "Team 1": "Group 1 2nd Place", "S1": 0, "Team 2": "Group 2 1st Place", "S2": 0},
    # Finals
    {"ID": "F1", "Sec": "Finals", "Wave": "Wave 6", "Phase": "Shit the Bed Cup Final (Loser SF1 v Loser SF2)", "Time": "18:35 - 18:55", "Ct": "4", "Team 1": "Loser Semi 1", "S1": 0, "Team 2": "Loser Semi 2", "S2": 0},
    {"ID": "F2", "Sec": "Finals", "Wave": "Wave 6", "Phase": "Shart in your pants Cup Final (Winner SF1 v Winner SF2)", "Time": "18:35 - 18:55", "Ct": "5", "Team 1": "Winner Semi 1", "S1": 0, "Team 2": "Winner Semi 2", "S2": 0},
    {"ID": "F3", "Sec": "Finals", "Wave": "Wave 7", "Phase": "Shitstain Cup Final (Loser SF3 v Loser SF4)", "Time": "19:00 - 19:20", "Ct": "3", "Team 1": "Loser Semi 3", "S1": 0, "Team 2": "Loser Semi 4", "S2": 0},
    {"ID": "F4", "Sec": "Finals", "Wave": "Wave 8", "Phase": "Champions Cup Final (Winner SF3 v Winner SF4)", "Time": "19:05 - 19:30", "Ct": "4", "Team 1": "Winner Semi 3", "S1": 0, "Team 2": "Winner Semi 4", "S2": 0}
]

# Cloud data persistence configuration
try:
    conn = st.connection("cache", type="dict")
except Exception:
    conn = st.session_state

if "matches" not in conn:
    conn["matches"] = initial_matches

# Working tracking dictionary for changes
updated_scores = {}

# --- SCORECARD ENGINE ROUTINE ---
def render_section_cards(section_title, section_key):
    st.header(f"📋 {section_title}")
    section_matches = [m for m in conn["matches"] if m["Sec"] == section_key]
    
    for m in section_matches:
        # Wrap each match entry in a mobile container block
        st.markdown(f"""
        <div class="match-box">
            <div class="match-meta">🕒 {m['Time']} &nbsp;|&nbsp; 📍 Court {m['Ct']} &nbsp;|&nbsp; 📦 {m['Wave']} - {m['Phase']}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Display side-by-side layout for mobile-friendly input tapping
        col_t1, col_s1, col_s2, col_t2 = st.columns([4, 2, 2, 4])
        with col_t1:
            st.write(f"**{m['Team 1']}**")
        with col_s1:
            score1 = st.number_input("", min_value=0, value=int(m["S1"]), step=1, key=f"s1_{m['ID']}", label_visibility="collapsed")
        with col_s2:
            score2 = st.number_input("", min_value=0, value=int(m["S2"]), step=1, key=f"s2_{m['ID']}", label_visibility="collapsed")
        with col_t2:
            st.write(f"**{m['Team 2']}**")
            
        updated_scores[m["ID"]] = (score1, score2)

# Run scorecard rendering for each block
render_section_cards("Group A Fixtures", "Group A")
render_section_cards("Group B Fixtures", "Group B")
render_section_cards("Knockout Stage", "Knockouts")
render_section_cards("The Finals Phase", "Finals")

# --- SAVE ACTION ---
if st.button("🔄 SAVE & SYNC ALL MATCH SCORES"):
    master_list = conn["matches"]
    for m in master_list:
        if m["ID"] in updated_scores:
            m["S1"] = updated_scores[m["ID"]][0]
            m["S2"] = updated_scores[m["ID"]][1]
    conn["matches"] = master_list
    st.success("Scores saved live to cloud memory!")
    st.rerun()

# --- LIVE AUTOMATED STANDINGS GENERATION ---
st.markdown("---")
st.header("📊 Live Group Leaderboards")

def compute_standings(group_name, match_list):
    group_subset = [m for m in match_list if m["Sec"] == group_name]
    
    # Track all static valid names explicitly from group profiles
    if group_name == "Group A":
        teams = {"Stu/Niall Hayden", "Eric/Dermo", "Richie/Steve", "Jason/Wonka"}
    else:
        teams = {"Jamie/Kevin", "Neil/Tom", "Simon/Cillian", "Gerry/Rob"}
        
    standings = {team: {"Played": 0, "Points": 0} for team in teams}
    
    for row in group_subset:
        if row["S1"] > 0 or row["S2"] > 0:
            t1, t2 = row["Team 1"], row["Team 2"]
            if t1 in standings and t2 in standings:
                standings[t1]["Played"] += 1
                standings[t2]["Played"] += 1
                if row["S1"] > row["S2"]:
                    standings[t1]["Points"] += 2
                elif row["S2"] > row["S1"]:
                    standings[t2]["Points"] += 2
                else:
                    standings[t1]["Points"] += 1
                    standings[t2]["Points"] += 1
                
    return pd.DataFrame.from_dict(standings, orient="index").reset_index().rename(columns={"index": "Team"}).sort_values(by="Points", ascending=False)

col1, col2 = st.columns(2)
with col1:
    st.subheader("Group A")
    st.dataframe(compute_standings("Group A", conn["matches"]), hide_index=True)
with col2:
    st.subheader("Group B")
    st.dataframe(compute_standings("Group B", conn["matches"]), hide_index=True)
