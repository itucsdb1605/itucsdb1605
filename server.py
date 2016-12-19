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
from companies import Companies
from locations import Locations
from articles import Articles
from myevents import Myevents
from myconnections import Myconnections
from func import Func
from topics import Topics
from job import Job
from users import users
from group import Group
from partners import Partners
from projects import Projects
from message import Message

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

isInitialized = False

@app.route('/')
def home_page():
    global isInitialized
    now = datetime.datetime.now()
    if isInitialized == False:
        initialize = INIT(app.config['dsn'])
        initialize.locations()
        initialize.companies()
        initialize.universities()
        initialize.universities_info()
        initialize.topics()
        initialize.messages()
        initialize.channels()
        initialize.partners()
        initialize.projects()
        initialize.articles()
        initialize.jobs()
        initialize.groups()
        initialize.users()
        isInitialized = True
    return page_login()

##Following 5 methods define select-add-delete-update operations
##on JOBS table
@app.route('/isilanlari')
def job_view():
    jobs = Job(app.config['dsn'])

    with dbapi2.connect(app.config['dsn']) as connection:
        with connection.cursor() as cursor:
            statement = """SELECT T1.ID , COMPANIES.TITLE,  T1.POSITION, T1.SALARY FROM (select * from jobs) AS T1
                    INNER JOIN COMPANIES
                    ON COMPANIES.ID=T1.COMPANYID"""
            cursor.execute(statement)
            job_list = cursor.fetchall()

    now = datetime.datetime.now()
    return render_template('jobs.html',jobs=job_list, current_time=now.ctime())

@app.route('/isilaniekle', methods=['GET', 'POST'])
def job_add():
    now = datetime.datetime.now()
    job = Job(app.config['dsn'])
    if request.method == 'GET':
        with dbapi2.connect(app.config['dsn']) as connection:
            with connection.cursor() as cursor:
                statement = """SELECT * FROM companies"""
                cursor.execute(statement)
                companies = cursor.fetchall()
        return render_template('job_add.html', companies = companies, current_time=now.ctime())

    if request.method == 'POST':
        with dbapi2.connect(app.config['dsn']) as connection:
            with connection.cursor() as cursor:
                statement = """INSERT INTO JOBS(CompanyId, Position, Salary)
                 VALUES ({}, '{}', {})""".format(request.form['companyId'][0], request.form['position'], request.form['salary'] )
                cursor.execute(statement)

        return redirect(url_for('job_view'))

@app.route('/isilanisil', methods=['GET','POST'])
def job_delete():
    job = Job(app.config['dsn'])
    jobs = ()
    if request.method == 'GET':
        jobs = job.get_jobs()
        now = datetime.datetime.now()
        return render_template('job_delete.html', jobs=jobs, current_time=now.ctime())
    if request.method == 'POST':
        ids = request.form.getlist('jobs_to_delete')
        job.delete_jobs(ids)
        jobs = job.get_jobs()
        now = datetime.datetime.now()
        return render_template('job_delete.html', jobs=jobs, current_time=now.ctime())

@app.route('/isilaniguncelle')
def job_update():
    job = Job(app.config['dsn'])
    with dbapi2.connect(app.config['dsn']) as connection:
        with connection.cursor() as cursor:
            statement = """SELECT T1.ID , T1.POSITION, T1.SALARY, COMPANIES.TITLE FROM (select * from jobs) AS T1
                    INNER JOIN COMPANIES
                    ON COMPANIES.ID=T1.COMPANYID"""
            cursor.execute(statement)
            jobs = cursor.fetchall()
    now = datetime.datetime.now()
    return render_template('job_update.html',jobs=jobs, current_time=now.ctime())

