from flask import Flask, render_template, request, session, url_for, redirect, jsonify,g
from flask.views import MethodView
import sqlite3,pickle
 
app = Flask(__name__)
 

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
 
@app.route('/', methods=['GET'])
def index():
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
