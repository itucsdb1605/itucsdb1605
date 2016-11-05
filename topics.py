import psycopg2 as dbapi2

class Topics:
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
            
    def add_topic(self, topic, description):
        with dbapi2.connect(self.cp) as connection:
            cursor = connection.cursor()
            query =  "INSERT INTO topics (topic, description) VALUES ('%s','%s')" % (topic, description)
            cursor.execute(query)
            connection.commit()
            return
            
    def update_topic(self, topicID, topic, description):
        with dbapi2.connect(self.cp) as connection:
            cursor = connection.cursor()
            query =  "UPDATE topics SET topic = '%s', description = '%s' WHERE topicID='%s'" % (topic, description, topicID)
            cursor.execute(query)
            connection.commit()
            return
