Mustafa Çoban Tarafından Yapılan Kısımlar
=========================================

Bu proje kapsamında **Jobs**, **Groups**, **Messages** ve **Membership**
tabloları benim tarafımdan oluşturuldu.

**Jobs Tablosu İçeriği**

.. code-block:: sql

      ID SERIAL PRIMARY KEY,
      Position VARCHAR(40) NOT NULL,
      Salary INT NOT NULL,
      CompanyId INT REFERENCES COMPANIES(id)

**Groups Tablosu İçeriği**

.. code-block:: sql

      ID SERIAL PRIMARY KEY,
      GroupName VARCHAR(40) NOT NULL,
      Description VARCHAR(200)


**Messages Tablosu İçeriği**

.. code-block:: sql

      ID SERIAL PRIMARY KEY,
      SenderID INT REFERENCES USERS(UserId),
      ReceiverID INT REFERENCES USERS(UserId),
      Text VARCHAR(200) NOT NULL

**Membership Tablosu İçeriği**

.. code-block:: sql

      GROUPID INT NOT NULL REFERENCES GROUPS(ID) ON DELETE CASCADE,
      MemberID INT NOT NULL REFERENCES USERS(USERID),
      Role VARCHAR(10) NOT NULL,
      PRIMARY KEY(GROUPID, MEMBERID)


Python kısmında *Job*, *Group* ve *Message* sınıfları benim tarafımdan oluşturuldu. Bu sınıfların kurucuları aşağıda
verilmiştir.

Sınıf kurucularında bulunan cp değişkeni database bağlantısı sağlanması için kullanılmaktadır. Bu sınıflardan
nesne oluştururuken yapılacak işlemin özelliğine göre sınıfın değişkenleri kurucu methoda verilebilir ya da verilmeyebilir
bu yüzden verilmesi veritabanı bağlantısı için zorunlu olan cp değişkeni dışındaki değişkenlerin
nesne oluşturulurken verilmemesi ihtimaline karşı *=None* opsiyonu eklenerek bu değişkenler verilmediğinde
değerleri *None* yapılmaktadır.


**Job Sınıfı Kurucusu**

.. code-block:: python

    def __init__(self, cp, id = None, companyId = None, position = None, salary = None):
        self.cp = cp
        self.id = id
        self.companyId = companyId
        self.position = position
        self.salary = salary

**Job Sınıfı Fonksiyonları**

.. code-block:: python

    def set_id(self, id):
        self.id = id

    def set_companyId(self, companyId):
        self.companyId = companyId

    def set_position(self, position):
        self.position = position

    def set_salary(self, salary):
        self.salary = salary


    def get_job(self,id):
        with dbapi2.connect(self.cp) as connection:
                with connection.cursor() as cursor:
                    cursor.execute("""
                                    SELECT T1.ID, COMPANIES.TITLE, T1.POSITION, T1.SALARY FROM (SELECT * FROM JOBS WHERE (ID={})) AS T1
                                    INNER JOIN COMPANIES
                                    ON COMPANIES.ID=T1.ID
                                """.format(id))
                    job_list = cursor.fetchall()
                    return job_list

    def get_jobs(self):
        with dbapi2.connect(self.cp) as connection:
            with connection.cursor() as cursor:
                cursor.execute("""
                                    SELECT T1.ID, COMPANIES.TITLE, T1.POSITION, T1.SALARY FROM (SELECT * FROM JOBS) AS T1
                                    INNER JOIN COMPANIES
                                    ON COMPANIES.ID=T1.ID
                                    """)
                job_list = cursor.fetchall()
                return job_list



    def add_job(self):
        with dbapi2.connect(self.cp) as connection:
            with connection.cursor() as cursor:
                print("""INSERT INTO JOBS(CompanyId, Position, Salary) VALUES
                        ( {}, '{}', {} )
                    """.format(self.companyId, self.position, self.salary))
                statement = """INSERT INTO JOBS(CompanyId, Position, Salary) VALUES
                        ( {}, '{}', {} )""".format(self.companyId, self.position, self.salary)
                cursor.execute(statement)

    def delete_jobs(self, ids):
        with dbapi2.connect(self.cp) as connection:
            with connection.cursor() as cursor:
                statement = """DELETE FROM JOBS WHERE ID = {}"""
                for id in ids:
                    id = id.split('/', maxsplit=1)
                    id = id[0]
                    cursor.execute(statement.format(id))

    def update_job(self):
        with dbapi2.connect(self.cp) as connection:
            with connection.cursor() as cursor:
                statement = """UPDATE JOBS
                    SET  CompanyId={}, Position='{}' ,Salary={}
                    WHERE ID={};""".format(self.companyId, self.position, self.salary, self.id)
                cursor.execute(statement)

Sırasıyla fonksiyonların özellikleri şu şekilde özetlenebilir:
   - **set_id**: id bilgisini belirler
   - **set_company**: şirket bilgisini belirler
   - **set_position**: pozisyon bilgisini belirler
   - **set_ salary**: maaş bilgisini belirler
   - **get_job**: parametre olarak verilen id'ye sahip şirketin bilgilerini dönderir
   - **get_jobs**: *jobs* tablosundaki bütün şirketlerin bilgilerini dönderir
   - **add_job**: *jobs* tablosuna o nesnenin bilgilerini barındıran bir şirket ekler
   - **delete_jobs**: parametre olarak verilen id'lere sahip şirketleri *jobs* tablosundan siler
   - **update_jobs**: *jobs* tablosuna o nesnenin bilgilerini barındıran şirketi günceller


