import psycopg2 as dbapi2

class Partners:
    def __init__(self, cp):
        self.cp = cp
        return

    def get_partnerlist(self):
        with dbapi2.connect(self.cp) as connection:
            cursor = connection.cursor()
            query = "SELECT * FROM partners"
            cursor.execute(query)
            rows = cursor.fetchall()
            return rows

    def delete_partner(self, PartnerId):
        with dbapi2.connect(self.cp) as connection:
            cursor = connection.cursor()
            query = "DELETE FROM partners WHERE PartnerId = '%s'" % (PartnerId)
            cursor.execute(query)
            connection.commit()
            return

    def add_partner(self, PartnerName, FoundationYear, Country):
        with dbapi2.connect(self.cp) as connection:
            cursor = connection.cursor()
            query =  "INSERT INTO partners (PartnerName, FoundationYear, Country) VALUES ('%s','%s','%s')" % (PartnerName, FoundationYear, Country)
            cursor.execute(query)
            connection.commit()
            return

    def update_partner(self, PartnerId, PartnerName, FoundationYear, Country):
        with dbapi2.connect(self.cp) as connection:
            cursor = connection.cursor()
            query =  "UPDATE partners SET PartnerName = '%s', FoundationYear='%s', Country='%s' WHERE PartnerId='%s'" % (PartnerName, FoundationYear, Country, PartnerId)
            cursor.execute(query)
            connection.commit()
            return
