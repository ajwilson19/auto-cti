import streamlit as st
import requests

st.title("Chalice Increment")

increment = st.text_input("Enter a number")
if st.button("Source"):
    url = st.secrets["endpoint"]
    url = url + "/" + increment
    response = requests.get(url)
    st.write(response.content)