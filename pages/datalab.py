import streamlit as st
import requests

st.title("Chalice API")

name = st.text_input("Name")
age = st.slider("Age", 0, 100, 0, 1)
json_post = {'name':name, 'age':age}

with st.expander("Request"):
    st.code(json_post)
    
if st.button("Source"):
    url = st.secrets["endpoint"] + "/api"

    response = requests.post(url, json=json_post)
    try:
        response = response.json()
        message = str(response['name']) + ' will be ' + str(response['age'])
        st.success(message)
    except:
        st.error("API error")

    with st.expander("Response"):
        st.code(response)
    