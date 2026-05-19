import streamlit as st
import pandas as pd

# Page Configuration
st.set_page_config(page_title="Portmarnock Padel Palooza", layout="centered")

# Custom CSS for Full App Customization (Black Background, Yellow Text)
st.markdown("""
    <style>
    /* Dark theme wrapper */
    html, body, [data-testid="stAppViewContainer"],
