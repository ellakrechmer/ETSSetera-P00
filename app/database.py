import sqlite3


class UsernamePasswordTable:

	'''
		UsernamePasswordTable Class

		A table inside of a database NOT  a database. Specifically
		designed for the username, password

		Ensures username IS UNIQUE

		Just wanted to make interacting w tables easier

		DB design:
			username TEXT
			password TEXT

	'''
	def __init__ (self,fileName, name):
		'''
		__init__
		Args
		    filename: database file name
			name: name of table
		Returns
			instance of UsernamePasswordTable


		Class attributes
			self._db : the file our database comes from. uses fileName Check_same_thread
			was set to false, if you want us to change it, let us know. PRIVATE,
			do not use.

			self._cursor is the cursor for that database. PRIVATE, do not use.

			self._name is the name of the table, used to aid in writing methods for
			this class; private, do not use!

		'''
		self._db = sqlite3.connect(fileName, check_same_thread=False)
		self._cursor = self._db.cursor()
		self._name = name
		self._cursor.execute(f"CREATE TABLE IF NOT EXISTS {self._name}(username TEXT, password TEXT, unique(username));")

	def insert(self,username, password):
		'''
		insert

		insert username and password. DOES NOT CHECK if it is duplicate.
		will throw error if duplicate! please use userExists method below!
		returns nothing

		Args
			username : username
			password : password

		Returns
			Nothing

		'''
		#insert vales & committing them
		self._cursor.execute(f"INSERT INTO {self._name} VALUES(\"{username}\", \"{password}\");")
		self._db.commit()


	def userExists(self,username):
		'''
		userExists

		Will return true if user name exists in table will throw false otherwise.

		@params
			username : usernamebeing checked

		Returns
			boolean t/f

		'''
		#executing query
		self._cursor.execute(f"SELECT * FROM {self._name} where username=\"{username}\";")

		if self._cursor.fetchone() is not None: #if there was an entry returned
			return True #meaning we had a match
		else:
			return False

	def passMatch(self,username, password):
		'''
		passMatch

		Will return true if user name and pass exists in table will throw false otherwise.

		@params
			username : username being checked
			password : password being checked

		Returns
			boolean t/f

		'''
		#executing query
		self._cursor.execute(f"SELECT * FROM {self._name} where username=\"{username}\" AND password=\"{password}\";")

		if self._cursor.fetchone() is not None: #if there was an entry returned
			return True #meaning we had a match
		else:
			return False



class BlogTable:
	'''
		BlogTable Class

		A table inside of a database NOT  a database. Specifically
		designed for the blog USING FTS4 for faster search

		Just wanted to make interacting w tables easier

		DB design:
			username TEXT,
			title TEXT NOT NULL,
			blog TEXT NOT NULL,
			topic TEXT NOT NULL

	'''

	def __init__ (self,fileName, name):
		'''
		__init__
		Args
		    filename: database file name
			name: name of table
		Returns
			instance of BlogTable



		Class attributes
			self._db : the file our database comes from. uses fileName Check_same_thread
			was set to false, if you want us to change it, let us know. PRIVATE,
			do not use.

			self._cursor is the cursor for that database. PRIVATE, do not use.

			self._name is the name of the table, used to aid in writing methods for
			this class; private, do not use!

		'''
		self._db = sqlite3.connect(fileName, check_same_thread=False)
		self._cursor = self._db.cursor()
		self._name = name
		self._cursor.execute(f"CREATE VIRTUAL TABLE IF NOT EXISTS {self._name} USING fts4( username TEXT, title TEXT NOT NULL,  blog TEXT NOT NULL, topic TEXT NOT NULL) ;")

	def insert(self, username, title,  blog, topic):
		'''
		insert

		insert username, title,  blog, topic. DOES NOT CHECK if it is duplicate.
		will throw error if duplicate! please use userExists method below!
		returns Nothing

		Args
			username, title,  blog, topic
		Returns
			Nothing

		'''
		#insert vales & committing them
		self._cursor.execute(f"INSERT INTO {self._name} VALUES( \"{username}\", \"{title}\", \"{blog}\",\"{topic}\" );")
		self._db.commit()

	def getEntryById(self, id : int): #ensuring param is int
		'''
		getEntryById

		returns entry with certain rowid

		Args
			id MUST BE INT
		Returns
			entry dict

		'''
		self._cursor.execute(f"SELECT rowid, * from {self._name} WHERE rowid={id} LIMIT 1;")
		data = self._cursor.fetchone()
		return data


	def popById(self, id : int):
		'''
		popById

		pops entry with certain rowid

		Args
			id MUST BE INT
		Returns
			entry dict

		'''
		self._cursor.execute(f"SELECT rowid, * from {self._name} WHERE rowid={id} LIMIT 1;")
		data = self._cursor.fetchone()
		self._cursor.execute(f"DELETE from {self._name} WHERE rowid={id};")
		self._db.commit()
		return data

	def searchByKeyWord(self, topic, limit : int):
		'''
		searchByKeyWord

		returns limit size list of entries searched by topic

		Args
			id MUST BE INT
		Returns
			entry dict

		'''
		self._cursor.execute(f"SELECT rowid, * from {self._name} WHERE topic MATCH \"{topic}\" LIMIT {limit};")
		data = self._cursor.fetchone()
		return data

	def _printall(self):
		'''
		_printall

		Debugging function. Prints all items in table.

		'''
		self._cursor.execute(f"SELECT * from {self._name}")
		data = self._cursor.fetchall()
		print(data)

	def seeContent(self):
		'''
		seeContent

		returns content of table as string

		'''
		self._cursor.execute(f"SELECT * from {self._name}")
		data = self._cursor.fetchall()
		return data
'''
Database testing code

This is mostly for my purposes only we can delete it when we're
Deploying the app

Thanks Patrick and Sean

from database import UsernamePasswordTable

userpass = UsernamePasswordTable("test.db", "db")


print(" should print false")
print(userpass.userExists("user"))

print(" should print false")
print(userpass.passMatch("user", "pass"))


#userpass.insert("user", "pass")

print(" should print true")
print(userpass.userExists("user"))


print(" should print true")
print(userpass.passMatch("user", "pass"))

print(" should print false")
print(userpass.passMatch("user", "passs"))
'''
