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
from universities import Universities
from articles import Articles
from func import Func

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
    initialize = INIT(app.config['dsn'])
    initialize.universities()
    initialize.universities_info()
    initialize.topics()
    initialize.messages()
    initialize.channels()
    initialize.partners()
    initialize.articles()
    initialize.jobs()
    return render_template('home.html', current_time=now.ctime())

##Following 5 methods define select-add-delete-update operations
##on JOBS table

@app.route('/isilanlari')
def job_view():
    jobs = ()
    connection = dbapi2.connect(app.config['dsn'])
    cursor = connection.cursor()       
    statement = """SELECT * FROM JOBS"""
    cursor.execute(statement)    
    jobs = cursor.fetchall()
    connection.commit()
    connection.close()
    now = datetime.datetime.now()
    return render_template('jobs.html',jobs=jobs, current_time=now.ctime())

@app.route('/isilaniekle', methods=['GET', 'POST'])
def job_add():
    if request.method == 'GET':
        now = datetime.datetime.now()
        return render_template('job_add.html', current_time=now.ctime())
    if request.method == 'POST':
        company = request.form['company']
        position = request.form['position']
        salary = int(request.form['salary'])
        connection = dbapi2.connect(app.config['dsn'])
        cursor = connection.cursor()       
        statement = """INSERT INTO JOBS(CompanyName, Position, Salary) VALUES
                        ( '{}', '{}', '{}' );
                    """.format(company, position, salary)
        cursor.execute(statement) 
        connection.commit()
        connection.close()  
        return redirect(url_for('job_view'))
 
@app.route('/isilanisil', methods=['GET','POST'])
def job_delete():
    if request.method == 'GET':
        jobs = ()
        connection = dbapi2.connect(app.config['dsn'])
        cursor = connection.cursor()       
        statement = """SELECT * FROM JOBS"""
        cursor.execute(statement)    
        jobs = cursor.fetchall()
        connection.commit()
        connection.close()
        now = datetime.datetime.now()
        return render_template('job_delete.html', jobs=jobs, current_time=now.ctime())
    if request.method == 'POST':
        ids = request.form.getlist('jobs_to_delete')
        connection = dbapi2.connect(app.config['dsn'])
        cursor = connection.cursor()       
        statement = """DELETE FROM JOBS WHERE ID = {};"""
        for id in ids:
            id = id.split('/', maxsplit=1)
            id = id[0]
            cursor.execute(statement.format(id))
            connection.commit()
        statement = """SELECT * FROM JOBS"""
        cursor.execute(statement)    
        jobs = cursor.fetchall()    
        connection.commit()
        connection.close()
        now = datetime.datetime.now()
        return render_template('job_delete.html', jobs=jobs, current_time=now.ctime())

@app.route('/isilaniguncelle')
def job_update():
    jobs = ()
    connection = dbapi2.connect(app.config['dsn'])
    cursor = connection.cursor()       
    statement = """SELECT * FROM JOBS"""
    cursor.execute(statement)    
    jobs = cursor.fetchall()
    connection.commit()
    connection.close()
    now = datetime.datetime.now()
    return render_template('job_update.html',jobs=jobs, current_time=now.ctime())

@app.route('/isilaniguncelle/<int:id>', methods=['GET','POST'])
def job_update_page(id):
    if request.method == 'GET':
        connection = dbapi2.connect(app.config['dsn'])
        cursor = connection.cursor()       
        statement = """SELECT * FROM JOBS WHERE ID={}""".format(id)
        cursor.execute(statement)    
        job = cursor.fetchall()
        connection.close()
        now = datetime.datetime.now()
        return render_template('job_edit.html',job=job, current_time=now.ctime())
    
    if request.method == 'POST':
        connection = dbapi2.connect(app.config['dsn'])
        company = request.form['company']
        position = request.form['position']
        salary = int(request.form['salary'])
        cursor = connection.cursor()       
        statement = """UPDATE JOBS
                    SET  CompanyName='{}', Position='{}' ,Salary={}     
                    WHERE ID={};""".format(company, position, salary, id)
        cursor.execute(statement)    
        connection.commit()
        statement = """SELECT * FROM JOBS"""
        cursor.execute(statement)    
        jobs = cursor.fetchall()
        connection.close()
        now = datetime.datetime.now()
        return render_template('jobs.html',jobs=jobs, current_time=now.ctime())

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

@app.route('/universiteler', methods=['GET', 'POST'])
def uni_page():
    unis = Universities(app.config['dsn'])
    fn = Func(app.config['dsn'])
    if request.method == 'GET':
        now = datetime.datetime.now()
        ulist = unis.get_universitylist()
        return render_template('universities.html', UniversityList = ulist, current_time = now.ctime())
    elif 'universities_to_delete' in request.form:
        unis.delete_university(request.form['id'])
        return redirect(url_for('uni_page'))
    elif 'universities_to_add' in request.form:
        unis.add_university(request.form['title'],request.form['local'],request.form['population'],request.form['type'])
        return redirect(url_for('uni_page'))
    elif 'universities_to_update' in request.form:
        unis.update_a_university(request.form['id'], request.form['title'],request.form['local'],request.form['population'],request.form['type'])
        return redirect(url_for('uni_page'))
    elif 'universities_to_select' in request.form:
        Uni_Index=request.form['id']
        return redirect(url_for('a_uni_page',uni_index=Uni_Index))

@app.route('/universiteler/<uni_index>', methods=['GET', 'POST'])
def a_uni_page(uni_index):
    now = datetime.datetime.now()
    fn = Func(app.config['dsn'])
    uni = Universities(app.config['dsn'])
    univ = uni.get_a_university(uni_index)
    if univ is None:
        return render_template('404.html', current_time = now.ctime())
    return render_template('a_university.html', University = univ, current_time = now.ctime())

@app.route('/sirketler')
def company_page():
    now = datetime.datetime.now()
    return render_template('companies.html', current_time=now.ctime())

@app.route('/etkinlikler')
def activities_page():
    now = datetime.datetime.now()
    return render_template('activities.html', current_time=now.ctime())

@app.route('/makaleler', methods=['GET', 'POST'])
def articles_page():
    arts = Articles(app.config['dsn'])
    fn = Func(app.config['dsn'])
    if request.method == 'GET':
        now = datetime.datetime.now()
        alist = arts.get_articlelist()
        return render_template('articles.html', ArticleList = alist, current_time = now.ctime())
    elif 'articles_to_delete' in request.form:
        articleids = request.form.getlist('articles_to_delete')
        for ArticleId in articleids:
            arts.delete_article(ArticleId)
        return redirect(url_for('articles_page'))
    elif 'articles_to_add' in request.form:
        arts.add_article(request.form['ArticleName'],request.form['UserId'],request.form['Name'],request.form['SurName'],request.form['ReleaseYear'],request.form['Mail'])
        return redirect(url_for('articles_page'))
    elif 'articles_to_update' in request.form:
        arts.update_article(request.form['ArticleId'], request.form['ArticleName'],request.form['UserId'],request.form['Name'],request.form['SurName'],request.form['ReleaseYear'],request.form['Mail'])
        return redirect(url_for('articles_page'))
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
    initialize.partners()
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
