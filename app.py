import streamlit as st

st.set_page_config(page_title="Auto CTI",)

tags = []

from pymongo import MongoClient
client = MongoClient(st.secrets['uri'])
db = client['test']
collection = db['cti-blob']

result = list(collection.find({}))
for entry in result:
    try:
        for tag in entry['tags']:
            if tag not in tags:
                tags.append(tag)
    except:
        print(entry['_id'])

tags.sort()

tag_select = st.multiselect("Tags", tags)
result = list(collection.find({"tags": {"$in": tag_select}}))
for entry in result:
    with st.expander(str(entry["_id"])):
        st.json(entry)
