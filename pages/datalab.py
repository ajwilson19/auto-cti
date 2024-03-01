import streamlit as st
import requests
from time import time
import WebScrape
import json

prompt = open("source/system_prompt.txt", 'r').read()
schema = json.load(open("source/schema.json", 'r'))

system_prompt = f"{prompt}\n\n{str(schema)}"
messages = [{"role": "system", "content": system_prompt},
            {"role": 'user', "content":""}]

link = st.text_input(label="Link:", value="")

if link != '':
    with st.spinner("Scraping Text"):
        text = WebScrape.scrape_article(link)
        with st.expander("Text"):
            st.write(text)

    messages[1]['content'] =  text


    if st.button("Generate"):
        with st.spinner("Generating"):
            start_time = time()
            request = {"model":"gpt-3.5-turbo", "messages": messages, "temperature":0}
            url = st.secrets['endpoint'] + "/gpt"
            response = requests.post(url, json=request).json()

        try:
            end_time = time()
            elapsed_time = end_time-start_time
            st.write(json.loads(response['choices'][0]['message']['content']))

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