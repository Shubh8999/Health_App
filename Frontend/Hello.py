import streamlit as st
import pandas as pd
import numpy as np
from gensim.models import Word2Vec
from datetime import datetime
import sqlite3

# Connect to the database
conn = sqlite3.connect('../Data/1_mental_health_chatbot.db')
c = conn.cursor()

# Create a table to store user information
c.execute('''CREATE TABLE IF NOT EXISTS users
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              username TEXT UNIQUE,
              password TEXT)''')



# Define a function to insert a new user account into the database


def insert_user_account(conn, username, password):
    c = conn.cursor()
    c.execute("INSERT INTO user_accounts (username, password) VALUES (?, ?)",
              (username, password))
    conn.commit()

# Define a function to check if a user account exists in the database


def check_user_account(conn, username, password):
    c = conn.cursor()
    c.execute("SELECT id FROM user_accounts WHERE username = ? AND password = ?",
              (username, password))
    result = c.fetchone()
    if result:
        return result[0]
    else:
        return None


def authenticate(username, password):
    # Check username and password (omitted for brevity)
    if username == "user" and password == "password":
        return True
    else:
        return False


def login():
    st.write("# Login")
    st.markdown("""

    <style>
    .css-1uii870.e16nr0p34{
        padding: 6px;
    }

    .css-1uii870.e16nr0p34 p{
        font-size: 18px;
        font-weight: bold;
    }

    .css-9gn890.e16nr0p34 p
    {
        font-weight: bold;

    }
    .css-10trblm.e16nr0p30
    {
        text-align: center;
    }
    .css-1e1k72n.e1fqkh3o1 {
            display: none;
    }

    </style>

    """, unsafe_allow_html=True)
    # st.markdown('<style>body { background-color: #000000; }</style>', unsafe_allow_html=True)
    # username = st.text_input("Username")
    # password = st.text_input("Password", type="password")
    # if st.button("Login"):
    #     if authenticate(username, password):
    #         # Set user as authenticated
    #         st.session_state.authenticated = True
    #         # Redirect to main app
    #         st.experimental_set_query_params(page="app")
    #         st.experimental_rerun()
    #     else:
    #         st.error("Invalid username or password")
    # Show the login or sign-up form
    form_type = st.radio("Select an option:", ["Login", "Sign up"])

    if form_type == "Login":
        st.write("Welcome back! Please enter your credentials to log in.")
        # Show the login form
        username = st.text_input("Username:")
        password = st.text_input("Password:", type="password")
        if st.button("Login"):
            # Check if the username and password are correct
            c.execute(
                "SELECT * FROM users WHERE username=? AND password=?", (username, password))
            user = c.fetchone()
            if user:
                # Store the user ID in session state
                st.session_state.user_id = user[0]
                st.write(f"Logged in as {user[1]}.")
                st.session_state.authenticated = True
                st.experimental_set_query_params(page="app", user=user[0])
                st.experimental_rerun()
            else:
                st.error("Incorrect username or password. Please try again.")
    elif form_type == "Sign up":
        st.write("Welcome! Please fill out the form below to create a new account.")
    # Show the sign-up form
        new_username = st.text_input("Username:")
        new_password = st.text_input("Password:", type="password")
        confirm_password = st.text_input("Confirm password:", type="password")
        if new_password != confirm_password:
            st.error("Passwords do not match. Please try again.")
        else:
            # Show the sign-up button
            if st.button("Sign up"):
                # Check if the username already exists
                c.execute("SELECT * FROM users WHERE username=?",
                          (new_username,))
                if c.fetchone() is not None:
                    st.error(
                        "Username already exists. Please choose a different username.")
                else:
                    # Add the new user to the database
                    c.execute(
                        "INSERT INTO users (username, password) VALUES (?, ?)", (new_username, new_password))
                    conn.commit()
                    st.success(
                        "Account created successfully. Please log in to continue.")


def app():
    st.session_state.authenticated = True
    st.write("# Welcome to Diet Recommendation System! 👋")
    query_params = st.experimental_get_query_params()
    user_id = query_params["user"][0]
    st.session_state.user_id = user_id
    st.markdown(
        """
        We have developed a diet recommendation system using Scikit-Learn, FastAPI and Streamlit.
        We will help you to achieve your health goals by giving you a the best diet.
        """

    )
    
    link1 = '<a href="/Chatbot?user_id={}#my_anchor" target="_self" style="font-size: 24px; color: blue; text-decoration: none;font-weight:bold;">Chatbot</a>'.format(user_id)
    st.markdown(link1, unsafe_allow_html=True)
    link2 = '<a href="/Custom_food#my_anchor" target="_self" style="font-size: 24px; color: blue; text-decoration: none;font-weight:bold;">Custom Food Recommendation</a>'
    st.markdown(link2, unsafe_allow_html=True)
    link3 = '<a href="/Diet_Recommendation#my_anchor" target="_self" style="font-size: 24px; color: blue; text-decoration: none;font-weight:bold;">Diet Recommendation</a>'
    st.markdown(link3, unsafe_allow_html=True)


def main():
    params = st.experimental_get_query_params()
    if "page" not in params:
        login()
    elif params["page"][0] == "app":
        if st.session_state.get("authenticated"):
            app()
        else:
            login()


if __name__ == '__main__':
    st.set_page_config(
        page_title="Hello",
        page_icon="👋",
        initial_sidebar_state="collapsed"
    )
    main()
