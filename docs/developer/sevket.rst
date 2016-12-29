Şevket Cerit Tarafından Yapılan Kısımlar
================================

Kullanıcılar Tablosu
-------------------------

Kullanıcıları temsil etmek icin "users" tablosu oluşturuldu.Users tablosu "userId" birincil anahtar ve serial olarak tanımlandı. "Firstname" kullanıcının ismi ,"Lastname" kullanıcının soyismi ,"Email_adress" kullanıcının mail adresi ,"password" kullanıcının siteye giriş yapmak için kullanacağı şifresi ve universities tablosuna dış anahtar olan "uni" niteliklerine sahiptir.


.. code-block:: python

    def users(self):
        with dbapi2.connect(self.cp) as connection:
            cursor = connection.cursor()
            query = "DROP TABLE IF EXISTS users CASCADE"
            cursor.execute(query)
            query = """CREATE TABLE users (
                uni VARCHAR (100) NOT NULL REFERENCES universities(title)
                ON DELETE CASCADE
                ON UPDATE CASCADE,
                UserId SERIAL PRIMARY KEY,
                Firstname VARCHAR (80) NOT NULL,
                Lastname VARCHAR (80) NOT NULL ,
                Email_adress VARCHAR (100) NOT NULL UNIQUE,
                password VARCHAR(10) NOT NULL
            )"""
            cursor.execute(query)
            query = """INSERT INTO users(Firstname, Lastname, Email_adress,uni,password) VALUES
              ('Sevket','Cerit','cerits@itu.er','Ankara Üniversitesi','sevko'),
              ('Mert','Yıldız','yildiz@itu.edr','İstanbul Üniversitesi','mert'),
              ('Halit','Ugurgelen','ugurgelen@itu.edu.tr','Boğaziçi Üniversitesi','halit'),
              ('Hasan','Caglar','caglarh@itu.edu','İstanbul Teknik Üniversitesi','hhc'),
              ('Donald','Hearn','Hearn@ise.ufl.edu','Boğaziçi Üniversitesi','hearn'),
              ('Ulug','Bayazit','ulugbayazit@itu.edu.tr','İstanbul Teknik Üniversitesi','ulug'),
              ('Fatih','Guler','gulerfa','İstanbul Teknik Üniversitesi','feg');
              """
            cursor.execute(query)
            connection.commit()
            
Kullanıcı Girişi
-------------------------

Kullanıcıların sayfaya girişi için mail adresleri ve şifreleri veritabanında kontrol edildi.Eşleşme sağlanırsa sitenin anasayfasına yönlendirildi.

.. code-block:: python

  @app.route('/home', methods = ['POST', 'GET'])
  def page_login():
    with dbapi2.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()
        if request.method == 'POST':
            mailentered = request.form['mail']
            passentered = request.form['password']
            query = """SELECT Firstname,Lastname,Email_adress FROM users WHERE Email_adress='%s' AND password='%s' """ % (mailentered, passentered)
            cursor.execute(query)
            global allusers
            allusers = cursor.fetchall()
            x = len(allusers)
            if x == 1:

                return render_template('home.html')
            else:
                return render_template('signup.html')
        elif request.method == 'GET':
            return render_template('signup.html')

Kullanıcı Kayıt
-------------------------

Siteye kayıt olmak isteyen kullanıcılar email,ad,soyad,üniversite ve şifre formlarını doldurarak kayıt olur.Girilen bilgiler veritabanına kaydedilir.Kayıt işleminden sonra giriş sayfasına yönlendirilir.

.. code-block:: python

  @app.route('/user_add', methods=['GET', 'POST'])
  def user_add():
    user = users(app.config['dsn'])
    if request.method == 'GET':
        now = datetime.datetime.now()
        return render_template('signup.html', current_time=now.ctime())
    if request.method == 'POST':
        user.set_mail(request.form['email'])
        user.set_name(request.form['firstname'])
        user.set_lastname(request.form['lastname'])
        user.set_uni(request.form['uni'])
        user.set_password(request.form['password'])
        user.add_user()
        now = datetime.datetime.now()
        return redirect(url_for('page_login'))

Kullanıcı Profil
-------------------------

Kullanıcı profil sayfasında bilgilerini güncelleyebilir.Formda yer alan mail bilgisi veritabanında kontrol edilir ve eşlesen kullanıcının yeni girilen bilgileri veritabanına kaydedilir.

.. code-block:: python

  @app.route('/user_update', methods=['GET', 'POST'])
  def user_update():
    user = users(app.config['dsn'])
    if request.method == 'GET':
        now = datetime.datetime.now()
        return render_template('signup.html', current_time=now.ctime())
    if request.method == 'POST':
        name = request.form['firstname']
        mail = request.form['email']
        uni = request.form['uni']
        connection = dbapi2.connect(app.config['dsn'])
        cursor = connection.cursor()
        statement = """UPDATE users
                    SET  Firstname='%s',uni='%s'
                    WHERE Email_adress='%s'""" % (name, uni, mail)
        cursor.execute(statement)
        connection.commit()
        now = datetime.datetime.now()
        return redirect(url_for('page_profile'))  
        
