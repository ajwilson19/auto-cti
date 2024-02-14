from chalice import Chalice
from openai import OpenAI
import json

app = Chalice(app_name='helloworld')

@app.route('/')
def index():
    return {'hello':'world'}

@app.route('/gpt', methods=['POST'])
def gpt():
    #ex: {"api_key":"key", "model":"gpt-3.5-turbo", "messages": [], "temperature":0}
    request = app.current_request
    try:
        json_data = request.json_body
        client = OpenAI(api_key=json_data['api_key'])
        response = client.chat.completions.create(
            model=json_data['model'],
            messages=json_data['messages'],
            temperature=json_data['temperature'],
        )
        return json.dumps(json.loads(response.model_dump_json()), indent=4)
    except Exception as e:
        return {'success': False, 'error': str(e)}


