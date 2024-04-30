from chalice import Chalice
import os
from pymongo import MongoClient
from chalicelib import Engine
from chalicelib import links
import json

app = Chalice(app_name='auto-cti')

mongo_uri = os.environ.get('MONGO')
mongo = MongoClient(mongo_uri)
db = mongo['test']

@app.route('/', methods=['GET'])
def index():
    count = db['api'].find_one()['count']
    return {'count':count}

@app.schedule('cron(0 * * * ? *)')
def gather(event):
    Engine.run()