@app.route('/isilaniguncelle/<int:id>', methods=['GET','POST'])
def job_update_page(id):
    job = Job(app.config['dsn'])

    if request.method == 'GET':
        with dbapi2.connect(app.config['dsn']) as connection:
            with connection.cursor() as cursor:
                statement = """SELECT T1.ID ,COMPANIES.TITLE, T1.POSITION, T1.SALARY FROM (select * from jobs WHERE ID={}) AS T1
                    INNER JOIN COMPANIES
                    ON COMPANIES.ID=T1.COMPANYID""".format(id)
                cursor.execute(statement)
                job = cursor.fetchall()
        now = datetime.datetime.now()
        return render_template('job_edit.html',job = job, current_time=now.ctime())

    else:
        print(request.form['companyName'])
        with dbapi2.connect(app.config['dsn']) as connection:
            with connection.cursor() as cursor:
                statement = """SELECT id FROM companies where TITLE='{}'""".format(request.form['companyName'])
                cursor.execute(statement)
                companyId = cursor.fetchall()
        print(companyId)
        job.set_companyId(companyId[0][0])
        job.set_position(request.form['position'])
        job.set_salary(int(request.form['salary']))
        job.set_id(id)
        job.update_job()
        with dbapi2.connect(app.config['dsn']) as connection:
            with connection.cursor() as cursor:
                statement = """SELECT T1.ID , T1.POSITION, T1.SALARY, COMPANIES.TITLE FROM (select * from jobs) AS T1
                        INNER JOIN COMPANIES
                        ON COMPANIES.ID=T1.COMPANYID"""
                cursor.execute(statement)
                jobs = cursor.fetchall()
        now = datetime.datetime.now()
        return render_template('jobs.html',jobs=jobs, current_time=now.ctime())

@app.route('/mesajlar', methods=['GET','POST'])
def inbox_page():
    if request.method == 'GET':
        now = datetime.datetime.now()
        with dbapi2.connect(app.config['dsn']) as connection:
            with connection.cursor() as cursor:
                statement = """SELECT ID, USERS.firstname AS senderName, USERS.lastname AS senderSurname, TEXT
     FROM (SELECT * FROM MESSAGES WHERE RECEIVERID=3) AS T1
     INNER JOIN USERS
     ON T1.senderID=USERS.userid"""
                cursor.execute(statement)
                messages = cursor.fetchall()
        return render_template('messages.html', user_role="Gönderen",header = "Gelen Kutusu",messages = messages, current_time=now.ctime())

    else:
        ids = request.form.getlist('messages_to_delete')
        message = Message(app.config['dsn'])
        message.delete_messages(ids)
        now = datetime.datetime.now()
        with dbapi2.connect(app.config['dsn']) as connection:
            with connection.cursor() as cursor:
                statement = """SELECT ID, USERS.firstname AS senderName, USERS.lastname AS senderSurname, TEXT
     FROM (SELECT * FROM MESSAGES WHERE RECEIVERID=3) AS T1
     INNER JOIN USERS
     ON T1.senderID=USERS.userid"""
                cursor.execute(statement)
                messages = cursor.fetchall()
        return render_template('messages.html', user_role="Gönderen",header = "Gelen Kutusu",messages = messages, current_time=now.ctime())


@app.route('/gonderilenler', methods=['GET','POST'])
def sent_messages_page():
    if request.method == 'GET':
        now = datetime.datetime.now()
        with dbapi2.connect(app.config['dsn']) as connection:
            with connection.cursor() as cursor:
                statement = """SELECT ID, USERS.firstname AS senderName, USERS.lastname AS senderSurname, TEXT
                             FROM (SELECT * FROM MESSAGES WHERE SENDERID=3) AS T1
                             INNER JOIN USERS
                             ON T1.receiverID=USERS.userid"""
                cursor.execute(statement)
                messages = cursor.fetchall()
        return render_template('messages.html', user_role="Alıcı", header = "Gönderilen Mesajlar", messages = messages,current_time=now.ctime())
    else:
        ids = request.form.getlist('messages_to_delete')
        message = Message(app.config['dsn'])
        message.delete_messages(ids)
        now = datetime.datetime.now()
        with dbapi2.connect(app.config['dsn']) as connection:
            with connection.cursor() as cursor:
                statement = """SELECT ID, USERS.firstname AS senderName, USERS.lastname AS senderSurname, TEXT
                             FROM (SELECT * FROM MESSAGES WHERE SENDERID=3) AS T1
                             INNER JOIN USERS
                             ON T1.receiverID=USERS.userid"""
                cursor.execute(statement)
                messages = cursor.fetchall()
        return render_template('messages.html', user_role="Alıcı",header = "Gönderilen Mesajlar", messages = messages, current_time=now.ctime())
@app.route('/yenimesaj', methods=['GET','POST'])
def new_message():
    now = datetime.datetime.now()
    if request.method == 'GET':
        with dbapi2.connect(app.config['dsn']) as connection:
            with connection.cursor() as cursor:
                statement = """SELECT * FROM users"""
                cursor.execute(statement)
                users = cursor.fetchall()
        return render_template('new_message.html', users = users, current_time=now.ctime())
    else:
        receiverId = request.form['receiverId'][0]
        text = request.form['text']
        message = Message(app.config['dsn'],3, receiverId, text)
        message.send()
        return redirect(url_for('sent_messages_page'))


