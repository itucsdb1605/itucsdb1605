Mert YILDIZ Tarafından Yapılan Kısımlar
=======================================

Psycopg2 Metodunun Açıklaması
----------------------------------

**con()** PostgreSQL veri tabanına bağlantı sağlanmasını halleder. 

**cursor()** PostgreSQL komutlarının python kodunda çalıştırılmasını sağlar. 

**execute()** Veri tabanı işleminin çalıştırılmasını sağlar.(Sorgu yada komutların)

**commit()** bekleyen değişiklik yada işlemleri veri tabanına işler. 

**fetchall()** Sorgu sonucunu alır ve satırlar halinde döner.


Üniversiteler
--------------

Üniversiteleri temsil etmek için sistemde iki adet tablo gerçeklendi. Bunlardan ilki olan "universities" tablosu "id" ve "title" niteliklerinden oluşan basit bir tablodur. "id" niteliği birincil anahtar olup "Serial" olarak tanımlanmıştır. Diğer nitelik olan "title" da ise üniversitelerin isimleri yer almaktadır. Bu tablo site açıldığında aşağıdaki kod ile oluşturulup, ilk değerleri atanmaktadır.


.. code-block:: python

        def universities(self):
        with dbapi2.connect(self.cp) as connection:
            cursor = connection.cursor()
            query = "DROP TABLE IF EXISTS universities CASCADE"
            cursor.execute(query)

            query = """CREATE TABLE universities (
                    id SERIAL PRIMARY KEY,
                    title VARCHAR(40) UNIQUE NOT NULL
                )"""
            cursor.execute(query)

            cursor.execute("""INSERT INTO universities (title) VALUES
              ('Ankara Üniversitesi'),
              ('Gazi Üniversitesi'),
              ('Bilkent Üniversitesi'),
              ('Hacettepe Üniversitesi'),
              ('Orta Doğu Teknik Üniversitesi'),
              ('Ege Üniversitesi '),
              ('Dokuz Eylül Üniversitesi'),
              ('Kocaeli Üniversitesi'),
              ('Sakarya Üniversitesi'),
              ('Boğaziçi Üniversitesi'),
              ('Yıldız Teknik Üniversitesi'),
              ('İstanbul Üniversitesi'),
              ('Bahçeşehir Üniversitesi'),
              ('Galatasaray Üniversitesi'),
              ('İstanbul Teknik Üniversitesi'),
              ('Özyeğin Üniversitesi'),
              ('Sabancı Üniversitesi'),
              ('Koç Üniversitesi'),
              ('Munzur Üniversitesi'),
              ('Gebze Teknik Üniversitesi'),
              ('Karadeniz Teknik Üniversitesi'),
              ('Işık Üniversitesi'),
              ('Kadir Has Üniversitesi'),
              ('Bursa Teknik Üniversitesi'),
              ('Fırat Üniversitesi'),
              ('Osmangazi Üniversitesi'),
              ('Kırıkkale Üniversitesi'),
              ('Sinop Üniversitesi'),
              ('Atılım Üniversitesi'),
              ('Erzincan Üniversitesi'),
              ('Yüzüncü Yıl Üniversitesi'),
              ('Anadolu Üniversitesi'),
              ('Akdeniz Üniversitesi'),
              ('Başkent Üniversitesi'),
              ('Şehir Üniversitesi'),
              ('Atatürk Üniversitesi'),
              ('Yeditepe Üniversitesi'),
              ('Marmara Üniversitesi'),
              ('Uludağ Üniversitesi'),
              ('Düzce Üniversitesi'),
              ('Trakya Üniversitesi'),
              ('Bilgi Üniversitesi');
            """)
            connection.commit()

Üniversiteler hakkında daha detaylı bilgilerin bulunduğu diğer bir tablo ise "universities_info" tablosudur. Bu tabloda "uni_id","local","population" ve "type" olmak üzere dört nitelik vardır. Bunlardan uni_id universities tablosundaki id ile ilişkili dış anahtar, local ise locations tablosundaki loc_id ile ilişkili bir dış anahtardır. Bu tabloda üniversitelere ait yeri, öğrenci sayısı ve türü(özel yada devlet) gibi bilgiler tutulmaktadır. Tablonun oluşturulması ve ilk değerlerin atanması aşağıdaki kod ile site açıldığında yapılmaktadır. 

