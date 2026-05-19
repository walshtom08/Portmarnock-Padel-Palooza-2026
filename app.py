import streamlit as st
import pandas as pd

# 1. Page Configuration
st.set_page_config(
    page_title="Portmarnock Padel Palooza",
    page_icon="🎾",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom Styling
st.markdown("""
    <style>
    .title-font { font-size:32px !important; font-weight: bold; color: #F7D060; text-align: center; }
    .section-font { font-size:24px !important; font-weight: bold; color: #F7D060; margin-top: 30px; margin-bottom: 15px; border-bottom: 2px solid #F7D060; padding-bottom: 5px;}
    </style>
    """, unsafe_allow_html=True)

st.markdown("<p class='title-font'>🎾 Portmarnock Padel Palooza 🎾</p>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Live Tournament Dashboard & Score Tracker</p>", unsafe_allow_html=True)
st.markdown("---")

# 2. INITIALIZE DATA - PLUGGED DIRECTLY FROM YOUR SPREADSHEET SCHEDULE
if 'matches' not in st.session_state:
    # We use None or blank strings for unplayed scores so the box shows up empty in the editor grid
    data = [
        # --- WAVE 1 (16:30) ---
        {"Wave": "Wave 1", "Time": "16:30", "Court": "Court 3", "Group": "Group A", "Team 1": "Stu/Niall Hayden", "Score 1": None, "Team 2": "Eric/Dermo", "Score 2": None, "Played": False},
        {"Wave": "Wave 1", "Time": "16:30", "Court": "Court 4", "Group": "Group A", "Team 1": "Richie/Steve", "Score 1": None, "Team 2": "Jason/Wonka", "Score 2": None, "Played": False},
        {"Wave": "Wave 1", "Time": "16:30", "Court": "Court 5", "Group": "Group B", "Team 1": "Jamie/Kevin", "Score 1": None, "Team 2": "Neil/Tom", "Score 2": None, "Played": False},
        
        # --- WAVE 2 (16:55) ---
        {"Wave": "Wave 2", "Time": "16:55", "Court": "Court 3", "Group": "Group A", "Team 1": "Stu/Niall Hayden", "Score 1": None, "Team 2": "Jason/Wonka", "Score 2": None, "Played": False},
        {"Wave": "Wave 2", "Time": "16:55", "Court": "Court 4", "Group": "Group B", "Team 1": "Simon/Cillian", "Score 1": None, "Team 2": "Gerry/Rob", "Score 2": None, "Played": False},
        {"Wave": "Wave 2", "Time": "16:55", "Court": "Court 5", "Group": "Group B", "Team 1": "Jamie/Kevin", "Score 1": None, "Team 2": "Gerry/Rob", "Score 2": None, "Played": False},
        
        # --- WAVE 3 (17:20) ---
        {"Wave": "Wave 3", "Time": "17:20", "Court": "Court 3", "Group": "Group A", "Team 1": "Richie/Steve", "Score 1": None, "Team 2": "Eric/Dermo", "Score 2": None, "Played": False},
        {"Wave": "Wave 3", "Time": "17:20", "Court": "Court 4", "Group": "Group A", "Team 1": "Eric/Dermo", "Score 1": None, "Team 2": "Jason/Wonka", "Score 2": None, "Played": False},
        {"Wave": "Wave 3", "Time": "17:20", "Court": "Court 4", "Group": "Group B", "Team 1": "Simon/Cillian", "Score 1": None, "Team 2": "Neil/Tom", "Score 2": None, "Played": False},
        
        # --- WAVE 4 (17:45) ---
        {"Wave": "Wave 4", "Time": "17:45", "Court": "Court 3", "Group": "Group A", "Team 1": "Stu/Niall Hayden", "Score 1": None, "Team 2": "Richie/Steve", "Score 2": None, "Played": False},
        {"Wave": "Wave 4", "Time": "17:45", "Court": "Court 5", "Group": "Group B", "Team 1": "Neil/Tom", "Score 1": None, "Team 2": "Gerry/Rob", "Score 2": None, "Played": False},
        {"id": 12, "Wave": "Wave 4", "Time": "17:45", "Court": "Court 5", "Group": "Group B", "Team 1": "Jamie/Kevin", "Score 1": None, "Team 2": "Simon/Cillian", "Score 2": None, "Played": False},
    ]
    st.session_state.matches = pd.DataFrame(data)

# 3. Dynamic Standings Engine
def calculate_standings(df, group_name):
    group_df = df[df['Group'] == group_name]
    teams = list(set(group_df['Team 1'].unique()).union(set(group_df['Team 2'].unique())))
    stats = {team: {"P": 0, "W": 0, "L": 0, "GF": 0, "GA": 0, "Diff": 0, "Pts": 0} for team in teams}
    
    for _, row in group_df.iterrows():
        # A match is counted if both score fields have been edited and are filled out
        if pd.notnull(row['Score 1']) and pd.notnull(row['Score 2']):
            t1, t2 = row['Team 1'], row['Team 2']
            s1, s2 = int(row['Score 1']), int(row['Score 2'])
            
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


# ==========================================
# SECTION 1: INTERACTIVE FIXTURES GRID (ENTER SCORES DIRECTLY IN BOXES)
# ==========================================
st.markdown("<p class='section-font'>📅 Full Tournament Schedule & Live Scores</p>", unsafe_allow_html=True)
st.caption("💡 Admin Instruction: Click directly on any cell in the 'Score 1' or 'Score 2' columns to type in the results live!")

# Streamlit's Data Editor maps inputs inside the table back onto our dataset
edited_df = st.data_editor(
    st.session_state.matches,
    column_order=["Wave", "Time", "Court", "Group", "Team 1", "Score 1", "Score 2", "Team 2"],
    disabled=["Wave", "Time", "Court", "Group", "Team 1", "Team 2"], # Locks down schedule info so users don't overwrite times
    use_container_width=True,
    hide_index=True,
    key="tournament_editor"
)

# Keep session state updated with your direct edits
if not edited_df.equals(st.session_state.matches):
    st.session_state.matches = edited_df
    st.rerun()


# Recalculate tables automatically using edited data
group_a_table = calculate_standings(st.session_state.matches, "Group A")
group_b_table = calculate_standings(st.session_state.matches, "Group B")


# ==========================================
# SECTION 2: LIVE GROUP TABLES
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
# SECTION 3: AUTOMATIC KNOCKOUT BRACKET PREDICTIONS
# ==========================================
st.markdown("<p class='section-font'>🏆 Projected Knockout Brackets & Finals</p>", unsafe_allow_html=True)

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
