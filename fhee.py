import arrow
import logging
from arrow.parser import ParserError
from flask import Flask
from flask import request
from flask import jsonify
from pyArango.connection import Connection
app = Flask(__name__)

DB = 'gs1'
COLLECTION = 'fhee'

logger = logging.getLogger(__name__)

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
            'after': '[datetime in ISO8601 format]'
            'events': [...],
            'count': 20
        }
    """
    # reset params
    page = None
    limit = None
    after, after_filter = None, None

    # get pagination params
    try:
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 20))
        after = request.args.get('after', None) 
    except ValueError:
        return None

    # validate datetime
    try:
        arrow.get(after).isoformat()
    except ParserError:
        return '"after" parameter must be in ISO format (e.g. 2016-12-09T06:12:08.000Z). Given: {}'.format(after), 400

    # do DB query
    docs = []
    after_filter = "FILTER d.analyzed_at > '{}'".format(after) if after else ''
    aql = "FOR d IN fhee SORT DATE_TIMESTAMP(d.analyzed_at) DESC LIMIT {offset}, {count} {after} RETURN d".format(count=limit, offset=(page-1)*limit, after=after_filter)
    result = db.AQLQuery(aql)
    for d in result:
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
        event (:obj:`dict`): an event object

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
    try:
        doc = collection.fetchFirstExample(exampleDict={'uid': int(uid)})[0]._store
        code = 200
    except IndexError:
        doc = {}
        code = 404

    return jsonify(doc), code

if __name__ == "__main__":
    app.run(host='0.0.0.0')
