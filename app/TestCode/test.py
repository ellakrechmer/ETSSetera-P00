import sqlite3
from database import BlogTable

def main():

	db = BlogTable("dbtest.db", "test")

	db.insert("sging04", "t1","Vivamus integer nom", "nom")
	db.insert("sean", "t2","Vivamus sucipit taciti", "vivamus")
	ret = db.getEntryById(1)
	print(ret)
	print(db.searchByKeyWord("vivamus", 1))
	db.popById(1)
	print(ret)

#are the keyword case sensitive
#only one keyword?
#check if username even exists in userpass table
# is blog inserted as a string? How to have paragraph spacing? line breaks (ie: <br>)? 

#what does each method return????
main()