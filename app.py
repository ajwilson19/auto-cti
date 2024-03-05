import streamlit as st

st.set_page_config(page_title="Auto CTI",)
st.title("Dashboard")

from pymongo import MongoClient
client = MongoClient(st.secrets['uri'])
db = client['test']
collection = db['cti-blob']

count = collection.count_documents({})
tags = collection.distinct('tags')
vuln = collection.distinct('vulnerabilities')

col1, col2, col3 = st.columns(3)
col1.metric("Alerts", count, "")
col2.metric("Tags", len(tags), "")
col3.metric("CVEs", len(vuln), "")


tag_select = st.multiselect("Tags", tags)
result = list(collection.find({"tags": {"$in": tag_select}}))
for entry in result:
    with st.expander(str(entry["_id"])):
        st.json(entry)
