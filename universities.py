import psycopg2 as dbapi2
from university import University

class Universities:
    def __init__(self, cp):
        self.cp = cp
        return

    def get_universitylist(self):
        with dbapi2.connect(self.cp) as connection:
            cursor = connection.cursor()
            query = "SELECT * FROM universities ORDER BY id ASC"
            cursor.execute(query)
            rows = cursor.fetchall()
            return rows

    def get_a_universitylist(self):
        with dbapi2.connect(self.cp) as connection:
            cursor = connection.cursor()
            query = "SELECT * FROM universities_info ORDER BY uni_id ASC"
            cursor.execute(query)
            rows = cursor.fetchall()
            return rows
        
    def delete_university(self, id):
        with dbapi2.connect(self.cp) as connection:
            cursor = connection.cursor()
            query = "DELETE FROM universities WHERE id = '%s'" % (id)
            cursor.execute(query)
            connection.commit()
            return

    def add_university(self, title, local, population, type):
        with dbapi2.connect(self.cp) as connection:
            cursor = connection.cursor()
            query = "INSERT INTO universities (title) VALUES ('%s')" % (title)
            cursor.execute(query)
            query = "SELECT * FROM universities WHERE title = '%s' " % (title)
            cursor.execute(query)
            row = cursor.fetchone()
            uni_id = row[0]
            query =  "INSERT INTO universities_info (uni_id,local,population,type) VALUES ('%s','%s','%s','%s')" % (uni_id,local,population,type)
            cursor.execute(query)
            connection.commit()
            return

    def update_university(self, id, title):
        with dbapi2.connect(self.cp) as connection:
            cursor = connection.cursor()
            query = "UPDATE universities SET title = '%s' WHERE id = '%s'" % (title, id)
            cursor.execute(query)
            connection.commit()
            return

    def update_a_university(self, id, title, local, population, type):
        with dbapi2.connect(self.cp) as connection:
            cursor = connection.cursor()
            query = "UPDATE universities SET title = '%s' WHERE id = '%s'" % (title, id)
            cursor.execute(query)
            query = "UPDATE universities_info SET local='%s', population='%s', type='%s' WHERE uni_id = '%s'" % (local,population,type,id)
            cursor.execute(query)
            connection.commit()
            return

    def get_a_university(self, id):
        if id is None:
            return None
        with dbapi2.connect(self.cp) as connection:
            cursor = connection.cursor()
            query = """SELECT uni.title AS Title, uninf.local AS Local,
                    uninf.population AS Population, uninf.type AS Type
                    FROM
                    universities_info uninf
                    JOIN (SELECT * FROM universities WHERE id = '%s') uni ON uninf.uni_id = uni.id
                    """ % (id)
            cursor.execute(query)
            row = cursor.fetchone()
            if row is None:
                return None
            uni = University(row[0], row[1], row[2], row[3])
            return uni


