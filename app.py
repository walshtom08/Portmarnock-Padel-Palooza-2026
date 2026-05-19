import streamlit as st
import pandas as pd

# Set up page config
st.set_page_config(page_title="Portmarnock Padel Palooza", layout="wide")

# Force full-app custom CSS styling (Pitch Black background, Pure Yellow Text)
st.markdown("""
    <style>
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #000000 !important;
        color: #FFFF00 !important;
    }
    h1, h2, h3, h4, p, span, label, div {
        color: #FFFF00 !important;
    }
    /* Force custom styling on editable grids */
    .stDataFrame div, .stDataFrame span, .stDataFrame table {
        color: #FFFF00 !important;
        background-color: #000000 !important;
    }
    /* Target inputs inside the grid cells */
    input {
        color: #FFFF00 !important;
        background-color: #111111 !important;
    }
    /* Style the main trigger button */
    .stButton>button {
        background-color: #111111 !important;
        color: #FFFF00 !important;
        border: 2px solid #FFFF00 !important;
        width: 100%;
        padding: 15px;
        font-weight: bold;
        font-size: 18px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🎾 PADEL PALOOZA 🎾")
st.write("Tap directly into any score cell below to enter results, then scroll to the bottom and click Save.")

# --- RAW MATCH DATA TEMPLATE ---
initial_matches = [
    # Group A
    {"ID": "GA1", "Sec": "Group A", "Wave": "W1", "Time": "16:30", "Ct": "3", "Team 1": "Stu/Niall Hayden", "S1": 0, "Team 2": "Eric/Dermo", "S2": 0},
    {"ID": "GA2", "Sec": "Group A", "Wave": "W1", "Time": "16:30", "Ct": "4", "Team 1": "Richie/Steve", "S1": 0, "Team 2": "Jason/Wonka", "S2": 0},
    {"ID": "GA3", "Sec": "Group A", "Wave": "W2", "Time": "16:55", "Ct": "3", "Team 1": "Stu/Niall Hayden", "S1": 0, "Team 2": "Jason/Wonka", "S2": 0},
    {"ID": "GA4", "Sec": "Group A", "Wave": "W3", "Time": "17:20", "Ct": "3", "Team 1": "Richie/Steve", "S1": 0, "Team 2": "Eric/Dermo", "S2": 0},
    {"ID": "GA5", "Sec": "Group A", "Wave": "W3", "Time": "17:20", "Ct": "4", "Team 1": "Eric/Dermo", "S1": 0, "Team 2": "Jason/Wonka", "S2": 0},
    {"ID": "GA6", "Sec": "Group A", "Wave": "W4", "Time": "17:45", "Ct": "3", "Team 1": "Stu/Niall Hayden", "S1": 0, "Team 2": "Richie/Steve", "S2": 0},
    # Group B
    {"ID": "GB1", "Sec": "Group B", "Wave": "W1", "Time": "16:30", "Ct": "5", "Team 1": "Jamie/Kevin", "S1": 0, "Team 2": "Neil/Tom", "S2": 0},
    {"ID": "GB2", "Sec": "Group B", "Wave": "W2", "Time": "16:55", "Ct": "4", "Team 1": "Simon/Cillian", "S1": 0, "Team 2": "Gerry/Rob", "S2": 0},
    {"ID": "GB3", "Sec": "Group B", "Wave": "W2", "Time": "16:55", "Ct": "5", "Team 1": "Jamie/Kevin", "S1": 0, "Team 2": "Gerry/Rob", "S2": 0},
    {"ID": "GB4", "Sec": "Group B", "Wave": "W3", "Time": "17:20", "Ct": "4", "Team 1": "Simon/Cillian", "S1": 0, "Team 2": "Neil/Tom", "S2": 0},
    {"ID": "GB5", "Sec": "Group B", "Wave": "W4", "Time": "17:45", "Ct": "5", "Team 1": "Neil/Tom", "S1": 0, "Team 2": "Gerry/Rob", "S2": 0},
    {"ID": "GB6", "Sec": "Group B", "Wave": "W4", "Time": "17:45", "Ct": "5", "Team 1": "Jamie/Kevin", "S1": 0, "Team 2": "Simon/Cillian", "S2": 0},
    # Knockouts
    {"ID": "KO1", "Sec": "Knockouts", "Wave": "W5", "Time": "18:10", "Ct": "3", "Team 1": "Group 1 3rd", "S1": 0, "Team 2": "Group 2 4th", "S2": 0},
    {"ID": "KO2", "Sec": "Knockouts", "Wave": "W5", "Time": "18:10", "Ct": "4", "Team 1": "Group 1 4th", "S1": 0, "Team 2": "Group 2 3rd", "S2": 0},
    {"ID": "KO3", "Sec": "Knockouts", "Wave": "W5", "Time": "18:10", "Ct": "5", "Team 1": "Jason/Wonka", "S1": 0, "Team 2": "Jamie/Kevin", "S2": 0},
    {"ID": "KO4", "Sec": "Knockouts", "Wave": "W6", "Time": "18:35", "Ct": "3", "Team 1": "Stu/Niall Hayden", "S1": 0, "Team 2": "Gerry/Rob", "S2": 0},
    # Finals
    {"ID": "F1", "Sec": "Finals", "Wave": "W6", "Time": "18:35", "Ct": "4", "Team 1": "Loser Semi 1", "S1": 0, "Team 2": "Loser Semi 2", "S2": 0},
    {"ID": "F2", "Sec": "Finals", "Wave": "W6", "Time": "18:35", "Ct": "5", "Team 1": "Winner Semi 1", "S1": 0, "Team 2": "Winner Semi 2", "S2": 0},
    {"ID": "F3", "Sec": "Finals", "Wave": "W7", "Time": "19:00", "Ct": "3", "Team 1": "Jamie/Kevin", "S1": 0, "Team 2": "Gerry/Rob", "S2": 0},
    {"ID": "F4", "Sec": "Finals", "Wave": "W8", "Time": "19:05", "Ct": "4", "Team 1": "Jamie/Kevin", "S1": 0, "Team 2": "Gerry/Rob", "S2": 0}
]

# Set up cloud synchronization database wrapper
try:
    conn = st.connection("cache", type="dict")
except Exception:
    conn = st.session_state

if "matches" not in conn:
    conn["matches"] = initial_matches

# Read latest state
current_data = pd.DataFrame(conn["matches"])

# Helper function to generate standardized grid configs optimized for mobile screens
def generate_grid(df_subset, unique_key):
    return st.data_editor(
        df_subset,
        key=unique_key,
        hide_index=True,
        column_order=["Wave", "Time", "Ct", "Team 1", "S1", "S2", "Team 2"],
        column_config={
            "Wave": st.column_config.TextColumn("W", width="small", disabled=True),
            "Time": st.column_config.TextColumn("Time", width="small", disabled=True),
            "Ct": st.column_config.TextColumn("Ct", width="small", disabled=True),
            "Team 1": st.column_config.TextColumn("Team 1", width="medium", disabled=True),
            "S1": st.column_config.NumberColumn("S1", width="small", min_value=0, max_value=100, step=1, required=True),
            "S2": st.column_config.NumberColumn("S2", width="small", min_value=0, max_value=100, step=1, required=True),
            "Team 2": st.column_config.TextColumn("Team 2", width="medium", disabled=True),
        }
    )

# --- RENDER THE SECTIONS ---

st.header("📋 Group A Fixtures")
df_a = current_data[current_data["Sec"] == "Group A"]
edited_a = generate_grid(df_a, "edit_group_a")

st.header("📋 Group B Fixtures")
df_b = current_data[current_data["Sec"] == "Group B"]
edited_b = generate_grid(df_b, "edit_group_b")

st.header("⚔️ Knockout Matches")
df_ko = current_data[current_data["Sec"] == "Knockouts"]
edited_ko = generate_grid(df_ko, "edit_ko")

st.header("🏆 The Cups & Finals")
df_f = current_data[current_data["Sec"] == "Finals"]
edited_f = generate_grid(df_f, "edit_finals")


# --- LIVE DATABASE RECONCILIATION AND SYNC ---
st.markdown("<br>", unsafe_allow_html=True)
if st.button("🔄 SAVE & SYNC ALL SCORES"):
    # Combine the edited data sheets back into a single frame
    combined_updated = pd.concat([edited_a, edited_b, edited_ko, edited_f])
    
    # Push back to cloud memory
    conn["matches"] = combined_updated.to_dict(orient="records")
    st.success("All match scores synchronized for the venue! Refreshing leaderboard...")
    st.rerun()

# --- DYNAMIC LIVE STANDINGS GENERATION ---
st.markdown("---")
st.header("📊 Live Group Standings")

def compute_standings(group_name, match_df):
    group_subset = match_df[match_df["Sec"] == group_name]
    teams = set(group_subset["Team 1"].unique()).union(set(group_subset["Team 2"].unique()))
    
    standings = {team: {"Played": 0, "Points": 0} for team in teams}
    
    for _, row in group_subset.iterrows():
        # Only evaluate scores if someone actually played/entered them (ignoring default 0-0 initialization states)
        if row["S1"] > 0 or row["S2"] > 0:
            t1, t2 = row["Team 1"], row["Team 2"]
            standings[t1]["Played"] += 1
            standings[t2]["Played"] += 1
            
            if row["S1"] > row["S2"]:
                standings[t1]["Points"] += 2  # 2 points for a win
            elif row["S2"] > row["S1"]:
                standings[t2]["Points"] += 2
            else:
                standings[t1]["Points"] += 1  # 1 point for a draw
                standings[t2]["Points"] += 1
                
    return pd.DataFrame.from_dict(standings, orient="index").reset_index().rename(columns={"index": "Team"}).sort_values(by="Points", ascending=False)

col1, col2 = st.columns(2)
with col1:
    st.subheader("Group A")
    st.dataframe(compute_standings("Group A", current_data), hide_index=True)
with col2:
    st.subheader("Group B")
    st.dataframe(compute_standings("Group B", current_data), hide_index=True)
