# -*- coding: utf-8 -*-

'''
    添加计算题界面
'''

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import QWebEngineView
import database as mydb
import myfunctions as myfun

class AddCalculation(QWidget):
    other_settings = pyqtSignal(list)
    
    def __init__(self, parent=None):
        super(AddCalculation, self).__init__(parent)
        # self.setFixedSize(900, 800)
        self.resize(900,800)
        self.setWindowTitle("添加计算题")
        self.setWindowModality(Qt.ApplicationModal)
        self.answer = '' # 设置初始答案为空
        self.modification = 0 # 是否是修改题目，0表示不是修改题目，否则赋予待修改题目id

        question_box = QGroupBox('在此输入题干(Alt + Q)')
        question_layout = QVBoxLayout()
        self.input_question = QPlainTextEdit()
        self.input_question.setMinimumHeight(140)
        self.input_question.textChanged.connect(self.update_preview)
        question_layout.addWidget(self.input_question)
        question_box.setLayout(question_layout)

        preview_box = QGroupBox('预览（仅供参考）')
        preview_layout = QVBoxLayout()
        self.webView = QWebEngineView()
        self.webView.setContextMenuPolicy(0) # 禁止右键菜单
        preview_layout.addWidget(self.webView)
        preview_box.setLayout(preview_layout)

        answer_box = QGroupBox('答案(Alt + A)')
        answer_layout = QVBoxLayout()
        self.input_answer = QPlainTextEdit()
        self.input_answer.setMinimumHeight(300)
        self.input_answer.textChanged.connect(self.update_answer)
        answer_layout.addWidget(self.input_answer)
        answer_box.setLayout(answer_layout)

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
        mainlayout.addWidget(answer_box, 1, 0, 2, 1)
        mainlayout.addWidget(others_box, 2, 1)
        mainlayout.addWidget(self.btn_add, 3, 0, 1, 2)
        mainlayout.setColumnStretch(0, 1)
        mainlayout.setColumnStretch(1, 1)
        mainlayout.setRowStretch(0,2)
        mainlayout.setRowStretch(1,3)
        mainlayout.setRowStretch(2,1)
        self.setLayout(mainlayout)
        self.webView.setHtml(myfun.gethtml(self.webView.width()))
        self.shortcut()


    # 改变章节数据库后重新载入章节
    def update_list_section(self):
        self.list_section.clear()
        searchstring = 'select * from sections'
        self.sections = mydb.search(searchstring)
        if self.sections:
            for row in self.sections:
                self.list_section.addItem(row[1])
        self.section_id = self.sections[self.list_section.currentIndex()][0]
	
    # 改变难度数据库后重新载入难度
    def update_list_difficulty(self):
        self.list_difficulty.clear()
        searchstring = 'select * from difficulties'
        self.difficulties = mydb.search(searchstring)
        if self.difficulties:
            for row in self.difficulties:
                self.list_difficulty.addItem(row[1])
        self.difficulty_id = self.difficulties[self.list_difficulty.currentIndex()][0]

    # 改变来源数据库后重新载入来源
    def update_list_source(self):
        self.list_source.clear()
        searchstring = 'select * from sources'
        self.sources = mydb.search(searchstring)
        if self.sources:
            for row in self.sources:
                self.list_source.addItem(row[1])
        self.source_id = self.sources[self.list_source.currentIndex()][0]

    # 改变章节时的事件
    def change_section(self):
        self.section_id = self.sections[self.list_section.currentIndex()][0]

    # 改变难度时的事件
    def change_difficulty(self):
        self.difficulty_id = self.difficulties[self.list_difficulty.currentIndex()][0]

    # 改变来源时的事件
    def change_source(self):
        self.source_id = self.sources[self.list_source.currentIndex()][0]

    def update_answer(self):
        self.answer = self.input_answer.toPlainText().strip()
        self.update_preview()

    # 更新预览
    def update_preview(self):
        pageSourceContent = ('<p>' + myfun.format_question_to_html(self.input_question.toPlainText(), '计算题') + '</p>'
                                    + '<p>解： ' + myfun.format_subquestion_to_html(self.answer) + '</p>')
        self.webView.setHtml(myfun.gethtml(self.webView.width(), pageSourceContent))

    def insert_question(self):
        add = False
        if self.input_question.toPlainText().strip() == '' or self.answer == '':
            QMessageBox.about(self, u'警告', u'题干和答案不能为空！')
        else:
            add = True
        if add:
            table = ' "main"."calculation"'
            if self.modification == 0:
                columns = '("question", "answer", "section", "difficulty", "source")'
                insertstring = ('INSERT INTO' + table + columns + ' VALUES ("'
                                    + myfun.format_question_to_latex(self.input_question.toPlainText(), '计算题') + '", "'
                                    + myfun.format_explain_to_latex(self.answer) + '", '
                                    + str(self.section_id) + ', '
                                    + str(self.difficulty_id) + ', '
                                    + str(self.source_id) + ');')
                if mydb.insert(insertstring):
                    self.other_settings.emit([self.section_id, self.difficulty_id, self.source_id])
                    reply = QMessageBox.information(self, u'通知', u'添加题目成功！是否关闭当前窗口？', QMessageBox.Yes, QMessageBox.No)
                    if reply == QMessageBox.Yes:
                        self.close()
                else:
                    QMessageBox.about(self, u'错误', u'添加题目失败！')
            else:
                updatestring = ('UPDATE ' + table + ' SET question="%s", answer="%s", section=%d, difficulty=%d, source=%d where id=%d;'
                                % (myfun.format_question_to_latex(self.input_question.toPlainText(), '计算题'),
                                    myfun.format_explain_to_latex(self.answer),
                                    self.section_id,
                                    self.difficulty_id,
                                    self.source_id,
                                    self.modification))
                if mydb.insert(updatestring):
                    self.other_settings.emit([self.section_id, self.difficulty_id, self.source_id])
                    reply = QMessageBox.information(self, u'通知', u'修改题目成功！是否关闭当前窗口？', QMessageBox.Yes, QMessageBox.No)
                    if reply == QMessageBox.Yes:
                        self.close()
                else:
                    QMessageBox.about(self, u'错误', u'修改题目失败！')

    # 调整窗口大小事件
    def resizeEvent(self, event):#调整窗口尺寸时，该方法被持续调用。event参数包含QResizeEvent类的实例，通过该类的下列方法获得窗口信息：
        self.update_preview()

    def showEvent(self, event):
        self.update_preview()

    def shortcut(self):
        self.act_setfocus_question = QAction()
        self.act_setfocus_question.setShortcut(QKeySequence(self.tr('Alt+Q')))
        self.act_setfocus_question.triggered.connect(lambda: self.input_question.setFocus())
        self.addAction(self.act_setfocus_question)
        self.act_setfocus_answer = QAction()
        self.act_setfocus_answer.setShortcut(QKeySequence(self.tr('Alt+A')))
        self.act_setfocus_answer.triggered.connect(lambda: self.input_answer.setFocus())
        self.addAction(self.act_setfocus_answer)
        self.act_insert_mathenv = QAction()
        self.act_insert_mathenv.setShortcut(QKeySequence(self.tr('Alt+M')))
        self.act_insert_mathenv.triggered.connect(self.insert_mathenv)
        self.addAction(self.act_insert_mathenv)

    def insert_mathenv(self):
        if self.input_question.hasFocus():
            input_now = self.input_question
        elif self.input_answer.hasFocus():
            input_now = self.input_answer
        else:
            return
        input_now.insertPlainText('$  $')
        for i in range(2):
            input_now.moveCursor(QTextCursor.PreviousCharacter)