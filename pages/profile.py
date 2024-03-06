import streamlit as st
import login
login.sidebar()

if st.session_state['user']:
    st.title(st.session_state['user'])

    #st.selectbox()
else:
    st.warning("Login or create an account")