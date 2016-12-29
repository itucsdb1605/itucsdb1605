Aydoğdu Demirci Tarafından Gerçeklenen İşlemler
===============================================

İş Ortakları Tablosu
-------------------------

İş Ortakları varlığı *partners* isimli tablo ile tanımlanmıştır. Bu tablo 4 kolondan oluşmaktadır. Bu kolonlar iş ortağı ID'si, ismi, kuruluş yılı ve ülkesini sırasıyla temsil eden PartnerId, PartnerName, FoundationYear ve Country anahtarlarından oluşmaktadır. Bunların arasından primary key olarak *PartnerId* belirlenmiştir. Veritabanı işlemleri sırasında hali hazırda zaten tablo oluşturulmuş ise hata almamak için *DROP TABLE IF EXISTS partners CASCADE* sorgusu kullanılmıştır. Tablonun niteliklerinden olan PartnerId primary key olarak tanımlanmıştır. PartnerName maksimum 40 uzunluğunda eşsiz bir katar olarak, FoundationYear bir tamsayı olarak ve Country ise yine maksimum 40 uzunluğunda bir katar olarak tanımlanmıştır. Tablo *init.py* konumunda tanımlanmış ve *insert into* komutu ile 9 adet iş ortağı kaydı başlangıç olarak tabloya eklenmiştir.

.. code-block:: python

 def partners(self):
        with dbapi2.connect(self.cp) as connection:
            cursor = connection.cursor()
            query = "DROP TABLE IF EXISTS partners CASCADE"
            cursor.execute(query)

            query = """CREATE TABLE partners (
                    PartnerId SERIAL PRIMARY KEY,
                    PartnerName VARCHAR(40) UNIQUE NOT NULL,
                    FoundationYear INT NOT NULL,
                    Country VARCHAR(40) NOT NULL
                    )"""
            cursor.execute(query)

            query = """INSERT INTO partners(PartnerName, FoundationYear, Country) VALUES
              ('Tesla', 2003, 'USA' ),
              ('Vestel', 1984, 'Turkey' ),
              ('Gigafactory', 2014, 'USA' ),
              ('SpaceX', 2002, 'USA' ),
              ('Foxconn', 1974, 'China' ),
              ('Panasonic', 1918, 'Japan' ),
              ('Casper', 1991, 'Turkey'),
              ('LG', 1947, 'Korea' ),
              ('Airbus', 1970, 'France');
              """
            cursor.execute(query)
            connection.commit()

Kullanılan Psycopg2 Metodları
--------------------------------

| **cursor**: Python kodunun PostgreSQL komutlarını çalıştırmasını sağlar.
| **execute**: Veritabanının çalışmasını sağlar.
| **commit**: Bekleyen işlemi veritabanına işler.
| **fetchall**: Sorgu sonuçlarının tüm satırlarını getirir.


İş Ortakları Class Yapısı
-------------------------
İş Ortakları varlığının class yapısı *partners.py* konumunda tanımlanmıştır. Bu class yapısında listeleyen, kayıt ekleyen, kayıt silen ve kayıt güncelleyen fonksiyonlar tanımlıdır.

*Listeleme*
-------------------------
 **get_partnerlist**: Veritabanından tüm iş ortağı kayıtlarını çekmek için bu fonksiyon tanımlanmıştır. Fonksiyon bu hali ile partners tablosundaki tüm kayıtları tüm bilgileri ile döndürmektedir. Farklı bir mekanizma istenirse sorgu değiştirilebilir.

.. code-block:: python

    def get_partnerlist(self):
        with dbapi2.connect(self.cp) as connection:
            cursor = connection.cursor()
            query = "SELECT * FROM partners"
            cursor.execute(query)
            rows = cursor.fetchall()
            return rows


*Silme*
-------------------------
 **delete_partner**: Veritabanından iş ortağı kaydı silmek için bu fonksiyon tanımlanmıştır. Arayüzde ID'ler checkbox ile tanımlanmış olup, işaretli checkboxlar ile silinmesi istenen kayıtların ID'leri bu fonksiyona yönlendirilir ve *delete* komutuyla kayıtlar silinir.

.. code-block:: python

    def delete_partner(self, PartnerId):
        with dbapi2.connect(self.cp) as connection:
            cursor = connection.cursor()
            query = "DELETE FROM partners WHERE PartnerId = '%s'" % (PartnerId)
            cursor.execute(query)
            connection.commit()
            return

*Ekleme*
-------------------------
 **add_partner**: Veritabanına yeni kayıt eklemek için bu fonksiyon tanımlanmıştır. Kaydı eklenmek istenen iş ortağına ait isim, kuruluş yılı ve ülkesi gibi bilgileri PartnerName, FoundationYear ve Country değişkenleri ile parametre olarak alır ve *insert into* komutu ile veritabanına yeni kayıt ekler.

.. code-block:: python

    def add_partner(self, PartnerName, FoundationYear, Country):
        with dbapi2.connect(self.cp) as connection:
            cursor = connection.cursor()
            query =  "INSERT INTO partners (PartnerName, FoundationYear, Country) VALUES ('%s','%s','%s')" % (PartnerName, FoundationYear, Country)
            cursor.execute(query)
            connection.commit()
            return

*Güncelleme*
-------------------------

 **update_partner**: Veritabanındaki bir kaydı güncellemek için bu fonksiyon tanımlanmıştır. Güncellenmek istenen kayda ait ID, isim, yıl ve ülke bilgilerini sırasıyla PartnerId, PartnerName, FoundationYear ve Country parametreleri ile alır ve *update* komutu ile ilgili ID'ye sahip olan kaydı bulup günceller.

.. code-block:: python

    def update_partner(self, PartnerId, PartnerName, FoundationYear, Country):
        with dbapi2.connect(self.cp) as connection:
            cursor = connection.cursor()
            query =  "UPDATE partners SET PartnerName = '%s', FoundationYear='%s', Country='%s' WHERE PartnerId='%s'" % (PartnerName, FoundationYear, Country, PartnerId)
            cursor.execute(query)
            connection.commit()
            return
