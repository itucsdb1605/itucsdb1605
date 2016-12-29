Aydoğdu Demirci Tarafından Gerçeklenen İşlemler
===============================================

Kullanılan Psycopg2 Metodları
--------------------------------

| **cursor()** Python kodunun veritabanında PostgreSQL komutunu çalıştırmasına izin verir.
| **execute()** Veritabanının çalışmasını sağlar.
| **commit()** Bekleyen işlemi veritabanına commit'ler.
| **fetchall()** Sorgu sonuçlarının tüm satırlarını getirir ve onları tuple listesi olarak döndürür.


İş Ortakları Class Yapısı
-------------------------
.. code-block:: python

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

| Partners tablosunun 4 kolonu vardır. Bunlar PartnerID, PartnerName, FoundationYear ve Country Country table has six columns. It takes six fields as consructor if any of them is is not entered by user it set them to empty space.
Even class mappers is not used for database operations, in class functions objects are created and sent to html page.
Countries class has fundamental database functions which are Create, Read, Update and Delete.

|