.. code-block:: python

	def universities_info(self):
        with dbapi2.connect(self.cp) as connection:
            cursor = connection.cursor()
            query = "DROP TABLE IF EXISTS universities_info CASCADE"
            cursor.execute(query)

            query = """CREATE TABLE universities_info (
                    uni_id INTEGER NOT NULL REFERENCES universities(id)
                        ON DELETE CASCADE
                        ON UPDATE CASCADE,
                    local INTEGER NOT NULL REFERENCES locations(loc_id)
                        ON DELETE CASCADE
                        ON UPDATE CASCADE,
                    population NUMERIC(10),
                    type VARCHAR(10),
                    UNIQUE (uni_id)
                )"""
            cursor.execute(query)
            query = """INSERT INTO universities_info VALUES
              (1, 6, 15020,'Devlet'),
              (2, 6, 25010,'Devlet'),
              (3, 6, 21008,'Özel'),
              (4, 6, 12504,'Devlet'),
              (5, 6, 27500,'Devlet'),
              (6, 35, 25412,'Devlet'),
              (7, 35, 10997,'Devlet'),
              (8, 41, 17627,'Devlet'),
              (9, 54, 6570,'Devlet'),
              (10, 34, 8879, 'Devlet'),
              (11, 34, 8690, 'Devlet'),
              (12, 34, 11994, 'Devlet'),
              (13, 34, 33424, 'Özel'),
              (14, 34, 11586, 'Devlet'),
              (15, 34, 17215, 'Devlet'),
              (16, 34, 15990,'Özel'),
              (17, 34, 3944,'Özel'),
              (18, 34, 3338, 'Özel'),
              (19, 62, 1330,'Devlet'),
              (20, 41, 1219, 'Devlet'),
              (21, 61, 8879, 'Devlet'),
              (22, 34, 8600, 'Özel'),
              (23, 34, 11994,'Özel'),
              (24, 16, 3384, 'Devlet'),
              (25, 23, 11586,'Devlet'),
              (26, 26, 17615,'Devlet'),
              (27, 71, 5110, 'Devlet'),
              (28, 57, 3774,'Devlet'),
              (29, 6, 3338,'Özel'),
              (30, 24, 2030, 'Devlet'),
              (31, 65, 1439,'Devlet'),
              (32, 26, 38424,'Devlet'),
              (33, 7, 11586,'Devlet'),
              (34, 6, 17215, 'Özel'),
              (35, 34, 24190,'Özel'),
              (36, 25, 7944, 'Devlet'),
              (37, 34, 3338,'Özel'),
              (38, 34, 9030,'Devlet'),
              (39, 16, 4139,'Devlet'),
              (40, 81, 2558, 'Devlet'),
              (41, 22, 9030,'Devlet'),
              (42, 34, 4239, 'Özel');
            """
            cursor.execute(query)
            connection.commit()

Üniversite Sınıfının Yapısı ve Kurucu Fonksiyonu
++++++++++++++++++++++++++++++++++++++++++++++

Üniversiteleri temsil etmek için oluşturulan sınıfın yapısı elemanları ve kurucu fonksiyonu aşağıdaki gibidir.

.. code-block:: python

	class University:
    def __init__(self, title, local, population, type):
        self.Title = title
        self.Local = local
        self.Population = population
        self.Type = type

Üniversiteler İçin Yazılan Fonksiyonlar
+++++++++++++++++++++++++++++++++++++++
 
Bu varlığın tablolarına ekleme, silme, güncelleme ve seçme işlemlerinin yapılabilmesi için gerekli olan kodlar projede "universities.py	" dosyasının altındadır.

Üniversite Ekleme
+++++++++++++++++

Sitenin arayüzünden girilen bilgileri kullanarak öncelikle "universities" tablosuna yeni üniversitenin adını, "universities_info" tablosuna da girilen diğer ilgili bilgileri ekler. Bu şekilde yeni bir üniversite eklenmiş olur. Bu işlem yazılan kod aşağıdaki gibidir.  

.. code-block:: python

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
            query =  "INSERT INTO universities_info (uni_id,local,population,type) VALUES ('%s','%s','%s','%s')" %                                   (uni_id,loca_id,population,type)
            cursor.execute(query)
            connection.commit()
            return

Bu ekleme fonksiyonu server.py'daki üniversiteler ile ilgili olan kısımda ekleme işlemi yapılacağı zaman kullanılır.


Üniversite Silme
++++++++++++++++

Arayüzdeki kontrol kutuları işaretlenen üniversitelerin id değerlerini alarak bu üniversiteleri tablodan kaldırır. Silme işlemi için kullanılan kod aşağıdaki gibidir. Bu kod server.py'da yazılmış olup, eğer arayüzde herhangi bir kontrol kutusu işaretlenmişse çalışır. Öncelikle "universities" ardından bağlantılı olduğu diğer tablo olan "universities_info" tablosundan kaldırılır.

.. code-block:: python

	elif 'unis_to_delete' in request.form:
        ids = request.form.getlist('unis_to_delete')

        for id in ids:
            id = id.split('/', maxsplit=1)
            id = id[0]
            unis.delete_university(id)
        connection = dbapi2.connect(app.config['dsn'])
        cursor = connection.cursor()
        statement = """SELECT * FROM universities"""
        cursor.execute(statement)
        ulist = cursor.fetchall()
        statement = """SELECT uni_id, locations.city, locations.country, population, type FROM universities_info JOIN locations ON               universities_info.local = locations.loc_id"""
        cursor.execute(statement)
        ilist = cursor.fetchall()
        connection.commit()
        now = datetime.datetime.now()
        return render_template('universities.html', UniversityList = ulist, InfoList=ilist, current_time = now.ctime())

