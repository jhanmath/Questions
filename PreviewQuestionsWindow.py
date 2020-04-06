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
        self.options = {'solution': True,
                        'random': True,
                        'randomchoice': False,
                        'white': True,
                        'follow': False,
                        'notsure': True,
                        'easy': True,
                        'medium': True,
                        'hard': True,
                        'hell': True}

    def createPreview(self):
        num_schoice = len(self.schoiceid)
        num_mchoice = len(self.mchoiceid)
        num_tof = len(self.tofid)
        num_blank = len(self.blankid)
        num_calculation = len(self.calculationid)
        num_proof = len(self.proofid)
        self.webView = QWebEngineView()
        self.webView.setContextMenuPolicy(0) # 禁止右键菜单
        self.pageSourceContent,_,_ = myfun.generate_html_body(self.schoiceid,self.mchoiceid,self.tofid,self.blankid,self.calculationid,self.proofid)

        self.webView.setHtml(myfun.gethtml(self.webView.width(), self.pageSourceContent))
        
        preview_layout = QGridLayout()
        preview_layout.addWidget(self.webView)

        layout_options = QGridLayout()
        self.chk_solution = QCheckBox('包含解答')
        self.chk_random = QCheckBox('打乱题目顺序')
        self.chk_randomchoice = QCheckBox('选择题选项乱序')
        self.chk_white = QCheckBox('主观题后留空')
        self.chk_follow = QCheckBox('解答跟随小题')
        self.chk_notsure = QCheckBox('未指定难度')
        self.chk_easy = QCheckBox('简单')
        self.chk_medium = QCheckBox('中等')
        self.chk_hard = QCheckBox('困难')
        self.chk_hell = QCheckBox('地狱')
        # self.chk_distribute = QCheckBox('平均分配各节题目数量')
        # self.chk_save_id = QCheckBox('保存导出题目id')
        # self.chk_save_id.setToolTip('保存导出的题目id，可以在自由选题导出标签页读取')
        self.chk_solution.setChecked(True)
        # self.chk_randomchoice.setEnabled(False)
        self.chk_white.setChecked(True)
        self.chk_follow.setChecked(False)
        self.chk_notsure.setChecked(True)
        self.chk_easy.setChecked(True)
        self.chk_medium.setChecked(True)
        self.chk_hard.setChecked(True)
        self.chk_hell.setChecked(True)
        self.chk_solution.clicked.connect(self.chk_solution_clicked)
        self.chk_white.clicked.connect(self.setoptions)
        self.chk_follow.clicked.connect(self.setoptions)
        self.chk_random.clicked.connect(self.setoptions)
        self.chk_randomchoice.clicked.connect(self.setoptions)
        self.chk_notsure.clicked.connect(self.setoptions)
        self.chk_easy.clicked.connect(self.setoptions)
        self.chk_medium.clicked.connect(self.setoptions)
        self.chk_hard.clicked.connect(self.setoptions)
        self.chk_hell.clicked.connect(self.setoptions)
        self.setoptions()
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
        layout_options.setHorizontalSpacing(10)

        layout_btn = QHBoxLayout()
        self.btn_export_to_latex = QPushButton('导出LaTeX')
        self.btn_export_to_latex.clicked.connect(self.export_questions_to_latex)
        self.btn_compile = QPushButton('导出并编译')
        self.btn_compile.setEnabled(False)
        self.btn_export_to_html = QPushButton('导出Html')
        self.btn_export_to_html.clicked.connect(self.export_questions_to_html)
        layout_btn.addWidget(self.btn_export_to_latex)
        layout_btn.addWidget(self.btn_compile)
        layout_btn.addWidget(self.btn_export_to_html)

        mainlayout = QVBoxLayout()
        mainlayout.addLayout(preview_layout)
        mainlayout.addLayout(layout_options)
        mainlayout.addLayout(layout_btn)

        self.setLayout(mainlayout)

    def chk_solution_clicked(self):
        self.chk_follow.setEnabled(self.chk_solution.isChecked())
        self.setoptions()

    # def chk_white_clicked(self):
    #     if self.chk_white.isChecked():
    #         self.chk_follow.setChecked(False)
    #     self.setoptions()

    # def chk_follow_clicked(self):
    #     if self.chk_follow.isChecked():
    #         self.chk_white.setChecked(False)
    #     self.setoptions()
            
    def resizeEvent(self, event):
        self.webView.setHtml(myfun.gethtml(self.webView.width(), self.pageSourceContent))
    
    def showEvent(self, event):
        self.webView.setHtml(myfun.gethtml(self.webView.width(), self.pageSourceContent))
    
    def setoptions(self):
        self.options['easy'] = self.chk_easy.isChecked()
        self.options['follow'] = self.chk_follow.isChecked()
        self.options['hard'] = self.chk_hard.isChecked()
        self.options['hell'] = self.chk_hell.isChecked()
        self.options['medium'] = self.chk_medium.isChecked()
        self.options['notsure'] = self.chk_notsure.isChecked()
        self.options['random'] = self.chk_random.isChecked()
        self.options['randomchoice'] = self.chk_randomchoice.isChecked()
        self.options['white'] = self.chk_white.isChecked()
        self.options['solution'] = self.chk_solution.isChecked()

    def export_questions_to_latex(self):
        result = myfun.export_to_latex(self.schoiceid,self.mchoiceid,self.tofid,self.blankid,self.calculationid,self.proofid,self.options)
        if result[0]:
            QMessageBox.about(self, u'通知', (u'导出文件 %s.tex 成功！' % (result[1])))
        else:
            QMessageBox.about(self, u'错误', u'导出失败！')
            print(result[1])

    def export_questions_to_html(self):
        result = myfun.export_to_html(self.schoiceid,self.mchoiceid,self.tofid,self.blankid,self.calculationid,self.proofid,self.options)
        if result[0]:
            QMessageBox.about(self, u'通知', (u'导出文件 %s.html 成功！' % (result[1])))
        else:
            QMessageBox.about(self, u'错误', u'导出失败！')
            print(result[1])