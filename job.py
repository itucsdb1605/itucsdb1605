import psycopg2 as dbapi2

class Job:
    def __init__(self, cp, id = None, companyId = None, position = None, salary = None):
        self.cp = cp
        self.id = id
        self.companyId = companyId
        self.position = position
        self.salary = salary

    def set_id(self, id):
        self.id = id

    def set_companyId(self, companyId):
        self.companyId = companyId

    def set_position(self, position):
        self.position = position

    def set_salary(self, salary):
        self.salary = salary


    def get_job(self,id):
        with dbapi2.connect(self.cp) as connection:
                with connection.cursor() as cursor:
                    cursor.execute("""
                                    SELECT T1.ID, COMPANIES.TITLE, T1.POSITION, T1.SALARY FROM (SELECT * FROM JOBS WHERE (ID={})) AS T1
                                    INNER JOIN COMPANIES
                                    ON COMPANIES.ID=T1.ID
                                """.format(id))
                    job_list = cursor.fetchall()
                    print(job_list)
                    return job_list

    def get_jobs(self):
        with dbapi2.connect(self.cp) as connection:
            with connection.cursor() as cursor:
                cursor.execute("""
                                    SELECT T1.ID, COMPANIES.TITLE, T1.POSITION, T1.SALARY FROM (SELECT * FROM JOBS) AS T1
                                    INNER JOIN COMPANIES
                                    ON COMPANIES.ID=T1.ID
                                    """)
                job_list = cursor.fetchall()
                print(job_list)
                return job_list



    def add_job(self):
        with dbapi2.connect(self.cp) as connection:
            with connection.cursor() as cursor:
                print("""INSERT INTO JOBS(CompanyId, Position, Salary) VALUES
                        ( {}, '{}', {} )
                    """.format(self.companyId, self.position, self.salary))
                statement = """INSERT INTO JOBS(CompanyId, Position, Salary) VALUES
                        ( {}, '{}', {} )""".format(self.companyId, self.position, self.salary)
                cursor.execute(statement)

    def delete_jobs(self, ids):
        with dbapi2.connect(self.cp) as connection:
            with connection.cursor() as cursor:
                statement = """DELETE FROM JOBS WHERE ID = {}"""
                for id in ids:
                    id = id.split('/', maxsplit=1)
                    id = id[0]
                    print(id)
                    cursor.execute(statement.format(id))

    def update_job(self):
        with dbapi2.connect(self.cp) as connection:
            with connection.cursor() as cursor:
                statement = """UPDATE JOBS
                    SET  CompanyId={}, Position='{}' ,Salary={}
                    WHERE ID={};""".format(self.companyId, self.position, self.salary, self.id)
                cursor.execute(statement)

