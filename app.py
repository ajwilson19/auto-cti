import streamlit as st

st.set_page_config(page_title="Auto CTI",)
st.title("tags")

from pymongo import MongoClient
client = MongoClient(st.secrets['uri'])
db = client['test']
collection = db['cti-blob']

result = list(collection.find({}))
for entry in result:
    try:
        st.write(entry['tags'])
    except:
        st.write(entry)
