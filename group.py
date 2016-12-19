import psycopg2 as dbapi2

class Group:
    def __init__(self, cp, name = None, id = None, description=None):
        self.cp = cp
        self.id = id
        self.name = name
        self.description = description

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
                statement = """INSERT INTO MEMBERSHIP(GroupID, UserId, role) VALUES
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

