import sqlite3

import sqlite3

conn = sqlite3.connect('C:\\Users\\Rex\\PycharmProjects\\pythonProject\\Demoproject\\db.sqlite3_33')
print ("Opened database successfully");

cursor = conn.execute("SELECT * from User")
for row in cursor:
   print ("ID = ", row[0])


print ("Operation done successfully");
conn.close()