**Group Sınıfı Kurucusu**

.. code-block:: python

    def __init__(self, cp, name = None, id = None, description=None):
        self.cp = cp
        self.id = id
        self.name = name
        self.description = description

**Group Sınıfı Fonksiyonları**

.. code-block:: python

    def set_id(self, id):
        self.id = id

    def set_name(self, name):
        self.name = name

    def set_description(self, description):
        self.description = description

    def find_group_name(self, id):
        with dbapi2.connect(self.cp) as connection:
            with connection.cursor() as cursor:
                cursor.execute("""SELECT groupName FROM GROUPS WHERE ID = {}""".format(id))
                groupName = cursor.fetchone()
                return groupName[0]

    def get_groups(self):
        if self.id is None:
            with dbapi2.connect(self.cp) as connection:
                with connection.cursor() as cursor:
                    cursor.execute("""SELECT * FROM GROUPS""")
                    group_list = cursor.fetchall()
                    return group_list
        else:
            with dbapi2.connect(self.cp) as connection:
                with connection.cursor() as cursor:
                    cursor.execute("""SELECT * FROM GROUPS WHERE ID = {}""".format(self.id))
                    group_list = cursor.fetchall()
                    return group_list


    def delete_groups(self, ids):
        with dbapi2.connect(self.cp) as connection:
            with connection.cursor() as cursor:
                statement = """DELETE FROM GROUPS WHERE ID = {}"""
                for id in ids:
                    id = id.split('/', maxsplit=1)
                    id = id[0]
                    cursor.execute(statement.format(id))

    def update_group(self):
        with dbapi2.connect(self.cp) as connection:
            with connection.cursor() as cursor:
                statement = """UPDATE GROUPS
                    SET  GroupName='{}', Description='{}'
                    WHERE ID={}""".format(self.name, self.description, self.id)
                cursor.execute(statement)

    def create_group(self):
        with dbapi2.connect(self.cp) as connection:
            with connection.cursor() as cursor:
                statement = """INSERT INTO GROUPS(GroupName, Description) VALUES
                        ( '{}', '{}' );
                    """.format(self.name, self.description)
                cursor.execute(statement)

    def add_member(self, userid, role):
        with dbapi2.connect(self.cp) as connection:
            with connection.cursor() as cursor:
                statement = """INSERT INTO MEMBERSHIP(GroupID, MemberId, role) VALUES
                        ( '{}', '{}' , '{}');
                    """.format(self.id, userid, role)
                cursor.execute(statement)

    def get_members(self,id):
        with dbapi2.connect(self.cp) as connection:
            with connection.cursor() as cursor:
                statement = """
                SELECT T1.role, Users.firstname, Users.lastname, Users.uni, Users.UserID FROM (SELECT * FROM membership WHERE groupid={}) AS T1
                    INNER JOIN USERS
                    ON Users.UserID=T1.MemberId
                """.format(id)
                cursor.execute(statement)
                users = cursor.fetchall()
                return users

Sırasıyla fonksiyonların özellikleri şu şekilde özetlenebilir:
   - **set_id**: grup id bilgisini belirler
   - **set_name**: grup ismi bilgisini belirler
   - **set_description**: grup tanımı bilgisini belirler
   - **find_group_name**: parametre olarak verilen id'ye sahip grubun ismini dönderir
   - **get_groups**: Eğer nesnenin id değeri *None* ise bütün grup bilgilerini, id değeri None değilse o idye sahip grubun bilgilerini dönderir
   - **delete_groups**: parametre olarak verilen idlere ait grupları *Groups* tablosundan siler
   - **update_group**: *Groups* tablosunda o nesnenin bilgilerini barındıran grubu günceller
   - **create_group**: *Groups* tablosunda o nesnenin bilgilerini barındıran bir grup oluşturur
   - **add_member**: parametre olarak verilen userid ve role'ü barındıran bir üyeyi *Membership* tablosuna ekler
   - **get_members**: parametre olarak verilen idye sahip grubun üyelerinin bilgilerini *Membership* ve *User* tablolarından katma işlemiyle ulaşarak dönderir.



**Message Sınıfı Kurucusu**

.. code-block:: python

    def __init__(self, cp, senderId=None, receiverId=None, text=None):
        self.cp = cp
        self.senderId = senderId
        self.receiverId = receiverId
        self.text = text


**Message Sınıfı Fonksiyonları**

.. code-block:: python

    def send(self):
        with dbapi2.connect(self.cp) as connection:
                with connection.cursor() as cursor:
                    statement = """INSERT INTO MESSAGES(senderId, receiverId, text) VALUES
                        ( '{}', '{}', '{}' )
                    """.format(self.senderId, self.receiverId, self.text)
                    cursor.execute(statement)

    def delete_messages(self, ids):
        with dbapi2.connect(self.cp) as connection:
            with connection.cursor() as cursor:
                statement = """DELETE FROM MESSAGES WHERE ID = {}"""
                for id in ids:
                    id = id.split('/', maxsplit=1)
                    id = id[0]
                    cursor.execute(statement.format(id))

Sırasıyla fonksiyonların özellikleri şu şekilde özetlenebilir:
  - **send**: O mesaj nesnesine ait *senderId*, *receiverId* ve *text* değişkenlerini kullanarak *Messages* tablosuna yeni bir mesaj ekler.
  - **delete_messages**: parametre olarak verilen id'lere sahip mesajları *Messages* tablosundan siler.
