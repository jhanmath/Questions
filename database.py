from PyQt5.QtSql import QSqlQuery, QSqlDatabase
from PyQt5.QtCore import QDir
import os

def open_database():
    global dbpath
    if QSqlDatabase.contains('qt_sql_default_connection'):
        db = QSqlDatabase.database('qt_sql_default_connection')
    else:
        db = QSqlDatabase.addDatabase('QSQLITE')
    db.setDatabaseName(dbpath)
    # 打开数据库
    db.open()
    return db

def close_database(db):
    db.close()

def search(searchstring):
    global dbpath
    db = open_database()
    q = QSqlQuery()
    if q.exec(searchstring):
        searchresult = []
        while q.next():
            rowdata = []
            i = 0
            while q.value(i) is not None:
                rowdata.append(q.value(i))
                i = i + 1
            searchresult.append(rowdata)
        close_database(db)
        return searchresult
    close_database(db)
    print(q.lastError().text())
    return False

def insert(insertstring):
    db = open_database()
    q = QSqlQuery()
    print(insertstring)
    if q.exec(insertstring):
        close_database(db)
        return True
    else:
        print(q.lastError().text())
        close_database(db)
        return False

# dbpath = os.path.dirname(os.path.abspath(__file__)) + '/db/database.db'
dbpath = QDir.currentPath() + r'/db/questions.db'
print(dbpath)

# database = QSqlDatabase.addDatabase('QSQLITE')
# database.setDatabaseName('./db/questions.db')
# database.open()

