import sqlite3
from database import BlogTable

def main():

	db = BlogTable("dbtest.db", "test")

	db.insert("pging04", "t0","YEE", "noeem")
	db.insert("sging04", "t1","Vivamus integer nom", "nom")
	db.insert("sean", "t2","Vivamus sucipit taciti", "vivamus")
	db.insert("pging0444", "t0","YEE", "noeem")
	db.insert("sging04444", "t1","Vivamus integer nom", "nom")
	db.insert("sean444", "t2","Vivamus sucipit taciti", "vivamus")
	print(db.getEntryById(1))
	print(db.searchByKeyWord("vivamus", 1))
	db.popById(0)
	db._printall()

	

#are the keyword case sensitive
#only one keyword?
#check if username even exists in userpass table
# is blog inserted as a string? How to have paragraph spacing? line breaks (ie: <br>)? 

#what does each method return????
main()
