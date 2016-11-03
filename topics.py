import psycopg2 as dbapi2

class topics:
    def __init__(self, cp):
        self.cp = cp
        return

    def get_topiclist(self):
        with dbapi2.connect(self.cp) as connection:
            cursor = connection.cursor()
            query = "SELECT * FROM topics"
            cursor.execute(query)
            rows = cursor.fetchall()
            return rows
            
    def delete_topic(self, topicID):
        with dbapi2.connect(self.cp) as connection:
            cursor = connection.cursor()
            query = "DELETE FROM topics WHERE topicID = '%s'" % (topicID)
            cursor.execute(query)
            connection.commit()
            return
            
    def add_topic(self, topic, desc):
        with dbapi2.connect(self.cp) as connection:
            cursor = connection.cursor()
            query =  "INSERT INTO topics (topic, desc) VALUES ('%s','%s','%s')" % (topic, desc)
            cursor.execute(query)
            connection.commit()
            return
            
    def update_topic(self, topicID, topic, desc):
        with dbapi2.connect(self.cp) as connection:
            cursor = connection.cursor()
            query =  "UPDATE topics SET topic = '%s' WHERE topicID='%s', topic='%s', desc='%s'" % (topicID, topic, desc)
            cursor.execute(query)
            connection.commit()
            return
