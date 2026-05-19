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

# 2. INITIALIZE DATA FROM YOUR SPREADSHEET SCHEDULE
if 'matches' not in st.session_state:
    data = [
        # --- WAVE 1 (16:30) ---
        {"Wave": "Wave 1", "Time": "16:30", "Court": "Court 3", "Group": "Group A", "Team 1": "Stu/Niall Hayden", "Score 1": None, "Team 2": "Eric/Dermo", "Score 2": None},
        {"Wave": "Wave 1", "Time": "16:30", "Court": "Court 4", "Group": "Group A", "Team 1": "Richie/Steve", "Score 1": None, "Team 2": "Jason/Wonka", "Score 2": None},
        {"Wave": "Wave 1", "Time": "16:30", "Court": "Court 5", "Group": "Group B", "Team 1": "Jamie/Kevin", "Score 1": None, "Team 2": "Neil/Tom", "Score 2": None},
        
        # --- WAVE 2 (16:55) ---
        {"Wave": "Wave 2", "Time": "16:55", "Court": "Court 3", "Group": "Group A", "Team 1": "Stu/Niall Hayden", "Score 1": None, "Team 2": "Jason/Wonka", "Score 2": None},
        {"Wave": "Wave 2", "Time": "16:55", "Court": "Court 4", "Group": "Group B", "Team 1": "Simon/Cillian", "Score 1": None, "Team 2": "Gerry/Rob", "Score 2": None},
        {"Wave": "Wave 2", "Time": "16:55", "Court": "Court 5", "Group": "Group B", "Team 1": "Jamie/Kevin", "Score 1": None, "Team 2": "Gerry/Rob", "Score 2": None},
        
        # --- WAVE 3 (17:20) ---
        {"Wave": "Wave 3", "Time": "17:20", "Court": "Court 3", "Group": "Group A", "Team 1": "Richie/Steve", "Score 1": None, "Team 2": "Eric/Dermo", "Score 2": None},
        {"Wave": "Wave 3", "Time": "17:20", "Court": "Court 4", "Group": "Group A", "Team 1": "Eric/Dermo", "Score 1": None, "Team 2": "Jason/Wonka", "Score 2": None},
        {"Wave": "Wave 3", "Time": "17:20", "Court": "Court 4", "Group": "Group B", "Team 1": "Simon/Cillian", "Score 1": None, "Team 2": "Neil/Tom", "Score 2": None},
        
        # --- WAVE 4 (17:45) ---
        {"Wave": "Wave 4", "Time": "17:45", "Court": "Court 3", "Group": "Group A", "Team 1": "Stu/Niall Hayden", "Score 1": None, "Team 2": "Richie/Steve", "Score 2": None},
        {"Wave": "Wave 4", "Time": "17:45", "Court": "Court 5", "Group": "Group B", "Team 1": "Neil/Tom", "Score 1": None, "Team 2": "Gerry/Rob", "Score 2": None},
        {"Wave": "Wave 4", "Time": "17:45", "Court": "Court 5", "Group": "Group B", "Team 1": "Jamie/Kevin", "Score 1": None, "Team 2": "Simon/Cillian", "Score 2": None},
    ]
    st.session_state.matches = pd.DataFrame(data)

# 3. Dynamic Standings Engine (With +100 Unbeaten Bonus and Points Scored Tracker)
def calculate_standings(df, group_name):
    group_df = df[df['Group'] == group_name]
    teams = list(set(group_df['Team 1'].unique()).union(set(group_df['Team 2'].unique())))
    
    # Tracking Match Points (2 points per win, 0 per loss) and Score Total (Sum of game scores)
    stats = {team: {"P": 0, "W": 0, "L": 0, "Match Points": 0, "Score Total": 0} for team in teams}
    
    for _, row in group_df.iterrows():
        if pd.
