import psycopg2 as dbapi2

class Myconnections:
    def __init__(self, cp):
        self.cp = cp
        return

    def get_connectionlist(self):
        with dbapi2.connect(self.cp) as connection:
            cursor = connection.cursor()
            query = """SELECT u1.FirstName AS Mfname, u1.LastName AS Mlname,
             u2.FirstName AS Ffname, u2.LastName AS Flname 
             FROM myconnections 
             LEFT JOIN users u1 ON myconnections.MainUserId = u1.UserId 
             LEFT JOIN users u2 ON myconnections.FriendUserId = u2.UserId"""
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

    def delete_connection(self, ConnectionId):
        with dbapi2.connect(self.cp) as connection:
            cursor = connection.cursor()
            query = "DELETE FROM myconnections WHERE ConnectionId = '%s'" % (ConnectionId)
            cursor.execute(query)
            connection.commit()
            return
    def add_connection(self, MainUserId, FriendUserId):
        with dbapi2.connect(self.cp) as connection:
            cursor = connection.cursor()
            query =  "INSERT INTO myconnections (MainUserId, FriendUserId) VALUES ('%s','%s')" % (MainUserId, FriendUserId)
            cursor.execute(query)
            connection.commit()
            return

