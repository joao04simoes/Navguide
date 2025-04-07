import sqlite3


def createDataBase():
    conn = sqlite3.connect("dataBase.db")
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS sections (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        x INTEGER NOT NULL,
        y INTEGER NOT NULL
    )
    ''')

    conn.commit()
    conn.close()


def addSectionToDataBase(name, x, y):
    conn = sqlite3.connect("dataBase.db")
    cursor = conn.cursor()
    cursor.execute(
        ''' INSERT INTO sections (name, x, y ) VALUES(?,?,?)''', (name, x, y))
    conn.commit()
    conn.close()


def getSectionsFromDataBase():
    conn = sqlite3.connect("dataBase.db")
    cursor = conn.cursor()
    cursor.execute(
        ''' SELECT * FROM sections''')
    sections = cursor.fetchall()
    conn.close()
    return sections
