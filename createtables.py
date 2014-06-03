#!/usr/bin/python

import psycopg2
import sys


con = None

try:
     
    con = psycopg2.connect(database='testdb', user='postgres')    
    
    cur = con.cursor()
  
    cur.execute("CREATE TABLE cars(id INT PRIMARY KEY, name VARCHAR(20), price INT)")
    cur.execute("INSERT INTO cars VALUES(1,'Honda',46000)")
    cur.execute("INSERT INTO cars VALUES(2,'Toyota',27000)")
    cur.execute("INSERT INTO cars VALUES(3,'Subaru',32000)")
    cur.execute("INSERT INTO cars VALUES(4,'Volvo',42000)")
    cur.execute("INSERT INTO cars VALUES(5,'Bentley',350000)")
    cur.execute("INSERT INTO cars VALUES(6,'Citroen',21000)")
    cur.execute("INSERT INTO cars VALUES(7,'Cadillac',41400)")
    cur.execute("INSERT INTO cars VALUES(8,'Volkswagen',21600)")
    
    con.commit()
    

except psycopg2.DatabaseError, e:
    
    if con:
        con.rollback()
    
    print 'Error %s' % e    
    sys.exit(1)
    
    
finally:
    
    if con:
        con.close()