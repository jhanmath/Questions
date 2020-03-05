# -*- coding: utf-8 -*-

'''
    主界面
'''

import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import database as mydb
from AddSingleChoiceWindow import *
from AddMultipleChoiceWindow import *
from AddToFWindow import *
from AddFillinBlanksWindow import *
from AddCalculationWindow import *
from AddProofWindow import *
from SelectSectionsWindow import *

class MainWindow(QWidget):
	singal_sectionid = pyqtSignal(list)

	def __init__(self, parent=None):
		super(MainWindow , self).__init__(parent)
		self.ver = '2020.03.06'
		self.selected_sectionid = [48]

		mainlayout = QVBoxLayout()
		self.qblabel = QLabel('test')
		self.createDBDisplayBox()
		mainlayout.addWidget(self.DBDisplayBox)
		self.createAddQuestionBox()
		mainlayout.addWidget(self.AddQuestionBox)
		self.createSectionsBox()
		mainlayout.addWidget(self.SectionsBox)
		self.createExportBox()
		mainlayout.addWidget(self.ExportBox)
		layout_about = QHBoxLayout()
		self.download_demo = QLabel(
			'<a href = "http://www.jhanmath.com/?page_id=125">'
			'下载视频演示</a>')
		self.download_demo.setOpenExternalLinks(True)
		self.download_demo.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
		layout_about.addWidget(self.download_demo)
		self.about = QLabel(
			'This software is developed by Jing Han. ver %s.' % (self.ver))
		self.about.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
		layout_about.addWidget(self.about)
		mainlayout.addLayout(layout_about)
		self.setLayout(mainlayout)

		self.update_sections(self.selected_sectionid)

		self.resize(1000, 800)
		self.setWindowTitle("数学题库")

	def createDBDisplayBox(self):
		self.DBDisplayBox = QGroupBox("当前题库中各题型题目数量")
		layout = QGridLayout()
		# self.lbl_dbname = QLabel('当前数据库')
		self.btn_dbname = QPushButton('更换题库')
		fm = QFontMetrics(self.btn_dbname.font())
		# self.btn_dbname.setFixedWidth(fm.width(self.btn_dbname.text())+20)
		num = '单选题'
		searchstring = ('select count(*) from schoice')
		num_schoice = mydb.search(searchstring)[0][0]
		num = num + str(num_schoice) + '道；多选题'
		searchstring = ('select count(*) from mchoice')
		num_mchoice = mydb.search(searchstring)[0][0]
		num = num + str(num_mchoice) + '道；判断题'
		searchstring = ('select count(*) from tof')
		num_tof = mydb.search(searchstring)[0][0]
		num = num + str(num_tof) + '道；填空题'
		searchstring = ('select count(*) from blank')
		num_blank = mydb.search(searchstring)[0][0]
		num = num + str(num_blank) + '道；计算题'
		searchstring = ('select count(*) from calculation')
		num_calculation = mydb.search(searchstring)[0][0]
		num = num + str(num_calculation) + '道；证明题'
		searchstring = ('select count(*) from proof')
		num_proof = mydb.search(searchstring)[0][0]
		num = num + str(num_proof) + '道.'
		self.lbl_numofquestions = QLabel(num)
		self.btn_details = QPushButton('查看详情')
		self.btn_details.setFixedWidth(fm.width(self.btn_details.text())+20)
		self.btn_details.setEnabled(False)
		# layout.setSpacing(10)
		# layout.addWidget(self.lbl_dbname, 0, 0)
		layout.addWidget(self.lbl_numofquestions, 1, 0)
		# layout.addWidget(self.btn_dbname, 0, 1)
		layout.addWidget(self.btn_details, 1, 1)
		self.DBDisplayBox.setLayout(layout)

	def createAddQuestionBox(self):
		self.AddQuestionBox = QGroupBox("添加题目")
		layout = QHBoxLayout()
		self.btn_addschoice = QPushButton('添加单选题')
		self.btn_addschoice.clicked.connect(self.btn_addschoice_clicked)
		self.btn_addmchoice = QPushButton('添加多选题')
		self.btn_addmchoice.clicked.connect(self.btn_addmchoice_clicked)
		self.btn_addtof = QPushButton('添加判断题')
		self.btn_addtof.clicked.connect(self.btn_addtof_clicked)
		self.btn_addblank = QPushButton('添加填空题')
		self.btn_addblank.clicked.connect(self.btn_addblank_clicked)
		self.btn_addcalculate = QPushButton('添加计算题')
		self.btn_addcalculate.clicked.connect(self.btn_addcalculate_clicked)
		self.btn_addprove = QPushButton('添加证明题')
		self.btn_addprove.clicked.connect(self.btn_addprove_clicked)
		layout.setSpacing(10)
		layout.addWidget(self.btn_addschoice)
		layout.addWidget(self.btn_addmchoice)
		layout.addWidget(self.btn_addtof)
		layout.addWidget(self.btn_addblank)
		layout.addWidget(self.btn_addcalculate)
		layout.addWidget(self.btn_addprove)
		self.AddQuestionBox.setLayout(layout)

	def createSectionsBox(self):
		self.SectionsBox = QGroupBox('选择导出章节')
		layout = QVBoxLayout()
		self.tbl_selectedsections = QTableWidget()
		self.tbl_selectedsections.setColumnCount(7)
		self.tbl_selectedsections.setHorizontalHeaderLabels(['章节','单选题数','多选题数','判断题数','填空题数','计算题数','证明题数'])
		self.tbl_selectedsections.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
		self.tbl_selectedsections.setEditTriggers(QAbstractItemView.NoEditTriggers)
		self.tbl_selectedsections.setSelectionBehavior(QAbstractItemView.SelectRows)
		layout.addWidget(self.tbl_selectedsections)
		self.btn_changesections = QPushButton('选择章节')
		self.btn_changesections.clicked.connect(self.btn_changesections_clicked)
		layout.addWidget(self.btn_changesections)
		self.SectionsBox.setLayout(layout)

	def createExportBox(self):
		self.lbl_schoice = QLabel('单选题数量：')
		self.lbl_mchoice = QLabel('多选题数量：')
		self.lbl_tof = QLabel('判断题数量：')
		self.lbl_blank = QLabel('填空题数量：')
		self.lbl_calculate = QLabel('计算题数量：')
		self.lbl_prove = QLabel('证明题数量:')
		self.ed_schoice = QLineEdit('0')
		self.ed_mchoice = QLineEdit('0')
		self.ed_tof = QLineEdit('0')
		self.ed_blank = QLineEdit('0')
		self.ed_calculate = QLineEdit('0')
		self.ed_prove = QLineEdit('0')
		regex = QRegExp("^[1-9]\d*|0$")
		validator = QRegExpValidator(regex)
		self.ed_schoice.setValidator(validator)
		self.ed_mchoice.setValidator(validator)
		self.ed_tof.setValidator(validator)
		self.ed_blank.setValidator(validator)
		self.ed_calculate.setValidator(validator)
		self.ed_prove.setValidator(validator)
		self.ed_schoice.setAlignment(Qt.AlignRight)
		self.ed_mchoice.setAlignment(Qt.AlignRight)
		self.ed_tof.setAlignment(Qt.AlignRight)
		self.ed_blank.setAlignment(Qt.AlignRight)
		self.ed_calculate.setAlignment(Qt.AlignRight)
		self.ed_prove.setAlignment(Qt.AlignRight)
		self.ed_schoice.setFixedWidth(100)
		self.ed_mchoice.setFixedWidth(100)
		self.ed_tof.setFixedWidth(100)
		self.ed_blank.setFixedWidth(100)
		self.ed_calculate.setFixedWidth(100)
		self.ed_prove.setFixedWidth(100)
		self.chk_solution = QCheckBox('包含解答')
		self.chk_random = QCheckBox('打乱题目顺序')
		self.chk_randomchoice = QCheckBox('选择题选项乱序')
		self.chk_white = QCheckBox('主观题后留空')
		self.chk_follow = QCheckBox('解答紧跟题')
		self.chk_easy = QCheckBox('简单')
		self.chk_medium = QCheckBox('中等')
		self.chk_hard = QCheckBox('困难')
		self.chk_hell = QCheckBox('地狱')
		self.btn_export = QPushButton('导出')
		self.btn_export.clicked.connect(self.export_questions)
		self.btn_compile = QPushButton('导出并编译')
		self.btn_compile.setEnabled(False)

		layout = QGridLayout()
		layout.addWidget(self.lbl_schoice, 0, 0)
		layout.addWidget(self.lbl_mchoice, 1, 0)
		layout.addWidget(self.lbl_tof, 2, 0)
		layout.addWidget(self.lbl_blank, 3, 0)
		layout.addWidget(self.lbl_calculate, 4, 0)
		layout.addWidget(self.lbl_prove, 5, 0)
		layout.addWidget(self.ed_schoice, 0, 1)
		layout.addWidget(self.ed_mchoice, 1, 1)
		layout.addWidget(self.ed_tof, 2, 1)
		layout.addWidget(self.ed_blank, 3, 1)
		layout.addWidget(self.ed_calculate, 4, 1)
		layout.addWidget(self.ed_prove, 5, 1)
		layout.addWidget(self.chk_solution, 0, 3)
		layout.addWidget(self.chk_follow, 1, 3)
		layout.addWidget(self.chk_white, 2, 3)
		layout.addWidget(self.chk_random, 3, 3)
		layout.addWidget(self.chk_randomchoice, 4, 3)
		layout.addWidget(self.chk_easy, 0, 4)
		layout.addWidget(self.chk_medium, 1, 4)
		layout.addWidget(self.chk_hard, 2, 4)
		layout.addWidget(self.chk_hell, 3, 4)
		layout.addWidget(self.btn_export, 1, 6, 2, 1)
		layout.addWidget(self.btn_compile, 3, 6, 2, 1)
		layout.addWidget(QLabel(' '), 0, 2)
		layout.addWidget(QLabel(' '), 0, 5)
		layout.setHorizontalSpacing(30)

		self.ExportBox = QGroupBox('导出选项')
		self.ExportBox.setLayout(layout)

	def btn_changesections_clicked(self):
		self.select_sections_ui = SelectSections()
		self.select_sections_ui.signal.connect(self.update_sections)
		self.singal_sectionid.connect(self.select_sections_ui.initialize)
		self.singal_sectionid.emit(self.selected_sectionid)
		self.select_sections_ui.show()

	def update_sections(self, sectionid):
		self.selected_sectionid = sectionid
		self.tbl_selectedsections.setRowCount(len(sectionid))
		searchstring = 'select * from sections'
		sections = mydb.search(searchstring)
		total_num_schoice = 0
		total_num_mchoice = 0
		total_num_tof = 0
		total_num_blank = 0
		total_num_calculation = 0
		total_num_proof = 0
		for i in range(len(sectionid)):
			j = 0
			while sections[j][0] != sectionid[i]:
				j = j + 1
			newItem = QTableWidgetItem(sections[j][1])
			self.tbl_selectedsections.setItem(i, 0, newItem)
			searchstring = ('select count(*) from schoice where section=%d' % (sectionid[i]))
			num_schoice = mydb.search(searchstring)[0][0]
			total_num_schoice = total_num_schoice + num_schoice
			newItem = QTableWidgetItem(str(num_schoice))
			self.tbl_selectedsections.setItem(i, 1, newItem)
			searchstring = ('select count(*) from mchoice where section=%d' % (sectionid[i]))
			num_mchoice = mydb.search(searchstring)[0][0]
			total_num_mchoice = total_num_mchoice + num_mchoice
			newItem = QTableWidgetItem(str(num_mchoice))
			self.tbl_selectedsections.setItem(i, 2, newItem)
			searchstring = ('select count(*) from tof where section=%d' % (sectionid[i]))
			num_tof = mydb.search(searchstring)[0][0]
			total_num_tof = total_num_tof + num_tof
			newItem = QTableWidgetItem(str(num_tof))
			self.tbl_selectedsections.setItem(i, 3, newItem)
			searchstring = ('select count(*) from blank where section=%d' % (sectionid[i]))
			num_blank = mydb.search(searchstring)[0][0]
			total_num_blank = total_num_blank + num_blank
			newItem = QTableWidgetItem(str(num_blank))
			self.tbl_selectedsections.setItem(i, 4, newItem)
			searchstring = ('select count(*) from calculation where section=%d' % (sectionid[i]))
			num_calculation = mydb.search(searchstring)[0][0]
			total_num_calculation = total_num_calculation + num_calculation
			newItem = QTableWidgetItem(str(num_calculation))
			self.tbl_selectedsections.setItem(i, 5, newItem)
			searchstring = ('select count(*) from proof where section=%d' % (sectionid[i]))
			num_proof = mydb.search(searchstring)[0][0]
			total_num_proof = total_num_proof + num_proof
			newItem = QTableWidgetItem(str(num_proof))
			self.tbl_selectedsections.setItem(i, 6, newItem)
		self.ed_schoice.setText(str(total_num_schoice))
		self.ed_mchoice.setText(str(total_num_mchoice))
		self.ed_tof.setText(str(total_num_tof))
		self.ed_blank.setText(str(total_num_blank))
		self.ed_calculate.setText(str(total_num_calculation))
		self.ed_prove.setText(str(total_num_proof))

	def btn_addschoice_clicked(self):
		self.add_schoice_ui = AddSingleChoice()
		self.add_schoice_ui.show()

	def btn_addmchoice_clicked(self):
		self.add_mchoice_ui = AddMultipleChoice()
		self.add_mchoice_ui.show()

	def btn_addtof_clicked(self):
		self.add_tof_ui = AddToF()
		self.add_tof_ui.show()
	
	def btn_addblank_clicked(self):
		self.add_blank_ui = AddFillinBlanks()
		self.add_blank_ui.show()

	def btn_addcalculate_clicked(self):
		self.add_calculation_ui = AddCalculation()
		self.add_calculation_ui.show()

	def btn_addprove_clicked(self):
		self.add_proof_ui = AddProof()
		self.add_proof_ui.show()

	def export_questions(self):
		if not self.selected_sectionid:
			QMessageBox.about(self, u'通知', u'请先选择章节！')
			return
		sectionstring = (' where section=' + str(self.selected_sectionid[0]))
		for i in range(1, len(self.selected_sectionid)):
			sectionstring = sectionstring + ' or section=' + str(self.selected_sectionid[i])
		# 读单选题表
		searchstring = ('select "question", "A", "B", "C", "D", "answer", "explain", "section", "difficulty", "source" from schoice' + sectionstring)
		schoice = mydb.search(searchstring)
		num_schoice = len(schoice)
		# 读多选题表
		searchstring = ('select "question", "A", "B", "C", "D", "pos_A", "pos_B", "pos_C", "pos_D", "explain", "section", "difficulty", "source" from mchoice' + sectionstring)
		mchoice = mydb.search(searchstring)
		num_mchoice = len(mchoice)
		# 读判断题表
		searchstring = ('select "question", "correct", "explain", "section", "difficulty", "source" from tof' + sectionstring)
		tof = mydb.search(searchstring)
		num_tof = len(tof)
		# 读填空题表
		searchstring = ('select "question", "answer1", "answer2", "answer3", "answer4", "explain", "section", "difficulty", "source" from blank' + sectionstring)
		blank = mydb.search(searchstring)
		num_blank = len(blank)
		# 读计算题表
		searchstring = ('select "question", "answer", "section", "difficulty", "source" from calculation' + sectionstring)
		calculation = mydb.search(searchstring)
		num_calculation = len(calculation)
		# 读证明题表
		searchstring = ('select "question", "answer", "section", "difficulty", "source" from proof' + sectionstring)
		proof = mydb.search(searchstring)
		num_proof = len(proof)

		if not (num_schoice or num_mchoice or num_tof or num_blank or num_calculation or num_proof):
			QMessageBox.about(self, u'通知', u'当前章节中没有题目！')
			return
		
		try:
			f = open('myquestions.tex', 'w', encoding='utf-8') # 若是'wb'就表示写二进制文件
			# 写入单选题
			if num_schoice>0:
				f.writelines('\\section{单项选择题}\n')
				f.writelines('\\begin{enumerate}[(1)]\n')
				for i in range(num_schoice):
					f.writelines('\t\\item %s\n' % (schoice[i][0]))
					f.writelines('\t\t\\begin{choice}(4)\n')
					f.writelines('\t\t\t\\choice %s\n' % (schoice[i][1]))
					f.writelines('\t\t\t\\choice %s\n' % (schoice[i][2]))
					f.writelines('\t\t\t\\choice %s\n' % (schoice[i][3]))
					f.writelines('\t\t\t\\choice %s\n' % (schoice[i][4]))
					f.writelines('\t\t\\end{choice}\n')
				f.writelines('\\end{enumerate}\n')
			# 写入多选题
			if num_mchoice>0:
				f.writelines('\\section{多项选择题}\n')
				f.writelines('\\begin{enumerate}[(1)]\n')
				for i in range(num_mchoice):
					f.writelines('\t\\item %s\n' % (mchoice[i][0]))
					f.writelines('\t\t\\begin{choice}(4)\n')
					f.writelines('\t\t\t\\choice %s\n' % (mchoice[i][1]))
					f.writelines('\t\t\t\\choice %s\n' % (mchoice[i][2]))
					f.writelines('\t\t\t\\choice %s\n' % (mchoice[i][3]))
					f.writelines('\t\t\t\\choice %s\n' % (mchoice[i][4]))
					f.writelines('\t\t\\end{choice}\n')
				f.writelines('\\end{enumerate}\n')
			# 写入判断题
			if num_tof>0:
				f.writelines('\\section{判断题}\n')
				f.writelines('\\begin{enumerate}[(1)]\n')
				for i in range(num_tof):
					f.writelines('\t\\item %s \\hfill\\emptychoice \n' % (tof[i][0]))
				f.writelines('\\end{enumerate}\n')
			# 写入填空题
			if num_blank>0:
				f.writelines('\\section{填空题}\n')
				f.writelines('\\begin{enumerate}[(1)]\n')
				for i in range(num_blank):
					f.writelines('\t\\item %s\n' % (blank[i][0]))
				f.writelines('\\end{enumerate}\n')
			# 写入计算题
			if num_calculation>0:
				f.writelines('\\section{计算题}\n')
				f.writelines('\\begin{enumerate}[(1)]\n')
				for i in range(num_calculation):
					f.writelines('\t\\item %s\n' % (calculation[i][0]))
				f.writelines('\\end{enumerate}\n')
			# 写入证明题
			if num_proof>0:
				f.writelines('\\section{证明题}\n')
				f.writelines('\\begin{enumerate}[(1)]\n')
				for i in range(num_proof):
					f.writelines('\t\\item %s\n' % (proof[i][0]))
				f.writelines('\\end{enumerate}\n')

			# 写入解答
			if self.chk_solution.isChecked():
				# 单选题解答
				if num_schoice>0:
					f.writelines('\\section{单项选择题解答}\n')
					f.writelines('\\begin{enumerate}[(1)]\n')
					for i in range(num_schoice):
						if schoice[i][6] != '':
							f.writelines('\t\\item %s\\\\\n' % (schoice[i][5]))
							f.writelines('\t\t解析：%s\n' % (schoice[i][6]))
						else:
							f.writelines('\t\\item %s\n' % (schoice[i][5]))
					f.writelines('\\end{enumerate}\n')
				# 多选题解答
				if num_mchoice>0:
					f.writelines('\\section{多项选择题解答}\n')
					f.writelines('\\begin{enumerate}[(1)]\n')
					for i in range(num_mchoice):
						answer = ''
						answer_raw = mchoice[i][5:9]
						for j in range(1, max(answer_raw)+1):
							thisanswer = ''
							for k in range(4):
								if answer_raw[k] == j:
									thisanswer = thisanswer + chr(k+65)
							answer = answer + '第'+str(j)+'空：' + thisanswer + '；' 
						if mchoice[i][9] != '':
							f.writelines('\t\\item %s\\\\\n' % (answer))
							f.writelines('\t\t解析：%s\n' % (mchoice[i][9]))
						else:
							f.writelines('\t\\item %s\n' % (answer))
					f.writelines('\\end{enumerate}\n')
				# 判断题解答
				if num_tof>0:
					f.writelines('\\section{判断题解答}\n')
					f.writelines('\\begin{enumerate}[(1)]\n')
					for i in range(num_tof):
						answer = ['错误', '正确']
						if tof[i][2] != '':
							f.writelines('\t\\item %s\\\\\n' % (answer(tof[i][1])))
							f.writelines('\t\t解析：%s\n' % (tof[i][2]))
						else:
							f.writelines('\t\\item %s\n' % (answer(tof[i][1])))
					f.writelines('\\end{enumerate}\n')
				# 填空题解答
				if num_blank>0:
					f.writelines('\\section{填空题解答}\n')
					f.writelines('\\begin{enumerate}[(1)]\n')
					for i in range(num_blank):
						if blank[i][5] != '':
							if blank[i][4] != '':
								f.writelines('\t\\item %s；%s；%s；%s\\\\\n' % (blank[i][1],blank[i][2],blank[i][3],blank[i][4]))
							elif blank[i][3] != '':
								f.writelines('\t\\item %s；%s；%s\\\\\n' % (blank[i][1],blank[i][2],blank[i][3]))
							elif blank[i][2] != '':
								f.writelines('\t\\item %s；%s\\\\\n' % (blank[i][1],blank[i][2]))
							else:
								f.writelines('\t\\item %s\\\\\n' % (blank[i][1]))
							f.writelines('\t\t解析：%s\n' % (blank[i][5]))
						else:
							if blank[i][4] != '':
								f.writelines('\t\\item %s；%s；%s；%s\n' % (blank[i][1],blank[i][2],blank[i][3],blank[i][4]))
							elif blank[i][3] != '':
								f.writelines('\t\\item %s；%s；%s\n' % (blank[i][1],blank[i][2],blank[i][3]))
							elif blank[i][2] != '':
								f.writelines('\t\\item %s；%s\n' % (blank[i][1],blank[i][2]))
							else:
								f.writelines('\t\\item %s\n' % (blank[i][1]))
					f.writelines('\\end{enumerate}\n')
				# 计算题解答
				if num_calculation>0:
					f.writelines('\\section{计算题解答}\n')
					f.writelines('\\begin{enumerate}[(1)]\n')
					for i in range(num_calculation):
						if calculation[i][1] == '':
							f.writelines('\t\\item 解：略\n')
						else:
							f.writelines('\t\\item 解：%s\n' % (calculation[i][1]))
					f.writelines('\\end{enumerate}\n')
				# 证明题解答
				if num_proof>0:
					f.writelines('\\section{计算题解答}\n')
					f.writelines('\\begin{enumerate}[(1)]\n')
					for i in range(num_proof):
						if proof[i][1] != '':
							f.writelines('\t\\item 证明：%s\n' % (proof[i][1]))
						else:
							f.writelines('\t\\item 证明：略\n')
					f.writelines('\\end{enumerate}\n')
			f.close()
			QMessageBox.about(self, u'通知', u'导出成功！')
		except Exception:
			QMessageBox.about(self, u'错误', u'导出失败！')
			return