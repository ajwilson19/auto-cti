import streamlit as st
from pymongo import MongoClient

def db_init():
    client = MongoClient(st.secrets['uri'])
    db = client['test']
    st.session_state['db'] = db