import streamlit as st
import requests

st.title("Chalice Increment")

increment = st.text_input("Enter a number")
if st.button("Source"):
    url = st.secrets["endpoint"]
    url = url + "/" + increment
    response = requests.get(url).json()
    for key in response:
        if key == 'result':
            st.success(response[key])
        elif key == 'error':
            st.error(response[key])
        else:
            st.warning(key + response[key])
    with st.expander("JSON"):
        st.json(response)
    