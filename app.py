import streamlit as st
import pandas as pd
import numpy as np

# Page setup for mobile and desktop tracking
st.set_page_config(
    page_title="Portmarnock Padel Palooza",
    page_icon="🎾",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for the clean tournament look
st.markdown("""
    <style>
    .title-font { font-size:32px !important; font-weight: bold; color: #F7D060; text-align: center; }
    .section-font { font-size:22px !important; font-weight: bold; color: #F7D060; margin-top: 15px; }
    .stTabs [data-baseweb="tab"] { font-size: 18px; font-weight: 600; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<p class='title-font'>🎾 Portmarnock Padel Palooza 🎾</p>", unsafe_allow_html=True)
st.center = st.markdown("<p style='text-align: center;'>Live Tournament Dashboard & Score Tracker</p>", unsafe_allow_html=True)
st.markdown("---")

# 1. INITIALIZE DATA (2 Groups, 4 Teams Each)
# Change the team placeholders below to match your exact spreadsheet names
if 'matches' not in st.session_state:
    group_a_teams = ["Stu/Niall Hayden", "Eric/Dermo", "Team A3", "Team A4"]
    group_b_teams = ["Team B1", "Team B2", "Team B3", "Team B4"]
    
    data = [
        # --- WAVE 1 (16:30 - 16:50) ---
        {"id": 1, "Wave": "Wave 1", "Stage": "Group A", "Time": "16:30", "Court": "Court 1", "Team1": group_a_teams[0], "Score1": 0, "Team2": group_a_teams[1], "Score2": 0, "Played": False},
        {"id": 2, "Wave": "Wave 1", "Stage": "Group A", "Time": "16:30", "Court": "Court 2", "Team1": group_a_teams[2], "Score2": 0, "Team2": group_a_teams[3], "Score2": 0, "Played": False},
        {"id": 3, "Wave": "Wave 1", "Stage": "Group B", "Time": "16:50", "Court": "Court 3", "Team1": group_b_teams[0], "Score1": 0, "Team2": group_b_teams[1], "Score2": 0, "Played": False},
        {"id": 4, "Wave": "Wave 1", "Stage": "Group B", "Time": "16:50", "Court": "Court 4", "Team1": group_b_teams[2], "Score1": 0, "Team2": group_b_teams[3], "Score2": 0, "Played": False},
        
        # --- WAVE 2 (17:10 - 17:30) ---
        {"id": 5, "Wave": "Wave 2", "Stage": "Group A", "Time": "17:10", "Court": "Court 1", "Team1": group_a_teams[0], "Score1": 0, "Team2": group_a_teams[2], "Score2": 0, "Played": False},
        {"id": 6, "Wave": "Wave 2", "Stage": "Group A", "Time": "17:10", "Court": "Court 2", "Team1": group_a_teams[1], "Score1": 0, "Team2": group_a_teams[3], "Score2": 0, "Played": False},
        {"id": 7, "Wave": "Wave 2", "Stage": "Group B", "Time": "17:30", "Court": "Court 3", "Team1": group_b_teams[0], "Score1": 0, "Team2": group_b_teams[2], "Score2": 0, "Played": False},
        {"id": 8, "Wave": "Wave 2", "Stage": "Group B", "Time": "17:30", "Court": "Court 4", "Team1": group_b_teams[1], "Score1": 0, "Team2": group_b_teams[3], "Score2": 0, "Played": False},
        
        # --- WAVE 3 (17:50 - 18:10) ---
        {"id": 9, "Wave": "Wave 3", "Stage": "Group A", "Time": "17:50", "Court": "Court 1", "Team1": group_a_teams[0], "Score1": 0, "Team2": group_a_teams[3], "Score2": 0, "Played": False},
        {"id": 10, "Wave": "Wave 3", "Stage": "Group A", "Time": "17:50", "Court": "Court 2", "Team1": group_a_teams[1], "Score1": 0, "Team2": group_a_teams[2], "Score2": 0, "Played": False},
        {"id": 11, "Wave": "Wave 3", "Stage": "Group B", "Time": "18:10", "Court": "Court 3", "Team1": group_b_teams[0], "Score1": 0, "Team2": group_b_teams[3], "Score2": 0, "Played": False},
        {"id": 12, "Wave": "Wave 3", "Stage": "Group B", "Time": "18:10", "Court": "Court 4", "Team1": group_b_teams[1], "Score1": 0, "Team2": group_b_teams[2], "Score2": 0, "Played": False},
    ]
    st.session_state.matches = pd.DataFrame(data)

# 2. STANDINGS CALCULATION (Tracks Points, Games Won/Lost Differentials)
def calculate_standings(df, group_name):
    group_df = df[df['Stage'] == group_name]
    teams = list(set(group_df['Team1'].unique()).union(set(group_df['Team2'].unique())))
    
    # Track Played, Wins, Losses, Games For, Games Against, Points
    stats = {team: {"P": 0, "W": 0, "L": 0, "GF": 0, "GA": 0, "Diff": 0, "Pts": 0} for team in teams}
    
    for _, row in group_df.iterrows():
        if row['Played']:
            t1, t2 = row['Team1'], row['Team2']
            s1, s2 = int(row['Score1']), int(row['Score2'])
            
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
                stats[t1]["L"] +=
