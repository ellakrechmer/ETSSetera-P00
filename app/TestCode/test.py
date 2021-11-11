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
	print(db.searchByKeyWord("Vivamus", 1))
	db._printall()

	#print(db.isAuthor("pging04", 0))
	print(db.getEntryById(0))
	db.popById(0)
	#print(db.isAuthor("pging04", 0))

	print(db.idExists(0))
	db.updatePost("I changed the title", "The quick brown fox jumped over the lazy dog.", "Keyword!", 1)
	print(db.getEntryById(1))
#are the keyword case sensitive
#only one keyword?
#check if username even exists in userpass table
# is blog inserted as a string? How to have paragraph spacing? line breaks (ie: <br>)? 

#what does each method return????
main()
