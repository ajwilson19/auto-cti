import streamlit as st
import bcrypt
from pymongo import MongoClient
import datetime

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
api = st.session_state['db']['api']

st.set_page_config(page_title="Auto CTI", initial_sidebar_state="expanded")
st.title("Dashboard")

sidebar()

if st.session_state['user'] != None:
    user_config = st.session_state['db']['config'].find({"user": st.session_state['user']})
    titles = [c["title"] for c in user_config]
    if not len(titles):
        st.warning("Create User Config in Profile Page")
    else:
        
        config_title = st.selectbox("Profile", titles)
        #gets list of tagged alerts in reverse order
        user_config = st.session_state['db']['config'].find_one({"user": st.session_state['user'], "title": config_title})['config']
        print(user_config)
        query = {
            "tags": {"$in": user_config},
        }
        # if st.toggle("Last 12 hrs"):
        #     query["time"] =  {"$gte":(datetime.datetime.now(tz=datetime.timezone.utc) - datetime.timedelta(hours=12)).strftime('%Y-%m-%dT%H:%M:%S.%fZ')}

        alerts = list(collection.find(query))[::-1]

        count = collection.count_documents({})
        #tags = collection.distinct('tags')
        # vuln = collection.distinct('vulnerabilities')
        activity = api.find_one({"activity": "list"})['count']
        new = sum(activity)

        # with st.expander("Recent Activity"):
        #     st.bar_chart(activity, use_container_width=True, height=200)

        col1, col2, col3 = st.columns(3)
        col1.metric("Flagged Alerts", len(alerts), "")
        col2.metric("Total Alerts", count, "")
        col3.metric("New in last 12hr", new, delta=str(activity[-1])+" in the last hour")



        for entry in alerts:
            with st.expander(entry["title"]):
                st.write(entry['summary'])
                bullet_list = "\n".join([f"* {item}" for item in entry["actionable_steps"]])
                st.markdown(bullet_list)
                st.link_button("Link", url=entry['metadata']['link'])
else:
    st.warning("Please Login or Create an Account")