Üniversite Güncelle
+++++++++++++++++++++

Üniversite güncellemek için önce arayüzde istenen üniversitenin yanındaki "Güncelle" linkine tıklanması ardından açılan yeni sayfada yeni bilgilerin girilerek "Güncelle" butonuna basılması gerekmektedir. İşte Html kodunda, istenen üniversitenin yanındaki linke tıklandığında bu üniversitenin id değerinin gönderilmesiyle "/universiteler/id" uzantılı yeni bir sayfa açılır. Daha sonra bu id değerine sahip üniversite için yeni girilen bilgiler kullanılarak güncelleme işlemi yapılır. Html kısmındaki yeni sayfaya yönlendiren ve id değerini gönderen kod şu şekildedir.

.. code-block:: html

				<br>
		<h3>Üniversiteler</h3>
		<br>
		<form method="POST">
		<table class="table table-hover">
		  <thead>
		    <tr>
		      <th>Adı</th>
		      <th>Şehir</th>
		      <th>Ülke</th>
		      <th>Öğrenci Sayısı</th>
		      <th>Türü</th>
		      <th>Güncellensin Mi?</th>
		      <th>Silinsin Mi?</th>
		    </tr>
		  </thead>
		  <tbody>

		  	{% for i in range(0,UniversityList|count) %}
			  <tr>
			  {% for j in range(1,2) %}
			  		<td>{{UniversityList[i][j]}}</td>
				{% endfor %}
 				{% for k in range(1,5) %}
					<td>{{InfoList[i][k]}}</td>
				{% endfor %}
			    <td><a href="{{request.path}}/{{InfoList[i]			[0]}}" class="text-info" name="unis_to_update">Güncelle</a></td>
				<td><input type="checkbox" 	name="unis_to_delete" value= {{UniversityList[i][0]}}/></td>
			  </tr>
			{% endfor %}


		  </tbody>
		</table>

Buradan gelen id ile yeni açılan sayfaya ait server.py daki kod ise aşağıdaki gibidir. Bu koda göre öncelikle sayfanın metodu "GET" ise güncellenecek olan üniversitenin bilgileri yeni açılan sayfadaki metin kutularına doldurulur. Eğer "POST" ise yani "Güncelle" butonuna basılırsa, seçili üniversitenin id değerine göre seçim yapılarak yeni veriler ile güncelleme işlemi yapılır ve ardından üniversiteler sayfasına geri dönülür.

.. code-block:: python
	
	@app.route('/universiteler/<int:id>', methods=		['GET','POST'])
	def uni_update_page(id):
    	unis = Universities(app.config['dsn'])
    	fn = Func(app.config['dsn'])
    	if request.method == 'GET':
        connection = dbapi2.connect(app.config['dsn'])
        cursor = connection.cursor()
        statement = """SELECT * FROM universities WHERE id=	{}""".format(id)
        cursor.execute(statement)
        univ = cursor.fetchall()
        statement = """SELECT uni_id, locations.city, 	locations.country, population, type FROM universities_info 	JOIN locations ON           universities_info.local = locations.loc_id 	WHERE uni_id={}""".format(id)
        cursor.execute(statement)
        infos = cursor.fetchall()
        connection.close()
        now = datetime.datetime.now()
        return render_template('a_university.html',ID=id, 	UniversityList = univ, InfoList=infos, 	current_time=now.ctime())
    	#elif 'universities_to_update' in request.form:
    	if request.method == 'POST':
        #unis.update_a_university(id,request.form['uni'], 	request.form['city'],request.form['cont'],request.form	                            ['number'],request.form['type'])
        connection = dbapi2.connect(app.config['dsn'])
        cursor = connection.cursor()
        statement = """UPDATE universities
                    SET  title ='{}'
                    WHERE id={};""".format(request.form['uni'], 	id)
        cursor.execute(statement)
        statement ="""SELECT loc_id FROM locations WHERE 	city='{}';""".format(request.form['city'])
        cursor.execute(statement)
        row = cursor.fetchone()
        if row is None:
            return None
        loca_id = row[0]
        statement = """UPDATE universities_info
                    SET local='{}', population='{}', type='{}' 	WHERE uni_id = {};""".format(loca_id,request.form	                              ['number'],request.form['type'],id)
        cursor.execute(statement)
        statement = """SELECT * FROM universities"""
        cursor.execute(statement)
        ulist = cursor.fetchall()
        statement = """SELECT uni_id, locations.city, 	locations.country, population, type FROM universities_info 	JOIN locations ON           universities_info.local = 	locations.loc_id"""
        cursor.execute(statement)
        ilist = cursor.fetchall()
        connection.commit()
        now = datetime.datetime.now()
        #return render_template('universities.html', 	UniversityList = ulist, InfoList=ilist, 	current_time=now.ctime())
     return redirect(url_for('uni_page'))


Üniversite Seçme
+++++++++++++++++++++

