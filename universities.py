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
            query = "SELECT uni_id, locations.city, locations.country, population, type FROM universities_info JOIN locations ON universities_info.local = locations.loc_id"
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
            query = "SELECT loc_id FROM locations WHERE city = '%s' " % (local)
            cursor.execute(query)
            row = cursor.fetchone()
            loca_id = row[0]
            query =  "INSERT INTO universities_info (uni_id,local,population,type) VALUES ('%s','%s','%s','%s')" % (uni_id,loca_id,population,type)
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

    def update_a_university(self, id, uni, city, country, number, type):
        with dbapi2.connect(self.cp) as connection:
            cursor = connection.cursor()
            query = "UPDATE universities SET title = '%s' WHERE id = '%s'" % (uni, id)
            cursor.execute(query)
            #query = "SELECT loc_id FROM locations WHERE city= '%s' " % (city)
            query = "UPDATE universities_info SET local= 62, population='%s', type='%s' WHERE uni_id = '%d'" % (number,type,id)
            cursor.execute(query)
            connection.commit()
            return

    def get_a_university(self, id):
        if id is None:
            return None
        with dbapi2.connect(self.cp) as connection:
            cursor = connection.cursor()
            query = """SELECT uni.title AS Title, loc.city AS City, loc.country AS Country,
                    uninf.population AS Population, uninf.type AS Type
                    FROM
                    universities_info uninf
                    JOIN (SELECT * FROM universities WHERE id = '%s') uni ON uninf.uni_id = uni.id
                    JOIN (SELECT * FROM locations WHERE loc_id ='%s') loc ON uninf.local = loc.loc_id
                    """ % (id)
            cursor.execute(query)
            row = cursor.fetchone()
            if row is None:
                return None
            uni = University(row[0], row[1], row[2], row[3], row[4])
            return uni