@app.route('/gruplar', methods=['GET','POST'])
def group_view():
    group = Group(app.config['dsn'])
    if request.method == 'GET':
        groups = Group(app.config['dsn'])
        group_list = groups.get_groups()
        now = datetime.datetime.now()
        return render_template('groups.html', groups = group_list, current_time=now.ctime())
    else:
        groupId = request.form['groupId']
        group.set_id(groupId)
        try:
            group.add_member(4,'member')
        except psycopg2.IntegrityError:
            print("duplicate error catched")
        finally:
            now = datetime.datetime.now()
            return redirect(url_for('group_view'))

@app.route('/grupsil', methods=['GET','POST'])
def group_delete():
    group = Group(app.config['dsn'])
    groups = ()
    if request.method == 'GET':
        groups = group.get_groups()
        now = datetime.datetime.now()
        return render_template('group_delete.html', groups=groups, current_time=now.ctime())
    if request.method == 'POST':
        ids = request.form.getlist('groups_to_delete')
        group.delete_groups(ids)
        groups = group.get_groups()
        now = datetime.datetime.now()
        return render_template('group_delete.html', groups=groups, current_time=now.ctime())

@app.route('/grupguncelle')
def group_update():
    group = Group(app.config['dsn'])
    groups = group.get_groups()
    now = datetime.datetime.now()
    return render_template('group_update.html',groups=groups, current_time=now.ctime())

@app.route('/grupguncelle/<int:id>', methods=['GET','POST'])
def group_update_page(id):
    group = Group(app.config['dsn'])
    if request.method == 'GET':
        group.set_id(id)
        group = group.get_groups()
        now = datetime.datetime.now()
        return render_template('group_edit.html',group = group, current_time=now.ctime())

    if request.method == 'POST':
        group.set_name(request.form['groupname'])
        group.set_description(request.form['groupDescription'])
        group.set_id(id)
        group.update_group()
        groups = group.get_groups()
        now = datetime.datetime.now()
        return render_template('groups.html',groups=groups, current_time=now.ctime())


@app.route('/gruplar/<int:id>', methods=['GET','POST'])
def group_members_page(id):
    group = Group(app.config['dsn'])
    groupName = group.find_group_name(id)
    members= group.get_members(id)
    print(members)
    now = datetime.datetime.now()
    return render_template('group_members_view.html',groupName = groupName, members = members, current_time=now.ctime())


@app.route('/grupolustur', methods=['GET', 'POST'])
def group_create():
    group = Group(app.config['dsn'])
    if request.method == 'GET':
        now = datetime.datetime.now()
        return render_template('group_add.html', current_time=now.ctime())
    if request.method == 'POST':
       group.set_name(request.form['groupName'])
       group.set_description(request.form['groupDescription'])
       group.create_group()
       return redirect(url_for('group_view'))

