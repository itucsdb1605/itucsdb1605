Hasan Hüseyin ÇAĞLAR Tarafından Yapılan Bölümler
=======================

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
           
articles, connections ve events tablolarının hepsi bu tanım metodu içinde oluşturulmuştur.

.. figure:: pictures/tables.png
    :figclass: align-center
    
    Tablo Diyagramları

Makaleler
--------------
Makaleler tablosu articles adıyla oluşturuldu. articles ikisi üniversities ve users tablosunu referans veren sütun, biri birincil anahtar olmak üzere toplamda 6 sütundan oluşur. Makaleler bir üniversiteye bağlı mail adresi olan bir kullanıcının beli bir yılda belli bir isimde çıkardığı makaleleri tutar.

.. code-block:: python

            query = """CREATE TABLE articles (
                    ArticleId SERIAL PRIMARY KEY,
                    ArticleName VARCHAR(400) UNIQUE NOT NULL,
                    UserId INTEGER NOT NULL REFERENCES users(UserId),
                    ReleaseYear SMALLINT NOT NULL,
                    Mail VARCHAR(100) NOT NULL,
                    uni_id INTEGER NOT NULL REFERENCES universities(id)
                    )"""
            cursor.execute(query)
            
İlk kayıtlar ekrandaki işlemleri kolaylaştırması amacıyla articles tablosuna eklendi.

.. code-block:: python

            query = """INSERT INTO articles(ArticleName, UserId,ReleaseYear, Mail, uni_id) VALUES
              ('Efficient algorithms for the (weighted) minimum circle problem',5,1982,'Hearn@ise.ufl.edu',5),
              ('3-D Mesh Geometry Compression with Set Partitioning in the Spectral Domain',6,2011,'ulugbayazit@itu.edu.tr',15),
              ('The minimum covering sphere problem',5,1972,'Hearn@ise.ufl.edu',5),
              ('Otonom araçların geleceği',7,2015,'gulerfa@itu.edu.tr',3);
              """
            cursor.execute(query)

articles.py dosyasında arayüzde yapılacak işlemler için gerekli sorgu metodları yazıldı; sırasıyla  tüm makale listesini çekme, referans verilen üniversite ve kullanıcı verilerini çekmek, makale silmek, güncellenecek veri için kullanılan tekli makale seçimi, makale ekleme ve makale güncelleme için yazıldı.

.. code-block:: python

      def get_articlelist(self):
        with dbapi2.connect(self.cp) as connection:
            cursor = connection.cursor()
            query = """SELECT articles.ArticleId, articles.ArticleName,
             articles.UserId, users.FirstName AS Name, users.LastName AS SurName,
             articles.ReleaseYear, articles.Mail, universities.title 
             FROM articles LEFT JOIN universities ON articles.uni_id = universities.id
             LEFT JOIN users ON users.UserId=articles.UserId ORDER BY articles.ArticleName ASC """
            cursor.execute(query)
            rows = cursor.fetchall()
            return rows
        
    def get_universitylist(self):
        with dbapi2.connect(self.cp) as connection:
            cursor = connection.cursor()
            query = "SELECT * FROM universities ORDER BY title ASC"
            cursor.execute(query)
            rows = cursor.fetchall()
            return rows
        
    def get_userlist(self):
        with dbapi2.connect(self.cp) as connection:
            cursor = connection.cursor()
            query = "SELECT UserId, concat(FirstName::text, LastName::text) AS name FROM users ORDER BY FirstName ASC"
            cursor.execute(query)
            rows = cursor.fetchall()
            return rows
    def delete_article(self, ArticleId):
        with dbapi2.connect(self.cp) as connection:
            cursor = connection.cursor()
            query = "DELETE FROM articles WHERE ArticleId = '%s'" % (ArticleId)
            cursor.execute(query)
            connection.commit()
            return
    def select_article(self, ArticleId):
        with dbapi2.connect(self.cp) as connection:
            cursor = connection.cursor()
            query = """SELECT articles.ArticleId, articles.ArticleName, articles.UserId,
             users.FirstName AS Name, users.lastName AS SurName, articles.ReleaseYear, articles.Mail, articles.uni_id  
             FROM articles
             LEFT JOIN users ON users.UserId=articles.UserId
             WHERE ArticleId = '%s' ORDER BY ArticleId ASC""" % (ArticleId)
            cursor.execute(query)
            rows=cursor.fetchall()
            return rows
    def add_article(self, ArticleName, UserId,ReleaseYear, Mail,uni_id):
        with dbapi2.connect(self.cp) as connection:
            cursor = connection.cursor()
            query =  """INSERT INTO articles (ArticleName, UserId, ReleaseYear,
             Mail, uni_id) VALUES ('%s','%s','%s','%s','%s')""" % (ArticleName, UserId,ReleaseYear, Mail, uni_id)
            cursor.execute(query)
            connection.commit()
            return

    def update_article(self, ArticleId, ArticleName, UserId, ReleaseYear, Mail,uni_id):
        with dbapi2.connect(self.cp) as connection:
            cursor = connection.cursor()
            query =  """UPDATE articles SET ArticleName = '%s', UserId='%s',
            ReleaseYear='%s', Mail='%s', uni_id='%s' WHERE ArticleId='%s'""" % (ArticleName, UserId,ReleaseYear, Mail, uni_id, ArticleId)
            cursor.execute(query)
            connection.commit()
            return

