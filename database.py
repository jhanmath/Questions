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

def get_schoice_by_id(id):
    searchstring = ('select "question", "A", "B", "C", "D", "answer", "explain", "section", "difficulty", "source" from schoice where id=' + str(id))
    searchresult = search(searchstring)
    schoice = [i for i in searchresult[0]]
    return schoice

def get_mchoice_by_id(id):
    searchstring = ('select "question", "A", "B", "C", "D", "pos_A", "pos_B", "pos_C", "pos_D", "explain", "section", "difficulty", "source" from mchoice where id=' + str(id))
    searchresult = search(searchstring)
    mchoice = [i for i in searchresult[0]]
    return mchoice

def get_tof_by_id(id):
    searchstring = ('select "question", "correct", "explain", "section", "difficulty", "source" from tof where id=' + str(id))
    searchresult = search(searchstring)
    tof = [i for i in searchresult[0]]
    return tof

def get_blank_by_id(id):
    searchstring = ('select "question", "answer1", "answer2", "answer3", "answer4", "explain", "section", "difficulty", "source" from blank where id=' + str(id))
    searchresult = search(searchstring)
    blank = [i for i in searchresult[0]]
    return blank

def get_calculation_by_id(id):
    searchstring = ('select "question", "answer", "section", "difficulty", "source" from calculation where id=' + str(id))
    searchresult = search(searchstring)
    calculation = [i for i in searchresult[0]]
    return calculation

def get_proof_by_id(id):
    searchstring = ('select "question", "answer", "section", "difficulty", "source" from proof where id=' + str(id))
    searchresult = search(searchstring)
    proof = [i for i in searchresult[0]]
    return proof