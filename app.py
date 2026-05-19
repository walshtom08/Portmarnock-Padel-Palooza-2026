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
    .section-font { font-size:24px !important; font-weight: bold; color: #F7D060; margin-top: 20px; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<p class='title-font'>🎾 Portmarnock Padel Palooza 🎾</p>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Live Tournament Dashboard & Score Tracker</p>", unsafe_allow_html=True)
st.markdown("---")

# 2. Initialize Tournament Data (2 Groups, 4 Teams Each)
if 'matches' not in st.session_state:
    # UPDATE THESE NAMES TO MATCH YOUR EXACT TOURNAMENT PAIRS
    group_a_teams = ["Stu/Niall Hayden", "Eric/Dermo", "Team A3", "Team A4"]
    group_b_teams = ["Team B1", "Team B2", "Team B3", "Team B4"]
    
    data = [
        # --- WAVE 1 ---
        {"id": 1, "Wave": "Wave 1", "Stage": "Group A", "Time": "16:30", "Court": "Court 1", "Team1": group_a_teams[0], "Score1": 0, "Team2": group_a_teams[1], "Score2": 0, "Played": False},
        {"id": 2, "Wave": "Wave 1", "Stage": "Group A", "Time": "16:30", "Court": "Court 2", "Team1": group_a_teams[2], "Score1": 0, "Team2": group_a_teams[3], "Score2": 0, "Played": False},
        {"id": 3, "Wave": "Wave 1", "Stage": "Group B", "Time": "16:50", "Court": "Court 3", "Team1": group_b_teams[0], "Score1": 0, "Team2": group_b_teams[1], "Score2": 0, "Played": False},
        {"id": 4, "Wave": "Wave 1", "Stage": "Group B", "Time": "16:50", "Court": "Court 4", "Team1": group_b_teams[2], "Score1": 0, "Team2": group_b_teams[3], "Score2": 0, "Played": False},
        
        # --- WAVE 2 ---
        {"id": 5, "Wave": "Wave 2", "Stage": "Group A", "Time": "17:10", "Court": "Court 1", "Team1": group_a_teams[0], "Score1": 0, "Team2": group_a_teams[2], "Score2": 0, "Played": False},
        {"id": 6, "Wave": "Wave 2", "Stage": "Group A", "Time": "17:10", "Court": "Court 2", "Team1": group_a_teams[1], "Score1": 0, "Team2": group_a_teams[3], "Score2": 0, "Played": False},
        {"id": 7, "Wave": "Wave 2", "Stage": "Group B", "Time": "17:30", "Court": "Court 3", "Team1": group_b_teams[0], "Score1": 0, "Team2": group_b_teams[2], "Score2": 0, "Played": False},
        {"id": 8, "Wave": "Wave 2", "Stage": "Group B", "Time": "17:30", "Court": "Court 4", "Team1": group_b_teams[1], "Score1": 0, "Team2":
