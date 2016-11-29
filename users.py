import psycopg2 as dbapi2
class users:
    def __init__(self, cp, userId = None, firstname=None, Lastname = None, password = None,mail_address = None,uni_id = None):
        self.Firstname = firstname
        self.mail_address = mail_address
        self.password = password
        self.Lastname = Lastname
        self.UserId = userId
        self.cp = cp
        self.uni_id = uni_id
    def set_id(self, uid):
        self.UserId = uid

    def set_uni_id(self, unid):
        self.uni_id = unid
    def set_name(self, name):
        self.Firstname = name

    def set_lastname(self, lname):
        self.Lastname = lname

    def set_mail(self, mail):
        self.mail_address = mail

    def set_password(self, psw):
        self.password = psw

    def get_user(self):
        if self.UserId is None:
            with dbapi2.connect(self.cp) as connection:
                with connection.cursor() as cursor:
                    cursor.execute("""SELECT uni_id, Firstname, Lastname,Email_adress,universities.title FROM users JOIN universities ON universities.id = users.UserId""")
                    user_list = cursor.fetchall()
                    return user_list
        else:
            with dbapi2.connect(self.cp) as connection:
                with connection.cursor() as cursor:
                    cursor.execute("""SELECT * FROM users WHERE (UserId = {})""".format(self.UserId))
                    user_list = cursor.fetchall()
                    return user_list

    def add_user(self):
        with dbapi2.connect(self.cp) as connection:
            with connection.cursor() as cursor:
                statement = """INSERT INTO users(Firstname, Lastname,Email_adress,password,uni_id) VALUES
                        ( '{}', '{}', '{}','{}','{}' );
                    """.format(self.Firstname, self.Lastname, self.mail_address, self.password, self.uni_id)
                cursor.execute(statement)


    def update_user(self):
        with dbapi2.connect(self.cp) as connection:
            with connection.cursor() as cursor:
                statement = """UPDATE users
                    SET  Email_adress='{}'
                    WHERE ID={};""".format(self.mail_address,self.UserId)
                cursor.execute(statement)


    def search_user(self):
        with dbapi2.connect(self.cp) as connection:
            with connection.cursor() as cursor:
                cursor.execute("""SELECT * FROM users WHERE (Email_adress = {})""".format(self.Email_adress))
                user_list = cursor.fetchall()
                return user_list
