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
        
        self.initialize_data()

        self.tree_candidates = QTreeWidget()
        self.tree_candidates.setColumnCount(1)
        self.tree_candidates.setSelectionMode(QAbstractItemView.MultiSelection)
        self.tree_candidates.setHeaderLabel('可选章节')
        self.tree_candidates.clicked.connect(self.tree_candidates_clicked)
        self.tree_selected = QTreeWidget()
        self.tree_selected.setColumnCount(1)
        self.tree_selected.setSelectionMode(QAbstractItemView.MultiSelection)
        self.tree_selected.setHeaderLabel('已选章节')
        self.tree_selected.clicked.connect(self.tree_selected_clicked)
        self.btn_add = QPushButton('->')
        self.btn_add.clicked.connect(self.add_sections)
        self.btn_delete = QPushButton('<-')
        self.btn_delete.clicked.connect(self.delete_sections)
        self.btn_ok = QPushButton('选择完毕')
        self.btn_ok.clicked.connect(self.send_sections)

        mainlayout = QGridLayout()
        mainlayout.setSpacing(20)
        mainlayout.addWidget(self.tree_candidates, 0, 0, 6, 1)
        mainlayout.addWidget(self.btn_add, 2, 1,)
        mainlayout.addWidget(self.btn_delete, 3, 1)
        mainlayout.addWidget(self.tree_selected, 0, 2, 6, 1)
        mainlayout.addWidget(self.btn_ok,6,1)
        self.setLayout(mainlayout)

    # 获取数据库中的章节
    def initialize_data(self):
        searchstring = 'select * from chapters'
        self.chapters = mydb.search(searchstring)
        searchstring = 'select * from sections'
        self.sections = mydb.search(searchstring)
        self.sectionid_candidates = [item[0] for item in self.sections] # 候选章节id
        self.sectionid_selected = [] # 设置初始选择章节id为空
        self.chapter_selected_in_candidates_previously = [] # 候选树中上次选中的章节点，实现选中章则选中节效果
        self.chapter_selected_in_selected_previously = [] # 选中树中上次选中的章节点，实现选中章则选中节效果
        self.sectionid_selected_in_candidates = [] # 候选树中当前选中的节id
        self.sectionid_selected_in_selected = [] # 选中树中当前选中的节id

    def tree_candidates_clicked(self):
        currentItem = self.tree_candidates.currentItem()
        if currentItem.parent() == None: # 如果点击的是章
            if (not currentItem.isSelected()) and (currentItem in self.chapter_selected_in_candidates_previously): # 如果上次选中，这次没选中，则设置所有子节点未选中
                self.chapter_selected_in_candidates_previously.remove(currentItem)
                for i in range(currentItem.childCount()):
                    currentItem.child(i).setSelected(False)
            elif (currentItem.isSelected()) and (currentItem not in self.chapter_selected_in_candidates_previously): # 如果上次未选中，这次选中，则设置所有子节点选中
                self.chapter_selected_in_candidates_previously.append(currentItem)
                for i in range(currentItem.childCount()):
                    currentItem.child(i).setSelected(True)
        else: # 如果点击的是节
            if (not currentItem.isSelected()) and currentItem.parent().isSelected(): # 如果点击的节取消选中，且其父节点章被选中，则设置父节点为未选中
                currentItem.parent().setSelected(False)
                self.chapter_selected_in_candidates_previously.remove(currentItem.parent())
        items = self.tree_candidates.selectedItems()
        self.sectionid_selected_in_candidates = []
        for item in items:
            if item.parent() != None: # 不是父节点的话，加入id
                for section in self.sections:
                    if section[1] == item.text(0):
                        self.sectionid_selected_in_candidates.append(section[0])
                        break
            else:
                pass
        # self.update_candidate()

    def tree_selected_clicked(self):
        currentItem = self.tree_selected.currentItem()
        if currentItem.parent() == None: # 如果点击的是章
            if (not currentItem.isSelected()) and (currentItem in self.chapter_selected_in_selected_previously): # 如果上次选中，这次没选中，则设置所有子节点未选中
                self.chapter_selected_in_selected_previously.remove(currentItem)
                for i in range(currentItem.childCount()):
                    currentItem.child(i).setSelected(False)
            elif (currentItem.isSelected()) and (currentItem not in self.chapter_selected_in_selected_previously): # 如果上次未选中，这次选中，则设置所有子节点选中
                self.chapter_selected_in_selected_previously.append(currentItem)
                for i in range(currentItem.childCount()):
                    currentItem.child(i).setSelected(True)
        else: # 如果点击的是节
            if (not currentItem.isSelected()) and currentItem.parent().isSelected(): # 如果点击的节取消选中，且其父节点章被选中，则设置父节点为未选中
                currentItem.parent().setSelected(False)
                self.chapter_selected_in_selected_previously.remove(currentItem.parent())
        items = self.tree_selected.selectedItems()
        self.sectionid_selected_in_selected = []
        for item in items:
            if item.parent() != None: # 不是父节点的话，加入id
                for section in self.sections:
                    if section[1] == item.text(0):
                        self.sectionid_selected_in_selected.append(section[0])
                        break
            else:
                pass
        # self.update_selected()

    def add_sections(self):
        for i in self.sectionid_selected_in_candidates:
            self.sectionid_selected.append(i)
            self.sectionid_candidates.remove(i)
        self.sectionid_selected_in_candidates.clear()
        self.sectionid_selected.sort()
        self.update_candidate()
        self.update_selected()

    def delete_sections(self):
        for i in self.sectionid_selected_in_selected:
            self.sectionid_selected.remove(i)
            self.sectionid_candidates.append(i)
        self.sectionid_selected_in_selected.clear()
        self.sectionid_candidates.sort()
        self.update_candidate()
        self.update_selected()

    def update_candidate(self):
        self.tree_candidates.clear()
        chapterid = self.retrieve_chapterid_from_sectionid(self.sectionid_candidates)
        for i in range(len(chapterid)):
            root = QTreeWidgetItem(self.tree_candidates)
            root.setText(0, self.chapter_name_by_id(chapterid[i]))
            sectionid_in_this_chapter = self.find_sectionid_by_chapterid(chapterid[i], self.sectionid_candidates)
            for j in range(len(sectionid_in_this_chapter)):
                child = QTreeWidgetItem(root)
                child.setText(0, self.section_name_by_id(sectionid_in_this_chapter[j]))
            self.tree_candidates.addTopLevelItem(root)
    
    def update_selected(self):
        self.tree_selected.clear()
        chapterid = self.retrieve_chapterid_from_sectionid(self.sectionid_selected)
        for i in range(len(chapterid)):
            root = QTreeWidgetItem(self.tree_selected)
            root.setText(0, self.chapter_name_by_id(chapterid[i]))
            sectionid_in_this_chapter = self.find_sectionid_by_chapterid(chapterid[i], self.sectionid_selected)
            for j in range(len(sectionid_in_this_chapter)):
                child = QTreeWidgetItem(root)
                child.setText(0, self.section_name_by_id(sectionid_in_this_chapter[j]))
            root.setExpanded(True)
            self.tree_selected.addTopLevelItem(root)

    def retrieve_chapterid_from_sectionid(self, sectionid):
        chapterid = []
        for i in sectionid:
            j = 0
            while i != self.sections[j][0]:
                j += 1
            if self.sections[j][2] not in chapterid:
                chapterid.append(self.sections[j][2])
        chapterid.sort()
        return chapterid

    def chapter_name_by_id(self, chapterid):
        for item in self.chapters:
            if item[0] == chapterid:
                return item[1]

    def section_name_by_id(self, sectionid):
        for item in self.sections:
            if item[0] == sectionid:
                return item[1]

    def find_sectionid_by_chapterid(self, chapterid, sectionid): # 在给定的节id中找出指定章id的节
        sectionid_filtered = []
        for i in sectionid:
            if self.find_chapterid_by_sectionid(i) == chapterid:
                sectionid_filtered.append(i)
        sectionid_filtered.sort()
        return sectionid_filtered

    def find_chapterid_by_sectionid(self, sectionid): # 从给定的一个节id找章id
        for item in self.sections:
            if item[0] == sectionid:
                return item[2]

    def send_sections(self):
        self.signal.emit(self.sectionid_selected)
        self.close()

    def initialize(self, sectionid): # 从主界面传递的sectionid更新
        for i in sectionid:
            self.sectionid_selected.append(i)
            self.sectionid_candidates.remove(i)
        self.update_candidate()
        self.update_selected()
        
