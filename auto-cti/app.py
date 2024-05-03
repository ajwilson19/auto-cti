from chalice import Chalice
import os
from pymongo import MongoClient
from chalicelib import Engine
from chalicelib import links
import json
import bcrypt

app = Chalice(app_name='auto-cti')

mongo_uri = os.environ.get('MONGO')
mongo = MongoClient(mongo_uri)
db = mongo['test']


@app.route('/', methods=['GET'])
def index():
    count = db['api'].find_one()['count']
    return {'count':count}

@app.route('/createuser', methods=['POST'])
def createuser():
    request = app.current_request.json_body
    try:
        auth = db['auth']
        
        if auth.find_one({"user": request['username']}):
            return {'success': False, 'error': "Username already exists"}
        
        hashed = bcrypt.hashpw(request['password'].encode('utf-8'), bcrypt.gensalt())
        if auth.insert_one({"user": request['username'], "pass": hashed}):
            return {'success': True, "user": request['username']}
    
    except Exception as e:
        return {"success": False, "error": e}

@app.route('/login', methods=['POST'])
def login():
    request = app.current_request.json_body
    try:
        auth = db['auth']
        id = auth.find_one({"user": request['username']})
        if bcrypt.checkpw(request['password'].encode('utf-8'), id["pass"]):
            return {'success': True, 'user': request['username']}
        else:
            return {'success': False, 'error': "Login failed"}
    except Exception as e:
        return {"success": False, "error": e}
    
@app.route('/userconfig', methods=['POST'])
def userconfig():
    request = app.current_request.json_body
    try:
        if type(request['username']) == str and type(request['title']) == str and type(request['tags']) == list:
            config = db['config']
            config.update_one({'user': request['username']}, {'$set': {"title": request['title'], 'tags': request['tags']}}, upsert=True)
            return {'success': True}
        else:
            return {'success': False, 'error': "Invalid request"}
    except Exception as e:
        return {"success": False, "error": e}
    
@app.route('/profiles', methods=['POST'])
def profiles():
    request = app.current_request.json_body
    try:
        config = db['config']
        user_config = config.find({"user": request['username']})
        titles = [c["title"] for c in user_config]
        return {'success': True, 'titles': titles}
    except Exception as e:
        return {"success": False, "error": e}
    
@app.route('/tags', methods=['POST'])
def tags():
    request = app.current_request.json_body
    try:
        config = db['config']
        tags = config.find_one({"user": request['username'], "title": request["title"]})['config']
        return {'success': True, 'titles': tags}
    except Exception as e:
        return {"success": False, "error": e}
    
@app.route('/feed', methods=['GET', 'POST'])
def feed():
    try:
        request = app.current_request
        if request.method == 'POST':
            query = {"tags": { "$in": request.json_body['tags'] }}
        else:
            query = {}

        alerts = list(db['cti-blob'].find(query, {'_id': 0}))

        return {'success': True, 'results': alerts}
    except Exception as e:
        return {"success": False, "error": e} 
    
@app.route('/stats', methods=['GET'])
def stats():
    try:
        cti = db['cti-blob']
        api = db['api']

        count = cti.count_documents({})
        activity = api.find_one({"activity": "list"})['count']
        last12 = sum(activity)
        last1 = activity[-1]

        return {'success': True, 'count': count, 'last12': last12, 'last1': last1}
    except Exception as e:
        return {"success": False, "error": e} 
        

@app.schedule('cron(0 * * * ? *)')
def gather(event):
    Engine.run()