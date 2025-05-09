import sqlite3


# this is the structure of mydb.db
my_db = sqlite3.connect("mydb.db")
c = my_db.cursor()
c.execute(
    """CREATE TABLE IF NOT EXISTS student
          (id INTEGER UNIQUE,
          fname TEXT NOT NULL,
          lname TEXT NOT NULL,
          email TEXT NOT NULL UNIQUE,
          password TEXT NOT NULL
              )"""
)
c.execute(
    """CREATE TABLE IF NOT EXISTS lecturer
          (id INTEGER UNIQUE,
          fname TEXT NOT NULL,
          lname TEXT NOT NULL,
          email TEXT NOT NULL UNIQUE,
          password TEXT NOT NULL
              )"""
)

c.execute(
    """CREATE TABLE IF NOT EXISTS enrolled
          (id INTEGER UNIQUE,
          course1 TEXT,
          course2 TEXT,
          course3 TEXT,
          course4 TEXT
          )"""
)

c.execute(
    """CREATE TABLE IF NOT EXISTS taught
          (id INTEGER UNIQUE,
          course1 TEXT,
          course2 TEXT,
          course3 TEXT,
          course4 TEXT
          )"""
)

c.execute(
    """CREATE TABLE IF NOT EXISTS admin
          (name TEXT NOT NULL,
          email TEXT NOT NULL UNIQUE,
          password TEXT NOT NULL
          )"""
)


my_db.commit()
c.close()
my_db.close()