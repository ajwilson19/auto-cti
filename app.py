import streamlit as st
import requests
import json

st.set_page_config(page_title="Auto CTI",)
st.title("Hello World")


if st.button("Hello World"):
    response = requests.get(url=st.secrets['endpoint'])
    st.write(response.content)