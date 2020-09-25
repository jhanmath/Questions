# -*- coding: utf-8 -*-

'''
    添加预览选中问题界面
'''

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import QWebEngineView
import myfunctions as myfun
import sys

class PreviewQuestions(QWidget):
    def __init__(self, db, parent=None):
        super(PreviewQuestions, self).__init__(parent)
        # self.setFixedSize(900, 800)
        self.mydb = db
        self.resize(900, 700)
        self.setWindowTitle("预览选中的问题")
        self.setWindowModality(Qt.ApplicationModal)
        self.schoiceid = [] # 预览窗口中所有单选题id
        self.mchoiceid = [] # 预览窗口中所有多选题id
        self.tofid = [] # 预览窗口中所有判断题id
        self.blankid = [] # 预览窗口中所有填空题id
        self.calculationid = [] # 预览窗口中所有计算题id
        self.proofid = [] # 预览窗口中所有证明题id
        self.schoice_seq = [] # 预览窗口中所有单选题选项顺序
        self.mchoice_seq = [] # 预览窗口中所有多选题选项顺序
        self.options = {'solution': True,
                        'random': True,
                        'randomchoice': False,
                        'white': True,
                        'follow': False,
                        'notsure': True,
                        'easy': True,
                        'medium': True,
                        'hard': True,
                        'hell': True,
                        'title': ''}

    def createPreview(self):
        num_schoice = len(self.schoiceid)
        num_mchoice = len(self.mchoiceid)
        num_tof = len(self.tofid)
        num_blank = len(self.blankid)
        num_calculation = len(self.calculationid)
        num_proof = len(self.proofid)
        self.webView = QWebEngineView()
        self.webView.setContextMenuPolicy(0) # 禁止右键菜单
        self.pageSourceContent,_,_ = myfun.generate_html_body(self.mydb,self.schoiceid,self.mchoiceid,self.tofid,self.blankid,self.calculationid,self.proofid,self.options,schoice_choiceseq=self.schoice_seq,mchoice_choiceseq=self.mchoice_seq)

        self.webView.setHtml(myfun.gethtml(self.webView.width(), self.pageSourceContent))
        
        preview_layout = QGridLayout()
        preview_layout.addWidget(self.webView)

        layout_options = QGridLayout()
        self.chk_solution = QCheckBox('包含解答')
        self.chk_solution.setToolTip('默认解答在所有题目之后显示')
        self.chk_random = QCheckBox('打乱题目顺序')
        self.chk_randomchoice = QCheckBox('打乱选择题选项顺序')
        self.chk_white = QCheckBox('主观题后留空')
        self.chk_follow = QCheckBox('解答跟随小题')
        self.chk_notsure = QCheckBox('未知难度')
        self.chk_easy = QCheckBox('简单难度')
        self.chk_medium = QCheckBox('中等难度')
        self.chk_hard = QCheckBox('困难难度')
        self.chk_hell = QCheckBox('地狱难度')
        # self.chk_distribute = QCheckBox('平均分配各节题目数量')
        # self.chk_save_id = QCheckBox('保存导出题目id')
        # self.chk_save_id.setToolTip('保存导出的题目id，可以在自由选题导出标签页读取')
        self.chk_solution.setChecked(self.options['solution'])
        # self.chk_randomchoice.setEnabled(False)
        self.chk_white.setChecked(self.options['white'])
        self.chk_follow.setChecked(self.options['follow'])
        self.chk_notsure.setChecked(self.options['notsure'])
        self.chk_easy.setChecked(self.options['easy'])
        self.chk_medium.setChecked(self.options['medium'])
        self.chk_hard.setChecked(self.options['hard'])
        self.chk_hell.setChecked(self.options['hell'])
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
        layout_options.addWidget(self.chk_random, 0, 1)
        layout_options.addWidget(self.chk_randomchoice, 1, 1)

        self.ed_title = QLineEdit()
        self.ed_title.setPlaceholderText('在此输入导出习题集的标题')
        self.ed_title.setText(self.options['title'])
        self.ed_title.setMinimumWidth(300)
        layout_title = QFormLayout()
        layout_title.addRow('标题：', self.ed_title)
        layout_options.addLayout(layout_title, 4, 0, 1, 2)

        layout_options.addWidget(self.chk_notsure, 0, 2)
        layout_options.addWidget(self.chk_easy, 1, 2)
        layout_options.addWidget(self.chk_medium, 2, 2)
        layout_options.addWidget(self.chk_hard, 3, 2)
        layout_options.addWidget(self.chk_hell, 4, 2)
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
        self.options['title'] = self.ed_title.text().strip()
        result = myfun.export_to_latex(self.mydb,self.schoiceid,self.mchoiceid,self.tofid,self.blankid,self.calculationid,self.proofid,self.options,self.schoice_seq,self.mchoice_seq)
        if result[0]:
            QMessageBox.about(self, u'通知', (u'导出文件 %s.tex 成功！' % (result[1])))
        else:
            QMessageBox.about(self, u'错误', u'导出失败！')
            print(result[1])

    def export_questions_to_html(self):
        self.options['title'] = self.ed_title.text().strip()
        result = myfun.export_to_html(self.mydb,self.schoiceid,self.mchoiceid,self.tofid,self.blankid,self.calculationid,self.proofid,self.options,self.schoice_seq,self.mchoice_seq)
        if result[0]:
            QMessageBox.about(self, u'通知', (u'导出文件 %s.html 成功！' % (result[1])))
        else:
            QMessageBox.about(self, u'错误', u'导出失败！')
            print(result[1])