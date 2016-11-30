from flask import Flask
from flask import request
from flask import jsonify
from pyArango.connection import Connection
app = Flask(__name__)

DB = 'gs1'
COLLECTION = 'fhee'

def _get_db():
    """Return DB & collection
    
    Returns:
        (db, collection)
    """
    conn = Connection(arangoURL='http://arango.kyoungrok.com',
                      username='root',
                      password='ir7753nlp!')

    if not conn.hasDatabase(DB):
        db = conn.createDatabase(DB)
    else:
        db = conn[DB]

    if not db.hasCollection(COLLECTION):
        collection = db.createCollection(name=COLLECTION)
    else:
        collection = db.collections[COLLECTION]

    return db, collection

db, collection = _get_db()

# /
@app.route('/')
def index():
    """Dummy index page"""
    return 'Index Page'

# /events
@app.route('/events')
def events():
    """Returns a list of events.

    Returns:
        events (:obj:`list`): a list of events

        {
            'page': 1,
            'limit': 20,
            'events': [...],
            'count': 20
        }
    """
    # get pagination params
    try:
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 20))
    except ValueError:
        return None

    # do DB query    
    docs = []
    for d in collection.fetchAll(limit=limit, skip=(page-1)*limit):
        docs.append(d._store)

    # result
    res = {}
    res['page'] = page
    res['limit'] = limit
    res['events'] = docs
    res['count'] = len(docs)
    return jsonify(res)

# /events/uid
@app.route('/events/<int:uid>')
def event(uid):
    """Return a single event

    Args:
        uid (int): an event unique id

    Returns:
        event (:obj:`Event`): an event object

            {
                "uid": "",
                "datetime": "",
                "media": "",
                "text": {
                    "title": "",
                    "processed": ""
                },
                "keywords": {
                    "food": [],
                    "ing": [],
                    "bio": [],
                    "chem": [],
                    "germ": [],
                    "city": [],
                    "county": []
                }
            }
    """
    # do DB query
    doc = collection.fetchFirstExample(exampleDict={'uid': int(uid)})[0]._store
    return jsonify(doc)

if __name__ == "__main__":
    app.run(host='0.0.0.0')
