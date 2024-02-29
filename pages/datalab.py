import streamlit as st
import requests
from time import time

st.title("GPT in Chalice")
# with st.expander("Resources"):
#     st.write("See guide [here](https://cookbook.openai.com/examples/how_to_format_inputs_to_chatgpt_models)")
#     st.write("Link guide [here](https://community.openai.com/t/how-is-gpt-4-getting-this-information-from-a-url/529074)")

system_prompt = '''You are a cyber threat intelligence analyst who helps extract information from articles.
                    Your job is to provide a concise high level summary of the report that includes the names and
                    relevant information about the entities such as threat actors and malware. A critical component of 
                    your response is what actionable steps are identified in the article. Please include information on 
                    potential patches or solutions and list any relevant cves. Add relevant tags that can be used to easily
                    filter the information you extracted. You may include information on who is reporting or providing guidance
                    but do not include company specific products unless it is explicitly said that it is the only viable solution.
                    Provide the information you extracted as a json object that follows the rules of the following schema:
                    {
                        "$schema": "http://json-schema.org/draft-07/schema#",
                        "type": "object",
                        "properties": {
                        "threat_actors": {
                            "type": "array",
                            "items": {
                            "type": "object",
                            "properties": {
                                "name": {
                                "type": "string"
                                },
                                "aliases": {
                                "type": "array",
                                "items": {
                                    "type": "string"
                                }
                                },
                                "country": {
                                "type": "string"
                                }
                            },
                            "required": ["name", "aliases", "country"],
                            "additionalProperties": false
                            }
                        },
                        "malware": {
                            "type": "array",
                            "items": {
                            "type": "string"
                            }
                        },
                        "vulnerabilities": {
                            "type": "array",
                            "items": {
                            "type": "object",
                            "properties": {
                                "cve_id": {
                                "type": "string"
                                },
                                "description": {
                                "type": "string"
                                }
                            },
                            "required": ["cve_id", "description"],
                            "additionalProperties": false
                            }
                        },
                        "actionable_steps": {
                            "type": "array",
                            "items": {
                            "type": "string"
                            }
                        },
                        "tags": {
                            "type": "array",
                            "items": {
                            "type": "string"
                            }
                        },
                        "summary": {
                            "type": "object",
                            "properties": {
                            "summary": {
                                "type": "string",
                                "maxLength": 360
                            }
                            },
                            "required": ["summary"],
                            "additionalProperties": false
                        }
                        },
                        "required": ["threat_actors", "malware", "vulnerabilities", "actionable_steps", "tags", "summary"],
                        "additionalProperties": false
                    }'''

messages = [{"role": "system", "content": system_prompt},
            {"role": 'user', "content":""}]

text = st.text_input(label="Text:", value="")
messages[1]['content'] =  text

st.code(
    """response = client.chat.completions.create(
        model=\'gpt-3.5-turbo\',
        messages={},
        temperature=0,
    )""".format(messages)
)

if st.button("Generate"):
    with st.spinner("Generating"):
        start_time = time()
        request = {"model":"gpt-3.5-turbo", "messages": messages, "temperature":0}
        url = st.secrets['endpoint'] + "/gpt"

        # header = {
        #     'x-api-key': st.secrets['key']
        # }
        response = requests.post(url, json=request).json() #headers=header

    try:
        end_time = time()
        elapsed_time = end_time-start_time

        st.write(response['choices'][0]['message']['content'])

        usage = response['usage']
        in_tokens = usage['prompt_tokens']
        out_tokens = usage['completion_tokens']
        estimate = (in_tokens / 1000) * 0.0005 + (out_tokens / 1000) * 0.0015

        with st.expander("Stats"):
            st.write(f"Total Tokens: {in_tokens+out_tokens}")
            st.write(f"Estimated Cost: {estimate}")
            st.write(f"Time Elapsed: {elapsed_time:.2f} seconds")

        
    except:
        st.error(response)


    