import psycopg2 as dbapi2

class Myevents:
    def __init__(self, cp):
        self.cp = cp
        return

    def get_eventlist(self):
        with dbapi2.connect(self.cp) as connection:
            cursor = connection.cursor()
            query = """SELECT myevents.EventId, myevents.EventName, users.FirstName, users.LastName,
            locations.city, myevents.Date, myevents.Time, myevents.Detail
            FROM myevents
            LEFT JOIN users ON myevents.OwnerId = users.UserId 
            LEFT JOIN locations ON myevents.CityId = locations.loc_id """
            cursor.execute(query)
            rows = cursor.fetchall()
            return rows
        
    def get_locationlist(self):
        with dbapi2.connect(self.cp) as connection:
            cursor = connection.cursor()
            query = "SELECT * FROM locations ORDER BY title ASC"
            cursor.execute(query)
            rows = cursor.fetchall()
            return rows
    def get_userlist(self):
        with dbapi2.connect(self.cp) as connection:
            cursor = connection.cursor()
            query = "SELECT * FROM users ORDER BY FirstName ASC"
            cursor.execute(query)
            rows = cursor.fetchall()
            return rows
    def delete_event(self, EventId):
        with dbapi2.connect(self.cp) as connection:
            cursor = connection.cursor()
            query = "DELETE FROM myevents WHERE EventId = '%s'" % (EventId)
            cursor.execute(query)
            connection.commit()
            return
    def select_event(self, EventId):
        with dbapi2.connect(self.cp) as connection:
            cursor = connection.cursor()
            query = """SELECT EventId, EventName, OwnerId, CityId,
             Date, Time, Detail FROM myevents WHERE EventId = '%s' ORDER BY EventId ASC
             """ % (EventId)
            cursor.execute(query)
            rows=cursor.fetchall()
            return rows
    def add_event(self, EventName, OwnerId, CityId, Date, Time, Detail):
        with dbapi2.connect(self.cp) as connection:
            cursor = connection.cursor()
            query =  "INSERT INTO myevents (EventName, OwnerId, CityId, Date, Time, Detail) VALUES ('%s','%s','%s','%s','%s','%s')" % (EventName, OwnerId, CityId, Date, Time, Detail)
            cursor.execute(query)
            connection.commit()
            return

    def update_event(self, EventId, EventName, OwnerId, CityId, Date, Time, Detail):
        with dbapi2.connect(self.cp) as connection:
            cursor = connection.cursor()
            query =  "UPDATE myevents SET EventName = '%s', OwnerId='%s', CityId='%s', Date = '%s', Time='%s', Detail='%s'WHERE EventId='%s'" % (EventName, OwnerId, CityId, Date, Time, Detail,EventId)
            cursor.execute(query)
            connection.commit()
            return