@app.route('/universiteler', methods=['GET', 'POST'])
def uni_page():
    unis = Universities(app.config['dsn'])
    fn = Func(app.config['dsn'])
    if request.method == 'GET':
        now = datetime.datetime.now()
        connection = dbapi2.connect(app.config['dsn'])
        cursor = connection.cursor()
        statement = """SELECT * FROM universities"""
        cursor.execute(statement)
        ulist = cursor.fetchall()
        statement = """SELECT uni_id, locations.city, locations.country, population, type FROM universities_info JOIN locations ON universities_info.local = locations.loc_id"""
        cursor.execute(statement)
        ilist = cursor.fetchall()
        connection.commit()
        return render_template('universities.html', UniversityList = ulist, InfoList=ilist, current_time = now.ctime())
    elif 'unis_to_delete' in request.form:
        ids = request.form.getlist('unis_to_delete')

        for id in ids:
            id = id.split('/', maxsplit=1)
            id = id[0]
            unis.delete_university(id)
        connection = dbapi2.connect(app.config['dsn'])
        cursor = connection.cursor()
        statement = """SELECT * FROM universities"""
        cursor.execute(statement)
        ulist = cursor.fetchall()
        statement = """SELECT uni_id, locations.city, locations.country, population, type FROM universities_info JOIN locations ON universities_info.local = locations.loc_id"""
        cursor.execute(statement)
        ilist = cursor.fetchall()
        connection.commit()
        now = datetime.datetime.now()
        return render_template('universities.html', UniversityList = ulist, InfoList=ilist, current_time = now.ctime())
        #return redirect(url_for('uni_page'))
    elif 'universities_to_add' in request.form:
        unis.add_university(request.form['title'],request.form['local'],request.form['population'],request.form['type'])
        return redirect(url_for('uni_page'))
    elif 'universities_to_update' in request.form:
        ids = int(request.form('universities_to_update'))
        return redirect(url_for('a_uni_page',id=ids))
    elif 'universities_to_select' in request.form:
        vals = request.form.getlist('unis_to_select')
        City=request.form['city']
        #l_id=fn.get_id("locations",City)
        length=len(vals)
        if length==2:
            connection = dbapi2.connect(app.config['dsn'])
            cursor = connection.cursor()
            statement = """SELECT loc_id FROM locations WHERE city='{}';""".format(City)
            cursor.execute(statement)
            row = cursor.fetchone()
            if row is None:
                 now = datetime.datetime.now()
                 return render_template('404.html', current_time = now.ctime())
            loca_id = row[0]
            statement = """SELECT universities.title, universities_info.population, universities_info.type FROM universities JOIN universities_info ON universities_info.uni_id = universities.id WHERE local ={}""".format(loca_id)
            cursor.execute(statement)
            ilist = cursor.fetchall()
            connection.commit()
            now = datetime.datetime.now()
            if ilist is None:
                return render_template('404.html', current_time = now.ctime())
            return render_template('b_university.html', UniversityList = ilist, current_time = now.ctime())
        elif length==1:
            connection = dbapi2.connect(app.config['dsn'])
            cursor = connection.cursor()
            statement = """SELECT loc_id FROM locations WHERE city='{}';""".format(City)
            cursor.execute(statement)
            row = cursor.fetchone()
            if row is None:
                 now = datetime.datetime.now()
                 return render_template('404.html', current_time = now.ctime())
            loca_id = row[0]
            statement = """SELECT universities.title, universities_info.population, universities_info.type FROM universities JOIN universities_info ON universities_info.uni_id = universities.id WHERE universities_info.local ={} AND universities_info.type='{}' """.format(loca_id,vals[0])
            cursor.execute(statement)
            ilist = cursor.fetchall()
            connection.commit()
            now = datetime.datetime.now()
            if ilist is None:
                return render_template('404.html', current_time = now.ctime())
            return render_template('b_university.html', UniversityList = ilist, current_time = now.ctime())




@app.route('/universiteler/<int:id>', methods=['GET','POST'])
def uni_update_page(id):
    unis = Universities(app.config['dsn'])
    fn = Func(app.config['dsn'])
    if request.method == 'GET':
        connection = dbapi2.connect(app.config['dsn'])
        cursor = connection.cursor()
        statement = """SELECT * FROM universities WHERE id={}""".format(id)
        cursor.execute(statement)
        univ = cursor.fetchall()
        statement = """SELECT uni_id, locations.city, locations.country, population, type FROM universities_info JOIN locations ON universities_info.local = locations.loc_id WHERE uni_id={}""".format(id)
        cursor.execute(statement)
        infos = cursor.fetchall()
        connection.close()
        now = datetime.datetime.now()
        return render_template('a_university.html',ID=id, UniversityList = univ, InfoList=infos, current_time=now.ctime())
    #elif 'universities_to_update' in request.form:
    if request.method == 'POST':
        #unis.update_a_university(id,request.form['uni'], request.form['city'],request.form['cont'],request.form['number'],request.form['type'])
        connection = dbapi2.connect(app.config['dsn'])
        cursor = connection.cursor()
        statement = """UPDATE universities
                    SET  title ='{}'
                    WHERE id={};""".format(request.form['uni'], id)
        cursor.execute(statement)
        statement ="""SELECT loc_id FROM locations WHERE city='{}';""".format(request.form['city'])
        cursor.execute(statement)
        row = cursor.fetchone()
        if row is None:
            return None
        loca_id = row[0]
        statement = """UPDATE universities_info
                    SET local='{}', population='{}', type='{}' WHERE uni_id = {};""".format(loca_id,request.form['number'],request.form['type'],id)
        cursor.execute(statement)
        statement = """SELECT * FROM universities"""
        cursor.execute(statement)
        ulist = cursor.fetchall()
        statement = """SELECT uni_id, locations.city, locations.country, population, type FROM universities_info JOIN locations ON universities_info.local = locations.loc_id"""
        cursor.execute(statement)
        ilist = cursor.fetchall()
        connection.commit()
        now = datetime.datetime.now()
        #return render_template('universities.html', UniversityList = ulist, InfoList=ilist, current_time=now.ctime())
        return redirect(url_for('uni_page'))