Arayüzde girilen belirli kriterlere göre üniversite bilgilerini seçme işlemi yapmak için kullanılan kısımdır. Seçme işlemi için önce bir şehir girilir, ardından bu şehirdeki özel, devlet yada her ikisi birden seçilerek istenen tür belirtilir. Yapılan bu seçimlere göre tablolardan istenen kriterlere uyan üniversiteler çekilerek yeni bir sayfada listelenir. Bu işlemler için server.py'da yazılan kod şu şekildedir:

.. code-block:: python

	elif 'universities_to_select' in request.form:
        vals = request.form.getlist('unis_to_select')
        City=request.form['city']
        #l_id=fn.get_id("locations",City)
        length=len(vals)
        if length==2:
            connection = dbapi2.connect(app.config['dsn'])
            cursor = connection.cursor()
            statement = """SELECT loc_id FROM locations WHERE city='{}';""".format(City)
            cursor.execute(statement)
            row = cursor.fetchone()
            if row is None:
                 now = datetime.datetime.now()
                 return render_template('404.html', current_time = now.ctime())
            loca_id = row[0]
            statement = """SELECT universities.title, universities_info.population, universities_info.type FROM universities JOIN                   universities_info ON universities_info.uni_id = universities.id WHERE local ={}""".format(loca_id)
            cursor.execute(statement)
            ilist = cursor.fetchall()
            connection.commit()
            now = datetime.datetime.now()
            if ilist is None:
                return render_template('404.html', current_time = now.ctime())
            return render_template('b_university.html', UniversityList = ilist, current_time = now.ctime())
        elif length==1:
            connection = dbapi2.connect(app.config['dsn'])
            cursor = connection.cursor()
            statement = """SELECT loc_id FROM locations WHERE city='{}';""".format(City)
            cursor.execute(statement)
            row = cursor.fetchone()
            if row is None:
                 now = datetime.datetime.now()
                 return render_template('404.html', current_time = now.ctime())
            loca_id = row[0]
            statement = """SELECT universities.title, universities_info.population, universities_info.type FROM universities JOIN                   universities_info ON universities_info.uni_id = universities.id WHERE universities_info.local ={} AND                                   universities_info.type='{}' """.format(loca_id,vals[0])
            cursor.execute(statement)
            ilist = cursor.fetchall()
            connection.commit()
            now = datetime.datetime.now()
            if ilist is None:
                return render_template('404.html', current_time = now.ctime())
            return render_template('b_university.html', UniversityList = ilist, current_time = now.ctime())


Görüldüğü üzere öncelikle "Seç" butonuna basılması beklenir, bu butona basılırsa, "Özel" ve "Devlet" değerlerini taşıyan kontrol kutularının değerleri ve girilen şehir bilgisi alınır. Önce kontrol kutularının ikisininde mi yoksa birinin mi seçildiğine bakılır. İkiside seçildiyse girilen şehre göre seçme işlemi yapılır. Eğer yanlızca "Özel" veya "Devlet" seçildiyse o zaman bu kriterde seçimde göz önüne alınır.

Eğer yanlış değer girilirse hata sayfasına yönlendirilir.(404.html)


Şirketler
-------------------

Şirketleri temsil etmek için sistemde "companies" tablosu gerçeklendi. Tablo "id", "title", "local2" ve "population" olmak üzere dört nitelikten oluşmaktadır. Bunlarda sırasıyla şirketin sıra numarası(birincil anahtar olarak kullanıldı.), şirketin ismi, yer bilgisi("locations" tablosuna dışa anahtar olarak) ve çalışan sayısı bilgileri tutulmaktadır. Bu tablo site açıldığında aşağıdaki kod ile oluşturulup, ilk değerleri atanmaktadır.


.. code-block:: python

        def companies(self):
        with dbapi2.connect(self.cp) as connection:
            cursor = connection.cursor()
            query = "DROP TABLE IF EXISTS companies CASCADE"
            cursor.execute(query)

            query = """CREATE TABLE companies (
                    id SERIAL PRIMARY KEY,
                    title VARCHAR(40) UNIQUE NOT NULL,
                    local2 INTEGER NOT NULL REFERENCES locations(loc_id)
                        ON DELETE CASCADE
                        ON UPDATE CASCADE,
                    population NUMERIC(10)
                )"""
            cursor.execute(query)

            cursor.execute("""INSERT INTO companies(title,local2,population) VALUES
              ('Apple', 34, 1200),
              ('Turkcell', 34, 4500),
              ('Vodafone', 34, 2100),
              ('Airties', 34, 800),
              ('Microsoft', 34, 6800),
              ('Google', 34, 1700),
              ('Avea', 34, 1700),
              ('Akbank', 41, 2700),
              ('Tüpraş', 41, 5800),
              ('Arkas', 35, 900),
              ('Logosoft', 6, 1700),
              ('NVIDIA', 34, 360);
            """)
            connection.commit()



Şirket Sınıfının Yapısı ve Kurucu Fonksiyonu
++++++++++++++++++++++++++++++++++++++++++++++

Şirketleri temsil etmek için oluşturulan sınıfın yapısı elemanları ve kurucu fonksiyonu aşağıdaki gibidir.

