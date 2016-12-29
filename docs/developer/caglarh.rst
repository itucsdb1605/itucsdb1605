Hasan Hüseyin ÇAĞLAR (caglarh - 150110042)
======

Raporun bu bölümünde İşteSen adlı sosyal medya sitesinin Makaleler, Bağlantılar ve Etkinlikler sayfalarının (varlıklarının) yazılım geliştirmesi ve detayları hakkında bilgi edinebilirsiniz

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
