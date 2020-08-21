import sqlite3

class Database:
	def __init__(self):
		self.conn = sqlite3.connect('example.db')

	def get_db():
		try:
			db = getattr(g, '_database', None)
		except NameError:
			db = Database()
			g = lambda: None #funny syntax that lets me set an attribute on global g
			setattr(g, '_database', db)
		return db

	def query(self, sql, parameters=[]):
		c = self.conn.cursor()
		c.execute(sql, parameters)
		return c.fetchall()

	def close(self):
		self.conn.close()