import psycopg2 as dbapi2

class Myconnections:
    def __init__(self, cp):
        self.cp = cp
        return

    def get_connectionlist(self):
        with dbapi2.connect(self.cp) as connection:
            cursor = connection.cursor()
            query = """SELECT connections.ConnectionId, u1.FirstName AS Mfname, u1.LastName AS Mlname,
             u2.FirstName AS Ffname, u2.LastName AS Flname 
             FROM connections 
             LEFT JOIN users u1 ON connections.MainUserId = u1.UserId 
             LEFT JOIN users u2 ON connections.FriendUserId = u2.UserId"""
            cursor.execute(query)
            rows = cursor.fetchall()
            return rows
        
    def get_connectionlistbyuser(self,byUserId):
        with dbapi2.connect(self.cp) as connection:
            cursor = connection.cursor()
            query = """SELECT connections.ConnectionId, u1.FirstName AS Mfname, u1.LastName AS Mlname,
             u2.FirstName AS Ffname, u2.LastName AS Flname 
             FROM connections 
             LEFT JOIN users u1 ON connections.MainUserId = u1.UserId 
             LEFT JOIN users u2 ON connections.FriendUserId = u2.UserId
             WHERE connections.MainUserId='%s'""" %(byUserId)
            cursor.execute(query)
            rows = cursor.fetchall()
            return rows
        
    def get_connectionlistbyuniversity(self,byUniversityId):
        with dbapi2.connect(self.cp) as connection:
            cursor = connection.cursor()
            query = """SELECT  users.uni, users.FirstName, users.LastName
             FROM users 
             LEFT JOIN universities ON universities.title = users.uni 
             WHERE universities.id='%s'""" %(byUniversityId)
            cursor.execute(query)
            rows = cursor.fetchall()
            return rows
        
    def get_universityconnectionlist(self):
        with dbapi2.connect(self.cp) as connection:
            cursor = connection.cursor()
            query = """SELECT  users.uni, users.FirstName, users.LastName
             FROM users """ 
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
        
    def get_universitylist(self):
        with dbapi2.connect(self.cp) as connection:
            cursor = connection.cursor()
            query = "SELECT * FROM universities ORDER BY title ASC"
            cursor.execute(query)
            rows = cursor.fetchall()
            return rows
        
    def delete_connection(self, ConnectionId):
        with dbapi2.connect(self.cp) as connection:
            cursor = connection.cursor()
            query = "DELETE FROM connections WHERE ConnectionId = '%s'" % (ConnectionId)
            cursor.execute(query)
            connection.commit()
            return
    def add_connection(self, MainUserId, FriendUserId):
        with dbapi2.connect(self.cp) as connection:
            cursor = connection.cursor()
            query =  "INSERT INTO connections (MainUserId, FriendUserId) VALUES ('%s','%s')" % (MainUserId, FriendUserId)
            cursor.execute(query)
            connection.commit()
            return

