# -*- coding: utf-8 -*-

'''
    添加预览选中问题界面
'''

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import QWebEngineView
import database as mydb
import myfunctions as myfun
import sys

class PreviewQuestions(QWidget):
    def __init__(self, parent=None):
        super(PreviewQuestions, self).__init__(parent)
        # self.setFixedSize(900, 800)
        self.resize(900,800)
        self.setWindowTitle("预览选中的问题")
        self.setWindowModality(Qt.ApplicationModal)
        self.schoiceid = [25,26] # 自由选择问题导出标签页中待导出的所有单选题id
        self.mchoiceid = [] # 自由选择问题导出标签页中待导出的所有多选题id
        self.tofid = [] # 自由选择问题导出标签页中待导出的所有判断题id
        self.blankid = [] # 自由选择问题导出标签页中待导出的所有填空题id
        self.calculationid = [] # 自由选择问题导出标签页中待导出的所有计算题id
        self.proofid = [] # 自由选择问题导出标签页中待导出的所有证明题id

    # 调整窗口大小事件
    # def resizeEvent(self, event):#调整窗口尺寸时，该方法被持续调用。event参数包含QResizeEvent类的实例，通过该类的下列方法获得窗口信息：
    #     self.update_preview()

    def createScrollWidget(self):
        self.scrolllayout = QGridLayout()
        num_schoice = len(self.schoiceid)
        num_mchoice = len(self.mchoiceid)
        num_tof = len(self.tofid)
        num_blank = len(self.blankid)
        num_calculation = len(self.calculationid)
        num_proof = len(self.proofid)
        height = 200
        for i in range(num_schoice):
            self.webView = QWebEngineView()
            self.webView.setFixedHeight(height)
            self.webView.setContextMenuPolicy(0) # 禁止右键菜单
            thisquestion = mydb.get_schoice_by_id(self.schoiceid[i])
            pageSourceContent = myfun.format_questiondata_to_html(thisquestion, '单选题', str(i+1), fromdatabase=1)
            if i == 0:
                pageSourceContent = ('</p><h2>单选题</h2>') + pageSourceContent
            self.webView.setHtml(myfun.gethtml(self.webView.width(), pageSourceContent))
            self.chk = QCheckBox()
            self.chk.clicked.connect(self.clicked)
            self.chk.setChecked(True)
            self.scrolllayout.addWidget(self.webView, i, 0)
            self.scrolllayout.addWidget(self.chk, i, 1)
        for i in range(num_mchoice):
            self.webView = QWebEngineView()
            self.webView.setFixedHeight(height)
            self.webView.setContextMenuPolicy(0) # 禁止右键菜单
            thisquestion = mydb.get_mchoice_by_id(self.mchoiceid[i])
            pageSourceContent = myfun.format_questiondata_to_html(thisquestion, '多选题', str(i+1), fromdatabase=1)
            if i == 0:
                pageSourceContent = ('</p><h2>多选题</h2>') + pageSourceContent
            self.webView.setHtml(myfun.gethtml(self.webView.width(), pageSourceContent))
            self.chk = QCheckBox()
            self.chk.clicked.connect(self.clicked)
            self.chk.setChecked(True)
            self.scrolllayout.addWidget(self.webView, i+num_schoice, 0)
            self.scrolllayout.addWidget(self.chk, i+num_schoice, 1)
        for i in range(num_tof):
            self.webView = QWebEngineView()
            self.webView.setFixedHeight(height)
            self.webView.setContextMenuPolicy(0) # 禁止右键菜单
            thisquestion = mydb.get_tof_by_id(self.tofid[i])
            pageSourceContent = myfun.format_questiondata_to_html(thisquestion, '判断题', str(i+1), fromdatabase=1)
            if i == 0:
                pageSourceContent = ('</p><h2>判断题</h2>') + pageSourceContent
            self.webView.setHtml(myfun.gethtml(self.webView.width(), pageSourceContent))
            self.chk = QCheckBox()
            self.chk.clicked.connect(self.clicked)
            self.chk.setChecked(True)
            self.scrolllayout.addWidget(self.webView, i+num_schoice+num_mchoice, 0)
            self.scrolllayout.addWidget(self.chk, i+num_schoice+num_mchoice, 1)
        for i in range(num_blank):
            self.webView = QWebEngineView()
            self.webView.setFixedHeight(height)
            self.webView.setContextMenuPolicy(0) # 禁止右键菜单
            thisquestion = mydb.get_blank_by_id(self.blankid[i])
            pageSourceContent = myfun.format_questiondata_to_html(thisquestion, '填空题', str(i+1), fromdatabase=1)
            if i == 0:
                pageSourceContent = ('</p><h2>填空题</h2>') + pageSourceContent
            self.webView.setHtml(myfun.gethtml(self.webView.width(), pageSourceContent))
            self.chk = QCheckBox()
            self.chk.clicked.connect(self.clicked)
            self.chk.setChecked(True)
            self.scrolllayout.addWidget(self.webView, i+num_schoice+num_mchoice+num_tof, 0)
            self.scrolllayout.addWidget(self.chk, i+num_schoice+num_mchoice+num_tof, 1)
        for i in range(num_calculation):
            self.webView = QWebEngineView()
            self.webView.setFixedHeight(height)
            self.webView.setContextMenuPolicy(0) # 禁止右键菜单
            thisquestion = mydb.get_calculation_by_id(self.calculationid[i])
            pageSourceContent = myfun.format_questiondata_to_html(thisquestion, '计算题', str(i+1), fromdatabase=1)
            if i == 0:
                pageSourceContent = ('</p><h2>计算题</h2>') + pageSourceContent
            self.webView.setHtml(myfun.gethtml(self.webView.width(), pageSourceContent))
            self.chk = QCheckBox()
            self.chk.clicked.connect(self.clicked)
            self.chk.setChecked(True)
            self.scrolllayout.addWidget(self.webView, i+num_schoice+num_mchoice+num_tof+num_blank, 0)
            self.scrolllayout.addWidget(self.chk, i+num_schoice+num_mchoice+num_tof+num_blank, 1)
        for i in range(num_proof):
            self.webView = QWebEngineView()
            self.webView.setFixedHeight(height)
            self.webView.setContextMenuPolicy(0) # 禁止右键菜单
            thisquestion = mydb.get_proof_by_id(self.proofid[i])
            pageSourceContent = myfun.format_questiondata_to_html(thisquestion, '证明题', str(i+1), fromdatabase=1)
            if i == 0:
                pageSourceContent = ('</p><h2>证明题</h2>') + pageSourceContent
            self.webView.setHtml(myfun.gethtml(self.webView.width(), pageSourceContent))
            self.chk = QCheckBox()
            self.chk.clicked.connect(self.clicked)
            self.chk.setChecked(True)
            self.scrolllayout.addWidget(self.webView, i+num_schoice+num_mchoice+num_tof+num_blank+num_calculation, 0)
            self.scrolllayout.addWidget(self.chk, i+num_schoice+num_mchoice+num_tof+num_blank+num_calculation, 1)
        
        self.scrolllayout.setColumnStretch(0, 100)
        self.scrolllayout.setColumnStretch(1, 1)

        self.scroll = QWidget()
        self.scroll.setLayout(self.scrolllayout)

        self.scrollarea = QScrollArea()
        self.scrollarea.setWidget(self.scroll)
        self.scrollarea.setWidgetResizable(True)

        mainlayout = QVBoxLayout()
        mainlayout.addWidget(self.scrollarea)

        self.setLayout(mainlayout)

    def clicked(self):
        self.schoiceid_status = []
        self.mchoiceid_status = []
        self.tofid_status = []
        self.blankid_status = []
        self.calculationid_status = []
        self.proofid_status = []
        endindex_schoice = len(self.schoiceid)
        endindex_mchoice = endindex_schoice + len(self.mchoiceid)
        endindex_tof = endindex_mchoice + len(self.tofid)
        endindex_blank = endindex_tof + len(self.blankid)
        endindex_calculation = endindex_tof + len(self.calculationid)
        endindex_proof = endindex_calculation + len(self.proofid)
        for i in range(endindex_schoice):
            item = self.scrolllayout.itemAtPosition(i, 1)
            widget = item.widget()
            self.schoiceid_status.append(widget.isChecked())
        for i in range(endindex_schoice, endindex_mchoice):
            item = self.scrolllayout.itemAtPosition(i, 1)
            widget = item.widget()
            self.mchoiceid_status.append(widget.isChecked())
        for i in range(endindex_mchoice, endindex_tof):
            item = self.scrolllayout.itemAtPosition(i, 1)
            widget = item.widget()
            self.tofid_status.append(widget.isChecked())
        for i in range(endindex_tof, endindex_blank):
            item = self.scrolllayout.itemAtPosition(i, 1)
            widget = item.widget()
            self.blankid_status.append(widget.isChecked())
        for i in range(endindex_blank, endindex_calculation):
            item = self.scrolllayout.itemAtPosition(i, 1)
            widget = item.widget()
            self.calculationid_status.append(widget.isChecked())
        for i in range(endindex_calculation, endindex_proof):
            item = self.scrolllayout.itemAtPosition(i, 1)
            widget = item.widget()
            self.proofid_status.append(widget.isChecked())
        print(self.schoiceid_status)