.. code-block:: python

	class Company:
    def __init__(self, title, local, population):
        self.Title = title
        self.Local = local
        self.Population = population

Üniversiteler İçin Yazılan Fonksiyonlar
+++++++++++++++++++++++++++++++++++++++
 
Bu varlığın tablolarına ekleme, silme, güncelleme ve seçme işlemlerinin yapılabilmesi için gerekli olan kodlar projede "companies.py" dosyasının altındadır.

Şirket Ekleme
+++++++++++++++++

Sitenin arayüzünden girilen bilgileri kullanarak "companies" tablosuna yeni şirketin adını, çalışan sayısını, şehrini gibi ilgili bilgileri ekler. Bu şekilde yeni bir şirket eklenmiş olur. Bu işlem yazılan kod aşağıdaki gibidir.  

.. code-block:: python

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

Bu ekleme fonksiyonu server.py'daki şirketler ile ilgili olan kısımda ekleme işlemi yapılacağı zaman kullanılır. 


Şirket Silme
++++++++++++++++

Arayüzdeki kontrol kutuları işaretlenen şirketlerin id değerlerini alarak bu şirketleri tablodan kaldırır. Silme işlemi için kullanılan kod aşağıdaki gibidir. Bu kod server.py'da yazılmış olup, eğer arayüzde herhangi bir kontrol kutusu işaretlenmişse çalışır. 

.. code-block:: python

	elif 'comps_to_delete' in request.form:
        ids = request.form.getlist('comps_to_delete')

        for id in ids:
            id = id.split('/', maxsplit=1)
            id = id[0]
            comps.delete_company(id)
        connection = dbapi2.connect(app.config['dsn'])
        cursor = connection.cursor()
        statement = """SELECT id, title, locations.city, locations.country, population FROM companies JOIN locations ON companies.local2          = locations.loc_id"""
        cursor.execute(statement)
        clist = cursor.fetchall()
        connection.commit()
        now = datetime.datetime.now()
        return render_template('companies.html', CompanyList = clist, current_time = now.ctime())


Şirket Güncelle
+++++++++++++++++++++

Şirket güncellemek için önce arayüzde istenen şirketin yanındaki "Güncelle" linkine tıklanması ardından açılan yeni sayfada yeni bilgilerin girilerek "Güncelle" butonuna basılması gerekmektedir. İşte Html kodunda, istenen şirketin yanındaki linke tıklandığında bu şirketin id değerinin gönderilmesiyle "/sirketler/id" uzantılı yeni bir sayfa açılır. Daha sonra bu id değerine sahip şirket için yeni girilen bilgiler kullanılarak güncelleme işlemi yapılır. Html kısmındaki yeni sayfaya yönlendiren ve id değerini gönderen kod şu şekildedir.

.. code-block:: python

		<form method="POST">
    <table class="table table-hover">
		  <thead>
		    <tr>
		      <th>Adı</th>
		      <th>Şehir</th>
		      <th>Ülke</th>
		      <th>Çalışan Sayısı</th>
		      <th>Güncellensin Mi?</th>
		      <th>Silinsin Mi?</th>
		    </tr>
		  </thead>
		  <tbody>

		  	{% for i in range(0,CompanyList|count) %}
			  <tr>
 				{% for k in range(1,5) %}
					<td>{{CompanyList[i][k]}}</td>
				{% endfor %}
			    <td><a href="{{request.path}}/{{CompanyList[i][0]}}" class="text-info" name="comps_to_update">Güncelle</a></td>
				<td><input type="checkbox" name="comps_to_delete" value= {{CompanyList[i][0]}}/></td>
			  </tr>
			{% endfor %}


		  </tbody>
		</table>

Buradan gelen id ile yeni açılan sayfaya ait server.py daki kod ise aşağıdaki gibidir. Bu koda göre öncelikle sayfanın metodu "GET" ise güncellenecek olan şirketin bilgileri yeni açılan sayfadaki metin kutularına doldurulur. Eğer "POST" ise yani "Güncelle" butonuna basılırsa, seçili şirketin id değerine göre seçim yapılarak yeni veriler ile güncelleme işlemi yapılır ve ardından şirketler sayfasına geri dönülür.

