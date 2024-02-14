from chalice import Chalice

app = Chalice(app_name='helloworld')

@app.route('/')
def index():
    return {'hello':'world'}

@app.route('/api', methods=['POST'])
def api():
    request = app.current_request
    try:
        json_data = request.json_body
        json_data['age'] = json_data['age']+1
        return json_data
    except Exception as e:
        return {'success': False, 'error': str(e)}

@app.route('/{number}')
def integer(number):
    try:
        return {'result': int(number)+1}
    except ValueError:
        return {'error': 'invalid input'}
