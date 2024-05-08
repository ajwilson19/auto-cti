import streamlit as st
import requests

def sidebar(page):
    with st.sidebar:
        if 'user' not in st.session_state:
            st.session_state['user'] = None

        if st.session_state['user'] == None:
            username = st.text_input("Username:", key=page+"usr")
            password = st.text_input("Password:", type="password", key=page+"pass")
            if st.button("Login", key=page+"log"):

                with st.spinner("Authenticating"):
                    auth = requests.post(st.secrets['endpoint']+'login', json={'username': username, 'password': password}).json()
                    if auth['success']:
                        st.session_state['user'] = auth['user']
                        st.rerun()
                    else:
                        st.error(auth['error'])

        else:
            st.title(f"Hello {st.session_state['user']}")
            if st.button("Logout", key=page+'out'):
                st.session_state['user'] = None
                st.rerun()

sidebar("home")

if st.session_state['user']:

    profiles = requests.post(st.secrets['endpoint']+'profiles', json={'username': st.session_state['user']}).json()
    if profiles['success']:

        user_profiles = list(profiles['titles'])
        user_profiles.append('*') 
        config = st.selectbox("Profiles", user_profiles)

        if config != '*':
            tags = requests.post(st.secrets['endpoint']+'tags', json={'username': st.session_state['user'], 'title': config}).json()
            alerts = requests.post(st.secrets['endpoint']+'feed', json={'tags': tags['tags']}).json()
        else:
            alerts = requests.get(st.secrets['endpoint']+'feed').json()

        if alerts['success']:

            # Metrics
            stats = requests.get(st.secrets['endpoint']+'stats').json()
            col1, col2, col3 = st.columns(3)
            col1.metric("Flagged Alerts", len(alerts['results']), "")
            col2.metric("Total Alerts", stats['count'], "")
            col3.metric("New in last 12hr", stats['last12'], delta=str(stats['last1'])+" in the last hour")

            # Display Alerts
            for entry in alerts['results'][::-1]:
                with st.expander(entry["title"]):
                    st.write(entry['summary'])
                    bullet_list = "\n".join([f"* {item}" for item in entry["actionable_steps"]])
                    st.markdown(bullet_list)
                    st.link_button("Link", url=entry['metadata']['link'])

        else:
            st.error("Error fetching data")
        
else:
    st.warning("Login or create an account")