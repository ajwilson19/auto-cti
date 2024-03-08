import streamlit as st
import bcrypt
from pymongo import MongoClient

def db_init():
    client = MongoClient(st.secrets['uri'])
    db = client['test']
    st.session_state['db'] = db

def sidebar():
    auth = st.session_state['db']['auth']

    # Login
    with st.sidebar:
        if 'user' not in st.session_state:
            st.session_state['user'] = None

        if st.session_state['user'] == None:
            username = st.text_input("Username:")
            password = st.text_input("Password:", type="password")
            if st.button("Login"):
                user = auth.find_one({"user": username})
                if user:
                    if bcrypt.checkpw(password.encode('utf-8'), user["pass"]):
                        st.session_state['user'] = username
                        st.rerun()
                    else:
                        st.error("Incorrect password")
                else:
                    st.error("User does not exist")
        else:
            st.title(f"Hello {st.session_state['user']}")
            if st.button("Logout"):
                st.session_state['user'] = None
                st.rerun()