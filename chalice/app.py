from chalice import Chalice
import os
from openai import OpenAI
from pymongo import MongoClient
import json

app = Chalice(app_name='auto-cti')
openai_api_key = os.environ.get('OPENAI_API_KEY')
client = OpenAI(api_key=openai_api_key)

mongo_uri = os.environ.get('MONGO')
mongo = MongoClient(mongo_uri)
db = mongo['test']

@app.route('/', methods=['GET'])
def index():
    count = db['api'].find_one()['count']
    return {'count':count}

@app.route('/gpt', methods=['POST'])
def gpt():

    request = app.current_request.json_body

    try:
        
        response = client.chat.completions.create(
            model=request['model'],
            messages=request['messages'],
            temperature=request['temperature'],
        )

        return json.dumps(json.loads(response.model_dump_json()), indent=4)
    except Exception as e:
        return {'success': False, 'error': str(e)}

@app.schedule('rate(1 minute)')
def gather(event):
    db['api'].update_one({}, {'$inc': {'count': 1}}, upsert=True)
    #articles = Engine.run()
    #articles in form [articlenum,article,article link]
    # check if link exists in db
    # if not, run /gpt on the article
    # if yes, ignore


