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

Kullanılan Psycopg2 Metodları
------------------------------

 **cursor**: Python kodunun PostgreSQL komutlarını çalıştırmasını sağlar.
 **execute**: Veritabanının çalışmasını sağlar.
 **commit**: Bekleyen işlemi veritabanına işler.
 **fetchall**: Sorgu sonuçlarının tüm satırlarını getirir.

Arayüz İşlemleri ve Veritabanı İlişkisi
=======================================

İş Ortakları arayüz Sayfasının Tanımlanması
-------------------------------------------

İş Ortakları sayfasına sitenin sol üst köşesindeki kategoriler sekmesinden erişebilmek için, *logged_in_layout.html* konumunda bir Bootstrap Glyphicon ile birlikte tıklandığında ilgili sayfaya yönlendiren bir buton tanımlanmıştır.

.. code-block:: html

 <li><a href="/partners"><span class="glyphicon glyphicon-signal"></span> İş Ortakları</a></li>

Bu butona tıklandığında gelen sayfa *logged_in_layout.html* sayfasına bir extension'dır. 

.. code-block:: html

 {% extends "logged_in_layout.html" %}
 {% block title %} İş Ortakları{%endblock%}
 {% block content %}

*Silme*
-------------------------
Sayfa ilk açıldığında her birine ait bir checkbox ile her bir İş Ortağı liste halinde gelir. Sayfada Bootstrap jumbotron, table ve buton stilleri kullanılmıştır. Sayfa yüklenirken veritabanına *partners_page* url'si ile bağlanılır ve veritabanından *PartnerList* istenir. Gelen bilgiler bootstrap stili bir tabloya ID değerleri bir checkbox olarak gözükecek şekilde form olarak hazırlanır. Bootstrap stili bir butona input görevi atanır ve arayüzde checkbox'ı işaretlenmiş olan kayıtların ID'leri butona tıklandığında sunucuya *partners_to_delete* isteğiyle submit edilir. Yani işaretli checkboxlara ait id'ler silinmesi talimatı ile birlikte submit edilir.

.. code-block:: html

  <div class="page-header">
  <h1>İş Ortakları</h1>
   <p>İş ortaklarımız hakkındaki bilgilere bu sayfadan erişebilir ve bilgileri düzenleyebilirsiniz. </p>
 </div>

 <div class="container">       
  <h2>İş Ortağı Silme</h2>
  <p>Kaydını silmek istediğiniz İş Ortağı'nı işaretleyebilirsiniz.</p>
  
  <form action="{{ url_for('partners_page') }}" method="post">
  
  <table class="table">
    
    <thead>
      <tr>
          <th>Sil</th>
    		<th>Adı </th>
    		<th>Kuruluş Yılı </th>
    		<th>Ülkesi </th>
      </tr>
    </thead>
   
    <tbody>
      
      {% for PartnerId, PartnerName, FoundationYear, Country in PartnerList %}
      
      <tr>
    		<td><input type="checkbox" name="partners_to_delete" value="{{ PartnerId }}" />     </td>
    		<th>{{ PartnerName }}</th>
    		<th>{{ FoundationYear }}</th>
    		<th>{{ Country }}</th>
      </tr>

      {% endfor %}
    </tbody>
  </table>
  <input type="submit" class="btn btn-primary btn-block" value="İşaretli İş Ortağını Sil" name="delete" /> 
  </form>
 </div>
 
*Ekleme*
-------------------------

Sayfada ikinci ana öğe olarak kayıt ekleme arayüzü bulunur. Bu kısımda *partners_page* url'si ile sunucuya bağlanılır eklenmek istenen iş ortağının adı, kuruluş yılı ve ülkesi bilgilerinin girilmesi istenen Bootstrap stili 3 adet form kutucuğu ekrana verilir. Bootstrap stili bir butona *partners_to_add* istemiyle girilen verileri sunucuya aktarması işlevi atanır.

