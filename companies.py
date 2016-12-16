import psycopg2 as dbapi2
from company import Company

class Companies:
    def __init__(self, cp):
        self.cp = cp
        return


    def get_companylist(self):
        with dbapi2.connect(self.cp) as connection:
            cursor = connection.cursor()
            query = "SELECT id, title, locations.city, locations.country, population FROM companies JOIN locations ON companies.local2 = locations.loc_id"
            cursor.execute(query)
            rows = cursor.fetchall()
            return rows

    def delete_company(self, id):
        with dbapi2.connect(self.cp) as connection:
            cursor = connection.cursor()
            query = "DELETE FROM companies WHERE id = '%s'" % (id)
            cursor.execute(query)
            connection.commit()
            return

    def add_company(self, title, local, population):
        with dbapi2.connect(self.cp) as connection:
            cursor = connection.cursor()
            query = "SELECT loc_id FROM locations WHERE city = '%s' " % (local)
            cursor.execute(query)
            row = cursor.fetchone()
            loca_id = row[0]
            query =  "INSERT INTO companies (title,local2,population) VALUES ('%s','%s','%s')" % (title,loca_id,population)
            cursor.execute(query)
            connection.commit()
            return

    def update_company(self, id, title, local, number):
        with dbapi2.connect(self.cp) as connection:
            cursor = connection.cursor()
            query = "UPDATE companies SET title= '%s', local2= '%s', population='%s' WHERE id = '%d'" % (title,local,number,id)
            cursor.execute(query)
            connection.commit()
            return

