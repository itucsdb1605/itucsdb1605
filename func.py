import psycopg2 as dbapi2

class Func:
    def __init__(self, cp):
        self.cp = cp
        return

    def get_id(self, tablename, value):
        with dbapi2.connect(self.cp) as connection:
            cursor = connection.cursor()
            query = "SELECT * FROM {0} WHERE city = '{0}' ".format(tablename, value)
            #query += "title = '{0}'".format(value)
            cursor.execute(query)
            row = cursor.fetchone()
            if row is None:
                return None
            ret_id = row[0]
            return ret_id

    def get_title(self, tablename, id):
        with dbapi2.connect(self.cp) as connection:
            cursor = connection.cursor()
            query = "SELECT * FROM {0} WHERE id = '{1}'".format(tablename, id)
            cursor.execute(query)
            row = cursor.fetchone()
            if row is None:
                return None
            ret_title = row[1]
            return ret_title

    def get_universities(self):
        with dbapi2.connect(self.cp) as connection:
            cursor = connection.cursor()
            query = """SELECT title FROM universities ORDER BY title"""
            cursor.execute(query)
            rows = cursor.fetchall()
            nrows=[]
            for row in rows:
                nrows.append(row[0])
            return nrows

    def get_uniname(self,id):
        with dbapi2.connect(self.cp) as connection:
            cursor = connection.cursor()
            query="""SELECT title FROM universities WHERE id='%s'"""%(id)
            cursor.execute(query)
            return cursor.fetchall()[0][0]
