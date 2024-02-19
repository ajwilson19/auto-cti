import streamlit as st
import requests

st.title("Chalice x GPT")
# with st.expander("Resources"):
#     st.write("See guide [here](https://cookbook.openai.com/examples/how_to_format_inputs_to_chatgpt_models)")
#     st.write("Link guide [here](https://community.openai.com/t/how-is-gpt-4-getting-this-information-from-a-url/529074)")

messages = [{
                "role": "system",
                "content": 'You are a cyber threat intelligence analyst who helps extract information from articles.'
            },
            {"role": 'user', "content":""}]

link = st.text_input(label="Link:", value="")
messages[1]['content'] = f'Here is a URL: {link}'

st.code(
    """response = client.chat.completions.create(
        model=\'gpt-4-0613\',
        messages={},
        temperature=0,
    )""".format(messages)
)

if st.button("Generate"):
    with st.spinner("Generating"):
        request = {"model":"gpt-4-0613", "messages": messages, "temperature":0}
        url = st.secrets['endpoint'] + "/gpt"
        response = requests.post(url, json=request).json()

    try:
        st.write(response['choices'][0]['message']['content'])
        usage = response['usage']
        in_tokens = usage['prompt_tokens']
        out_tokens = usage['completion_tokens']

        estimate = (in_tokens / 1000) * 0.03 + (out_tokens / 1000) * 0.06
        st.warning(f'Estimated cost: ${estimate}')
    except:
        st.error("API Error")


    