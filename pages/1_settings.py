import streamlit as st
import requests
import time
from app import sidebar

sidebar("settings")

if st.session_state['user']:
    st.title(st.session_state['user'])

    profiles = requests.post(st.secrets['endpoint']+'profiles', json={'username': st.session_state['user']}).json()
    if profiles['success']:

        user_profiles = list(profiles['titles'])
        user_profiles.append('*') 
        config = st.selectbox("Profiles", user_profiles)

        tags = requests.post(st.secrets['endpoint']+'tags', json={'username': st.session_state['user'], 'title': config}).json()
        all_tags = requests.get(st.secrets['endpoint']+'tags').json()['tags']

        if config != '*':
            st.write(tags['tags'])
            with st.expander("Edit Existing Config"):
                profile_tags = list(tags['tags'])
                selection = st.multiselect("Update Tags", all_tags, profile_tags)
                payload = {'username': st.session_state['user'], 'title': config, 'config': selection}
                if st.button("Update"):
                    update = requests.post(st.secrets['endpoint']+'userconfig', json=payload).json()
                    if update['success']:
                        st.success("Successfully updated")
                        time.sleep(1)
                        st.rerun()
        else:
            st.success("This profile will display all alerts")

        with st.expander("Create New Config"):
            title = st.text_input("Title")
            selection = st.multiselect("Tags", all_tags)
            payload = {'username': str(st.session_state['user']), 'title': title, 'config': selection}
            if st.button("Create"):
                response = requests.post(st.secrets['endpoint']+'userconfig', json=payload).json()
                if response['success']:
                    st.success("Successfully created")
                    time.sleep(1)
                    st.rerun()
            
else:
    with st.expander("Create Account"):
        username = st.text_input("Username")
        password = st.text_input('Password')
        if st.button("Create"):
            payload = {'username': username, 'password': password}
            with st.spinner(""):
                response = requests.post(st.secrets['endpoint']+'createuser', json=payload).json()
            if response['success']:
                st.success("Account created")
                st.session_state['user'] = response['user']
                time.sleep(2)
                st.rerun()
            else:
                st.error(response['error'])
