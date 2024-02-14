import streamlit as st
import requests

st.title("Chalice x GPT")
st.write("See guide [here](https://cookbook.openai.com/examples/how_to_format_inputs_to_chatgpt_models)")

if 'messages' not in st.session_state:
    st.session_state.messages = []
else:
    messages = st.session_state.messages

role = st.selectbox(label="Select Role:", options=["system", "user", "assistant"], index=1)
content = st.text_input(label="Content:", value="")


if st.button(label="Add message"):
    messages.append({"role": role, "content": content})
    st.session_state.messages = messages

if st.button(label="Reset"):
    st.session_state.messages = []

if st.session_state.messages == []:
    st.warning("Please enter a message before requesting response")
else:
    st.code(
        """response = client.chat.completions.create(
            model=\"gpt-3.5-turbo\",
            messages={},
            temperature=0,
        )""".format(messages)
    )

    if st.button("Generate"):
        request = {"api_key":st.secrets['key'], "model":"gpt-3.5-turbo", "messages": messages, "temperature":0}
        url = st.secrets['endpoint'] + "/gpt"
        response = requests.post(url, json=request)
        print(response.content)
        st.code(response.content)