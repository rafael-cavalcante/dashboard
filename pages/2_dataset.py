import streamlit as st

st.set_page_config(
    page_title="Dashboard PRF",
    page_icon=":bar_chart:",
    layout="wide")

st.title("Página Datasets")

dataset = st.session_state["dataset"]

dataset