Yukarıdaki metotlar **server.py** dosyasında articles'a bağlı metotlar tarafından **articles.html**'de gerekli işlemleri sağlayabilmesi amacıyla kullanılıyor. Örneğin articles.html'içindeki değişkenler, listeler bu şekilde belirleniyor. articles.html de dış anahtar ile referans verilen tablo verilerini checkbox'lara eklemek için user ve universities listeleri kullanıldı. Diğer metotlar klasik CRUD işlemlerini gerçekleştirmek için kullanıldı. **server.py**'ın **articles_page** metodu, **articles.html** ekranının ne şekilde hangi verilerle açılacağını kontrol eder.

.. code-block:: python

      def articles_page():
    arts = Articles(app.config['dsn'])
    fn = Func(app.config['dsn'])
    if request.method == 'GET':
        now = datetime.datetime.now()
        article = arts.get_articlelist()
        article[0]=list(article[0])
        article[0][0]="kayıt seçiniz"
        article[0][1]="kayıt seçiniz"
        article[0][2]="kayıt seçiniz"
        article[0][3]="kayıt seçiniz"
        article[0][4]="kayıt seçiniz"
        article[0][5]="kayıt seçiniz"
        article[0][6]="kayıt seçiniz"
        article[0][7]="kayıt seçiniz"
        article[0]=tuple(article[0])
        alist = arts.get_articlelist()
        unilist=arts.get_universitylist()
        userlist=arts.get_userlist()
        return render_template('articles.html', ArticleList = alist, UniversityList=unilist, UserList=userlist, article= article, current_time = now.ctime())
    elif 'articles_to_delete' in request.form:
        articleids = request.form.getlist('articles_to_delete')
        for ArticleId in articleids:
            arts.delete_article(ArticleId)
        return redirect(url_for('articles_page'))
    elif 'select_record' in request.form:
        articleids = request.form.getlist('select_record')
        now = datetime.datetime.now()
        alist = arts.get_articlelist()
        unilist=arts.get_universitylist()
        userlist=arts.get_userlist()
        slist=arts.select_article(articleids[0])
        return render_template('articles.html', ArticleList = alist, UniversityList=unilist, UserList=userlist, article=slist, current_time=now.ctime())
    elif 'articles_to_add' in request.form:
        arts.add_article(request.form['ArticleName'],request.form['UserId'],request.form['ReleaseYear'],request.form['Mail'],request.form['uni_id'])
        return redirect(url_for('articles_page'))
    elif 'articles_to_update' in request.form:
        arts.update_article(request.form['ArticleId'], request.form['ArticleName'],request.form['UserId'],request.form['ReleaseYear'],request.form['Mail'],request.form['uni_id'])
        return redirect(url_for('articles_page'))


Metotlar aracılığıyla veri ve iş akışını şöyle sıralayabiliriz : init.py -> articles.py -> server.py -> articles.html

**articles.html** dosyasında accordion button tasarımını gerçekleyen javascript kod parçası kullanıldı. Ekranlarda kullanılan bu buton yapısına göre ilgili alan butonuna tıklayınca alt bölmenin açılması, aynı yere tıklayınca ya da başka bir alanın tıklanarak aktif edilmesiylede eski alanın kapatılması html dosyası içinde bu kod yapısıyla sağlanıyor.

