import psycopg2 as dbapi2

class Message:
    def __init__(self, cp, senderId, receiverId, text):
        self.cp = cp
        self.senderId = senderId
        self.receiverId = receiverId
        self.text = text

    def send(self):
        with dbapi2.connect(self.cp) as connection:
                with connection.cursor() as cursor:
                    statement = """INSERT INTO MESSAGES(senderId, receiverId, text) VALUES
                        ( '{}', '{}', '{}' );
                    """.format(self.senderId, self.receiverId, self.text)
                    cursor.execute(statement)