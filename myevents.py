import psycopg2 as dbapi2

class Myevents:
    def __init__(self, cp):
        self.cp = cp
        return

    def get_eventlist(self):
        with dbapi2.connect(self.cp) as connection:
            cursor = connection.cursor()
            query = """SELECT events.EventId, events.EventName, users.FirstName, users.LastName,
            locations.city, events.DateTime, events.Detail
            FROM events
            LEFT JOIN users ON events.OwnerId = users.UserId 
            LEFT JOIN locations ON events.CityId = locations.loc_id """
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
            query = "SELECT UserId, concat(FirstName::text, LastName::text) AS name FROM users ORDER BY FirstName ASC"
            cursor.execute(query)
            rows = cursor.fetchall()
            return rows
    def delete_event(self, EventId):
        with dbapi2.connect(self.cp) as connection:
            cursor = connection.cursor()
            query = "DELETE FROM events WHERE EventId = '%s'" % (EventId)
            cursor.execute(query)
            connection.commit()
            return
    def select_event(self, EventId):
        with dbapi2.connect(self.cp) as connection:
            cursor = connection.cursor()
            query = """SELECT EventId, EventName, OwnerId, CityId,
             DateTime, Detail FROM events WHERE EventId = '%s' ORDER BY EventId ASC
             """ % (EventId)
            cursor.execute(query)
            rows=cursor.fetchall()
            return rows
    def add_event(self, EventName, OwnerId, CityId, DateTime, Detail):
        with dbapi2.connect(self.cp) as connection:
            cursor = connection.cursor()
            query =  "INSERT INTO events (EventName, OwnerId, CityId, DateTime, Detail) VALUES ('%s','%s','%s','%s','%s')" % (EventName, OwnerId, CityId, DateTime, Detail)
            cursor.execute(query)
            connection.commit()
            return

    def update_event(self, EventId, EventName, OwnerId, CityId, DateTime, Detail):
        with dbapi2.connect(self.cp) as connection:
            cursor = connection.cursor()
            query =  "UPDATE events SET EventName = '%s', OwnerId='%s', CityId='%s', DateTime='%s', Detail='%s'WHERE EventId='%s'" % (EventName, OwnerId, CityId, DateTime, Detail,EventId)
            cursor.execute(query)
            connection.commit()
            return
