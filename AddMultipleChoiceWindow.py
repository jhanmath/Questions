# -*- coding: utf-8 -*-

'''
    添加多选题界面
'''

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import QWebEngineView
import re
import database as mydb

class AddMultipleChoice(QWidget):
    def __init__(self, parent=None):
        super(AddMultipleChoice, self).__init__(parent)
        # self.setFixedSize(900, 800)
        self.resize(900,800)
        self.setWindowTitle("添加多选题")
        self.setWindowModality(Qt.ApplicationModal)
        self.pos = [0, 0, 0, 0] # 设置ABCD选项的填写位置

        question_box = QGroupBox('在此输入题干')
        question_layout = QVBoxLayout()
        self.input_question = QPlainTextEdit(r'\emptychoice')
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

        options_box = QGroupBox('输入选项并选择每项填写位置')
        options_layout = QGridLayout()
        self.btn_A = QComboBox()
        self.btn_A.addItems(['No','1','2','3','4'])
        self.btn_A.currentIndexChanged.connect(self.clickA)
        self.btn_B = QComboBox()
        self.btn_B.addItems(['No','1','2','3','4'])
        self.btn_B.currentIndexChanged.connect(self.clickB)
        self.btn_C = QComboBox()
        self.btn_C.addItems(['No','1','2','3','4'])
        self.btn_C.currentIndexChanged.connect(self.clickC)
        self.btn_D = QComboBox()
        self.btn_D.addItems(['No','1','2','3','4'])
        self.btn_D.currentIndexChanged.connect(self.clickD)
        self.lbl_A = QLabel('A')
        self.lbl_B = QLabel('B')
        self.lbl_C = QLabel('C')
        self.lbl_D = QLabel('D')
        self.input_answerA = QPlainTextEdit()
        self.input_answerA.setMinimumHeight(60)
        self.input_answerA.setMaximumHeight(90)
        self.input_answerA.textChanged.connect(self.update_preview)
        self.input_answerB = QPlainTextEdit()
        self.input_answerB.setMinimumHeight(60)
        self.input_answerB.setMaximumHeight(90)
        self.input_answerB.textChanged.connect(self.update_preview)
        self.input_answerC = QPlainTextEdit()
        self.input_answerC.setMinimumHeight(60)
        self.input_answerC.setMaximumHeight(90)
        self.input_answerC.textChanged.connect(self.update_preview)
        self.input_answerD = QPlainTextEdit()
        self.input_answerD.setMinimumHeight(60)
        self.input_answerD.setMaximumHeight(90)
        self.input_answerD.textChanged.connect(self.update_preview)
        options_layout.addWidget(self.btn_A, 0, 0)
        options_layout.addWidget(self.btn_B, 1, 0)
        options_layout.addWidget(self.btn_C, 2, 0)
        options_layout.addWidget(self.btn_D, 3, 0)
        options_layout.addWidget(self.lbl_A, 0, 1)
        options_layout.addWidget(self.lbl_B, 1, 1)
        options_layout.addWidget(self.lbl_C, 2, 1)
        options_layout.addWidget(self.lbl_D, 3, 1)
        options_layout.addWidget(self.input_answerA, 0, 2)
        options_layout.addWidget(self.input_answerB, 1, 2)
        options_layout.addWidget(self.input_answerC, 2, 2)
        options_layout.addWidget(self.input_answerD, 3, 2)
        options_box.setLayout(options_layout)

        explain_box = QGroupBox('解析')
        explain_layout = QVBoxLayout()
        self.input_explain = QPlainTextEdit()
        self.input_explain.setMinimumHeight(140)
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
        mainlayout.addWidget(preview_box, 0, 1, 2, 1)
        mainlayout.addWidget(options_box, 1, 0)
        mainlayout.addWidget(explain_box, 2, 0)
        mainlayout.addWidget(others_box, 2, 1)
        mainlayout.addWidget(self.btn_add, 3, 0, 1, 2)
        mainlayout.setColumnStretch(0, 1)
        mainlayout.setColumnStretch(1, 1)
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

    def clickA(self):
        self.pos[0] = self.btn_A.currentIndex()
        self.update_preview()

    def clickB(self):
        self.pos[1] = self.btn_B.currentIndex()
        self.update_preview()

    def clickC(self):
        self.pos[2] = self.btn_C.currentIndex()
        self.update_preview()

    def clickD(self):
        self.pos[3] = self.btn_D.currentIndex()
        self.update_preview()

    # 更新预览
    def update_preview(self):
        answer = ''
        if max(self.pos)>0:
            for i in range(1, max(self.pos)+1):
                thisanswer = ''
                for j in range(4):
                    if self.pos[j] == i:
                        thisanswer = thisanswer + chr(j+65)
                answer = answer + '第'+str(i)+'空：' + thisanswer + '；' 
        self.pageSourceContent = (self.input_question.toPlainText().strip().replace('\n','</br>').replace('\emptychoice','（&emsp;）') 
                                    + '</p><p>A. ' + self.input_answerA.toPlainText().strip().replace('\n','</br>')
                                    + '</p><p>B. ' + self.input_answerB.toPlainText().strip().replace('\n','</br>')
                                    + '</p><p>C. ' + self.input_answerC.toPlainText().strip().replace('\n','</br>')
                                    + '</p><p>D. ' + self.input_answerD.toPlainText().strip().replace('\n','</br>')
                                    + '</p><p>答案： ' + answer
                                    + '</p><p>解析： ' + self.input_explain.toPlainText().strip().replace('\n','</br>'))
        self.webView.setHtml(self.pageSourceHead+self.pageSourceContent+self.pageSourceFoot)

    def insert_question(self):
        add = False
        num_blanks = self.input_question.toPlainText().count('\emptychoice')
        pos_sorted = sorted(self.pos)
        pos_diff = [pos_sorted[i+1]-pos_sorted[i] for i in range(3)]
        if self.input_question.toPlainText().strip() == '':
            QMessageBox.about(self, u'警告', u'题干不能为空！')
        elif num_blanks<1 or num_blanks>4:
            QMessageBox.about(self, u'警告', u'待填选项空位数量应在1-4之间！')
        elif num_blanks != max(self.pos) or max(pos_diff)>1:
            QMessageBox.about(self, u'警告', u'待填空位与设定答案位置不匹配！')
        elif self.input_answerA.toPlainText().strip() == '' or self.input_answerB.toPlainText().strip() == '':
            QMessageBox.about(self, u'警告', u'选项A和B不能为空！')
        elif ((self.input_answerB.toPlainText().strip() == '' and (self.input_answerC.toPlainText().strip() != '' or self.input_answerD.toPlainText().strip() != ''))
                or (self.input_answerC.toPlainText().strip() == '' and self.input_answerD.toPlainText().strip() != '')):
            QMessageBox.about(self, u'警告', u'请按照ABCD顺序填写选项！')
        elif ((self.pos[1]>0  and self.input_answerB.toPlainText().strip() == '')
                or (self.pos[2]>0  and self.input_answerC.toPlainText().strip() == '')
                or (self.pos[3]>0  and self.input_answerD.toPlainText().strip() == '')):
            QMessageBox.about(self, u'警告', u'正确选项不能为空！')
        elif (self.input_answerB.toPlainText().strip() == '' or self.input_answerC.toPlainText().strip() == '' or self.input_answerD.toPlainText().strip() == ''):
            reply = QMessageBox.warning(self, u'警告', u'选项BCD没有全部填写，确定添加题目？', QMessageBox.Yes, QMessageBox.No)
            if reply == QMessageBox.Yes:
                add = True
        else:
            add = True
        if add:
            table = ' "main"."mchoice"'
            columns = '("question", "A", "B", "C", "D", "pos_A", "pos_B", "pos_C", "pos_D", "explain", "section", "difficulty", "source")'
            insertstring = ('INSERT INTO' + table + columns + ' VALUES ("'
                                + self.input_question.toPlainText().strip().replace('\n',r'\\') + '", "'
                                + self.input_answerA.toPlainText().strip().replace('\n',r'\\') + '", "'
                                + self.input_answerB.toPlainText().strip().replace('\n',r'\\') + '", "'
                                + self.input_answerC.toPlainText().strip().replace('\n',r'\\') + '", "'
                                + self.input_answerD.toPlainText().strip().replace('\n',r'\\') + '", "'
                                + str(self.pos[0]) + '", "'
                                + str(self.pos[1]) + '", "'
                                + str(self.pos[2]) + '", "'
                                + str(self.pos[3]) + '", "'
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
