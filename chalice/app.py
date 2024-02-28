from chalice import Chalice
import os
from openai import OpenAI
import json

app = Chalice(app_name='helloworld')
openai_api_key = os.environ.get('OPENAI_API_KEY')
client = OpenAI(api_key=openai_api_key)

@app.route('/', methods=['GET'])
def index():
    return {'hello':'world'}

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


