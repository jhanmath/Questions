# -*- coding: utf-8 -*-

'''
    添加判断题界面
'''

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import QWebEngineView
import re
import database as mydb

class AddToF(QWidget):
    def __init__(self, parent=None):
        super(AddToF, self).__init__(parent)
        # self.setFixedSize(900, 800)
        self.resize(900,800)
        self.setWindowTitle("添加判断题")
        self.setWindowModality(Qt.ApplicationModal)
        self.answer = 0 # 设置初始答案为错误

        question_box = QGroupBox('在此输入题干')
        question_layout = QVBoxLayout()
        self.input_question = QPlainTextEdit()
        self.input_question.setMinimumHeight(140)
        self.input_question.textChanged.connect(self.update_preview)
        question_layout.addWidget(self.input_question)
        question_box.setLayout(question_layout)

        preview_box = QGroupBox('预览（仅供参考）')
        preview_layout = QVBoxLayout()
        path = QDir.current().filePath(r'MathJax-3.0.1/es5/tex-mml-chtml.js') 
        mathjax = QUrl.fromLocalFile(path).toString()
        self.pageSourceHead = r'''
        <html><head>
        <script>
            window.MathJax = {
                loader: {load: ['[tex]/physics']},
                tex: {
                    packages: {'[+]': ['physics']},
                    inlineMath: [['$','$'],['\\(','\\)']],
                }
            };
            </script>
        <script type="text/javascript" id="MathJax-script" async src="''' + mathjax + r'''"></script>
        <style>
            body {
                margin: 0 auto;
                width: 429px;
            }
            p {
                font-size: 18pt;
            }
        </style>
        </head>
        <body>
        <p>'''
        self.pageSourceFoot = r'''</p>
        </body>
        </html>'''
        self.webView = QWebEngineView()
        self.webView.setContextMenuPolicy(0) # 禁止右键菜单
        preview_layout.addWidget(self.webView)
        preview_box.setLayout(preview_layout)

        answers_box = QGroupBox('选择本题答案')
        answers_layout = QGridLayout()
        self.list_answer = QComboBox()
        self.list_answer.addItems(['错误','正确'])
        self.list_answer.currentIndexChanged.connect(self.change_answer)
        self.lbl_answer = QLabel('答案')
        answers_layout.addWidget(self.lbl_answer, 0, 0)
        answers_layout.addWidget(self.list_answer, 0, 1)
        answers_box.setLayout(answers_layout)

        explain_box = QGroupBox('解析')
        explain_layout = QVBoxLayout()
        self.input_explain = QPlainTextEdit()
        self.input_explain.setMinimumHeight(300)
        self.input_explain.textChanged.connect(self.update_preview)
        explain_layout.addWidget(self.input_explain)
        explain_box.setLayout(explain_layout)

        others_box = QGroupBox('其他设置')
        others_layout = QGridLayout()
        self.lbl_section = QLabel('章节')
        self.lbl_difficulty = QLabel('难度')
        self.lbl_source = QLabel('来源')
        self.list_section = QComboBox()
        self.list_section.setMaximumWidth(350)
        self.update_list_section()
        self.list_section.currentIndexChanged.connect(self.change_section)
        self.list_difficulty = QComboBox()
        self.list_difficulty.setMaximumWidth(350)
        self.update_list_difficulty()
        self.list_difficulty.currentIndexChanged.connect(self.change_difficulty)
        self.list_source = QComboBox()
        self.list_source.setMaximumWidth(350)
        self.update_list_source()
        self.list_source.currentIndexChanged.connect(self.change_source)
        others_layout.addWidget(self.lbl_section, 0, 0)
        others_layout.addWidget(self.lbl_difficulty, 1, 0)
        others_layout.addWidget(self.lbl_source, 2, 0)
        others_layout.addWidget(self.list_section, 0, 1)
        others_layout.addWidget(self.list_difficulty, 1, 1)
        others_layout.addWidget(self.list_source, 2, 1)
        others_box.setLayout(others_layout)

        self.btn_add = QPushButton('添加题目')
        self.btn_add.clicked.connect(self.insert_question)

        mainlayout = QGridLayout()
        mainlayout.setSpacing(20)
        mainlayout.addWidget(question_box, 0, 0)
        mainlayout.addWidget(preview_box, 0, 1, 3, 1)
        mainlayout.addWidget(answers_box, 1, 0)
        mainlayout.addWidget(explain_box, 2, 0, 2, 1)
        mainlayout.addWidget(others_box, 3, 1)
        mainlayout.addWidget(self.btn_add, 4, 0, 1, 2)
        mainlayout.setColumnStretch(0, 1)
        mainlayout.setColumnStretch(1, 1)
        mainlayout.setRowStretch(0,2)
        mainlayout.setRowStretch(2,2)
        mainlayout.setRowStretch(3,1)
        self.setLayout(mainlayout)
        self.webView.setHtml(self.pageSourceHead+self.pageSourceFoot)


    # 改变章节数据库后重新载入章节
    def update_list_section(self):
        self.list_section.clear()
        searchstring = 'select * from sections'
        self.sections = mydb.search(searchstring)
        if self.sections:
            for row in self.sections:
                self.list_section.addItem(row[1])
        self.section = self.sections[self.list_section.currentIndex()][0]
	
    # 改变难度数据库后重新载入难度
    def update_list_difficulty(self):
        self.list_difficulty.clear()
        searchstring = 'select * from difficulties'
        self.difficulties = mydb.search(searchstring)
        if self.difficulties:
            for row in self.difficulties:
                self.list_difficulty.addItem(row[1])
        self.difficulty = self.difficulties[self.list_difficulty.currentIndex()][0]

    # 改变来源数据库后重新载入来源
    def update_list_source(self):
        self.list_source.clear()
        searchstring = 'select * from sources'
        self.sources = mydb.search(searchstring)
        if self.sources:
            for row in self.sources:
                self.list_source.addItem(row[1])
        self.source = self.sources[self.list_source.currentIndex()][0]

    # 改变章节时的事件
    def change_section(self):
        self.section = self.sections[self.list_section.currentIndex()][0]

    # 改变难度时的事件
    def change_difficulty(self):
        self.difficulty = self.difficulties[self.list_difficulty.currentIndex()][0]

    # 改变来源时的事件
    def change_source(self):
        self.source = self.sources[self.list_source.currentIndex()][0]

    def change_answer(self):
        self.answer = self.list_answer.currentIndex()
        self.update_preview()

    # 更新预览
    def update_preview(self):
        answertext = ['错误', '正确']
        self.pageSourceContent = (self.input_question.toPlainText().strip().replace('\n','</br>')
                                    + '</p><p>答案： ' + answertext[self.answer]
                                    + '</p><p>解析： ' + self.input_explain.toPlainText().strip().replace('\n','</br>'))
        self.webView.setHtml(self.pageSourceHead+self.pageSourceContent+self.pageSourceFoot)

    def insert_question(self):
        add = False
        if self.input_question.toPlainText().strip() == '':
            QMessageBox.about(self, u'警告', u'题干不能为空！')
        else:
            add = True
        if add:
            table = ' "main"."tof"'
            columns = '("question", "correct", "explain", "section", "difficulty", "source")'
            insertstring = ('INSERT INTO' + table + columns + ' VALUES ("'
                                + self.input_question.toPlainText().strip().replace('\n',r'\\') + '", "'
                                + str(self.answer) + '", "'
                                + self.input_explain.toPlainText().strip().replace('\n',r'\\') + '", '
                                + str(self.section) + ', '
                                + str(self.difficulty) + ', '
                                + str(self.source) + ');')
            if mydb.insert(insertstring):
                reply = QMessageBox.information(self, u'通知', u'添加题目成功！是否关闭当前窗口？', QMessageBox.Yes, QMessageBox.No)
                if reply == QMessageBox.Yes:
                    self.close()
            else:
                QMessageBox.about(self, u'错误', u'添加题目失败！')

    def refresh_prevew(self):
        newwidth='width: '+ str(self.webView.width()) +'px;'
        self.pageSourceHead = re.sub(r'width: \d*px;', newwidth, self.pageSourceHead)
        self.update_preview()

    # 调整窗口大小事件
    def resizeEvent(self, event):#调整窗口尺寸时，该方法被持续调用。event参数包含QResizeEvent类的实例，通过该类的下列方法获得窗口信息：
        self.refresh_prevew()
