import sqlite3

courseID = "2801ICT"
database = sqlite3.connect('database.db')
c = database.cursor()
c.execute("SELECT * FROM Staff_Contact WHERE CourseID=?", (courseID,))
rows = c.fetchall()

for row in rows:
    print(row)