import psycopg2 as dbapi2

class Projects:
    def __init__(self, cp):
        self.cp = cp
        return

    def get_projectlist(self):
        with dbapi2.connect(self.cp) as connection:
            cursor = connection.cursor()
            query = "SELECT * FROM projects"
            cursor.execute(query)
            rows = cursor.fetchall()
            return rows

    def delete_project(self, ProjectId):
        with dbapi2.connect(self.cp) as connection:
            cursor = connection.cursor()
            query = "DELETE FROM projectS WHERE ProjectId = '%s'" % (ProjectId)
            cursor.execute(query)
            connection.commit()
            return

    def add_project(self, ProjectName, ProjectYear, ProjectPartner):
        with dbapi2.connect(self.cp) as connection:
            cursor = connection.cursor()
            query =  "INSERT INTO projects (ProjectName, ProjectYear, ProjectPartner) VALUES ('%s','%s','%s')" % (ProjectName, ProjectYear, ProjectPartner)
            cursor.execute(query)
            connection.commit()
            return

    def update_project(self, ProjectId, ProjectName, ProjectYear, ProjectPartner):
        with dbapi2.connect(self.cp) as connection:
            cursor = connection.cursor()
            query =  "UPDATE projects SET ProjectName = '%s', ProjectYear='%s', ProjectPartner='%s' WHERE ProjectId='%s'" % (ProjectName, ProjectYear, ProjectPartner, ProjectId)
            cursor.execute(query)
            connection.commit()
            return
