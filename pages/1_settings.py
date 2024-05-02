import streamlit as st
import bcrypt
import time

if 'db' not in st.session_state:
    st.switch_page("app.py")
collection = st.session_state['db']['cti-blob']
auth = st.session_state['db']['auth']
config = st.session_state['db']['config']


auth = st.session_state['db']['auth']

# Login
with st.sidebar:
    if 'user' not in st.session_state:
        st.session_state['user'] = None

    if st.session_state['user'] == None:
        username = st.text_input("Username:")
        password = st.text_input("Password:", type="password")
        if st.button("Login"):
            user = auth.find_one({"user": username})
            if user:
                if bcrypt.checkpw(password.encode('utf-8'), user["pass"]):
                    st.session_state['user'] = username
                    st.rerun()
                else:
                    st.error("Incorrect password")
            else:
                st.error("User does not exist")
    else:
        st.title(f"Hello {st.session_state['user']}")
        if st.button("Logout"):
            st.session_state['user'] = None
            st.rerun()


if st.session_state['user']:
    st.title(st.session_state['user'])

    user_config = config.find({"user": st.session_state['user']})
    titles = [c["title"] for c in user_config]
        
    if len(titles):
        config_title = st.selectbox("Current Configuration", titles)
        config_doc = config.find_one({"user": st.session_state['user'], "title": config_title})
        st.write(config_doc["config"])
        with st.expander("Edit Config"):
            ut = config_doc["config"]
            uc = st.multiselect("Update Tags", collection.distinct('tags'), ut)
            if st.button("Update"):
                id = config.find_one_and_replace({"user": st.session_state['user'], "title": config_title, "config": ut}, {"user": st.session_state['user'], "title": config_title, "config": uc})
                if id:
                    st.success("Configuration updated")
                    time.sleep(2)
                    st.rerun()
    
    with st.expander("New User Config"):
        title = st.text_input("Title")
        tags = st.multiselect("Select tags", collection.distinct('tags'))
        if st.button("Save"):
            if title != "":
                id = config.insert_one({"user": st.session_state['user'], "title":title, "config": tags})
                if id:
                    st.success("Configuration created sucessfully")
                    time.sleep(2)
                    st.rerun()
            else:
                st.error("Title Required")

else:
    st.warning("Login or create an account")

    with st.expander("Create an account"):
        username = st.text_input("Username")
        password = st.text_input('Password')
        #try:
        if auth.find_one({"user": username}):
            st.warning("User already exists")
        elif str(username) and str(password):
            hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            if st.button("Create User"):
                with st.spinner("Creating User"):
                    auth.insert_one({"user": username, "pass": hashed})
                    time.sleep(2)
                st.session_state['user'] = username
                st.rerun()
            

        # except:
        #      st.error("Invalid username and password")
