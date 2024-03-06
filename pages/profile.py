import streamlit as st
import bcrypt
import login
import time

auth = login.sidebar()

if st.session_state['user']:
    st.title(st.session_state['user'])

    #st.selectbox()
else:
    st.warning("Login or create an account")

    with st.expander("Create an account"):
        username = st.text_input("Username")
        password = st.text_input('Password')
        #try:
        if auth.find_one({"user": username}):
            st.warning("User already exists")
        elif str(username) and str(password):
            hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            if st.button("Create User"):
                with st.spinner("Creating User"):
                    auth.insert_one({"user": username, "pass": hashed})
                    time.sleep(2)
                st.session_state['user'] = username
                st.rerun()
            

        # except:
        #      st.error("Invalid username and password")