.. code-block:: javascript

      <script>
      var acc = document.getElementsByClassName("accordion");
      for (i = 0; i < acc.length; i++) {
        acc[i].onclick = function(){
        var active = document.querySelector(".accordion.active");
    if (active && active != this) {
      active.classList.remove("active");
      active.nextElementSibling.classList.remove("show");
    }
    this.classList.toggle("active");
    this.nextElementSibling.classList.toggle("show"); }}</script>

Bağlantılar
--------------
Bağlantılar tablosu connections adıyla oluşturuldu. connections ikisi users tablosunu referans veren sütun, biri birincil anahtar olmak üzere toplamda 3 sütundan oluşur. Bağlantılar tablosu bir kullanıcıyla o kullanıcının kendisine arkadaş olarak bağlantı kurduğu kişileri tutar.

.. code-block:: python

            query = """CREATE TABLE connections (
                    ConnectionId SERIAL PRIMARY KEY,
                    MainUserId INT NOT NULL REFERENCES users(UserId),
                    FriendUserId INT NOT NULL REFERENCES users(UserId)
                    )"""
            cursor.execute(query)

İlk kayıtlar ekrandaki işlemleri kolaylaştırması amacıyla connections tablosuna eklendi.

.. code-block:: python

            query = """INSERT INTO connections(MainUserId, FriendUserId) VALUES
              (1,2),
              (1,3),
              (2,3),
              (4,5),
              (4,2),
              (2,5),
              (6,7),
              (3,5);
              """
            cursor.execute(query)
            
**myconnections.py** dosyasında arayüzde yapılacak işlemler için gerekli sorgu metodları yazıldı; tüm baağlantılar listesi, kullanıcı bazında bağlantılar listesi, seçili üniversite bazında bağlantılar listesi, tüm üniversiteler bazında bağlantı listesi, kullanıcı listesi, üniversite listesi,silme ve ekleme amaçları için kullanıldı.

.. code-block:: python

    def get_connectionlist(self):
        with dbapi2.connect(self.cp) as connection:
            cursor = connection.cursor()
            query = """SELECT connections.ConnectionId, u1.FirstName AS Mfname, u1.LastName AS Mlname,
             u2.FirstName AS Ffname, u2.LastName AS Flname 
             FROM connections 
             LEFT JOIN users u1 ON connections.MainUserId = u1.UserId 
             LEFT JOIN users u2 ON connections.FriendUserId = u2.UserId"""
            cursor.execute(query)
            rows = cursor.fetchall()
            return rows
        
    def get_connectionlistbyuser(self,byUserId):
        with dbapi2.connect(self.cp) as connection:
            cursor = connection.cursor()
            query = """SELECT connections.ConnectionId, u1.FirstName AS Mfname, u1.LastName AS Mlname,
             u2.FirstName AS Ffname, u2.LastName AS Flname 
             FROM connections 
             LEFT JOIN users u1 ON connections.MainUserId = u1.UserId 
             LEFT JOIN users u2 ON connections.FriendUserId = u2.UserId
             WHERE connections.MainUserId='%s'""" %(byUserId)
            cursor.execute(query)
            rows = cursor.fetchall()
            return rows
        
    def get_connectionlistbyuniversity(self,byUniversityId):
        with dbapi2.connect(self.cp) as connection:
            cursor = connection.cursor()
            query = """SELECT  users.uni, users.FirstName, users.LastName
             FROM users 
             LEFT JOIN universities ON universities.title = users.uni 
             WHERE universities.id='%s'""" %(byUniversityId)
            cursor.execute(query)
            rows = cursor.fetchall()
            return rows
        
    def get_universityconnectionlist(self):
        with dbapi2.connect(self.cp) as connection:
            cursor = connection.cursor()
            query = """SELECT  users.uni, users.FirstName, users.LastName
             FROM users """ 
            cursor.execute(query)
            rows = cursor.fetchall()
            return rows
    def get_userlist(self):
        with dbapi2.connect(self.cp) as connection:
            cursor = connection.cursor()
            query = "SELECT UserId, concat(FirstName::text, LastName::text) AS name FROM users ORDER BY FirstName ASC"
            cursor.execute(query)
            rows = cursor.fetchall()
            return rows
        
    def get_universitylist(self):
        with dbapi2.connect(self.cp) as connection:
            cursor = connection.cursor()
            query = "SELECT * FROM universities ORDER BY title ASC"
            cursor.execute(query)
            rows = cursor.fetchall()
            return rows
        
    def delete_connection(self, ConnectionId):
        with dbapi2.connect(self.cp) as connection:
            cursor = connection.cursor()
            query = "DELETE FROM connections WHERE ConnectionId = '%s'" % (ConnectionId)
            cursor.execute(query)
            connection.commit()
            return
    def add_connection(self, MainUserId, FriendUserId):
        with dbapi2.connect(self.cp) as connection:
            cursor = connection.cursor()
            query =  "INSERT INTO connections (MainUserId, FriendUserId) VALUES ('%s','%s')" % (MainUserId, FriendUserId)
            cursor.execute(query)
            connection.commit()
            return

