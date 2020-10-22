from PyQt5.QtSql import QSqlQuery, QSqlDatabase
from PyQt5.QtCore import QDir
import os

class DataBase:
    dbpath = ''
    def __init__(self,path):
        self.dbpath = path

    def open_database(self):
        if QSqlDatabase.contains('qt_sql_default_connection'):
            db = QSqlDatabase.database('qt_sql_default_connection')
        else:
            db = QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName(self.dbpath)
        # 打开数据库
        db.open()
        return db

    def close_database(self, db):
        db.close()

    def search(self, searchstring):
        db = self.open_database()
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
            self.close_database(db)
            return searchresult
        self.close_database(db)
        print(q.lastError().text())
        return False

    def insert(self, insertstring):
        db = self.open_database()
        q = QSqlQuery()
        print(insertstring)
        if q.exec(insertstring):
            self.close_database(db)
            return True
        else:
            print(q.lastError().text())
            self.close_database(db)
            return False

    def get_schoice_by_id(self, id):
        searchstring = ('select "question", "A", "B", "C", "D", "answer", "explain", "section", "difficulty", "source" from schoice where id=' + str(id))
        searchresult = self.search(searchstring)
        schoice = [i for i in searchresult[0]]
        return schoice

    def get_mchoice_by_id(self, id):
        searchstring = ('select "question", "A", "B", "C", "D", "pos_A", "pos_B", "pos_C", "pos_D", "explain", "section", "difficulty", "source" from mchoice where id=' + str(id))
        searchresult = self.search(searchstring)
        mchoice = [i for i in searchresult[0]]
        return mchoice

    def get_tof_by_id(self, id):
        searchstring = ('select "question", "correct", "explain", "section", "difficulty", "source" from tof where id=' + str(id))
        searchresult = self.search(searchstring)
        tof = [i for i in searchresult[0]]
        return tof

    def get_blank_by_id(self, id):
        searchstring = ('select "question", "answer1", "answer2", "answer3", "answer4", "explain", "section", "difficulty", "source" from blank where id=' + str(id))
        searchresult = self.search(searchstring)
        blank = [i for i in searchresult[0]]
        return blank

    def get_calculation_by_id(self, id):
        searchstring = ('select "question", "answer", "section", "difficulty", "source" from calculation where id=' + str(id))
        searchresult = self.search(searchstring)
        calculation = [i for i in searchresult[0]]
        return calculation

    def get_proof_by_id(self, id):
        searchstring = ('select "question", "answer", "section", "difficulty", "source" from proof where id=' + str(id))
        searchresult = self.search(searchstring)
        proof = [i for i in searchresult[0]]
        return proof

    def build_structure(self): # 初始化新数据库
        createstring = '''CREATE TABLE "dbname" (
                            "id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                            "name"	TEXT NOT NULL
                        )'''
        self.insert(createstring)
        createstring = '''CREATE TABLE "users" (
                            "id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                            "name"	TEXT NOT NULL
                        )'''
        self.insert(createstring)
        createstring = '''CREATE TABLE "difficulties" (
                            "id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                            "difficulty"	TEXT NOT NULL
                        )'''
        self.insert(createstring)
        createstring = '''CREATE TABLE "chapters" (
                            "id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                            "chapter"	TEXT NOT NULL
                        )'''
        self.insert(createstring)
        createstring = '''CREATE TABLE "sections" (
                            "id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                            "section"	TEXT NOT NULL,
                            "chapter"	INTEGER NOT NULL,
                            FOREIGN KEY("chapter") REFERENCES "chapters"("id")
                        )'''
        self.insert(createstring)
        createstring = '''CREATE TABLE "sources" (
                            "id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                            "source"	TEXT NOT NULL
                        )'''
        self.insert(createstring)
        createstring = '''CREATE TABLE "schoice" (
                            "id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                            "question"	TEXT NOT NULL,
                            "A"	TEXT NOT NULL,
                            "B"	TEXT NOT NULL,
                            "C"	TEXT,
                            "D"	TEXT,
                            "answer"	TEXT NOT NULL CHECK(answer='A' or answer='B' or answer='C' or answer='D'),
                            "explain"	TEXT,
                            "section"	INTEGER NOT NULL DEFAULT 1,
                            "difficulty"	INTEGER NOT NULL DEFAULT 1,
                            "source"	INTEGER NOT NULL DEFAULT 1,
                            "inputuser"	INTEGER NOT NULL DEFAULT 1,
                            "inputdate"	TEXT NOT NULL,
                            "modifyuser"	INTEGER,
                            "modifydate"	TEXT,
                            FOREIGN KEY("difficulty") REFERENCES "difficulties"("id"),
                            FOREIGN KEY("source") REFERENCES "sources"("id"),
                            FOREIGN KEY("inputuser") REFERENCES "users"("id"),
                            FOREIGN KEY("section") REFERENCES "sections"("id")
                        )'''
        self.insert(createstring)
        createstring = '''CREATE TABLE "mchoice" (
                            "id"	INTEGER NOT NULL UNIQUE,
                            "question"	TEXT NOT NULL,
                            "A"	TEXT NOT NULL,
                            "B"	TEXT NOT NULL,
                            "C"	TEXT,
                            "D"	TEXT,
                            "pos_A"	INTEGER NOT NULL DEFAULT 0,
                            "pos_B"	INTEGER NOT NULL DEFAULT 0,
                            "pos_C"	INTEGER NOT NULL DEFAULT 0,
                            "pos_D"	INTEGER NOT NULL DEFAULT 0,
                            "explain"	TEXT,
                            "section"	INTEGER NOT NULL,
                            "difficulty"	INTEGER NOT NULL DEFAULT 1,
                            "source"	INTEGER NOT NULL DEFAULT 1,
                            "inputuser"	INTEGER NOT NULL DEFAULT 1,
                            "inputdate"	TEXT NOT NULL,
                            "modifyuser"	INTEGER,
                            "modifydate"	TEXT,
                            PRIMARY KEY("id" AUTOINCREMENT),
                            FOREIGN KEY("section") REFERENCES "sections"("id"),
                            FOREIGN KEY("difficulty") REFERENCES "difficulties"("id"),
                            FOREIGN KEY("source") REFERENCES "sources"("id")
                        )'''
        self.insert(createstring)
        createstring = '''CREATE TABLE "tof" (
                            "id"	INTEGER NOT NULL UNIQUE,
                            "question"	TEXT NOT NULL,
                            "correct"	INTEGER NOT NULL CHECK("correct" IN (0, 1)),
                            "explain"	TEXT,
                            "section"	INTEGER NOT NULL,
                            "difficulty"	INTEGER NOT NULL DEFAULT 1,
                            "source"	INTEGER NOT NULL DEFAULT 1,
                            "inputuser"	INTEGER NOT NULL DEFAULT 1,
                            "inputdate"	TEXT NOT NULL,
                            "modifyuser"	INTEGER,
                            "modifydate"	TEXT,
                            PRIMARY KEY("id" AUTOINCREMENT),
                            FOREIGN KEY("difficulty") REFERENCES "difficulties"("id"),
                            FOREIGN KEY("section") REFERENCES "sections"("id"),
                            FOREIGN KEY("source") REFERENCES "sources"("id")
                        )'''
        self.insert(createstring)
        createstring = '''CREATE TABLE "blank" (
                            "id"	INTEGER NOT NULL UNIQUE,
                            "question"	TEXT,
                            "answer1"	TEXT,
                            "answer2"	TEXT,
                            "answer3"	TEXT,
                            "answer4"	TEXT,
                            "explain"	TEXT,
                            "section"	INTEGER NOT NULL,
                            "difficulty"	INTEGER NOT NULL DEFAULT 1,
                            "source"	INTEGER NOT NULL DEFAULT 1,
                            "inputuser"	INTEGER NOT NULL DEFAULT 1,
                            "inputdate"	TEXT NOT NULL,
                            "modifyuser"	INTEGER,
                            "modifydate"	TEXT,
                            PRIMARY KEY("id" AUTOINCREMENT),
                            FOREIGN KEY("difficulty") REFERENCES "difficulties"("id"),
                            FOREIGN KEY("source") REFERENCES "sources"("id"),
                            FOREIGN KEY("section") REFERENCES "sections"("id")
                        )'''
        self.insert(createstring)
        createstring = '''CREATE TABLE "calculation" (
                            "id"	INTEGER NOT NULL UNIQUE,
                            "question"	TEXT NOT NULL,
                            "answer"	TEXT,
                            "section"	INTEGER NOT NULL,
                            "difficulty"	INTEGER NOT NULL DEFAULT 1,
                            "source"	INTEGER NOT NULL DEFAULT 1,
                            "inputuser"	INTEGER NOT NULL DEFAULT 1,
                            "inputdate"	TEXT NOT NULL,
                            "modifyuser"	INTEGER,
                            "modifydate"	TEXT,
                            PRIMARY KEY("id" AUTOINCREMENT),
                            FOREIGN KEY("section") REFERENCES "sections"("id"),
                            FOREIGN KEY("difficulty") REFERENCES "difficulties"("id"),
                            FOREIGN KEY("source") REFERENCES "sources"("id")
                        )'''
        self.insert(createstring)
        createstring = '''CREATE TABLE "proof" (
                            "id"	INTEGER NOT NULL UNIQUE,
                            "question"	TEXT NOT NULL,
                            "answer"	TEXT,
                            "section"	INTEGER NOT NULL,
                            "difficulty"	INTEGER NOT NULL DEFAULT 1,
                            "source"	INTEGER NOT NULL DEFAULT 1,
                            "inputuser"	INTEGER NOT NULL DEFAULT 1,
                            "inputdate"	TEXT NOT NULL,
                            "modifyuser"	INTEGER,
                            "modifydate"	TEXT,
                            PRIMARY KEY("id" AUTOINCREMENT),
                            FOREIGN KEY("difficulty") REFERENCES "difficulties"("id"),
                            FOREIGN KEY("source") REFERENCES "sources"("id"),
                            FOREIGN KEY("section") REFERENCES "sections"("id")
                        )'''
        self.insert(createstring)