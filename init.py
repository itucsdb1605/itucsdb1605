import psycopg2 as dbapi2

class INIT:
    def __init__(self, cp):
        self.cp = cp
        return
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

    def universities_info(self):
        with dbapi2.connect(self.cp) as connection:
            cursor = connection.cursor()
            query = "DROP TABLE IF EXISTS universities_info CASCADE"
            cursor.execute(query)

            query = """CREATE TABLE universities_info (
                    uni_id INTEGER NOT NULL REFERENCES universities
                        ON DELETE RESTRICT
                        ON UPDATE CASCADE,
                    local VARCHAR(40) NOT NULL,
                    population NUMERIC(10),
                    type VARCHAR(10),
                    UNIQUE (uni_id)
                )"""
            cursor.execute(query)
            query = """INSERT INTO universities_info VALUES
              (1, 'Ankara', 15020,'Devlet'),
              (2, 'Ankara', 25010,'Devlet'),
              (3, 'Ankara', 21008,'Özel'),
              (4, 'Ankara', 12504,'Devlet'),
              (5, 'Ankara', 27500,'Devlet'),
              (6, 'İzmir', 25412,'Devlet'),
              (7, 'İzmir', 10997,'Devlet'),
              (8, 'Kocaeli', 17627,'Devlet'),
              (9, 'Sakarya', 6570,'Devlet'),
              (10, 'İstanbul', 8879, 'Devlet'),
              (11, 'İstanbul', 8690, 'Devlet'),
              (12, 'İstanbul', 11994, 'Devlet'),
              (13, 'İstanbul', 33424, 'Özel'),
              (14, 'İstanbul', 11586, 'Devlet'),
              (15, 'İstanbul', 17215, 'Devlet'),
              (16, 'İstanbul', 15990,'Özel'),
              (17, 'İstanbul', 3944,'Özel'),
              (18, 'İstanbul', 3338, 'Özel'),
              (19, 'Tunceli', 1330,'Devlet'),
              (20, 'Kocaeli', 1219, 'Devlet'),
              (21, 'Trabzon', 8879, 'Devlet'),
              (22, 'İstanbul', 8600, 'Özel'),
              (23, 'İstanbul', 11994,'Özel'),
              (24, 'Bursa', 3384, 'Devlet'),
              (25, 'Elazığ', 11586,'Devlet'),
              (26, 'Eskişehir', 17615,'Devlet'),
              (27, 'Kırıkkale', 5110, 'Devlet'),
              (28, 'Sinop', 3774,'Devlet'),
              (29, 'Ankara', 3338,'Özel'),
              (30, 'Erzincan', 2030, 'Devlet'),
              (31, 'Van', 1439,'Devlet'),
              (32, 'Eskişehir', 38424,'Devlet'),
              (33, 'Antalya', 11586,'Devlet'),
              (34, 'Ankara', 17215, 'Özel'),
              (35, 'İstanbul', 24190,'Özel'),
              (36, 'Erzurum', 7944, 'Devlet'),
              (37, 'İstanbul', 3338,'Özel'),
              (38, 'İstanbul', 9030,'Devlet'),
              (39, 'Bursa', 4139,'Devlet'),
              (40, 'Düzce', 2558, 'Devlet'),
              (41, 'Edirne', 9030,'Devlet'),
              (42, 'İstanbul', 4239, 'Özel');
            """
            cursor.execute(query)
            connection.commit()

    def topics(self):
		with dbapi2.connect(self.cp) as connection:
			cursor = connection.cursor()
			query = """CREATE TABLE topics (
					id SERIAL PRIMARY KEY,
					title VARCHAR(40) UNIQUE NOT NULL
				)"""
			cursor.execute(query)
			
			cursor.execute("""INSERT INTO topics (title) VALUES
			('Careers'),
			('Engineering'),
			('Finance'),
			('International'),
			('Jobs'),
			('Languages'),
			('Miscellaneous'),
			('Technology');
			""")
			connection.commit()

    def All(self):
        self.universities()
        self.universities_info()
        self.topics()
