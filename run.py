from flask import Flask, render_template, request, session, url_for, redirect, jsonify,g
from flask.views import MethodView
import sqlite3,pickle
import logging
import logging.handlers
from pythonjsonlogger import jsonlogger
from ddtrace import patch_all; patch_all(logging=True)
from ddtrace import tracer
 
app = Flask(__name__)

handler = logging.handlers.RotatingFileHandler(
        '/var/log/log.txt',
        maxBytes=1024 * 1024)
formatter = jsonlogger.JsonFormatter('%(asctime)s %(levelname)s [%(name)s] [%(filename)s:%(lineno)d] '
          '[dd.service=%(dd.service)s dd.env=%(dd.env)s dd.version=%(dd.version)s dd.trace_id=%(dd.trace_id)s dd.span_id=%(dd.span_id)s] '
          '- %(message)s')
handler.setFormatter(formatter)
logging.basicConfig(format=formatter)
log = logging.getLogger(__name__)
log.level = logging.INFO
logging.getLogger().addHandler(handler)


# get Database Object.
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect('db.db')
        return g.db
 
# close Database Object.
def close_db(e=None):
    db = g.pop('db', None)
 
    if db is not None:
        db.close()

@tracer.wrap() 
@app.route('/', methods=['GET'])
def index():
    log.info('Hello, World')
    mydata = []
    db = get_db()
    cur = db.execute("select * from mydata")
    mydata = cur.fetchall()
    return render_template('index.html',\
        title='Hello world!初めてのDatadog!', \
        message='※FlaskのDB連携サンプルアプリ',
        data=mydata)
 
if __name__ == '__main__':
    #app.debug=True
    app.run(host='0.0.0.0', port=8080)

