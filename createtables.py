#!/usr/bin/python3.4

import psycopg2
import sys


con = None

try:
     
    con = psycopg2.connect(database='testdb', user='postgres')    
    
    cur = con.cursor()
  
    cur.execute("CREATE TABLE airlines(id INT PRIMARY KEY, name VARCHAR(100), name VARCHAR(100)")
    cur.execute("INSERT INTO airlines VALUES(1,'Air_Canada',Canada)")
    cur.execute("INSERT INTO airlines VALUES(2,'Lufthansa',Germany)")
    cur.execute("INSERT INTO airlines VALUES(3,'Aer_Lingus',Ireland)")
    cur.execute("INSERT INTO airlines VALUES(4,'Etihad',UAE)")
    cur.execute("INSERT INTO airlines VALUES(5,'Emirates',UAE)")
    cur.execute("INSERT INTO airlines VALUES(6,'Singapore_Airlines',Singapore)")
    cur.execute("INSERT INTO airlines VALUES(7,'Qantas',Australia)")
    cur.execute("INSERT INTO airlines VALUES(8,'Air_India',India)")
    
    con.commit()
    

except psycopg2.DatabaseError, e:
    
    if con:
        con.rollback()
    
    print 'Error %s' % e    
    sys.exit(1)
    
    
finally:
    
    if con:
        con.close()
