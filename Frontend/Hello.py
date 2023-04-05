import streamlit as st

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)

st.write("# Welcome to Diet Recommendation System! 👋")

st.sidebar.success("Select a recommendation app.")

st.markdown(
    """
    We have developed a diet recommendation system using Scikit-Learn, FastAPI and Streamlit.
    We will help you to achieve your health goals by giving you a the best diet.
    """
)