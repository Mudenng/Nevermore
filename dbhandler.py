import tornado.database

class DBHandler:
    #Init the connection
    def __init__(self):
        self.db = tornado.database.Connection("localhost", "nevermore", "root")
    
    #Just for test
    '''
    def test(self, table):
        str = ''
        for i in self.db.query("SELECT * FROM %s" % table):
            str += i['title'] + ', '
        return str[:-1]
    '''
    
    #Login check 
    def login(self, name, pwd):
        if self.db.execute_rowcount("SELECT * FROM admin WHERE name = '%s' and pwd = '%s'" % (name, pwd)) == 1:
            return 1
        else:
            return 0
    
    #Look up the table
    def look_table(self, table):
        return self.db.query("SELECT * FROM %s" % table)
        
    #Add one staff in db
    def add_staff(self, sid, name, age, idnumber, spic, eigenface):
        self.db.execute("INSERT INTO staff (sid, name, age, idnumber, spic, eigenface) VALUES ('%s', '%s', %d, '%s', '%s', '%s')" \
                  % (sid, name, age, idnumber, spic, eigenface))

    #Update one staff's eigenface in db
    def update_eigenface(self, sid, eigenface):
        self.db.execute("UPDATE staff SET eigenface = '%s' WHERE sid = '%s'" % (eigenface, sid))
    
    #Delete one staff in db
    def del_staff(self, sid):
        self.db.execute("DELETE FROM staff WHERE sid = '%s'" % sid)
        
    #Add one record in db
    def add_record(self, sid, type, rpic):
        self.db.execute("INSERT INTO record (sid, type, rpic) VALUES ('%s', '%s', '%s')" % (sid, type, rpic))
        
    #Add one log in db
    def add_log(self, sid, type, lpic, static):
        self.db.execute("INSERT INTO log (sid, type, lpic, static) VALUES ('%s', '%s', '%s', %d)" % (sid, type, lpic, static))

    #Update mean and eigenvectors
    def update_pca(self, mean, eigenvectors):
        self.db.execute("UPDATE settings SET value = '%s' WHERE sid = 'mean'" % (mean))
        self.db.execute("UPDATE settings SET value = '%s' WHERE sid = 'eigenvectors'" % (eigenvectors))

    # Get mean and eigenvectors
    def get_pca(self):
        mean = self.db.query("SELECT value FROM settings WHERE sid = 'mean'")
        eigenvectors = self.db.query("SELECT value FROM settings WHERE sid = 'eigenvectors'")
        return (mean[0]['value'], eigenvectors[0]['value'])
