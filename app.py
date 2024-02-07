import streamlit as st
import requests

st.title("Hello World")
st.multiselect("Options", ["Linux", "Windows", "MacOS", "iOS", "Android"])


testData = {
            "Instance 1": ["1", "10/18/2022", "Linux", "ssh"],
            "Instance 2": ["5", "10/18/2022", "Linux", "ufw"],
            "Instance 3": ["2", "10/18/2022", "Windows", "Chrome"],
            "Instance 4": ["3", "10/18/2022", "iOS", "Finder"],
            "Instance 5": ["1", "10/18/2022", "Windows", "Microsoft Word"],
            "Instance 6": ["2", "10/18/2022", "iOS", "Messaging"],
            "Instance 7": ["3", "10/18/2022", "Linux", "fail2ban"]
           }
with st.expander("Data"):
    st.dataframe(data=testData)