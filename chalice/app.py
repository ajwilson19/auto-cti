from chalice import Chalice
import os
from openai import OpenAI
import json

app = Chalice(app_name='helloworld')

@app.route('/')
def index():
    return {'hello':'world'}

@app.route('/gpt', methods=['POST'])
def gpt():
    openai_api_key = os.environ.get('OPENAI_API_KEY')
    request = app.current_request.json_body
    
    #ex: {"api_key":"key", "model":"gpt-3.5-turbo", "messages": [], "temperature":0}

    try:
        
        client = OpenAI(api_key=openai_api_key)
        response = client.chat.completions.create(
            model=request['model'],
            messages=request['messages'],
            temperature=request['temperature'],
        )

        return json.dumps(json.loads(response.model_dump_json()), indent=4)
    except Exception as e:
        return {'success': False, 'error': str(e)}


