import psycopg2 as dbapi2

class Articles:
    def __init__(self, cp):
        self.cp = cp
        return

    def get_articlelist(self):
        with dbapi2.connect(self.cp) as connection:
            cursor = connection.cursor()
            query = """SELECT articles.ArticleId, articles.ArticleName,
             articles.UserId, users.FirstName AS Name, users.LastName AS SurName,
             articles.ReleaseYear, articles.Mail, universities.title 
             FROM articles LEFT JOIN universities ON articles.uni_id = universities.id
             LEFT JOIN users ON users.UserId=articles.UserId ORDER BY articles.ArticleName ASC """
            cursor.execute(query)
            rows = cursor.fetchall()
            return rows
        
    def get_universitylist(self):
        with dbapi2.connect(self.cp) as connection:
            cursor = connection.cursor()
            query = "SELECT * FROM universities ORDER BY title ASC"
            cursor.execute(query)
            rows = cursor.fetchall()
            return rows
        
    def get_userlist(self):
        with dbapi2.connect(self.cp) as connection:
            cursor = connection.cursor()
            query = "SELECT UserId, concat(FirstName::text, LastName::text) AS name FROM users ORDER BY FirstName ASC"
            cursor.execute(query)
            rows = cursor.fetchall()
            return rows
    def delete_article(self, ArticleId):
        with dbapi2.connect(self.cp) as connection:
            cursor = connection.cursor()
            query = "DELETE FROM articles WHERE ArticleId = '%s'" % (ArticleId)
            cursor.execute(query)
            connection.commit()
            return
    def select_article(self, ArticleId):
        with dbapi2.connect(self.cp) as connection:
            cursor = connection.cursor()
            query = """SELECT articles.ArticleId, articles.ArticleName, articles.UserId,
             users.FirstName AS Name, users.lastName AS SurName, articles.ReleaseYear, articles.Mail, articles.uni_id  
             FROM articles
             LEFT JOIN users ON users.UserId=articles.UserId
             WHERE ArticleId = '%s' ORDER BY ArticleId ASC""" % (ArticleId)
            cursor.execute(query)
            rows=cursor.fetchall()
            return rows
    def add_article(self, ArticleName, UserId,ReleaseYear, Mail,uni_id):
        with dbapi2.connect(self.cp) as connection:
            cursor = connection.cursor()
            query =  "INSERT INTO articles (ArticleName, UserId, ReleaseYear, Mail, uni_id) VALUES ('%s','%s','%s','%s','%s')" % (ArticleName, UserId,ReleaseYear, Mail, uni_id)
            cursor.execute(query)
            connection.commit()
            return

    def update_article(self, ArticleId, ArticleName, UserId, ReleaseYear, Mail,uni_id):
        with dbapi2.connect(self.cp) as connection:
            cursor = connection.cursor()
            query =  "UPDATE articles SET ArticleName = '%s', UserId='%s',ReleaseYear='%s', Mail='%s', uni_id='%s' WHERE ArticleId='%s'" % (ArticleName, UserId,ReleaseYear, Mail, uni_id, ArticleId)
            cursor.execute(query)
            connection.commit()
            return
