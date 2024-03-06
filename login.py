import streamlit as st
from pymongo import MongoClient
def sidebar():
    client = MongoClient(st.secrets['uri'])
    db = client['test']
    auth = db['auth']

    # Login
    with st.sidebar:
        if 'user' not in st.session_state:
            st.session_state['user'] = None

        if st.session_state['user'] == None:
            username = st.text_input("Username:")
            password = st.text_input("Password:")
            if st.button("Login"):
                # add hash
                if auth.find_one({"user": username, "pass": password}):
                    st.session_state['user'] = username
                    st.rerun()
                else:
                    st.error("Incorrect username/password")
        else:
            st.title(f"Hello {st.session_state['user']}")
            if st.button("Logout"):
                st.session_state['user'] = None
                st.rerun()