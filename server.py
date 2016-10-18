import datetime
import os

from flask import Flask
from flask import render_template


app = Flask(__name__)


@app.route('/')
def home_page():
    now = datetime.datetime.now()
    return render_template('home.html', current_time=now.ctime())

@app.route('/isilanlari')
def jobs_page():
    now = datetime.datetime.now()
    return render_template('jobs.html', current_time=now.ctime())

@app.route('/mesajlar')
def messages_page():
    now = datetime.datetime.now()
    return render_template('messages.html', current_time=now.ctime())

@app.route('/gruplar')
def groups_page():
    now = datetime.datetime.now()
    return render_template('groups.html', current_time=now.ctime())

@app.route('/universiteler')
def uni_page():
    now = datetime.datetime.now()
    return render_template('universities.html', current_time=now.ctime())

@app.route('/sirketler')
def company_page():
    now = datetime.datetime.now()
    return render_template('companies.html', current_time=now.ctime())

@app.route('/etkinlikler')
def activities_page():
    now = datetime.datetime.now()
    return render_template('activities.html', current_time=now.ctime())

@app.route('/makaleler')
def articles_page():
    now = datetime.datetime.now()
    return render_template('articles.html', current_time=now.ctime())
@app.route('/kanallar')
def kanal_page():
    now = datetime.datetime.now()
    return render_template('kanallar.html', current_time=now.ctime())

@app.route('/partners')
def partners_page():
    now = datetime.datetime.now()
    return render_template('partners.html', current_time=now.ctime())

@app.route('/konular')
def kanal_page():
    now = datetime.datetime.now()
    return render_template('topics.html', current_time=now.ctime())

if __name__ == '__main__':
    VCAP_APP_PORT = os.getenv('VCAP_APP_PORT')
    if VCAP_APP_PORT is not None:
        port, debug = int(VCAP_APP_PORT), False
    else:
        port, debug = 5000, True
    app.run(host='0.0.0.0', port=port, debug=debug)
