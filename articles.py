import psycopg2 as dbapi2

class Articles:
    def __init__(self, cp):
        self.cp = cp
        return

    def get_articlelist(self):
        with dbapi2.connect(self.cp) as connection:
            cursor = connection.cursor()
            query = "SELECT articles.ArticleId, articles.ArticleName, articles.UserId, articles.Name, articles.SurName, articles.ReleaseYear, articles.Mail, universities.title FROM articles JOIN universities ON articles.uni_id = universities.id ORDER BY ArticleId ASC"
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
            query = "SELECT ArticleName, UserId, Name, SurName, ReleaseYear, Mail, uni_id  FROM articles WHERE ArticleId = '%s' ORDER BY ArticleId ASC" % (ArticleId)
            cursor.execute(query)
            rows=cursor.fetchall()
            return rows
    def add_article(self, ArticleName, UserId, Name, SurName, ReleaseYear, Mail,uni_id):
        with dbapi2.connect(self.cp) as connection:
            cursor = connection.cursor()
            query =  "INSERT INTO articles (ArticleName, UserId, Name, SurName, ReleaseYear, Mail, uni_id) VALUES ('%s','%s','%s','%s','%s','%s','%s')" % (ArticleName, UserId, Name, SurName, ReleaseYear, Mail, uni_id)
            cursor.execute(query)
            connection.commit()
            return

    def update_article(self, ArticleId, ArticleName, UserId, Name, SurName, ReleaseYear, Mail,uni_id):
        with dbapi2.connect(self.cp) as connection:
            cursor = connection.cursor()
            query =  "UPDATE articles SET ArticleName = '%s', UserId='%s', Name='%s', SurName = '%s', ReleaseYear='%s', Mail='%s', uni_id='%s' WHERE ArticleId='%s'" % (ArticleName, UserId, Name, SurName, ReleaseYear, Mail, uni_id, ArticleId)
            cursor.execute(query)
            connection.commit()
            return
