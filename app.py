import streamlit as st
import login
import mongo

if 'db' not in st.session_state:
    mongo.db_init()

collection = st.session_state['db']['cti-blob']
auth = st.session_state['db']['auth']

st.set_page_config(page_title="Auto CTI", initial_sidebar_state="expanded")
st.title("Dashboard")

login.sidebar()

if st.session_state['user'] != None:
    user_config = st.session_state['db']['config'].find_one({"user": st.session_state['user']})
    if not user_config:
        st.warning("Create User Config in Profile Page")
    else:
        user_config = user_config["config"]
        alerts = list(collection.find({"tags": {"$in": user_config}}))

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
                st.write(entry['actionable_steps'])
                st.link_button("Link", url=entry['metadata']['link'])
else:
    st.warning("Please Login or Create an Account")