.. code-block:: html

 <h2>İş Ortağı Ekleme</h2>
  <p>Yeni kayıt oluşturmak için gerekli alanları doldurunuz.</p>
  
  <form action="{{ url_for('partners_page') }}" method="post"> 
    
    <div class="form-group">
      <label for="PartnerName">Adı:</label>
      <input type="text" class="form-control" name="PartnerName">
    </div>
    
    <div class="form-group">
      <label for="FoundationYear">Kuruluş Yılı:</label>
      <input type="text" class="form-control" name="FoundationYear">
    </div>
    
    <div class="form-group">
      <label for="Country">Ülkesi:</label>
      <input type="text" class="form-control" name="Country">
    </div>
    
    <input type="submit" class="btn btn-primary btn-block" value="İş Ortağı Ekle" name="partners_to_add" />
  </form>
 </div>
 
*Güncelleme*
-------------------------

Sayfada üçüncü ana öğe olarak güncelleme arayüzü bulunur. Bu kısımda *partners_page* url'si ile sunucuya bağlanılır ve veritabanından istenen *PartnerList*'deki veriler bir for döngüsü ile Bootstrap stili form kutucuklarına yazılı olarak ekrana getirilir ve her bir satır sonuna Bootstrap stili bir buton eklenir. Kullanıcı, form kutucuklarına yazılı olarak getirilmiş verilerde bir değişiklik yaptığında o satıra ait güncelle butonuna tıklar ve form kutucuklarındaki veriler *partners_to_update* istemiyle sunucuya submit edilir.

.. code-block:: html

 <table class="table">

	    <thead>
	      <tr>
			<th>ID</th>
			<th>Adı </th>
			<th>Kuruluş Yılı </th>
			<th>Ülkesi </th>
		    <th>Güncelle</th>
	      </tr>
	    </thead>
		
	    <tbody>
		
	      {% for PartnerId, PartnerName, FoundationYear, Country in PartnerList %}
		  
		<form class="form-inline" action="{{ url_for('partners_page') }}" method="post">
		
			  <tr>        
				 <td><div class="form-group">
				  <input type="text" class="form-control" value = {{PartnerId}} name="PartnerId" required autofocus readonly >
				</div></td>  
				
				<th><div class="form-group">
				  <input type="text" class="form-control" value = {{PartnerName}} name="PartnerName" required autofocus >
				</div></th>
				
				<th><div class="form-group">
				  <input type="text" class="form-control" value = {{FoundationYear}} name="FoundationYear" required autofocus >
				</div></th>
				
				<th><div class="form-group">
				  <input type="text" class="form-control" value = {{Country}} name="Country" required autofocus >
				</div></th>   
				
				<th>
				  <input type="submit" class="btn btn-primary" value="Güncelle" name="partners_to_update" />
				</th>    
			  </tr>
			  
		</form>
		
	      {% endfor %}
		
	    </tbody>
	  
 </table>

*İş Ortakları Sayfası Sunucu Bağlantısı*
----------------------------------------

*server.py* konumunda öncelikle Partners sınıfı için import işlemi yapılmıştır.

.. code-block:: python

 from partners import Partners

Sonrasında partners tablosu initialize edilmiştir.

.. code-block:: python

 initialize.partners() 


Arayüz sayfasından gelecek olan get_partnerlist, partners_to_delete, partners_to_add ve partners_to_update istemlerini işleyip ilgili Partners sınıfı fonsiyonunu yürütücek kodlar yazılmıştır. Her bir istem işlendikten sonra arayüzde güncel verilerin gözükmesi için *partners.html* gönderilerek arayüz sayfasının yenilenmesi sağlanmıştır.

.. code-block:: python

 @app.route('/partners', methods=['GET', 'POST'])
 def partners_page():

    prtnrs = Partners(app.config['dsn'])
    fn = Func(app.config['dsn'])

    if request.method == 'GET':
        now = datetime.datetime.now()
        plist = prtnrs.get_partnerlist()
        return render_template('partners.html', PartnerList = plist, current_time = now.ctime())

    elif 'partners_to_delete' in request.form:
        partnerids = request.form.getlist('partners_to_delete')
        for PartnerId in partnerids:
            prtnrs.delete_partner(PartnerId)
        return redirect(url_for('partners_page'))

    elif 'partners_to_add' in request.form:
  prtnrs.add_partner(request.form['PartnerName'],request.form['FoundationYear'],request.form['Country'])
        return redirect(url_for('partners_page'))

    elif 'partners_to_update' in request.form:
        prtnrs.update_partner(request.form['PartnerId'], request.form['PartnerName'],request.form['FoundationYear'],request.form['Country'])
        return redirect(url_for('partners_page'))