Yukarıdaki metotlar **server.py** dosyasında connections'a bağlı metotlar tarafından **connectionss.html**'de gerekli işlemleri sağlayabilmesi amacıyla kullanılıyor. Örneğin **connections.html**'içindeki değişkenler, listeler bu şekilde belirleniyor. connections.html de dış anahtar ile referans verilen tablo verilerini checkboxlar'a eklemek için users tablosundan türetilen listeler kullanıldı. Diğer metotlar klasik CRUD işlemlerini gerçekleştirmek için kullanıldı(Güncelleme Hariç). **server.py**'nin **connections_page** metodu **connections.html** ekranının ne şekilde hangi verilerle açılacağını kontrol eder.

.. code-block:: python
      def connections_page():
    cons = Myconnections(app.config['dsn'])
    fn = Func(app.config['dsn'])
    if request.method == 'GET':
        now = datetime.datetime.now()
        connectionlist = cons.get_connectionlist()
        userlist=cons.get_userlist()
        universitylist=cons.get_universitylist()
        connectionlistbyuniversity=cons.get_universityconnectionlist()
        return render_template('connections.html', ConnectionList = connectionlist,
                                UserList=userlist, UniversityList=universitylist,
                                UniversityConnectionList=connectionlistbyuniversity, current_time = now.ctime())
    elif 'selectByUser' in request.form:
        temp=request.form.getlist('selectByUser')
        now = datetime.datetime.now()
        connectionlist = cons.get_connectionlistbyuser(temp[0])
        userlist=cons.get_userlist()
        universitylist=cons.get_universitylist()
        connectionlistbyuniversity=cons.get_universityconnectionlist()
        return render_template('connections.html', ConnectionList = connectionlist,
                                UserList=userlist, UniversityList=universitylist,
                                UniversityConnectionList=connectionlistbyuniversity, current_time = now.ctime())
    elif 'selectByUniversity' in request.form:
        temp=request.form.getlist('selectByUniversity')
        now = datetime.datetime.now()
        connectionlist = cons.get_connectionlist()
        userlist=cons.get_userlist()
        universitylist=cons.get_universitylist()
        connectionlistbyuniversity=cons.get_connectionlistbyuniversity(temp[0])
        return render_template('connections.html', ConnectionList = connectionlist,
                                UserList=userlist, UniversityList=universitylist,
                                UniversityConnectionList=connectionlistbyuniversity, current_time = now.ctime())
    elif 'Delete' in request.form:
        connectionids = request.form.getlist('DeletedConnections')
        for ConnectionId in connectionids:
            cons.delete_connection(ConnectionId)
        return redirect(url_for('connections_page'))
    elif 'Connect' in request.form:
        cons.add_connection(request.form['User'],request.form['Connection'])
        return redirect(url_for('connections_page'))

Metotlar aracılığıyla veri ve iş akışını şöyle sıralayabiliriz : init.py -> myconnections.py -> server.py -> connections.html

**connections.html** dosyasında da articles gibi accordion button tasarımını gerçekleyen javascript kod parçası kullanıldı. Ekranlarda kullanılan bu buton yapısına göre ilgili alan butonuna tıklayınca alt bölmenin açılması, aynı yere tıklayınca ya da başka bir alanın tıklanarak aktif edilmesiylede eski alanın kapatılması html dosyası içinde bu kod yapısıyla sağlanıyor.

.. code-block:: javascript

      <script>
      var acc = document.getElementsByClassName("accordion");
      for (i = 0; i < acc.length; i++) {
        acc[i].onclick = function(){
        var active = document.querySelector(".accordion.active");
    if (active && active != this) {
      active.classList.remove("active");
      active.nextElementSibling.classList.remove("show");
    }
    this.classList.toggle("active");
    this.nextElementSibling.classList.toggle("show"); }}</script>