@app.route('/sirketler', methods=['GET', 'POST'])
def company_page():
    comps = Companies(app.config['dsn'])
    fn = Func(app.config['dsn'])
    if request.method == 'GET':
        now = datetime.datetime.now()
        connection = dbapi2.connect(app.config['dsn'])
        cursor = connection.cursor()
        statement = """SELECT id, title, locations.city, locations.country, population FROM companies JOIN locations ON companies.local2 = locations.loc_id"""
        cursor.execute(statement)
        clist = cursor.fetchall()
        connection.commit()
        return render_template('companies.html', CompanyList = clist, current_time = now.ctime())
    elif 'comps_to_delete' in request.form:
        ids = request.form.getlist('comps_to_delete')

        for id in ids:
            id = id.split('/', maxsplit=1)
            id = id[0]
            comps.delete_company(id)
        connection = dbapi2.connect(app.config['dsn'])
        cursor = connection.cursor()
        statement = """SELECT id, title, locations.city, locations.country, population FROM companies JOIN locations ON companies.local2 = locations.loc_id"""
        cursor.execute(statement)
        clist = cursor.fetchall()
        connection.commit()
        now = datetime.datetime.now()
        return render_template('companies.html', CompanyList = clist, current_time = now.ctime())
        #return redirect(url_for('uni_page'))
    elif 'companies_to_add' in request.form:
        comps.add_company(request.form['title'],request.form['local'],request.form['population'])
        return redirect(url_for('company_page'))
    elif 'companies_to_update' in request.form:
        ids = int(request.form('companies_to_update'))
        return redirect(url_for('a_company_page',id=ids))
    elif 'companies_to_select' in request.form:
        City=request.form['city']
        #l_id=fn.get_id("locations",City)
        connection = dbapi2.connect(app.config['dsn'])
        cursor = connection.cursor()
        statement = """SELECT loc_id FROM locations WHERE city='{}';""".format(City)
        cursor.execute(statement)
        row = cursor.fetchone()
        if row is None:
            now = datetime.datetime.now()
            return render_template('404.html', current_time = now.ctime())
        loca_id = row[0]
        statement = """SELECT id, title, locations.city, locations.country, population FROM companies JOIN locations ON companies.local2 = locations.loc_id WHERE local2 ={}""".format(loca_id)
        cursor.execute(statement)
        clist = cursor.fetchall()
        connection.commit()
        now = datetime.datetime.now()
        if clist is None:
            return render_template('404.html', current_time = now.ctime())
        return render_template('b_company.html', CompanyList = clist, current_time = now.ctime())
    elif 'companies_to_select2' in request.form:
        Title=request.form['title']
        #l_id=fn.get_id("locations",City)
        connection = dbapi2.connect(app.config['dsn'])
        cursor = connection.cursor()
        statement = """SELECT id, title, locations.city, locations.country, population FROM companies JOIN locations ON companies.local2 = locations.loc_id WHERE title ='{}'""".format(Title)
        cursor.execute(statement)
        clist = cursor.fetchall()
        connection.commit()
        now = datetime.datetime.now()
        if clist is None:
            return render_template('404.html', current_time = now.ctime())
        return render_template('b_company.html', CompanyList = clist, current_time = now.ctime())

@app.route('/sirketler/<int:id>', methods=['GET','POST'])
def comp_update_page(id):
    comps = Companies(app.config['dsn'])
    fn = Func(app.config['dsn'])
    if request.method == 'GET':
        connection = dbapi2.connect(app.config['dsn'])
        cursor = connection.cursor()
        statement = """SELECT id, title, locations.city, locations.country, population FROM companies JOIN locations ON companies.local2 = locations.loc_id WHERE id={}""".format(id)
        cursor.execute(statement)
        clist = cursor.fetchall()
        connection.close()
        now = datetime.datetime.now()
        return render_template('a_company.html',ID=id, CompanyList = clist, current_time=now.ctime())
    #elif 'universities_to_update' in request.form:
    if request.method == 'POST':
        #unis.update_a_university(id,request.form['uni'], request.form['city'],request.form['cont'],request.form['number'],request.form['type'])
        connection = dbapi2.connect(app.config['dsn'])
        cursor = connection.cursor()
        statement ="""SELECT loc_id FROM locations WHERE city='{}';""".format(request.form['city'])
        cursor.execute(statement)
        row = cursor.fetchone()
        if row is None:
            return None
        loca_id = row[0]
        statement = """UPDATE companies
                    SET title='{}', local2='{}', population='{}' WHERE id = {};""".format(request.form['comp'],loca_id,request.form['number'],id)
        cursor.execute(statement)
        statement = """SELECT id, title, locations.city, locations.country, population FROM companies JOIN locations ON companies.local2 = locations.loc_id"""
        cursor.execute(statement)
        clist = cursor.fetchall()
        connection.commit()
        now = datetime.datetime.now()
        #return render_template('universities.html', UniversityList = ulist, InfoList=ilist, current_time=now.ctime())
        return redirect(url_for('company_page'))

