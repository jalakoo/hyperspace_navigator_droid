import os
import streamlit as st

OPENAI_KEY = os.environ.get("OPENAI_API_KEY", None)
if OPENAI_KEY is None:
        OPENAI_KEY = st.secrets["OPENAI_API_KEY"]

PLOTTER_URL = os.environ.get("PLOTTER_URL", None)
if PLOTTER_URL is None:
    plotter_url = st.secrets["PLOTTER_URL"]

