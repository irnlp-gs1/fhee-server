from flask import Flask
from flask import request
app = Flask(__name__)

# /
@app.route('/')
def index():
    return 'Index Page'

# /events
@app.route('/events')
def events():
    # get pagination params
    page = request.args.get('page', 1)
    limit = request.args.get('limit', 20)

    # do DB query
    return '{}_{}'.format(page, limit)

# /events/uid
@app.route('/events/<int:uid>')
def event(uid):
    # do DB query
    return '{}'.format(uid)
    