.. code-block:: python
	
	@app.route('/sirketler/<int:id>', methods=['GET','POST'])
    def comp_update_page(id):
    comps = Companies(app.config['dsn'])
    fn = Func(app.config['dsn'])
    if request.method == 'GET':
        connection = dbapi2.connect(app.config['dsn'])
        cursor = connection.cursor()
        statement = """SELECT id, title, locations.city, locations.country, population FROM companies JOIN locations ON companies.local2         = locations.loc_id WHERE id={}""".format(id)
        cursor.execute(statement)
        clist = cursor.fetchall()
        connection.close()
        now = datetime.datetime.now()
        return render_template('a_company.html',ID=id, CompanyList = clist, current_time=now.ctime())
    #elif 'universities_to_update' in request.form:
    if request.method == 'POST':
        #unis.update_a_university(id,request.form['uni'],                                                                                       request.form['city'],request.form['cont'],request.form['number'],request.form['type'])
        connection = dbapi2.connect(app.config['dsn'])
        cursor = connection.cursor()
        statement ="""SELECT loc_id FROM locations WHERE city='{}';""".format(request.form['city'])
        cursor.execute(statement)
        row = cursor.fetchone()
        if row is None:
            return None
        loca_id = row[0]
        statement = """UPDATE companies
                    SET title='{}', local2='{}', population='{}' WHERE id =                                                                     {};""".format(request.form['comp'],loca_id,request.form['number'],id)
        cursor.execute(statement)
        statement = """SELECT id, title, locations.city, locations.country, population FROM companies JOIN locations ON companies.local2         = locations.loc_id"""
        cursor.execute(statement)
        clist = cursor.fetchall()
        connection.commit()
        now = datetime.datetime.now()
        #return render_template('universities.html', UniversityList = ulist, InfoList=ilist, current_time=now.ctime())
        return redirect(url_for('company_page'))


Şirket Seçme
+++++++++++++++++++++

Arayüzde girilen belirli kriterlere göre şirket bilgilerini seçme işlemi yapmak için kullanılan kısımdır. Seçme işlemi için şehir yada şirket ismi kriter olarak kullanılabilir. Yapılan bu seçimlere göre tablolardan istenen kriterlere uyan şirketler çekilerek yeni bir sayfada listelenir. Bu işlemler için server.py'da yazılan kod şu şekildedir:

.. code-block:: python

	elif 'companies_to_select' in request.form:
        City=request.form['city']
        #l_id=fn.get_id("locations",City)
        connection = dbapi2.connect(app.config['dsn'])
        cursor = connection.cursor()
        statement = """SELECT loc_id FROM locations WHERE city='{}';""".format(City)
        cursor.execute(statement)
        row = cursor.fetchone()
        if row is None:
            now = datetime.datetime.now()
            return render_template('404.html', current_time = now.ctime())
        loca_id = row[0]
        statement = """SELECT id, title, locations.city, locations.country, population FROM companies JOIN locations ON companies.local2          = locations.loc_id WHERE local2 ={}""".format(loca_id)
        cursor.execute(statement)
        clist = cursor.fetchall()
        connection.commit()
        now = datetime.datetime.now()
        if clist is None:
            return render_template('404.html', current_time = now.ctime())
        return render_template('b_company.html', CompanyList = clist, current_time = now.ctime())
    elif 'companies_to_select2' in request.form:
        Title=request.form['title']
        #l_id=fn.get_id("locations",City)
        connection = dbapi2.connect(app.config['dsn'])
        cursor = connection.cursor()
        statement = """SELECT id, title, locations.city, locations.country, population FROM companies JOIN locations ON companies.local2         = locations.loc_id WHERE title ='{}'""".format(Title)
        cursor.execute(statement)
        clist = cursor.fetchall()
        connection.commit()
        now = datetime.datetime.now()
        if clist is None:
            return render_template('404.html', current_time = now.ctime())
        return render_template('b_company.html', CompanyList = clist, current_time = now.ctime())


Görüldüğü üzere öncelikle "Seç" butonuna basılması beklenir, iki farklı "Seç" butonu vardır. İlki olan "companies_to_select" butonuna basılırsa seçme için şehir kriterine bakılacağı anlamına gelir. Bu nedenle girilen şehir değeri kullanılarak buna uygun olan şirketler tablodan çekilerek, yeni bir sayfada listelenir. Eğer ikinci buton olan "companies_to_select2" kullanılırsa bu isme göre seçme yapılacağını gösterir ve girilen isim değeri kullanılarak işlem yapılır. Bulunan sonuçlar yeni bir ekranda listelenir.

Eğer yanlış değer girilirse hata sayfasına yönlendirilir.(404.html)


Hata Sayfası
+++++++++++++

Eğer kullanıcı seçme gibi işlemlerde yanlış yada sistemde olmayan veriler girerse "internal server error" hatası yerine bu hazırlanan sayfanın görünmesi sağlandı. Bunun için bu koşula uygun durumlar belirlenerek server.py dosyasında gerekli yerlerde yönlendirmeler yapıldı. Örnek kullanım yerleri aşağıda gösterilmiştir.

**Şirketler için:**

.. code-block:: python

	elif 'companies_to_select2' in request.form:
        Title=request.form['title']
        #l_id=fn.get_id("locations",City)
        connection = dbapi2.connect(app.config['dsn'])
        cursor = connection.cursor()
        statement = """SELECT id, title, locations.city, locations.country, population FROM companies JOIN locations ON companies.local2         = locations.loc_id WHERE title ='{}'""".format(Title)
        cursor.execute(statement)
        clist = cursor.fetchall()
        connection.commit()
        now = datetime.datetime.now()
        if clist is None:
            return render_template('404.html', current_time = now.ctime())
        return render_template('b_company.html', CompanyList = clist, current_time = now.ctime())


Yerler
-------------------

