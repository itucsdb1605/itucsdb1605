import psycopg2 as dbapi2

class Articles:
    def __init__(self, cp):
        self.cp = cp
        return

    def get_articlelist(self):
        with dbapi2.connect(self.cp) as connection:
            cursor = connection.cursor()
            query = "SELECT * FROM articles"
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

    def add_article(self, ArticleName, UserId, Name, SurName, ReleaseYear, Mail):
        with dbapi2.connect(self.cp) as connection:
            cursor = connection.cursor()
            query =  "INSERT INTO articles (ArticleName, UserId, Name, SurName, ReleaseYear, Mail) VALUES ('%s','%s','%s','%s','%s','%s')" % (ArticleName, UserId, Name, SurName, ReleaseYear, Mail)
            cursor.execute(query)
            connection.commit()
            return

    def update_article(self, ArticleId, ArticleName, UserId, Name, SurName, ReleaseYear, Mail):
        with dbapi2.connect(self.cp) as connection:
            cursor = connection.cursor()
            query =  "UPDATE articles SET ArticleName = '%s', UserId='%s', Name='%s', SurName = '%s', ReleaseYear='%s', Mail='%s' WHERE ArticleId='%s'" % (ArticleName, UserId, Name, SurName, ReleaseYear, Mail, ArticleId)
            cursor.execute(query)
            connection.commit()
            return
