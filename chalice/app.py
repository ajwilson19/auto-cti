from chalice import Chalice
import os
from pymongo import MongoClient
import web.Engine as Engine

app = Chalice(app_name='auto-cti')

mongo_uri = os.environ.get('MONGO')
mongo = MongoClient(mongo_uri)
db = mongo['test']

@app.route('/', methods=['GET'])
def index():
    count = db['api'].find_one()['count']
    return {'count':count}


@app.schedule('rate(1 hour)')
def gather(event):
    Engine.run()


