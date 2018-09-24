import sqlite3

class sqlDB:
    def __init__(self):
        self.conn = sqlite3.connect("gesture.db")
        self.c = self.conn.cursor()

    
    def search(self,val):
        self.c.execute('SELECT * FROM GEST WHERE value='+str(val))
        for row in self.c.fetchall():
            return(row[1])

        
