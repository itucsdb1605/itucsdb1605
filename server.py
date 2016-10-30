import datetime
import json
import os
import psycopg2 as dbapi2
import re

from flask import Flask
from flask import redirect
from flask import render_template
from flask.helpers import url_for
from flask import request
from init import INIT

app = Flask(__name__)

def get_elephantsql_dsn(vcap_services):
    """Returns the data source name for ElephantSQL."""
    parsed = json.loads(vcap_services)
    uri = parsed["elephantsql"][0]["credentials"]["uri"]
    match = re.match('postgres://(.*?):(.*?)@(.*?)(:(\d+))?/(.*)', uri)
    user, password, host, _, port, dbname = match.groups()
    dsn = """user='{}' password='{}' host='{}' port={}
             dbname='{}'""".format(user, password, host, port, dbname)
    return dsn


@app.route('/')
def home_page():
    now = datetime.datetime.now()
    return render_template('home.html', current_time=now.ctime())

@app.route('/isilanlari')
def jobs_page():
    now = datetime.datetime.now()
    return render_template('jobs.html', current_time=now.ctime())

@app.route('/baglantilar')
def connections_page():
    now = datetime.datetime.now()
    return render_template('connections.html', current_time=now.ctime())
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
def topics_page():
    now = datetime.datetime.now()
    return render_template('topics.html', current_time=now.ctime())

@app.route('/initdb')
def init_db():
    initialize = INIT(app.config['dsn'])
    #initialize.All()
    initialize.universities()
    initialize.universities_info()
    initialize.topics()
    initialize.messages()
    initialize.channels()
    initialize.articles()
    return redirect(url_for('home_page'))

if __name__ == '__main__':
    VCAP_APP_PORT = os.getenv('VCAP_APP_PORT')
    if VCAP_APP_PORT is not None:
        port, debug = int(VCAP_APP_PORT), False
    else:
        port, debug = 5000, True

    VCAP_SERVICES = os.getenv('VCAP_SERVICES')
    if VCAP_SERVICES is not None:
        app.config['dsn'] = get_elephantsql_dsn(VCAP_SERVICES)
    else:
        app.config['dsn'] = """user='vagrant' password='vagrant' host='localhost' port=5432 dbname='itucsdb'"""
    app.run(host='0.0.0.0', port=port, debug=debug)
