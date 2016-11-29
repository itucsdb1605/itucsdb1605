import psycopg2 as dbapi2

class Group:
    def __init__(self, cp, name = None, id = None):
        self.cp = cp
        self.id = id
        self.name = name
        
    def set_id(self, id):
        self.id = id
    
    def set_name(self, name):
        self.name = name
        
    def find_group_name(self, id):
        with dbapi2.connect(self.cp) as connection:
            with connection.cursor() as cursor:     
                cursor.execute("""SELECT groupName FROM GROUPS WHERE ID = {}""".format(id))    
                groupName = cursor.fetchone() 
                return groupName[0]
    
    def get_groups(self):
        if self.id is None:
            with dbapi2.connect(self.cp) as connection:
                with connection.cursor() as cursor:     
                    cursor.execute("""SELECT * FROM GROUPS""")    
                    group_list = cursor.fetchall() 
                    return group_list
        else:
            with dbapi2.connect(self.cp) as connection:
                with connection.cursor() as cursor:     
                    cursor.execute("""SELECT * FROM GROUPS WHERE ID = {}""".format(self.id))    
                    group_list = cursor.fetchall() 
                    return group_list
    
    def get_jobs(self, companyName):
        if companyName is None:
            with dbapi2.connect(self.cp) as connection:
                with connection.cursor() as cursor:     
                    cursor.execute("""SELECT Position, Salary FROM JOBS""")    
                    job_list = cursor.fetchall() 
                    return job_list
        else:
            with dbapi2.connect(self.cp) as connection:
                with connection.cursor() as cursor:     
                    cursor.execute("""SELECT Position, Salary FROM JOBS
                                    WHERE CompanyName = '{}'""".format(companyName))    
                    job_list = cursor.fetchall() 
                    return job_list
    
    def delete_groups(self, ids):
        with dbapi2.connect(self.cp) as connection:
            with connection.cursor() as cursor:   
                statement = """DELETE FROM GROUPS WHERE ID = {}"""
                for id in ids:
                    id = id.split('/', maxsplit=1)
                    id = id[0]
                    cursor.execute(statement.format(id))
    
    def update_group(self):
        with dbapi2.connect(self.cp) as connection:
            with connection.cursor() as cursor:   
                statement = """UPDATE GROUPS
                    SET  GroupName='{}'  
                    WHERE ID={}""".format(self.name, self.id)
                cursor.execute(statement)   
                
    def create_group(self):
        with dbapi2.connect(self.cp) as connection:
            with connection.cursor() as cursor:   
                statement = """INSERT INTO GROUPS(GroupName) VALUES
                        ( '{}' );
                    """.format(self.name)
                cursor.execute(statement) 