Yerler temsil etmek için sistemde "locations" tablosu gerçeklendi. Tablo "id", "city" ve "country" olmak üzere üç nitelikten oluşmaktadır. Bunlarda sırasıyla yerin numarası(birincil anahtar olarak kullanıldı.), şehir ve ülke bilgileri tutulmaktadır. Bu tablo site açıldığında aşağıdaki kod ile oluşturulup, ilk değerleri atanmaktadır. Başlangıç için Türkiye'deki 81 ilin hepsi plaka kodlarına göre eklenmiştir.


.. code-block:: python

        def locations(self):
        with dbapi2.connect(self.cp) as connection:
            cursor = connection.cursor()
            query = "DROP TABLE IF EXISTS locations CASCADE"
            cursor.execute(query)

            query = """CREATE TABLE locations (
                    loc_id INTEGER PRIMARY KEY,
                    city VARCHAR(40) NOT NULL,
                    country VARCHAR(40),
                    UNIQUE (loc_id),
                    UNIQUE (city)
                )"""
            cursor.execute(query)
            query = """INSERT INTO locations VALUES
              (1, 'Adana','Türkiye'),
              (2, 'Adıyaman', 'Türkiye'),
              (3, 'Afyon', 'Türkiye'),
              (4, 'Ağrı', 'Türkiye'),
              (5, 'Amasya', 'Türkiye'),
              (6, 'Ankara', 'Türkiye'),
              (7, 'Antalya', 'Türkiye'),
              (8, 'Artvin', 'Türkiye'),
              (9, 'Aydın', 'Türkiye'),
              (10, 'Balıkesir','Türkiye'),
              (11, 'Bilecik', 'Türkiye'),
              (12, 'Bingöl', 'Türkiye'),
              (13, 'Bitlis', 'Türkiye'),
              (14, 'Bolu', 'Türkiye'),
              (15, 'Burdur', 'Türkiye'),
              (16, 'Bursa', 'Türkiye'),
              (17, 'Çanakkale', 'Türkiye'),
              (18, 'Çankırı', 'Türkiye'),
              (19, 'Çorum', 'Türkiye'),
              (20, 'Denizli', 'Türkiye'),
              (21, 'Diyarbakır','Türkiye'),
              (22, 'Edirne', 'Türkiye'),
              (23, 'Elazığ', 'Türkiye'),
              (24, 'Erzincan', 'Türkiye'),
              (25, 'Erzurum', 'Türkiye'),
              (26, 'Eskişehir', 'Türkiye'),
              (27, 'Gaziantep', 'Türkiye'),
              (28, 'Giresun', 'Türkiye'),
              (29, 'Gümüşhane', 'Türkiye'),
              (30, 'Hakkari', 'Türkiye'),
              (31, 'Hatay', 'Türkiye'),
              (32, 'Isparta', 'Türkiye'),
              (33, 'Mersin', 'Türkiye'),
              (34, 'İstanbul', 'Türkiye'),
              (35, 'İzmir', 'Türkiye'),
              (36, 'Kars', 'Türkiye'),
              (37, 'Kastamonu', 'Türkiye'),
              (38, 'Kayseri', 'Türkiye'),
              (39, 'Kırklareli','Türkiye'),
              (40, 'Kırşehir', 'Türkiye'),
              (41, 'Kocaeli', 'Türkiye'),
              (42, 'Konya', 'Türkiye'),
              (43, 'Kütahya', 'Türkiye'),
              (44, 'Malatya', 'Türkiye'),
              (45, 'Manisa', 'Türkiye'),
              (46, 'Kahramanmaraş', 'Türkiye'),
              (47, 'Mardin', 'Türkiye'),
              (48, 'Muğla','Türkiye'),
              (49, 'Muş', 'Türkiye'),
              (50, 'Nevşehir', 'Türkiye'),
              (51, 'Niğde', 'Türkiye'),
              (52, 'Ordu', 'Türkiye'),
              (53, 'Rize', 'Türkiye'),
              (54, 'Sakarya', 'Türkiye'),
              (55, 'Samsun', 'Türkiye'),
              (56, 'Siirt', 'Türkiye'),
              (57, 'Sinop','Türkiye'),
              (58, 'Sivas', 'Türkiye'),
              (59, 'Tekirdağ', 'Türkiye'),
              (60, 'Tokat', 'Türkiye'),
              (61, 'Trabzon', 'Türkiye'),
              (62, 'Tunceli', 'Türkiye'),
              (63, 'Şanlıurfa', 'Türkiye'),
              (64, 'Uşak', 'Türkiye'),
              (65, 'Van', 'Türkiye'),
              (66, 'Yozgat', 'Türkiye'),
              (67, 'Zonguldak', 'Türkiye'),
              (68, 'Aksaray', 'Türkiye'),
              (69, 'Bayburt', 'Türkiye'),
              (70, 'Karaman', 'Türkiye'),
              (71, 'Kırıkkale', 'Türkiye'),
              (72, 'Batman', 'Türkiye'),
              (73, 'Şırnak', 'Türkiye'),
              (74, 'Bartın', 'Türkiye'),
              (75, 'Ardahan', 'Türkiye'),
              (76, 'Iğdır', 'Türkiye'),
              (77, 'Yalova','Türkiye'),
              (78, 'Karabük', 'Türkiye'),
              (79, 'Kilis', 'Türkiye'),
              (80, 'Osmaniye', 'Türkiye'),
              (81, 'Düzce', 'Türkiye');
            """
            cursor.execute(query)
            connection.commit()



