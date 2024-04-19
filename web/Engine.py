# heart of the program to run the webscraping
from pymongo import MongoClient
import web.WebScrape as WebScrape
import json
from openai import OpenAI
import os

openai_key = os.environ.get('OPENAI_API_KEY')
mongo_uri = os.environ.get('MONGO')

def run():
    mongo = MongoClient(mongo_uri)

    new_articles=[]
    sources = read_links()

    for link in sources:
        for article in WebScrape.scrape_link(link):
            
            if is_new(mongo, article):
                print(article)
                new_articles.append(article)
    
    status = upload(mongo, new_articles)
    if status['status']:
        print(status['count'])
    else:
        print(status['error'])



def read_links():
    links = open("cti-links.txt").readlines()
    return [link.replace("\n", "") for link in links]

def is_new(mongo, link):
    db = mongo['test']['cti-blob']
    return not db.find_one({"metadata.link": link})

    
def upload(mongo, links):
    count = 0

    client = OpenAI(api_key=openai_key)

    prompt = open("web/source/system_prompt.txt", 'r').read()
    schema = json.load(open("web/source/schema.json", 'r'))
    system_prompt = f"{prompt}\n\n{str(schema)}"

    payload = WebScrape.get_formatted(links)
    for bundle in payload:
        link = bundle[0]
        text = bundle[1]

        messages = [{"role": "system", "content": system_prompt},
                {"role": 'user', "content":text}]
        
        try:
            
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                temperature=0,
            )

            output = json.loads(response.choices[0].message.content)
            estimate = (response.usage.prompt_tokens / 1000) * 0.0005 + (response.usage.completion_tokens / 1000) * 0.0015
            metadata = {"link": link, "cost": estimate}
            output["metadata"] = metadata

            db = mongo['test']['cti-blob']
            db.insert_one(output)
            count += 1
            
        except Exception as e:
            return {'status': False, 'error': str(e)}
    
    return {'status': True, 'count': count}
        