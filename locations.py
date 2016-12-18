import psycopg2 as dbapi2
from location import Location

class Locations:
    def __init__(self, cp):
        self.cp = cp
        return


    def get_locationlist(self):
        with dbapi2.connect(self.cp) as connection:
            cursor = connection.cursor()
            query = "SELECT loc_id, city, country FROM locations"
            cursor.execute(query)
            rows = cursor.fetchall()
            return rows

    def delete_location(self, id):
        with dbapi2.connect(self.cp) as connection:
            cursor = connection.cursor()
            query = "DELETE FROM locations WHERE loc_id = '%s'" % (id)
            cursor.execute(query)
            connection.commit()
            return

    def add_location(self, id, city, country):
        with dbapi2.connect(self.cp) as connection:
            cursor = connection.cursor()
            query =  "INSERT INTO locations (loc_id,city,country) VALUES ('%s','%s','%s')" % (id,city,country)
            cursor.execute(query)
            connection.commit()
            return

    def update_location(self, id, city, country):
        with dbapi2.connect(self.cp) as connection:
            cursor = connection.cursor()
            query = "UPDATE locations SET loc_id= '%s', city= '%s', country='%s' WHERE id = '%d'" % (id,city,country,id)
            cursor.execute(query)
            connection.commit()
            return

