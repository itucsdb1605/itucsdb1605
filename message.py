import psycopg2 as dbapi2

class Message:
    def __init__(self, cp, senderId=None, receiverId=None, text=None):
        self.cp = cp
        self.senderId = senderId
        self.receiverId = receiverId
        self.text = text

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