Yerler Sınıfının Yapısı ve Kurucu Fonksiyonu
++++++++++++++++++++++++++++++++++++++++++++++

Yerleri temsil etmek için oluşturulan sınıfın yapısı elemanları ve kurucu fonksiyonu aşağıdaki gibidir.

.. code-block:: python

	class Location:
    def __init__(self, loc_id, city, country):
        self.Loc_id = loc_id
        self.City = city
        self.Country = country

Yerler İçin Yazılan Fonksiyonlar
+++++++++++++++++++++++++++++++++++++++
 
Bu varlığın tablolarına ekleme, silme, güncelleme ve seçme işlemlerinin yapılabilmesi için gerekli olan kodlar projede "locations.py" dosyasının altındadır.

Yer Ekleme
+++++++++++++++++

Sitenin arayüzünden girilen bilgileri kullanarak "locations" tablosuna yeni yerin numara, şehir ve ülke gibi ilgili bilgileri ekler. Bu şekilde yeni bir yer eklenmiş olur. Bu işlem yazılan kod aşağıdaki gibidir.  

.. code-block:: python

	 def add_location(self, id, city, country):
        with dbapi2.connect(self.cp) as connection:
            cursor = connection.cursor()
            query =  "INSERT INTO locations (loc_id,city,country) VALUES ('%s','%s','%s')" % (id,city,country)
            cursor.execute(query)
            connection.commit()
            return

Bu ekleme fonksiyonu server.py'daki yerler ile ilgili olan kısımda ekleme işlemi yapılacağı zaman kullanılır. 


Yer Silme
++++++++++++++++

Bu tablo diğer tablolarla bağlantılı olduğu(dış anahtar ve restrict özellikten dolayı) ve bu yerlerin sistemden silinmemesi istendiği için arayüzde bu işlem yapılamamaktadır. Ancak yinede gerekli durumlarda kullanılabilir düşüncesiyle bu işlem içinde kod yazılmıştır.
Bu koda göre id değerine göre silme işlemi yapılır.

.. code-block:: python

	def delete_location(self, id):
        with dbapi2.connect(self.cp) as connection:
            cursor = connection.cursor()
            query = "DELETE FROM locations WHERE loc_id = '%s'" % (id)
            cursor.execute(query)
            connection.commit()
            return


Yer Güncelle
+++++++++++++++++++++

Bu tablo diğer tablolarla bağlantılı olduğu(dış anahtar ve restrict özellikten dolayı)için arayüzde bu işlem yapılamamaktadır. Ancak yinede gerekli durumlarda kullanılabilir düşüncesiyle bu işlem içinde kod yazılmıştır.


.. code-block:: python

		def update_location(self, id, city, country):
        with dbapi2.connect(self.cp) as connection:
            cursor = connection.cursor()
            query = "UPDATE locations SET loc_id= '%s', city= '%s', country='%s' WHERE id = '%d'" % (id,city,country,id)
            cursor.execute(query)
            connection.commit()
            return



Yer Seçme
+++++++++++++++++++++

Arayüzde tüm yerleri listelemek için kullanılmıştır. Kodu aşağıdaki gibidir.

.. code-block:: python

	def get_locationlist(self):
        with dbapi2.connect(self.cp) as connection:
            cursor = connection.cursor()
            query = "SELECT loc_id, city, country FROM locations"
            cursor.execute(query)
            rows = cursor.fetchall()
            return rows


Hata Sayfası
+++++++++++++

Eğer kullanıcı seçme gibi işlemlerde yanlış yada sistemde olmayan veriler girerse "internal server error" hatası yerine bu hazırlanan sayfanın görünmesi sağlandı. Bunun için bu koşula uygun durumlar belirlenerek server.py dosyasında gerekli yerlerde yönlendirmeler yapıldı. Örnek kullanım yerleri aşağıda gösterilmiştir.

**Şirketler için:**

.. code-block:: python

	elif 'companies_to_select2' in request.form:
        Title=request.form['title']
        #l_id=fn.get_id("locations",City)
        connection = dbapi2.connect(app.config['dsn'])
        cursor = connection.cursor()
        statement = """SELECT id, title, locations.city, locations.country, population FROM companies JOIN locations ON companies.local2         = locations.loc_id WHERE title ='{}'""".format(Title)
        cursor.execute(statement)
        clist = cursor.fetchall()
        connection.commit()
        now = datetime.datetime.now()
        if clist is None:
            return render_template('404.html', current_time = now.ctime())
        return render_template('b_company.html', CompanyList = clist, current_time = now.ctime())




