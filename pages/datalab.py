import streamlit as st
import requests
from time import time
import json

import WebScrape
from pymongo import MongoClient

# potentially obfuscate + true handling
try:
    client = MongoClient(st.secrets['uri'])
    db = client['test']
    collection = db['cti-blob']
except:
    st.warning("DB offline")

# session state?
prompt = open("source/system_prompt.txt", 'r').read()
schema = json.load(open("source/schema.json", 'r'))

system_prompt = f"{prompt}\n\n{str(schema)}"
messages = [{"role": "system", "content": system_prompt},
            {"role": 'user', "content":""}]

link = st.text_input(label="Link:", value="")

#+value checking for links
if link != '':
    start_time = time()
    with st.spinner("Scraping Text"): 
        messages[1]['content'] =  WebScrape.scrape_article(link)

    with st.spinner("Generating"):
        request = {"model":"gpt-3.5-turbo", "messages": messages, "temperature":0}
        url = st.secrets['endpoint'] + "/gpt"
        response = requests.post(url, json=request).json()

    try:
        end_time = time()
        elapsed_time = end_time-start_time
        result = json.loads(response['choices'][0]['message']['content'])
        st.write(result)

        usage = response['usage']
        in_tokens = usage['prompt_tokens']
        out_tokens = usage['completion_tokens']
        estimate = (in_tokens / 1000) * 0.0005 + (out_tokens / 1000) * 0.0015


        result['metadata'] = {"link": link, "time": elapsed_time, "cost": estimate}
        print(result)

        collection.insert_one(result)
        st.success("Uploaded to DB")
        
    except:
        st.error(response)