import tornado.ioloop
import tornado.web
import tornado.database

class MainHandler(tornado.web.RequestHandler):
	def get(self):
		#Make a instance first
		db = MysqlHandler()
				
		#Add staff test
		#db.add_staff("1010", "test", 12, "1232345345", "adsf.jpg")
		
		#Delete staff test
		#db.del_staff("1010")
		
		#Look up table test
		'''
		list = db.look_table("staff")
		for i in list:
			print i.sid, i.name, i.age, i.idnumber, i.spic
		'''
		
		#Add record test
		#db.add_record("1010", "am", "fff.jpg")
		
		#Add log test
		#db.add_log("1010", "am", "ffaa.jpg", 1)
			
		#Login test
		'''
		test1 = db.login("aaa", "aaaa")
		test2 = db.login("lituo", "123")
		print test1,test2
		'''
		
		self.write("ok")
	
class MysqlHandler:
	#Init the connection
	def __init__(self):
		self.db = tornado.database.Connection("localhost", "python", "root", "h")
	
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
	def add_staff(self, sid, name, age, idnumber, spic):
		self.db.execute("INSERT INTO staff (sid, name, age, idnumber, spic) VALUES ('%s', '%s', %d, '%s', '%s')" % (sid, name, age, idnumber, spic))  	  
		
	#Update one staff in db
	#...
		
	#Delete one staff in db
	def del_staff(self, sid):
		self.db.execute("DELETE FROM staff WHERE sid = '%s'" % sid)
		
	#Add one record in db
	def add_record(self, sid, type, rpic):
		self.db.execute("INSERT INTO record (sid, type, rpic) VALUES ('%s', '%s', '%s')" % (sid, type, rpic))	
		
	#Add one log in db
	def add_log(self, sid, type, lpic, static):
		self.db.execute("INSERT INTO log (sid, type, lpic, static) VALUES ('%s', '%s', '%s', %d)" % (sid, type, lpic, static))
		
				

#Define first and reference		
application = tornado.web.Application([
	(r"/", MainHandler),
])
		
		
if __name__ == "__main__":
	application.listen(8888)
	tornado.ioloop.IOLoop.instance().start()
