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

# 2. INITIALIZE DATA - PULLING DIRECTLY FROM YOUR SPREADSHEET SCHEDULE
if 'matches' not in st.session_state:
    data = [
        # --- GROUP A FIXTURES ---
        {"Wave": "Wave 1", "Time": "16:30", "Court": "Court 3", "Group": "Group A", "Team 1": "Stu/Niall Hayden", "Score 1": None, "Team 2": "Eric/Dermo"},
        {"Wave": "Wave 1", "Time": "16:30", "Court": "Court 4", "Group": "Group A", "Team 1": "Richie/Steve", "Team 2": "Jason/Wonka"},
        {"Wave": "Wave 2", "Time": "16:55", "Court": "Court 3", "Group": "Group A", "Team 1": "Stu/Niall Hayden", "Team 2": "Jason/Wonka"},
        {"Wave": "Wave 3", "Time": "17:20", "Court": "Court 3", "Group": "Group A", "Team 1": "Richie/Steve", "Team 2": "Eric/Dermo"},
        {"Wave": "Wave 3", "Time": "17:20", "Court": "Court 4", "Group": "Group A", "Team 1": "Eric/Dermo", "Team 2": "Jason/Wonka"},
        {"Wave": "Wave 4", "Time": "17:45", "Court": "Court 3", "Group": "Group A", "Team 1": "Stu/Niall Hayden", "Team 2": "Richie/Steve"},
        
        # --- GROUP B FIXTURES ---
        {"Wave": "Wave 1", "Time": "16:30", "Court": "Court 5", "Group": "Group B", "Team 1": "Jamie/Kevin", "Team 2": "Neil/Tom"},
        {"Wave": "Wave 2", "Time": "16:55", "Court": "Court 4", "Group": "Group B", "Team 1": "Simon/Cillian", "Team 2": "Gerry/Rob"},
        {"Wave": "Wave 2", "Time": "16:55", "Court": "Court 5", "Group": "Group B", "Team 1": "Jamie/Kevin", "Team 2": "Gerry/Rob"},
        {"Wave": "Wave 3", "Time": "17:20", "Court": "Court 4", "Group": "Group B", "Team 1": "Simon/Cillian", "Team 2": "Neil/Tom"},
        {"Wave": "Wave 4", "Time": "17:45", "Court": "Court 5", "Group": "Group B", "Team 1": "Neil/Tom", "Team 2": "Gerry/Rob"},
        {"Wave": "Wave 4", "Time": "17:45", "Court": "Court 5", "Group": "Group B", "Team 1": "Jamie/Kevin", "Team 2": "Simon/Cillian"},
    ]
    st.session_state.matches = pd.DataFrame(data)
    # Add empty numeric columns for live scoring input if not already present
    if "Score 1" not in st.session_state.matches.columns:
        st.session_state.matches["Score 1"] = None
    if "Score 2" not in st.session_state.matches.columns:
        st.session_state.matches["Score 2"] = None

# 3. Dynamic Standings Engine (Fixed Syntax Error & Tracking Points Scored Only)
def calculate_standings(df, group_name):
    group_df = df[df['Group'] == group_name]
    teams = list(set(group_df['Team 1'].unique()).union(set(group_df['Team 2'].unique())))
    
    # Tracking Match Points (2 pts per win, 0 per loss) and Score Total (Points Scored Summed)
    stats = {team: {"P": 0, "W": 0, "L": 0, "Match Points": 0, "Score Total": 0} for team in teams}
    
    for _, row in group_df.iterrows():
        if pd.notnull(row['Score 1']) and pd.notnull(row['Score 2']):
            t1, t2 = row['Team 1'], row['Team 2']
            try:
                s1, s2 = int(float(row['Score 1'])), int(float(row['Score 2']))
            except (ValueError, TypeError):
                continue
            
            stats[t1]["P"] += 1
            stats[t2]["P"] += 1
            stats[t1]["Score Total"] += s1
            stats[t2]["Score Total"] += s2
            
            if s1 > s2:
                stats[t1]["W"] += 1
                stats[t1]["Match Points"] += 2
                stats[t2]["L"] += 1
            elif s2 > s1:
                stats[t2]["W"] += 1
                stats[t2]["Match Points"] += 2
                stats[t1]["L"] += 1
            else:
                # If there's an exact draw, allocate 1 match point to each team
                stats[t1]["Match Points"] += 1
                stats[t2]["Match Points"] += 1

    # Apply the Spreadsheet Rule: If a team wins all 3 group matches, award +100 bonus to Score Total
    for team in stats:
        if stats[team]["W"] == 3:
            stats[team]["Score Total"] += 100
        
    standings_df = pd.DataFrame.from_dict(stats, orient='index').reset_index()
    standings_df.columns = ['Team', 'P', 'W', 'L', 'Match Points', 'Score Total']
    
    # Sort by Match Points first, then break ties with points Score Total
    return standings_df.sort_values(by=['Match Points', 'Score Total'], ascending=False).reset_index(drop=True)


# ==========================================
# SECTION 1: INTERACTIVE FIXTURES GRID
# ==========================================
st.markdown("<p class='section-font'>📅 Full Tournament Schedule & Live Scores</p>", unsafe_allow_html=True)
st.caption("💡 Admin Instruction: Click directly on any box in the 'Score 1' or 'Score 2' columns to type in results live!")

edited_df = st.data_editor(
    st.session_state.matches,
    column_order=["Wave", "Time", "Court", "Group", "Team 1", "Score 1", "Score 2", "Team 2"],
    disabled=["Wave", "Time", "Court", "Group", "Team 1", "Team 2"], 
    use_container_width=True,
    hide_index=True,
    key="tournament_editor"
)

if not edited_df.equals(st.session_state.matches):
    st.session_state.matches = edited_df
    st.rerun()

# Run calculations using safe data state
group_a_table = calculate_standings(st.session_state.
