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

    def createPreview(self):
        num_schoice = len(self.schoiceid)
        num_mchoice = len(self.mchoiceid)
        num_tof = len(self.tofid)
        num_blank = len(self.blankid)
        num_calculation = len(self.calculationid)
        num_proof = len(self.proofid)
        self.webView = QWebEngineView()
        self.webView.setContextMenuPolicy(0) # 禁止右键菜单
        self.pageSourceContent = ''
        for i in range(num_schoice):
            thisquestion = mydb.get_schoice_by_id(self.schoiceid[i])
            if i == 0:
                self.pageSourceContent += ('</p><h2>单选题</h2>')
            self.pageSourceContent += myfun.format_questiondata_to_html(thisquestion, '单选题', str(i+1), fromdatabase=1)
        for i in range(num_mchoice):
            if i == 0:
                self.pageSourceContent += ('</p><h2>多选题</h2>')
            thisquestion = mydb.get_mchoice_by_id(self.mchoiceid[i])
            self.pageSourceContent += myfun.format_questiondata_to_html(thisquestion, '多选题', str(i+1), fromdatabase=1)
        for i in range(num_tof):
            if i == 0:
                self.pageSourceContent += ('</p><h2>判断题</h2>')
            thisquestion = mydb.get_tof_by_id(self.tofid[i])
            self.pageSourceContent += myfun.format_questiondata_to_html(thisquestion, '判断题', str(i+1), fromdatabase=1)
        for i in range(num_blank):
            if i == 0:
                self.pageSourceContent += ('</p><h2>填空题</h2>')
            thisquestion = mydb.get_blank_by_id(self.blankid[i])
            self.pageSourceContent += myfun.format_questiondata_to_html(thisquestion, '填空题', str(i+1), fromdatabase=1)
        for i in range(num_calculation):
            if i == 0:
                self.pageSourceContent += ('</p><h2>计算题</h2>')
            thisquestion = mydb.get_calculation_by_id(self.calculationid[i])
            self.pageSourceContent += myfun.format_questiondata_to_html(thisquestion, '计算题', str(i+1), fromdatabase=1)
        for i in range(num_proof):
            if i == 0:
                self.pageSourceContent += ('</p><h2>证明题</h2>')
            thisquestion = mydb.get_proof_by_id(self.proofid[i])
            self.pageSourceContent += myfun.format_questiondata_to_html(thisquestion, '证明题', str(i+1), fromdatabase=1)
        self.webView.setHtml(myfun.gethtml(self.webView.width(), self.pageSourceContent))
        
        preview_layout = QGridLayout()
        preview_layout.addWidget(self.webView)

        layout_options = QGridLayout()
        self.chk_solution = QCheckBox('包含解答')
        self.chk_solution.setChecked(True)
        self.chk_solution.clicked.connect(self.chk_solution_clicked)
        self.chk_random = QCheckBox('打乱题目顺序')
        self.chk_randomchoice = QCheckBox('选择题选项乱序')
        self.chk_randomchoice.setEnabled(False)
        self.chk_white = QCheckBox('主观题后留空')
        self.chk_white.setChecked(True)
        self.chk_white.clicked.connect(self.chk_white_clicked)
        self.chk_follow = QCheckBox('解答跟随小题')
        self.chk_follow.setChecked(False)
        self.chk_follow.clicked.connect(self.chk_follow_clicked)
        self.chk_distribute = QCheckBox('平均分配各节题目数量')
        self.chk_notsure = QCheckBox('不确定难度')
        self.chk_notsure.setChecked(True)
        self.chk_easy = QCheckBox('简单')
        self.chk_easy.setChecked(True)
        self.chk_medium = QCheckBox('中等')
        self.chk_medium.setChecked(True)
        self.chk_hard = QCheckBox('困难')
        self.chk_hard.setChecked(True)
        self.chk_hell = QCheckBox('地狱')
        self.chk_hell.setChecked(True)
        self.chk_save_id = QCheckBox('保存导出题目id')
        self.chk_save_id.setToolTip('保存导出的题目id，可以在自由选题导出标签页读取')
        layout_options.addWidget(self.chk_solution, 0, 0)
        layout_options.addWidget(self.chk_follow, 1, 0)
        layout_options.addWidget(self.chk_white, 2, 0)
        layout_options.addWidget(self.chk_random, 3, 0)
        layout_options.addWidget(self.chk_randomchoice, 4, 0)
        layout_options.addWidget(self.chk_notsure, 0, 1)
        layout_options.addWidget(self.chk_easy, 1, 1)
        layout_options.addWidget(self.chk_medium, 2, 1)
        layout_options.addWidget(self.chk_hard, 3, 1)
        layout_options.addWidget(self.chk_hell, 4, 1)
        layout_options.addWidget(self.chk_distribute, 1, 2)
        layout_options.addWidget(self.chk_save_id, 0, 2)
        layout_options.setHorizontalSpacing(10)

        mainlayout = QVBoxLayout()
        mainlayout.addLayout(preview_layout)
        mainlayout.addLayout(layout_options)

        self.setLayout(mainlayout)

    def chk_solution_clicked(self):
        self.chk_follow.setEnabled(self.chk_solution.isChecked())

    def chk_white_clicked(self):
        if self.chk_white.isChecked():
            self.chk_follow.setChecked(False)

    def chk_follow_clicked(self):
        if self.chk_follow.isChecked():
            self.chk_white.setChecked(False)
            
    def resizeEvent(self, event):
        self.webView.setHtml(myfun.gethtml(self.webView.width(), self.pageSourceContent))
    
    def showEvent(self, event):
        self.webView.setHtml(myfun.gethtml(self.webView.width(), self.pageSourceContent))