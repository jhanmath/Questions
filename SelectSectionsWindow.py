# -*- coding: utf-8 -*-

'''
    选择章节界面
'''

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import database as mydb

class SelectSections(QWidget):
    signal = pyqtSignal(list)

    def __init__(self, parent=None):
        super(SelectSections, self).__init__(parent)
        # self.setFixedSize(900, 800)
        self.resize(900,500)
        self.setWindowTitle("选择章节")
        self.setWindowModality(Qt.ApplicationModal)
        self.index_candidates = []
        self.index_selected = [] # 设置初始选择章节为空
    
        self.list_candidate = QListWidget()
        self.retrieve_list_section()

        self.list_candidate.setSelectionMode(QAbstractItemView.MultiSelection)
        self.list_selected = QListWidget()
        self.list_selected.setSelectionMode(QAbstractItemView.MultiSelection)
        self.btn_add = QPushButton('->')
        self.btn_add.clicked.connect(self.add_sections)
        self.btn_delete = QPushButton('<-')
        self.btn_delete.clicked.connect(self.delete_sections)
        self.btn_ok = QPushButton('选择完毕')
        self.btn_ok.clicked.connect(self.send_sections)

        mainlayout = QGridLayout()
        mainlayout.setSpacing(20)
        mainlayout.addWidget(self.list_candidate, 0, 0, 6, 1)
        mainlayout.addWidget(self.btn_add, 2, 1,)
        mainlayout.addWidget(self.btn_delete, 3, 1)
        mainlayout.addWidget(self.list_selected, 0, 2, 6, 1)
        mainlayout.addWidget(self.btn_ok,6,1)
        self.setLayout(mainlayout)

    # 获取数据库中的章节
    def retrieve_list_section(self):
        searchstring = 'select * from sections'
        self.sections = mydb.search(searchstring)
	
    def add_sections(self):
        items_changing = self.list_candidate.selectedItems()
        if not items_changing: return
        index_changing = []
        for item in items_changing:
            i = 0
            while self.sections[i][1]!=item.text():
                i = i + 1
            index_changing.append(i)
        for index in index_changing:
            self.index_candidates.remove(index)
            self.index_selected.append(index)
        self.index_candidates.sort()
        self.index_selected.sort()
        self.update_candidate()
        self.update_selected()

    def delete_sections(self):
        items_changing = self.list_selected.selectedItems()
        if not items_changing: return
        index_changing = []
        for item in items_changing:
            i = 0
            while self.sections[i][1]!=item.text():
                i = i + 1
            index_changing.append(i)
        for index in index_changing:
            self.index_selected.remove(index)
            self.index_candidates.append(index)
        self.index_candidates.sort()
        self.index_selected.sort()
        self.update_candidate()
        self.update_selected()

    def update_candidate(self):
        self.list_candidate.clear()
        for index in self.index_candidates:
            self.list_candidate.addItem(self.sections[index][1])
    
    def update_selected(self):
        self.list_selected.clear()
        for index in self.index_selected:
            self.list_selected.addItem(self.sections[index][1])

    def send_sections(self):
        sectionid = []
        for index in self.index_selected:
            sectionid.append(self.sections[index][0])
        self.signal.emit(sectionid)
        self.close()
        # self.destroy()
    def initialize(self, sectionid):
        self.index_candidates = []
        self.index_selected = []
        for i in range(len(self.sections)):
            if self.sections[i][0] in sectionid:
                self.index_selected.append(i)
            else:
                self.index_candidates.append(i)
        self.update_candidate()
        self.update_selected()
        