@app.route('/yerler', methods=['GET', 'POST'])
def location_page():
    locs = Locations(app.config['dsn'])
    fn = Func(app.config['dsn'])
    if request.method == 'GET':
        now = datetime.datetime.now()
        connection = dbapi2.connect(app.config['dsn'])
        cursor = connection.cursor()
        statement = """SELECT loc_id, city, country FROM locations"""
        cursor.execute(statement)
        llist = cursor.fetchall()
        connection.commit()
        return render_template('locations.html', LocationList = llist, current_time = now.ctime())
    elif 'locations_to_add' in request.form:
        locs.add_location(request.form['no'],request.form['city'],request.form['country'])
        return redirect(url_for('location_page'))


@app.route('/etkinlikler', methods=['GET', 'POST'])
def events_page():
    evts = Myevents(app.config['dsn'])
    fn = Func(app.config['dsn'])
    if request.method == 'GET':
        now = datetime.datetime.now()
        event = evts.get_eventlist()
        event[0]=list(article[0])
        event[0][0]="kayıt seçiniz"
        event[0][1]="kayıt seçiniz"
        event[0][2]="kayıt seçiniz"
        event[0][3]="kayıt seçiniz"
        event[0][4]="kayıt seçiniz"
        event[0][5]="kayıt seçiniz"
        event[0][6]="kayıt seçiniz"
        event[0]=tuple(event[0])
        eventlist = evts.get_eventlist()
        locationlist=evts.get_locationlist()
        userlist=evts.get_userlist()
        return render_template('events.html', EventList = eventlist, LocationList=locationlist, UserList=userlist, event = event, current_time = now.ctime())
    elif 'events_to_delete' in request.form:
        eventids = request.form.getlist('events_to_delete')
        for EventId in eventids:
            evts.delete_event(EventId)
        return redirect(url_for('events_page'))
    elif 'select_record' in request.form:
        eventids = request.form.getlist('select_record')
        now = datetime.datetime.now()
        eventlist = evts.get_eventlist()
        userlist=evts.get_userlist()
        locationlist=evts.get_locationlist()
        slist=evts.select_event(eventids[0])
        return render_template('events.html', EventList = eventlist, LocationList=locationlist, UserList=userlist, event=slist, current_time=now.ctime())
    elif 'events_to_add' in request.form:
        evts.add_event(request.form['EventName'],request.form['OwnerId'],request.form['CityId'],request.form['DateWithTime'],request.form['Detail'])
        return redirect(url_for('events_page'))
    elif 'events_to_update' in request.form:
        evts.update_event(request.form['EventId'],request.form['EventName'],request.form['OwnerId'],request.form['CityId'],request.form['DateWithTime'],request.form['Detail'])
        return redirect(url_for('events_page'))
@app.route('/projects')
def projects_page():
    now = datetime.datetime.now()
    return render_template('projects.html', current_time=now.ctime())

