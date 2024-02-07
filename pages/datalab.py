import streamlit as st
import requests

st.title("Chalice Increment")

increment = st.text_input("Enter a number")
if st.button("Source"):
    url = st.secrets["endpoint"]
    url = url + "/" + increment
    response = requests.get(url).json()
    st.write(response)
    with st.expander("JSON"):
        st.json(response)
    