import streamlit as st
import requests

st.title("Chalice x GPT")
st.write("See guide [here](https://cookbook.openai.com/examples/how_to_format_inputs_to_chatgpt_models)")
st.write("Link guide [here](https://community.openai.com/t/how-is-gpt-4-getting-this-information-from-a-url/529074)")

# if 'messages' not in st.session_state:
#     st.session_state.messages = []
# else:
#     messages = st.session_state.messages

messages = [{
                "role": "system",
                "content": 'You are a cyber threat intelligence analyst who helps extract information from articles.'
            },
            {"role": 'user', "content":""}]

#role = st.selectbox(label="Select Role:", options=["system", "user", "assistant"], index=1)
link = st.text_input(label="Link:", value="")
messages[1]['content'] = f'Here is a URL: {link}'

st.write(messages)

# if st.button(label="Reset"):
#     st.session_state.messages = []

# if st.session_state.messages == []:
#     st.warning("Please enter a message before requesting response")
# else:
    

st.code(
    """response = client.chat.completions.create(
        model=\'gpt-4-0613\',
        messages={},
        temperature=0,
    )""".format(messages)
)

if st.button("Generate"):
    request = {"model":"gpt-4-0613", "messages": messages, "temperature":0}
    #print(request)
    url = st.secrets['endpoint'] + "/gpt"
    response = requests.post(url, json=request)
    st.write(response)
    st.code(response.content)