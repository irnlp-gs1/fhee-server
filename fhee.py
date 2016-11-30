from flask import Flask
from flask import request
app = Flask(__name__)

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
    """
    # get pagination params
    page = request.args.get('page', 1)
    limit = request.args.get('limit', 20)

    # do DB query
    return '{}_{}'.format(page, limit)

# /events/uid
@app.route('/events/<int:uid>')
def event(uid):
    """Return a single event

    Args:
        uid (int): an event unique id

    Returns:
        event (:obj:`event`): an event object

            {
                "uid": "",
                "datetime": "",
                "media": "",
                "text": {
                    "title": "",
                    "processed": ""
                },
                "keywords": {
                    "food": "",
                    "ing": "",
                    "bio": "",
                    "chem": "",
                    "germ": "",
                    "city": "",
                    "county": ""
                }
            }
    """
    # do DB query
    return '{}'.format(uid)
    
if __name__ == "__main__":
    app.run(host='0.0.0.0')
