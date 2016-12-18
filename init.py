import psycopg2 as dbapi2

class INIT:
    def __init__(self, cp):
        self.cp = cp
        return
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


    def topics(self):
        with dbapi2.connect(self.cp) as connection:
            cursor = connection.cursor()
            query = "DROP TABLE IF EXISTS topics CASCADE"
            cursor.execute(query)
            query = """CREATE TABLE topics (
                    topicID SERIAL PRIMARY KEY,
                    topic VARCHAR(40) UNIQUE NOT NULL,
                    description VARCHAR(80) NOT NULL
                    )"""
            cursor.execute(query)

            query = """INSERT INTO topics (topic, description) VALUES
              ('Careers','Talk about careers here!'),
              ('Engineering','Talk about engineering here!'),
              ('Finance','Talk about finance here!'),
              ('International','Talk about international topics here!'),
              ('Jobs','Talk about jobs here!'),
              ('Languages','Talk about languages here!'),
              ('Miscellaneous','Talk about various stuff here!'),
              ('Technology','Talk about technology here!');
              """
            cursor.execute(query)
            connection.commit()

    def channels(self):
        with dbapi2.connect(self.cp) as connection:
            cursor = connection.cursor()
            query = "DROP TABLE IF EXISTS channels CASCADE"
            cursor.execute(query)
            query = """CREATE TABLE channels (
                    id SERIAL PRIMARY KEY,
                    title VARCHAR(40) UNIQUE NOT NULL
                    )"""
            cursor.execute(query)

            query = """INSERT INTO channels (title) VALUES
              ('Yazılım'),
              ('Eğlence'),
              ('Ekonomi'),
              ('Spor'),
              ('Sosyal Medya'),
              ('Liderlik'),
              ('Mobil'),
              ('Sinema'),
              ('Eğitim'),
              ('Müzik');
              """
            cursor.execute(query)
            connection.commit()

    def messages(self):
        with dbapi2.connect(self.cp) as connection:
            cursor = connection.cursor()
            statement = "DROP TABLE IF EXISTS Messages CASCADE"
            cursor.execute(statement)
            statement = """CREATE TABLE Messages (
                        ID SERIAL PRIMARY KEY,
                        SenderID INT REFERENCES USERS(UserId),
                        ReceiverID INT REFERENCES USERS(UserId),
                        Text VARCHAR(200) NOT NULL
                        )"""
            cursor.execute(statement)
            statement = """INSERT INTO MESSAGES(SenderID, ReceiverID, Text) VALUES
                        (1, 3, 'Hi! How are you?'),
                        (2, 1, 'Hi!'),
                        (1, 4, 'Hello'),
                        (4, 3, 'Merhaba!'),
                        (3, 2, 'Heey Deneme!'),
                        (3, 5, 'Naber?')
                        """
            cursor.execute(statement)
            connection.commit()
    def jobs(self):
        with dbapi2.connect(self.cp) as connection:
            cursor = connection.cursor()
            statement = "DROP TABLE IF EXISTS JOBS CASCADE"
            cursor.execute(statement)
            statement = """CREATE TABLE JOBS (
                    ID SERIAL PRIMARY KEY,
                    CompanyName VARCHAR(40) NOT NULL,
                    Position VARCHAR(40) NOT NULL,
                    Salary INT NOT NULL
                    )
                    """
            cursor.execute(statement)
            statement = """INSERT INTO JOBS(CompanyName, Position, Salary) VALUES
                        ('Apple', 'Software Engineer', 12000),
                        ('Google', 'Software Engineer', 10000),
                        ('Microsoft', 'Industrial Engineer', 7500),
                        ('Vodafone', 'Android Developer', 9700),
                        ('Turkcell', 'Software Engineer', 7400),
                        ('Apple', 'iOS Developer', 14000),
                        ('Turkcell', 'Software Engineer', 5000),
                        ('Avea', 'Server Maintainer', 4000),
                        ('Airties', 'Network Engineer', 5000),
                        ('NVIDIA', 'Electronics Engineer', 15000);
                        """
            cursor.execute(statement)
            connection.commit()

    def groups(self):
        with dbapi2.connect(self.cp) as connection:
            with connection.cursor() as cursor:
                cursor.execute("DROP TABLE IF EXISTS GROUPS CASCADE")
                statement = """CREATE TABLE GROUPS (
                        ID SERIAL PRIMARY KEY,
                        GroupName VARCHAR(40) NOT NULL,
                        JobId INT REFERENCES JOBS(ID) ON DELETE RESTRICT
                        )
                        """
                cursor.execute(statement)
                statement = """INSERT INTO GROUPS(GroupName) VALUES
                            ('Turkcell'),
                            ('İstanbul Teknik Üniversitesi Mezunları'),
                            ('Silicon Valley'),
                            ('Apple')
                            """
                cursor.execute(statement)

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
              ('Tesla Motors', 1998, 'USA' ),
              ('New Horizons', 1999, 'Spain' ),
              ('Gigafactory', 1985, 'Italy' ),
              ('SpaceX', 1996, 'China' ),
              ('Foxconn', 2005, 'Brasil' ),
              ('Panasonic', 2001, 'Korea' ),
              ('LG Electronics', 1945, 'Turkey' );
              """
            cursor.execute(query)
            connection.commit()

    def articles(self):
        with dbapi2.connect(self.cp) as connection:
            cursor = connection.cursor()
            query = "DROP TABLE IF EXISTS articles CASCADE"
            cursor.execute(query)

            query = """CREATE TABLE articles (
                    ArticleId SERIAL PRIMARY KEY,
                    ArticleName VARCHAR(400) UNIQUE NOT NULL,
                    UserId INTEGER NOT NULL REFERENCES users(UserId),
                    Name VARCHAR(90) NOT NULL,
                    SurName VARCHAR(80) NOT NULL,
                    ReleaseYear SMALLINT NOT NULL,
                    Mail VARCHAR(100) NOT NULL,
                    uni_id INTEGER NOT NULL REFERENCES universities(id)
                    )"""
            cursor.execute(query)

            query = """INSERT INTO articles(ArticleName, UserId, Name, SurName, ReleaseYear, Mail, uni_id) VALUES
              ('Efficient algorithms for the (weighted) minimum circle problem',5,'Donald','Hearn',1982,'Hearn@ise.ufl.edu',24),
              ('3-D Mesh Geometry Compression with Set Partitioning in the Spectral Domain',6,'Uluğ','Bayazıt',2011,'ulugbayazit@itu.edu.tr',34),
              ('The minimum covering sphere problem',5,'Donald','Hearn',1972,'Hearn@ise.ufl.edu',24);
              """
            cursor.execute(query)
            connection.commit()
    def connections(self):
        with dbapi2.connect(self.cp) as connection:
            cursor = connection.cursor()
            query = "DROP TABLE IF EXISTS connections CASCADE"
            cursor.execute(query)

            query = """CREATE TABLE connections (
                    ConenctionId SERIAL PRIMARY KEY,
                    MainUserId INT NOT NULL,
                    FriendUserId INT NOT NULL,
                    MainUserId INTEGER NOT NULL REFERENCES users(UserId),
                    FriendUserId INTEGER NOT NULL REFERENCES users(UserId)
                    )"""
            cursor.execute(query)

            query = """INSERT INTO connections(MainUserId, FriendUserId) VALUES
              (1,2),
              (1,3),
              (2,3),
              (4,5),
              (4,2),
              (2,5);
              """
            cursor.execute(query)
            connection.commit()
    def events(self):
        with dbapi2.connect(self.cp) as connection:
            cursor = connection.cursor()
            query = "DROP TABLE IF EXISTS events CASCADE"
            cursor.execute(query)

            query = """CREATE TABLE events (
                    EventId SERIAL PRIMARY KEY,
                    EventName VARCHAR(300) UNIQUE NOT NULL,
                    OwnerId INT NOT NULL,
                    CityId INT NOT NULL,
                    Date VARCHAR(20) NOT NULL,
                    Time VARCHAR(15) NOT NULL,
                    Detail VARCHAR(500) NOT NULL,
                    OwnerId INTEGER NOT NULL REFERENCES users(UserId),
                    CityId INTEGER NOT NULL REFERENCES locations(loc_id)
                    )"""
            cursor.execute(query)

            query = """INSERT INTO events(EventName, OwnerId, CityId, Date, Time, Detail) VALUES
              ('İTÜ Arı-Çekirdek Proje Yarışması',4,34,'20.12.2016','13:30','2016 yılı proje yarışması sonuçları, İTÜ Ayazağa'),
              ('Medikal alanda Görüntü İşleme',2,34,'01.01.2017','16:00','Bilgisayarla görüntü işlemenin sağlık alanında uygulamaları, Sabancı Üniversitesi Merkez Kampüsü');
              """
            cursor.execute(query)
            connection.commit()
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
