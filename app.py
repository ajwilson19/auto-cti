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

if 'db' not in st.session_state:
    db_init()

collection = st.session_state['db']['cti-blob']
auth = st.session_state['db']['auth']

st.set_page_config(page_title="Auto CTI", initial_sidebar_state="expanded")
st.title("Dashboard")

sidebar()

if st.session_state['user'] != None:
    user_config = st.session_state['db']['config'].find_one({"user": st.session_state['user']})
    if not user_config:
        st.warning("Create User Config in Profile Page")
    else:
        user_config = user_config["config"]
        alerts = list(collection.find({"tags": {"$in": user_config}})) # reverse w/[::-1]

        count = collection.count_documents({})
        #tags = collection.distinct('tags')
        vuln = collection.distinct('vulnerabilities')

        col1, col2, col3 = st.columns(3)
        col1.metric("Flagged Alerts", len(alerts), "")
        col2.metric("Total Alerts", count, "")
        col3.metric("CVEs", len(vuln), "")



        for entry in alerts:
            with st.expander(entry["title"]):
                st.write(entry['summary'])
                bullet_list = "\n".join([f"* {item}" for item in entry["actionable_steps"]])
                st.markdown(bullet_list)
                st.link_button("Link", url=entry['metadata']['link'])
else:
    st.warning("Please Login or Create an Account")



