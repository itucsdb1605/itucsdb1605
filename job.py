import psycopg2 as dbapi2

class Job:
    def __init__(self, cp, id = None, company = None, position = None, salary = None):
        self.cp = cp
        self.id = id
        self.company = company
        self.position = position
        self.salary = salary
        
    def set_id(self, id):
        self.id = id
        
    def set_company(self, company):
        self.company = company
    
    def set_position(self, position):
        self.position = position
    
    def set_salary(self, salary):
        self.salary = salary    
    
    def get_jobs(self):
        if self.id is None:  
            with dbapi2.connect(self.cp) as connection:
                with connection.cursor() as cursor:     
                    cursor.execute("""SELECT * FROM JOBS""")    
                    job_list = cursor.fetchall() 
                    return job_list
        else:
            with dbapi2.connect(self.cp) as connection:
                with connection.cursor() as cursor:     
                    cursor.execute("""SELECT * FROM JOBS WHERE (ID = {})""".format(self.id))    
                    job_list = cursor.fetchall() 
                    return job_list
                
    
    def add_job(self):
        with dbapi2.connect(self.cp) as connection:
            with connection.cursor() as cursor:   
                statement = """INSERT INTO JOBS(CompanyName, Position, Salary) VALUES
                        ( '{}', '{}', '{}' );
                    """.format(self.company, self.position, self.salary)
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
                    SET  CompanyName='{}', Position='{}' ,Salary={}     
                    WHERE ID={};""".format(self.company, self.position, self.salary, self.id)
                cursor.execute(statement)    
                