Etkinlikler
--------------
Etkinlikler tablosu events adıyla oluşturuldu. events ikisi locations ve  users tablolarını referans veren sütunlar, biri birincil anahtar olmak üzere toplamda 6 sütundan oluşur. Etkinlikler tablosu bir kullanıcının bir yerde belli bir tarihte belli bir isimle ve belli detaylarla oluşturduğu etkinlik verilerini tutar.

.. code-block:: python

            query = """CREATE TABLE events (
                    EventId SERIAL PRIMARY KEY,
                    EventName VARCHAR(300) UNIQUE NOT NULL,
                    OwnerId INTEGER NOT NULL REFERENCES users(UserId),
                    CityId INTEGER NOT NULL REFERENCES locations(loc_id),
                    DateWithTime VARCHAR(50) NOT NULL,
                    Detail VARCHAR(500) NOT NULL
                    )"""
            cursor.execute(query)

İlk kayıtlar ekrandaki işlemleri kolaylaştırması amacıyla events tablosuna eklendi.

.. code-block:: python

            query = """INSERT INTO events(EventName, OwnerId, CityId, DateWithTime, Detail) VALUES
              ('İTÜ Arı-Çekirdek Proje Yarışması',4,34,'20.12.2016, 13:30','2016 yılı proje yarışması sonuçları, İTÜ Ayazağa'),
              ('Medikal alanda Görüntü İşleme Konferansı',2,34,'01.01.2017, 16:00','Bilgisayarla görüntü işlemenin sağlık alanında uygulamaları, Sabancı Üniversitesi Merkez Kampüsü');
              """
            cursor.execute(query)
            
**myevents.py** dosyasında arayüzde yapılacak işlemler için gerekli sorgu metodları yazıldı; sırasıyla tüm etkinlik listesini çekme, referans verilen yerler ve kullanıcı verilerini çekmek, etkinlik silmek, güncellenecek veri için kullanılan tekli etkinlik seçimi, etkinlik ekleme ve etkinlik güncelleme için yazıldı.

.. code-block:: python

    def get_eventlist(self):
        with dbapi2.connect(self.cp) as connection:
            cursor = connection.cursor()
            query = """SELECT events.EventId, events.EventName, users.FirstName, users.LastName,
            locations.city, events.DateWithTime, events.Detail
            FROM events
            LEFT JOIN users ON events.OwnerId = users.UserId 
            LEFT JOIN locations ON events.CityId = locations.loc_id """
            cursor.execute(query)
            rows = cursor.fetchall()
            return rows
        
    def get_locationlist(self):
        with dbapi2.connect(self.cp) as connection:
            cursor = connection.cursor()
            query = "SELECT loc_id, city FROM locations"
            cursor.execute(query)
            rows = cursor.fetchall()
            return rows
    def get_userlist(self):
        with dbapi2.connect(self.cp) as connection:
            cursor = connection.cursor()
            query = "SELECT UserId, concat(FirstName::text, LastName::text) AS name FROM users ORDER BY FirstName ASC"
            cursor.execute(query)
            rows = cursor.fetchall()
            return rows
    def delete_event(self, EventId):
        with dbapi2.connect(self.cp) as connection:
            cursor = connection.cursor()
            query = "DELETE FROM events WHERE EventId = '%s'" % (EventId)
            cursor.execute(query)
            connection.commit()
            return
    def select_event(self, EventId):
        with dbapi2.connect(self.cp) as connection:
            cursor = connection.cursor()
            query = """SELECT events.EventId, events.EventName, users.FirstName, users.LastName,
             locations.city, events.DateWithTime, events.Detail 
             FROM events
             LEFT JOIN users ON events.OwnerId = users.UserId 
             LEFT JOIN locations ON events.CityId = locations.loc_id 
             WHERE EventId = '%s' ORDER BY EventId ASC
             """ % (EventId)
            cursor.execute(query)
            rows=cursor.fetchall()
            return rows
    def add_event(self, EventName, OwnerId, CityId, DateWithTime, Detail):
        with dbapi2.connect(self.cp) as connection:
            cursor = connection.cursor()
            query =  "INSERT INTO events (EventName, OwnerId, CityId, DateWithTime, Detail) VALUES ('%s','%s','%s','%s','%s')" % (EventName, OwnerId, CityId, DateWithTime, Detail)
            cursor.execute(query)
            connection.commit()
            return

    def update_event(self, EventId, EventName, OwnerId, CityId, DateWithTime, Detail):
        with dbapi2.connect(self.cp) as connection:
            cursor = connection.cursor()
            query =  "UPDATE events SET EventName = '%s', OwnerId='%s', CityId='%s', DateWithTime='%s', Detail='%s'WHERE EventId='%s'" % (EventName, OwnerId, CityId, DateWithTime, Detail,EventId)
            cursor.execute(query)
            connection.commit()
            return
            
