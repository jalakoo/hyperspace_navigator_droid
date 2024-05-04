import os
import streamlit as st

# Permits using either .env or Streamlit's secrets TOML file

OPENAI_KEY = os.environ.get("OPENAI_API_KEY", None)
if OPENAI_KEY is None:
        OPENAI_KEY = st.secrets["OPENAI_API_KEY"]

NEO4J_URI = os.environ.get("NEO4J_URI", None)
if NEO4J_URI is None:
    NEO4J_URI = st.secrets["NEO4J_URI"]
NEO4J_USER = os.environ.get("NEO4J_USER", None)
if NEO4J_USER is None:
   NEO4J_USER = st.secrets["NEO4J_USER"]
NEO4J_PASSWORD = os.environ.get("NEO4J_PASSWORD", None)
if NEO4J_PASSWORD is None:
    NEO4J_PASSWORD = st.secrets["NEO4J_PASSWORD"]
NEO4J_DATABASE = os.environ.get("NEO4J_DATABASE", None)
if NEO4J_DATABASE is None:
    NEO4J_DATABASE = st.secrets["NEO4J_DATABASE"]