@app.route('/baglantilar', methods=['GET', 'POST'])
def connections_page():
    cons = Myconnections(app.config['dsn'])
    fn = Func(app.config['dsn'])
    if request.method == 'GET':
        now = datetime.datetime.now()
        connectionlist = cons.get_connectionlist()
        userlist=cons.get_userlist()
        universitylist=cons.get_universitylist()
        connectionlistbyuniversity=cons.get_universityconnectionlist()
        return render_template('connections.html', ConnectionList = connectionlist,
                                UserList=userlist, UniversityList=universitylist,
                                UniversityConnectionList=connectionlistbyuniversity, current_time = now.ctime())
    elif 'selectByUser' in request.form:
        temp=request.form.getlist('selectByUser')
        now = datetime.datetime.now()
        connectionlist = cons.get_connectionlistbyuser(temp[0])
        userlist=cons.get_userlist()
        universitylist=cons.get_universitylist()
        connectionlistbyuniversity=cons.get_universityconnectionlist()
        return render_template('connections.html', ConnectionList = connectionlist,
                                UserList=userlist, UniversityList=universitylist,
                                UniversityConnectionList=connectionlistbyuniversity, current_time = now.ctime())
    elif 'selectByUniversity' in request.form:
        temp=request.form.getlist('selectByUniversity')
        now = datetime.datetime.now()
        connectionlist = cons.get_connectionlist()
        userlist=cons.get_userlist()
        universitylist=cons.get_universitylist()
        connectionlistbyuniversity=cons.get_connectionlistbyuniversity(temp[0])
        return render_template('connections.html', ConnectionList = connectionlist,
                                UserList=userlist, UniversityList=universitylist,
                                UniversityConnectionList=connectionlistbyuniversity, current_time = now.ctime())
    elif 'Delete' in request.form:
        connectionids = request.form.getlist('DeletedConnections')
        for ConnectionId in connectionids:
            cons.delete_connection(ConnectionId)
        return redirect(url_for('connections_page'))
    elif 'Connect' in request.form:
        cons.add_connection(request.form['User'],request.form['Connection'])
        return redirect(url_for('connections_page'))

@app.route('/makaleler', methods=['GET', 'POST'])
def articles_page():
    arts = Articles(app.config['dsn'])
    fn = Func(app.config['dsn'])
    if request.method == 'GET':
        now = datetime.datetime.now()
        article = arts.get_articlelist()
        article[0]=list(article[0])
        article[0][0]="kayıt seçiniz"
        article[0][1]="kayıt seçiniz"
        article[0][2]="kayıt seçiniz"
        article[0][3]="kayıt seçiniz"
        article[0][4]="kayıt seçiniz"
        article[0][5]="kayıt seçiniz"
        article[0][6]="kayıt seçiniz"
        article[0][7]="kayıt seçiniz"
        article[0]=tuple(article[0])
        alist = arts.get_articlelist()
        unilist=arts.get_universitylist()
        userlist=arts.get_userlist()
        return render_template('articles.html', ArticleList = alist, UniversityList=unilist, UserList=userlist, article= article, current_time = now.ctime())
    elif 'articles_to_delete' in request.form:
        articleids = request.form.getlist('articles_to_delete')
        for ArticleId in articleids:
            arts.delete_article(ArticleId)
        return redirect(url_for('articles_page'))
    elif 'select_record' in request.form:
        articleids = request.form.getlist('select_record')
        now = datetime.datetime.now()
        alist = arts.get_articlelist()
        unilist=arts.get_universitylist()
        userlist=arts.get_userlist()
        slist=arts.select_article(articleids[0])
        return render_template('articles.html', ArticleList = alist, UniversityList=unilist, UserList=userlist, article=slist, current_time=now.ctime())
    elif 'articles_to_add' in request.form:
        arts.add_article(request.form['ArticleName'],request.form['UserId'],request.form['ReleaseYear'],request.form['Mail'],request.form['uni_id'])
        return redirect(url_for('articles_page'))
    elif 'articles_to_update' in request.form:
        arts.update_article(request.form['ArticleId'], request.form['ArticleName'],request.form['UserId'],request.form['ReleaseYear'],request.form['Mail'],request.form['uni_id'])
        return redirect(url_for('articles_page'))
@app.route('/kanallar')
def kanal_page():
    now = datetime.datetime.now()
    return render_template('kanallar.html', current_time=now.ctime())

@app.route('/partners', methods=['GET', 'POST'])
def partners_page():
    prtnrs = Partners(app.config['dsn'])
    fn = Func(app.config['dsn'])
    if request.method == 'GET':
        now = datetime.datetime.now()
        plist = prtnrs.get_partnerlist()
        return render_template('partners.html', PartnerList = plist, current_time = now.ctime())
    elif 'partners_to_delete' in request.form:
        partnerids = request.form.getlist('partners_to_delete')
        for PartnerId in partnerids:
            prtnrs.delete_partner(PartnerId)
        return redirect(url_for('partners_page'))
    elif 'partners_to_add' in request.form:
        prtnrs.add_partner(request.form['PartnerName'],request.form['FoundationYear'],request.form['Country'])
        return redirect(url_for('partners_page'))
    elif 'partners_to_update' in request.form:
        prtnrs.update_partner(request.form['PartnerId'], request.form['PartnerName'],request.form['FoundationYear'],request.form['Country'])
        return redirect(url_for('partners_page'))

    