Yukarıdaki metotlar **server.py** dosyasında events'a bağlı metotlar tarafından **events.html**'de gerekli işlemleri sağlayabilmesi amacıyla kullanılıyor. Örneğin events.html'içindeki değişkenler, listeler bu şekilde belirleniyor. **events.html** de dış anahtar ile referans verilen tablo verilerini checkbox'a eklemek için users ve locations tablosundan oluşturulan listeler kullanıldı. Diğer metotlar klasik CRUD işlemlerini gerçekleştirmek için kullanıldı. **server.py**'nin **events_page()** metodu **events.html** ekranının ne şekilde hangi verilerle açılacağını kontrol eder.

.. code-block:: python

      def events_page():
    evts = Myevents(app.config['dsn'])
    fn = Func(app.config['dsn'])
    if request.method == 'GET':
        now = datetime.datetime.now()
        event = evts.get_eventlist()
        event[0]=list(event[0])
        event[0][0]="kayıt seçiniz"
        event[0][1]="kayıt seçiniz"
        event[0][2]="kayıt seçiniz"
        event[0][3]="kayıt seçiniz"
        event[0][4]="kayıt seçiniz"
        event[0][5]="kayıt seçiniz"
        event[0][6]="kayıt seçiniz"
        event[0]=tuple(event[0])
        eventlist = evts.get_eventlist()
        locationlist=evts.get_locationlist()
        userlist=evts.get_userlist()
        return render_template('events.html', EventList = eventlist, LocationList=locationlist, UserList=userlist, event = event, current_time = now.ctime())
    elif 'events_to_delete' in request.form:
        eventids = request.form.getlist('events_to_delete')
        for EventId in eventids:
            evts.delete_event(EventId)
        return redirect(url_for('events_page'))
    elif 'select_record' in request.form:
        eventids = request.form.getlist('select_record')
        now = datetime.datetime.now()
        eventlist = evts.get_eventlist()
        userlist=evts.get_userlist()
        locationlist=evts.get_locationlist()
        slist=evts.select_event(eventids[0])
        return render_template('events.html', EventList = eventlist, LocationList=locationlist, UserList=userlist, event=slist, current_time=now.ctime())
    elif 'events_to_add' in request.form:
        evts.add_event(request.form['EventName'],request.form['OwnerId'],request.form['CityId'],request.form['DateWithTime'],request.form['Detail'])
        return redirect(url_for('events_page'))
    elif 'events_to_update' in request.form:
        evts.update_event(request.form['EventId'],request.form['EventName'],request.form['OwnerId'],request.form['CityId'],request.form['DateWithTime'],request.form['Detail'])
        return redirect(url_for('events_page'))
   
Metotlar aracılığıyla veri ve iş akışını şöyle sıralayabiliriz : init.py -> myevents.py -> server.py -> events.html

**events.html** dosyasında da articles ve connections gibi accordion button tasarımını gerçekleyen javascript kod parçası kullanıldı. Ekranlarda kullanılan bu buton yapısına göre ilgili alan butonuna tıklayınca alt bölmenin açılması, aynı yere tıklayınca ya da başka bir alanın tıklanarak aktif edilmesiylede eski alanın kapatılması html dosyası içinde bu kod yapısıyla sağlanıyor.

.. code-block:: javascript

      <script>
      var acc = document.getElementsByClassName("accordion");
      for (i = 0; i < acc.length; i++) {
        acc[i].onclick = function(){
        var active = document.querySelector(".accordion.active");
    if (active && active != this) {
      active.classList.remove("active");
      active.nextElementSibling.classList.remove("show");
    }
    this.classList.toggle("active");
    this.nextElementSibling.classList.toggle("show"); }}</script>
