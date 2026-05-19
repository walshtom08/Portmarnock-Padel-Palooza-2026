import streamlit as st
import pandas as pd

# 1. Page Configuration for Great Desktop & Mobile View
st.set_page_config(
    page_title="Portmarnock Padel Palooza",
    page_icon="🎾",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom Styling for Theme Consistency
st.markdown("""
    <style>
    .title-font { font-size:32px !important; font-weight: bold; color: #F7D060; text-align: center; }
    .section-font { font-size:24px !important; font-weight: bold; color: #F7D060; margin-top: 30px; margin-bottom: 15px; border-bottom: 2px solid #F7D060; padding-bottom: 5px;}
    </style>
    """, unsafe_allow_html=True)

st.markdown("<p class='title-font'>🎾 Portmarnock Padel Palooza 🎾</p>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Live Tournament Dashboard & Score Tracker</p>", unsafe_allow_html=True)
st.markdown("---")

# 2. INITIALIZE TOURNAMENT DATA WITH YOUR EXACT SCHEDULE & COURTS
if 'matches' not in st.session_state:
    data = [
        # --- GROUP A FIXTURES ---
        {"id": 1, "Wave": "Wave 1", "Phase": "Group stage", "Time": "16:30", "Court": "Court 3", "Stage": "Group A", "Team1": "Stu/Niall Hayden", "Score1": 0, "Team2": "Eric/Dermo", "Score2": 0, "Played": False},
        {"id": 2, "Wave": "Wave 1", "Phase": "Group stage", "Time": "16:30", "Court": "Court 4", "Stage": "Group A", "Team1": "Richie/Steve", "Score1": 0, "Team2": "Jason/Wonka", "Score2": 0, "Played": False},
        {"id": 3, "Wave": "Wave 2", "Phase": "Group stage", "Time": "16:55", "Court": "Court 3", "Stage": "Group A", "Team1": "Stu/Niall Hayden", "Score1": 0, "Team2": "Jason/Wonka", "Score2": 0, "Played": False},
        {"id": 4, "Wave": "Wave 3", "Phase": "Group stage", "Time": "17:20", "Court": "Court 3", "Stage": "Group A", "Team1": "Richie/Steve", "Score1": 0, "Team2": "Eric/Dermo", "Score2": 0, "Played": False},
        {"id": 5, "Wave": "Wave 3", "Phase": "Group stage", "Time": "17:20", "Court": "Court 4", "Stage": "Group A", "Team1": "Eric/Dermo", "Score1": 0, "Team2": "Jason/Wonka", "Score2": 0, "Played": False},
        {"id": 6, "Wave": "Wave 4", "Phase": "Group stage", "Time": "17:45", "Court": "Court 3", "Stage": "Group A", "Team1": "Stu/Niall Hayden", "Score1": 0, "Team2": "Richie/Steve", "Score2": 0, "Played": False},
        
        # --- GROUP B FIXTURES ---
        {"id": 7, "Wave": "Wave 1", "Phase": "Group stage", "Time": "16:30", "Court": "Court 5", "Stage": "Group B", "Team1": "Jamie/Kevin", "Score1": 0, "Team2": "Neil/Tom", "Score2": 0, "Played": False},
        {"id": 8, "Wave": "Wave 2", "Phase": "Group stage", "Time": "16:55", "Court": "Court 4", "Stage": "Group B", "Team1": "Simon/Cillian", "Score1": 0, "Team2": "Gerry/Rob", "Score2": 0, "Played": False},
        {"id": 9, "Wave": "Wave 2", "Phase": "Group stage", "Time": "16:55", "Court": "Court 5", "Stage": "Group B", "Team1": "Jamie/Kevin", "Score1": 0, "Team2": "Gerry/Rob", "Score2": 0, "Played": False},
        {"id": 10, "Wave": "Wave 3", "Phase": "Group stage", "Time": "17:20", "Court": "Court 4", "Stage": "Group B", "Team1": "Simon/Cillian", "Score1": 0, "Team2": "Neil/Tom", "Score2": 0, "Played": False},
        {"id": 11, "Wave": "Wave 4", "Phase": "Group stage", "Time": "17:45", "Court": "Court 5", "Stage": "Group B", "Team1": "Neil/Tom", "Score1": 0, "Team2": "Gerry/Rob", "Score2": 0, "Played": False},
        {"id": 12, "Wave": "Wave 4", "Phase": "Group stage", "Time": "17:45", "Court": "Court 5", "Stage": "Group B", "Team1": "Jamie/Kevin", "Score1": 0, "Team2": "Simon/Cillian", "Score2": 0, "Played": False},
    ]
    st.session_state.matches = pd.DataFrame(data)

# 3. Dynamic Standings Engine (Calculates purely via safe dictionary manipulation)
def calculate_standings(df, group_name):
    group_df = df[df['Stage'] == group_name]
    teams = list(set(group_df['Team1'].unique()).union(set(group_df['Team2'].unique())))
    stats = {team: {"P": 0, "W": 0, "L": 0, "GF": 0, "GA": 0, "Diff": 0, "Pts": 0} for team in teams}
    
    for _, row in group_df.iterrows():
        if row['Played']:
            t1, t2 = row['Team1'], row['Team2']
            s1, s2 = int(float(row['Score1'])), int(float(row['Score2']))
            
            stats[t1]["P"] += 1
            stats[t2]["P"] += 1
            stats[t1]["GF"] += s1
            stats[t1]["GA"] += s2
            stats[t2]["GF"] += s2
            stats[t2]["GA"] += s1
            
            if s1 > s2:
                stats[t1]["W"] += 1
                stats[t1]["Pts"] += 3
                stats[t2]["L"] += 1
            elif s2 > s1:
                stats[t2]["W"] += 1
                stats[t2]["Pts"] += 3
                stats[t1]["L"] += 1
            else:
                stats[t1]["Pts"] += 1
                stats[t2]["Pts"] += 1

    for team in stats:
        stats[team]["Diff"] = stats[team]["GF"] - stats[team]["GA"]
        
    standings_df = pd.DataFrame.from_dict(stats, orient='index').reset_index()
    standings_df.columns = ['Team', 'P', 'W', 'L', 'GF', 'GA', 'Diff', 'Pts']
    return standings_df.sort_values(by=['Pts', 'Diff', 'W'], ascending=False).reset_index(drop=True)

# Run calculations safely
group_a_table = calculate_standings(st.session_state.matches, "Group A")
group_b_table = calculate_standings(st.session_state.matches, "Group B")


# ==========================================
# SECTION 1: SCORE ENTRY INPUT (Always Visible at Top)
# ==========================================
st.markdown("<p class='section-font'>📝 Admin Score Entry Panel</p>", unsafe_allow_html=True)

match_titles = st.session_state.matches.apply(
    lambda r: f"[{r['Stage']}] {r['Time']} ({r['Court']}): {r['Team1']} vs {r['Team2']} " + ("✅ Done" if r['Played'] else "⏳ Waiting"), 
    axis=1
)
selected_idx = st.selectbox("Choose a Match to Enter/Update Scores:", options=st.session_state.matches.index, format_func=lambda x: match_titles[x])
match_row = st.session_state.matches.loc[selected_idx]

col1, col2 = st.columns(2)
with col1:
    score1 = st.number_input(f"Games for {match_row['Team1']}", min_value=0, value=int(float(match_row['Score1'])), step=1, key="input_s1")
with col2:
    score2 = st.number_input(f"Games for {match_row['Team2']}", min_value=0, value=int(float(match_row['Score2'])), step=1, key="input_s2")
    
if st.button("Save & Sync Score across Dashboard", use_container_width=True, type="primary"):
    st.session_state.matches.loc[selected_idx, 'Score1'] = score1
    st.session_state.matches.loc[selected_idx, 'Score2'] = score2
    st.session_state.matches.loc[selected_idx, 'Played'] = True
    st.success(f"Successfully saved score: {match_row['Team1']} {score1} - {score2} {match_row['Team2']}!")
    st.rerun()


# ==========================================
# SECTION 2: FULL FIXTURES GRID
# ==========================================
st.markdown("<p class='section-font'>📅 Full Tournament Schedule & Results</p>", unsafe_allow_html=True)

grid_df = st.session_state.matches.copy()
def format_result(row):
    if row['Played']:
        s1 = str(int(float(row['Score1']))) if pd.notnull(row['Score1']) else "0"
        s2 = str(int(float(row['Score2']))) if pd.notnull(row['Score2']) else "0"
        return f"{s1} - {s2}"
    return "vs"

grid_df['Result'] = grid_df.apply(format_result, axis=1)
st.dataframe(
    grid_df[["Wave", "Time", "Court", "Stage", "Team1", "Result", "Team2"]], 
    use_container_width=True, 
    hide_index=True
)


# ==========================================
# SECTION 3: LIVE GROUP TABLES
# ==========================================
st.markdown("<p class='section-font'>📊 Live Standing Tables</p>", unsafe_allow_html=True)
col_left, col_right = st.columns(2)

with col_left:
    st.markdown("### Group A Leaderboard")
    st.dataframe(group_a_table, use_container_width=True, hide_index=True)

with col_right:
    st.markdown("### Group B Leaderboard")
    st.dataframe(group_b_table, use_container_width=True, hide_index=True)


# ==========================================
# SECTION 4: AUTOMATIC KNOCKOUT BRACKET PREDICTIONS (Crash-Proofed)
# ==========================================
st.markdown("<p class='section-font'>🏆 Projected Knockout Brackets & Finals</p>", unsafe_allow_html=True)

# Defensive checks to extract rankings safely without crashing if rows are missing
gA_list = group_a_table['Team'].tolist() if not group_a_table.empty else []
while len(gA_list) < 4:
    gA_list.append("TBD")

gB_list = group_b_table['Team'].tolist() if not group_b_table.empty else []
while len(gB_list) < 4:
    gB_list.append("TBD")

st.markdown("### 🔀 Projected Semi-Final Matchups")
col_sf1, col_sf2 = st.columns(2)
with col_sf1:
    st.info(f"**Semi Final 1 (18:10 | Court 3)**\n\n🥉 Group A 3rd Place: **{gA_list[2]}**\n\nvs\n\n🏅 Group B 4th Place: **{gB_list[3]}**")
    st.info(f"**Semi Final 3 (18:10 | Court 5)**\n\n🥇 Group A 1st Place: **{gA_list[0]}**\n\nvs\n\n🥈 Group B 2nd Place: **{gB_list[1]}**")

with col_sf2:
    st.info(f"**Semi Final 2 (18:10 | Court 4)**\n\n🏅 Group A 4th Place: **{gA_list[3]}**\n\nvs\n\n🥉 Group B 3rd Place: **{gB_list[2]}**")
    st.info(f"**Semi Final 4 (18:35 | Court 3)**\n\n🥈 Group A 2nd Place: **{gA_list[1]}**\n\nvs\n\n🥇 Group B 1st Place: **{gB_list[0]}**")

st.markdown("### 🏁 Cup Finals (Wave 6, 7, and 8 Schedule)")
col_f1, col_f2 = st.columns(2)
with col_f1:
    st.error("**💩 Shit the Bed Cup Final (18:35 | Court 4)**\n\nLoser Semi Final 1 vs Loser Semi Final 2")
    st.warning("**🍑 Shart in your pants Cup Final (18:35 | Court 5)**\n\nWinner Semi Final 1 vs Winner Semi Final 2")

with col_f2:
    st.error("**🩸 Shitstain Cup Final (19:00 | Court 3)**\n\nLoser Semi Final 3 vs Loser Semi Final 4")
    st.success("**👑 Champions Cup Final (19:05 | Court 4)**\n\nWinner Semi Final 3 vs Winner Semi Final 4")