@app.route('/projects', methods=['GET', 'POST'])
def projects_page():
    prjcts = Projects(app.config['dsn'])
    fn = Func(app.config['dsn'])
    if request.method == 'GET':
        now = datetime.datetime.now()
        prlist = prjcts.get_projectlist()
        return render_template('projects.html', ProjectList = prlist, current_time = now.ctime())
    elif 'projects_to_delete' in request.form:
        projectids = request.form.getlist('projects_to_delete')
        for ProjectId in projectids:
            prjcts.delete_project(ProjectId)
        return redirect(url_for('projects_page'))
    elif 'projects_to_add' in request.form:
        prjcts.add_project(request.form['ProjectName'],request.form['ProjectYear'],request.form['ProjectPartner'])
        return redirect(url_for('projects_page'))
    elif 'projects_to_update' in request.form:
        prjcts.update_project(request.form['ProjectId'], request.form['ProjectName'],request.form['ProjectYear'],request.form['ProjectPartner'])
        return redirect(url_for('projects_page'))
    
@app.route('/konular')
def topics_page():
	tops = topics(app.config['dsn'])
    fn = Func(app.config['dsn'])
    if request.method == 'GET':
        now = datetime.datetime.now()
        tlist = tops.get_topiclist()
    return render_template('topics.html', topics = tlist, current_time = now.ctime())
    elif 'delete_selected' in request.form:
        topicids = request.form.getlist('delete_selected')
    for topicID in topicids:
        tops.delete_topic(topicID)
    return redirect(url_for('topics_page'))
    elif 'add' in request.form:
        tops.add_topic(request.form['topic'],request.form['description'])
    return redirect(url_for('topics_page'))
    elif 'update' in request.form:
        tops.update_topic(request.form['topicID'], request.form['topic'],request.form['description'])
    return redirect(url_for('topics_page'))
    
@app.route('/user_view')
def user_view():
    user = users(app.config['dsn'])
    user_list = user.get_user()
    now = datetime.datetime.now()
    return render_template('profile.html', users=user_list, current_time=now.ctime())

@app.route('/user_add', methods=['GET', 'POST'])
def user_add():
    user = users(app.config['dsn'])
    if request.method == 'GET':
        now = datetime.datetime.now()
        return render_template('signup.html', current_time=now.ctime())
    if request.method == 'POST':
        user.set_mail(request.form['email'])
        user.set_name(request.form['firstname'])
        user.set_lastname(request.form['lastname'])
        user.set_uni(request.form['uni'])
        user.set_password(request.form['password'])
        user.add_user()
        now = datetime.datetime.now()
        return redirect(url_for('page_login'))

@app.route('/user_update', methods=['GET', 'POST'])
def user_update():
    user = users(app.config['dsn'])
    if request.method == 'GET':
        now = datetime.datetime.now()
        return render_template('signup.html', current_time=now.ctime())
    if request.method == 'POST':
        name = request.form['firstname']
        mail = request.form['email']
        uni = request.form['uni']
        connection = dbapi2.connect(app.config['dsn'])
        cursor = connection.cursor()
        statement = """UPDATE users
                    SET  Firstname='%s',uni='%s'
                    WHERE Email_adress='%s'""" % (name, uni, mail)
        cursor.execute(statement)
        connection.commit()
        now = datetime.datetime.now()
        return redirect(url_for('page_profile'))

@app.route('/profil', methods = ['POST', 'GET'])

def page_profile():
    user = users(app.config['dsn'])
    userlist=user.get_user()
    now = datetime.datetime.now()
    return render_template('profile.html', users=userlist, current_time=now.ctime())

@app.route('/home', methods = ['POST', 'GET'])
def page_login():
    with dbapi2.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()
        if request.method == 'POST':
            mailentered = request.form['mail']
            passentered = request.form['password']
            query = """SELECT Firstname,Lastname,Email_adress FROM users WHERE Email_adress='%s' AND password='%s' """ % (mailentered, passentered)
            cursor.execute(query)
            global allusers
            allusers = cursor.fetchall()
            x = len(allusers)
            if x == 1:

                return render_template('home.html')
            else:
                return render_template('signup.html')
        elif request.method == 'GET':
            return render_template('signup.html')
@app.route('/initdb')
def init_db():
    initialize = INIT(app.config['dsn'])
    #initialize.All()
    initialize.locations()
    initialize.companies()
    initialize.universities()
    initialize.universities_info()
    initialize.topics()
    initialize.messages()
    initialize.channels()
    initialize.partners()
    initialize.projects()
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
