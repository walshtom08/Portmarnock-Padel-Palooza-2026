import streamlit as st
import pandas as pd

# 1. Page Configuration (Wide mode, sets up clean mobile viewport)
st.set_page_config(
    page_title="Portmarnock Padel Palooza",
    page_icon="🎾",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Theme Stylesheet overrides
st.markdown("""
    <style>
    .title-text { font-size:32px !important; font-weight: bold; color: #F7D060; text-align: center; }
    .header-text { font-size:24px !important; font-weight: bold; color: #F7D060; margin-top: 25px; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<p class='title-text'>🎾 Portmarnock Padel Palooza 🎾</p>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Live Tournament Dashboard & Score Tracker</p>", unsafe_allow_html=True)
st.markdown("---")

# 2. Hardcoded Tournament Schedule Data Structure (No External File Dependencies)
# CHANGE THESE STRING NAMES TO YOUR EXACT PAIRS BEFORE PUSHING TO GITHUB
if 'matches' not in st.session_state:
    st.session_state.matches = [
        # --- WAVE 1 (16:30) ---
        {"id": 1, "Wave": "Wave 1", "Time": "16:30", "Court": "Court 1", "Group": "Group A", "Team1": "Stu/Niall Hayden", "Team2": "Eric/Dermo", "Score1": 0, "Score2": 0, "Played": False},
        {"id": 2, "Wave": "Wave 1", "Time": "16:30", "Court": "Court 2", "Group": "Group A", "Team1": "Team A3", "Team2": "Team A4", "Score1": 0, "Score2": 0, "Played": False},
        {"id": 3, "Wave": "Wave 1", "Time": "16:50", "Court": "Court 3", "Group": "Group B", "Team1": "Team B1", "Team2": "Team B2", "Score1": 0, "Score2": 0, "Played": False},
        {"id": 4, "Wave": "Wave 1", "Time": "16:50", "Court": "Court 4", "Group": "Group B", "Team1": "Team B3", "Team2": "Team B4", "Score1": 0, "Score2": 0, "Played": False},
        
        # --- WAVE 2 (17:10) ---
        {"id": 5, "Wave": "Wave 2", "Time": "17:10", "Court": "Court 1", "Group": "Group A", "Team1": "Stu/Niall Hayden", "Team2": "Team A3", "Score1": 0, "Score2": 0, "Played": False},
        {"id": 6, "Wave": "Wave 2", "Time": "17:10", "Court": "Court 2", "Group": "Group A", "Team1": "Eric/Dermo", "Team2": "Team A4", "Score1": 0, "Score2": 0, "Played": False},
        {"id": 7, "Wave": "Wave 2", "Time": "17:30", "Court": "Court 3", "Group": "Group B", "Team1": "Team B1", "Team2": "Team B3", "Score1": 0, "Score2": 0, "Played": False},
        {"id": 8, "Wave": "Wave 2", "Time": "17:30", "Court": "Court 4", "Group": "Group B", "Team1": "Team B2", "Team2": "Team B4", "Score1": 0, "Score2": 0, "Played": False},
        
        # --- WAVE 3 (17:50) ---
        {"id": 9, "Wave": "Wave 3", "Time": "17:50", "Court": "Court 1", "Group": "Group A", "Team1": "Stu/Niall Hayden", "Team2": "Team A4", "Score1": 0, "Score2": 0, "Played": False},
        {"id": 10, "Wave": "Wave 3", "Time": "17:50", "Court": "Court 2", "Group": "Group A", "Team1": "Eric/Dermo", "Team2": "Team A3", "Score1": 0, "Score2": 0, "Played": False},
        {"id": 11, "Wave": "Wave 3", "Time": "18:10", "Court": "Court 3", "Group": "Group B", "Team1": "Team B1", "Team2": "Team B4", "Score1": 0, "Score2": 0, "Played": False},
        {"id": 12, "Wave": "Wave 3", "Time": "18:10", "Court": "Court 4", "Group": "Group B", "Team1": "Team B2", "Team2": "Team B3", "Score1": 0, "Score2": 0, "Played": False}
    ]

# 3. Defensive Standings Engine (Calculates purely via safe dictionary manipulation)
def get_standings(group_label):
    # Find all unique teams listed under this group
    teams = set()
    for m in st.session_state.matches:
        if m["Group"] == group_label:
            teams.add(m["Team1"])
            teams.add(m["Team2"])
            
    # Structure standings table framework
    table = {team: {"P": 0, "W": 0, "L": 0, "GF": 0, "GA": 0, "Diff": 0, "Pts": 0} for team in teams}
    
    for m in st.session_state.matches:
        if m["Group"] == group_label and m["Played"]:
            t1, t2 = m["Team1"], m["Team2"]
            s1, s2 = int(m["Score1"]), int(m["Score2"])
            
            table[t1]["P"] += 1
            table[t2]["P"] += 1
            table[t1]["GF"] += s1
            table[t1]["GA"] += s2
            table[t2]["GF"] += s2
            table[t2]["GA"] += s1
            
            if s1 > s2:
                table[t1]["W"] += 1
                table[t1]["Pts"] += 3
                table[t2]["L"] += 1
            elif s2 > s1:
                table[t2]["W"] += 1
                table[t2]["Pts"] += 3
                table[t1]["L"] += 1
            else:
                table[t1]["Pts"] += 1
                table[t2]["Pts"] += 1
                
    for team in table:
        table[team]["Diff"] = table[team]["GF"] - table[team]["GA"]
        
    df = pd.DataFrame.from_dict(table, orient='index').reset_index()
    df.columns = ['Team', 'P', 'W', 'L', 'GF', 'GA', 'Diff', 'Pts']
    return df.sort_values(by=['Pts', 'Diff', 'W'], ascending=False).reset_index(drop=True)

# Generate Live Tables
group_a_table = get_standings("Group A")
group_b_table = get_standings("Group B")


# 4. Interactive Live Score Tracker Input (Expandable Admin Interface)
with st.expander("📝 Update Live Match Scores", expanded=False):
    options = []
    for i, m in enumerate(st.session_state.matches):
        status = "✅ Finished" if m["Played"] else "⏳ Pending"
        options.append(f"{m['Wave']} | {m['Time']} ({m['Court']}): {m['Team1']} vs {m['Team2']} [{status}]")
        
    selected_match_str = st.selectbox("Select Match to Score", options=options, index=0)
    selected_index = options.index(selected_match_str)
    
    match = st.session_state.matches[selected_index]
    
    c1, c2 = st.columns(2)
    with c1:
        new_score1 = st.number_input(f"Games for {match['Team1']}", min_value=0, value=int(match['Score1']), step=1, key=f"t1_score_{selected_index}")
    with c2:
        new_score2 = st.number_input(f"Games for {match['Team2']}", min_value=0, value=int(match['Score2']), step=1, key=f"t2_score_{selected_index}")
        
    if st.button("Save & Sync Scores across Tournament", use_container_width=True, type="primary"):
        st.session_state.matches[selected_index]["Score1"] = new_score1
        st.session_state.matches[selected_index]["Score2"] = new_score2
        st.session_state.matches[selected_index]["Played"] = True
        st.success("Scores Synced Automatically!")
        st.rerun()


# 5. UI SECTION ONE: Full Fixtures Display Matrix
st.markdown("<p class='header-text'>📅 Full Tournament Grid</p>", unsafe_allow_html=True)

display_rows = []
for m in st.session_state.matches:
    result_str = f"{int(m['Score1'])} - {int(m['Score2'])}" if m["Played"] else "vs"
    display_rows.append({
        "Wave": m["Wave"],
        "Time": m["Time"],
        "Court": m["Court"],
        "Group": m["Group"],
        "Team 1": m["Team1"],
        "Result": result_str,
        "Team 2": m["Team2"]
    })

st.dataframe(pd.DataFrame(display_rows), use_container_width=True, hide_index=True)


# 6. UI SECTION TWO: Standings Display Matrix (Sits directly underneath schedule)
st.markdown("<p class='header-text'>📊 Live Group Tables</p>", unsafe_allow_html=True)
col_left, col_right = st.columns(2)

with col_left:
    st.markdown("### Group A Leaderboard")
    st.dataframe(group_a_table, use_container_width=True, hide_index=True)

with col_right:
    st.markdown("### Group B Leaderboard")
    st.dataframe(group_b_table, use_container_width=True, hide_index=True)


# 7. UI SECTION THREE: Automatic Cup Projections
st.markdown("<p class='header-text'>🏆 Projected Bracket Configurations</p>", unsafe_allow_html=True)

# Guard checks to populate dummy text if teams haven't filled standings out yet
gA = group_a_table['Team'].tolist() + ["1st Group A", "2nd Group A", "3rd Group A", "4th Group A"]
gB = group_b_table['Team'].tolist() + ["1st Group B", "2nd Group B", "3rd Group B", "4th Group B"]

col_champs, col_sbt = st.columns(2)
with col_champs:
    st.info(f"🏆 **Champions Cup Semis**\n\n🥇 {gA[0]} vs 🥈 {gB[1]}\n\n🥇 {gB[0]} vs 🥈 {gA[1]}")
with col_sbt:
    st.error(f"💩 **Shit the Bed Cup Semis**\n\n🥉 {gA[2]} vs 🏅 {gB[3]}\n\n🥉 {gB[2]} vs 🏅 {gA[3]}")
