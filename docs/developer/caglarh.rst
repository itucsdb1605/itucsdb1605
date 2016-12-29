Hasan Hüseyin ÇAĞLAR tarafından gerçekleştirilen Bölümler
================================
MAKALELER, BAĞLANTILAR VE ETKİNLİKLER
================================
Veritabanı Tablolarını Hazırlama Metodu
----------------------------------
İlgili tabloları oluşturmak ve ilk kayıtları eklemek için, **init.py** dosyasının **class INIT:** isimli sınıfı ve ona bağı olan **def ArticleEventConnection(self):** adlı metodu içerisinde işlemler gerçekleştirilmiştir, **init.py** dosyasının içerik yapısı:

.. code-block:: python

      import psycopg2 as dbapi2
      class INIT:
           #...Other methods
         def ArticleEventConnection(self):
           #... creating tables, inserting rows
           # for the articles, events and conenctions...
  
Makaleler
--------------

Bağlantılar
--------------

Etkinlikler
--------------
