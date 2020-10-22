# -*- coding: utf-8 -*-

'''
    主界面
'''

import random
import os
import requests
from webbrowser import open as webopen
import regex
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from AddSingleChoiceWindow import *
from AddMultipleChoiceWindow import *
from AddToFWindow import *
from AddFillinBlanksWindow import *
from AddCalculationWindow import *
from AddProofWindow import *
from SelectSectionsWindow import *
from PreviewQuestionsWindow import *

import myfunctions as myfun
from database import *


class MainWindow(QWidget):
	singal_sectionid = pyqtSignal(list)

	def __init__(self, parent=None):
		super(MainWindow , self).__init__(parent)
		self.ver = '2020.10.22'
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

		mainlayout = QVBoxLayout()

		self.createInfoBox()
		mainlayout.addLayout(self.InfoLayout)

		self.tabs = QTabWidget()
		self.tab_information = QWidget()
		self.tab_modification = QWidget()
		self.tab_export_by_section = QWidget()
		self.tab_export_by_question = QWidget()
		self.tab_settings = QWidget()
		self.tabs.addTab(self.tab_information, '题库概览')
		self.tabs.addTab(self.tab_modification, '录入与修改题目')
		self.tabs.addTab(self.tab_export_by_section, '按章节导出')
		self.tabs.addTab(self.tab_export_by_question, '自由选题导出')
		self.tabs.addTab(self.tab_settings, '题库设置')
		self.tab_informationUI()
		self.tab_modificationUI()
		self.tab_export_by_sectionUI()
		self.tab_export_by_questionUI()
		self.tab_settingsUI()
		mainlayout.addWidget(self.tabs)

		layout_about = QHBoxLayout()
		self.download_demo = QLabel(
			'<a href = "http://www.jhanmath.com/?page_id=228">'
			'观看视频演示</a>')
		self.download_demo.setOpenExternalLinks(True)
		self.download_demo.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
		layout_about.addWidget(self.download_demo)
		self.about = QLabel(
			f'This software is developed by Jing Han. ver. {self.ver}')
		self.about.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
		layout_about.addWidget(self.about)
		mainlayout.addLayout(layout_about)
		self.setLayout(mainlayout)
		self.resize(1000, 700)
		self.setWindowTitle("数学题库")

		self.btn_addschoice.setEnabled(False)
		self.btn_addmchoice.setEnabled(False)
		self.btn_addtof.setEnabled(False)
		self.btn_addblank.setEnabled(False)
		self.btn_addcalculation.setEnabled(False)
		self.btn_addproof.setEnabled(False)
		self.btn_changesections.setEnabled(False)
		self.btn_export_to_latex.setEnabled(False)
		self.btn_switch.setEnabled(False)
		self.btn_export_to_html.setEnabled(False)
		self.btn_import_id.setEnabled(False)
		self.btn_preview.setEnabled(False)
		self.radio_chap_sec.setEnabled(False)
		self.radio_source.setEnabled(False)
		self.radio_difficulty.setEnabled(False)
		self.stack_chap_sec.setEnabled(False)
		self.stack_source.setEnabled(False)
		self.combo_user.setEnabled(False)

		self.thread_update = Thread_update()  # 创建线程
		self.thread_update.setCurrentVer(self.ver)
		self.thread_update.res.connect(self.ask_update)
		self.thread_update.start()  # 开始线程

	def start(self):
		cwd = QDir.currentPath() + r'/db/'
		dbpath, _ = QFileDialog.getOpenFileName(self,  
											"选取数据库文件",  
											cwd, # 起始路径 
											"数据库文件 (*.db)")   # 设置文件扩展名过滤,用双分号间隔

		if not dbpath: # 如果没选择文件，即点击取消
			return
		try:
			self.mydb = DataBase(dbpath)
		except:
			QMessageBox.about(self, u'警告', u'读取数据库失败！')
			return
		self.data_init()
	
	def data_init(self):
		searchstring = 'select name from dbname'
		self.dbname = self.mydb.search(searchstring)[0][0]
		self.lbl_dbname.setText(self.dbname)

		self.update_total_questions_sum()
		self.update_tree_sections()
		self.selected_sectionids_in_ExportBox = []
		self.update_sections_in_ExportBox(self.selected_sectionids_in_ExportBox)
		self.update_combo_users()

		self.btn_addschoice.setEnabled(True)
		self.btn_addmchoice.setEnabled(True)
		self.btn_addtof.setEnabled(True)
		self.btn_addblank.setEnabled(True)
		self.btn_addcalculation.setEnabled(True)
		self.btn_addproof.setEnabled(True)
		self.btn_changesections.setEnabled(True)
		self.btn_export_to_latex.setEnabled(True)
		self.btn_switch.setEnabled(True)
		self.btn_export_to_html.setEnabled(True)
		self.btn_import_id.setEnabled(True)
		self.btn_preview.setEnabled(True)
		self.radio_chap_sec.setEnabled(True)
		self.radio_source.setEnabled(True)
		# self.radio_difficulty.setEnabled(True)
		self.stack_chap_sec.setEnabled(True)
		self.stack_source.setEnabled(True)
		self.combo_user.setEnabled(True)
	
	def btn_changedb_clicked(self):
		self.start()

	def btn_newdb_clicked(self):
		text, ok = QInputDialog.getText(self,'新建题库','请输入要新建的题库名称(课程名)')
		if ok:
			cwd = QDir.currentPath() + r'/db/'
			dbpath, _ = QFileDialog.getSaveFileName(self,  
                                    "保存数据库文件",  
                                    cwd, # 起始路径 
                                    "数据库文件 (*.db)") 
			if not dbpath: # 如果没保存，即点击取消
				return
			if os.path.exists(dbpath):
				os.remove(dbpath)
			self.mydb = DataBase(dbpath)
			self.mydb.build_structure()
			insertstring = f'INSERT INTO dbname ("name") VALUES ("{text.strip()}");'
			self.mydb.insert(insertstring)
			if self.combo_user.currentText() == '':
				insertstring = f'INSERT INTO users ("name") VALUES ("无名氏");'
			else:
				insertstring = f'INSERT INTO users ("name") VALUES ("{self.combo_user.currentText()}");'
			self.mydb.insert(insertstring)
			insertstring = f'INSERT INTO difficulties ("difficulty") VALUES ("未知");'
			self.mydb.insert(insertstring)
			insertstring = f'INSERT INTO difficulties ("difficulty") VALUES ("简单");'
			self.mydb.insert(insertstring)
			insertstring = f'INSERT INTO difficulties ("difficulty") VALUES ("中等");'
			self.mydb.insert(insertstring)
			insertstring = f'INSERT INTO difficulties ("difficulty") VALUES ("困难");'
			self.mydb.insert(insertstring)
			insertstring = f'INSERT INTO difficulties ("difficulty") VALUES ("地狱");'
			self.mydb.insert(insertstring)
			self.data_init()

	def check_settings(self):
		searchstring = 'select count(*) from users'
		check_users = self.mydb.search(searchstring)[0][0]
		searchstring = 'select count(*) from difficulties'
		check_difficulties = self.mydb.search(searchstring)[0][0]
		searchstring = 'select count(*) from sections'
		check_sections = self.mydb.search(searchstring)[0][0]
		searchstring = 'select count(*) from sources'
		check_sources = self.mydb.search(searchstring)[0][0]
		if check_users == 0 or check_difficulties == 0 or check_sections == 0 or check_sources == 0:
			QMessageBox.about(self, u'警告', u'题库中章节、难度、题目来源、操作人都不能为空，请每项至少添加一个条目！')
			return False
		return True

		
	def update_combo_users(self):
		self.combo_user.clear()
		searchstring = 'select * from users'
		self.users = self.mydb.search(searchstring)
		for i in range(len(self.users)):
			self.combo_user.addItem(self.users[i][1])

	def combo_user_changed(self):
		for item in self.users:
			if item[1] == self.combo_user.currentText():
				self.current_userid = item[0]

	def tab_informationUI(self):
		layout = QVBoxLayout()
		self.createTotalQuestionsNumBox()
		layout.addWidget(self.TotalQuestionsNumBox)
		self.createBrowseBox()
		layout.addWidget(self.BrowseBox)
		layout.setStretchFactor(self.TotalQuestionsNumBox, 1)
		layout.setStretchFactor(self.BrowseBox, 100)
		self.tab_information.setLayout(layout)		

	def tab_modificationUI(self):
		layout = QVBoxLayout()
		self.createAddQuestionBox()
		layout.addWidget(self.AddQuestionBox)
		self.createModifyQuestionBox()
		layout.addWidget(self.ModifyQuestionBox)
		self.tab_modification.setLayout(layout)
		self.last_added_section_id = 1
		self.last_added_difficulty_id = 1
		self.last_added_source_id = 1

	def tab_export_by_sectionUI(self):
		layout = QVBoxLayout()
		self.createSectionsBox()
		layout.addWidget(self.SectionsBox)
		self.createExportOptionsBox()
		layout.addWidget(self.ExportOptionsBox)
		self.tab_export_by_section.setLayout(layout)

	def tab_export_by_questionUI(self):
		layout = QVBoxLayout()
		self.createSelectedNumBox()
		layout.addWidget(self.SelectedNumBox)
		self.createSelectQuestionBox()
		layout.addWidget(self.SelectQuestionBox)
		layout.setStretchFactor(self.SelectedNumBox, 1)
		layout.setStretchFactor(self.SelectQuestionBox, 100)
		self.tab_export_by_question.setLayout(layout)
		self.update_selectedNum()

	def tab_settingsUI(self):
		layout = QVBoxLayout()
		hbox = QHBoxLayout()
		self.radio_chap_sec = QRadioButton()
		self.radio_chap_sec.setText('章节设置')
		self.radio_chap_sec.toggled.connect(self.on_radio_button_toggled)
		self.radio_difficulty = QRadioButton()
		self.radio_difficulty.setText('难度设置')
		self.radio_difficulty.toggled.connect(self.on_radio_button_toggled)
		self.radio_source = QRadioButton()
		self.radio_source.setText('题目来源设置')
		self.radio_source.toggled.connect(self.on_radio_button_toggled)
		self.radio_users = QRadioButton()
		self.radio_users.setText('操作人设置')
		self.radio_users.toggled.connect(self.on_radio_button_toggled)
		hbox.addWidget(self.radio_chap_sec)
		hbox.addWidget(self.radio_difficulty)
		hbox.addWidget(self.radio_source)
		hbox.addWidget(self.radio_users)
		layout.addLayout(hbox)

		self.stack_chap_sec = QWidget()
		grid_chap_sec = QGridLayout()
		self.tree_sections_in_settings = QTreeWidget()
		self.tree_sections_in_settings.setColumnCount(1)
		self.tree_sections_in_settings.setSelectionMode(QAbstractItemView.SingleSelection)
		self.tree_sections_in_settings.setHeaderLabels(['选择章或节(单选节点)'])
		self.tree_sections_in_settings.itemSelectionChanged.connect(self.tree_sections_in_settings_changed)
		grid_chap_sec.addWidget(self.tree_sections_in_settings, 0, 0, 1, 4)
		self.sectionid_selected_in_settings = 0
		self.chapterid_selected_in_settings = 0
		
		self.btn_add_chap_in_settings = QPushButton('添加章')
		self.btn_add_chap_in_settings.clicked.connect(self.btn_add_chap_in_settings_clicked)
		self.btn_add_sec_in_settings = QPushButton('添加节')
		self.btn_add_sec_in_settings.clicked.connect(self.btn_add_sec_in_settings_clicked)
		self.btn_modify_chap_sec_in_settings = QPushButton('修改章节名称')
		self.btn_modify_chap_sec_in_settings.clicked.connect(self.btn_modify_chap_sec_in_settings_clicked)
		self.btn_delete_chap_sec_in_settings = QPushButton('删除章节')
		self.btn_delete_chap_sec_in_settings.clicked.connect(self.btn_delete_chap_sec_in_settings_clicked)
		grid_chap_sec.addWidget(self.btn_add_chap_in_settings,1,0)
		grid_chap_sec.addWidget(self.btn_add_sec_in_settings,1,1)
		grid_chap_sec.addWidget(self.btn_modify_chap_sec_in_settings,1,2)
		grid_chap_sec.addWidget(self.btn_delete_chap_sec_in_settings,1,3)
		self.stack_chap_sec.setLayout(grid_chap_sec)

		self.stack_difficulty = QWidget()
		grid_difficulty = QGridLayout()
		self.list_difficulty_in_settings = QListWidget()
		self.list_difficulty_in_settings.addItem('难度')
		grid_difficulty.addWidget(self.list_difficulty_in_settings,0,0,1,3)
		self.btn_add_difficulty_in_settings = QPushButton('添加难度')
		self.btn_modify_difficulty_in_settings = QPushButton('修改难度名称')
		self.btn_delete_difficulty_in_settings = QPushButton('删除难度')
		grid_difficulty.addWidget(self.btn_add_difficulty_in_settings,1,0)
		grid_difficulty.addWidget(self.btn_modify_difficulty_in_settings,1,1)
		grid_difficulty.addWidget(self.btn_delete_difficulty_in_settings,1,2)
		self.stack_difficulty.setLayout(grid_difficulty)

		self.stack_source = QWidget()
		grid_source = QGridLayout()
		self.list_source_in_settings = QListWidget()
		# self.list_source_in_settings.addItem('来源')
		grid_source.addWidget(self.list_source_in_settings,0,0,1,3)
		self.btn_add_source_in_settings = QPushButton('添加来源')
		self.btn_add_source_in_settings.clicked.connect(self.btn_add_source_in_settings_clicked)
		self.btn_modify_source_in_settings = QPushButton('修改来源名称')
		self.btn_modify_source_in_settings.clicked.connect(self.btn_modify_source_in_settings_clicked)
		self.btn_delete_source_in_settings = QPushButton('删除来源')
		self.btn_delete_source_in_settings.clicked.connect(self.btn_delete_source_in_settings_clicked)
		grid_source.addWidget(self.btn_add_source_in_settings,1,0)
		grid_source.addWidget(self.btn_modify_source_in_settings,1,1)
		grid_source.addWidget(self.btn_delete_source_in_settings,1,2)
		self.stack_source.setLayout(grid_source)

		self.stack_users = QWidget()
		grid_users = QGridLayout()
		self.list_users_in_settings = QListWidget()
		# self.list_users_in_settings.addItem('来源')
		grid_users.addWidget(self.list_users_in_settings,0,0,1,3)
		self.btn_add_user_in_settings = QPushButton('添加操作人')
		self.btn_add_user_in_settings.clicked.connect(self.btn_add_user_in_settings_clicked)
		self.btn_modify_user_in_settings = QPushButton('修改操作人')
		self.btn_modify_user_in_settings.clicked.connect(self.btn_modify_user_in_settings_clicked)
		self.btn_delete_user_in_settings = QPushButton('删除操作人')
		self.btn_delete_user_in_settings.clicked.connect(self.btn_delete_user_in_settings_clicked)
		grid_users.addWidget(self.btn_add_user_in_settings,1,0)
		grid_users.addWidget(self.btn_modify_user_in_settings,1,1)
		grid_users.addWidget(self.btn_delete_user_in_settings,1,2)
		self.stack_users.setLayout(grid_users)

		self.stacks_in_settings = QStackedWidget()
		self.stacks_in_settings.addWidget(self.stack_chap_sec)
		self.stacks_in_settings.addWidget(self.stack_difficulty)
		self.stacks_in_settings.addWidget(self.stack_source)
		self.stacks_in_settings.addWidget(self.stack_users)
		layout.addWidget(self.stacks_in_settings)
		self.tab_settings.setLayout(layout)
		self.radio_chap_sec.setChecked(True)

	def on_radio_button_toggled(self):
		radiobutton = self.sender()
		if radiobutton.isChecked():
			if radiobutton.text() == '章节设置':
				self.stacks_in_settings.setCurrentIndex(0)
			elif radiobutton.text() == '难度设置':
				self.stacks_in_settings.setCurrentIndex(1)
			elif radiobutton.text() == '题目来源设置':
				self.stacks_in_settings.setCurrentIndex(2)
				self.update_list_source_in_settings()
			elif radiobutton.text() == '操作人设置':
				self.stacks_in_settings.setCurrentIndex(3)
				self.update_list_users_in_settings()

	def createInfoBox(self):
		self.DBDisplayBox = QGroupBox('')
		layout_db = QHBoxLayout()
		self.lbl_dbnamelabel = QLabel('当前题库: ')
		# self.lbl_dbnamelabel.setFixedWidth(60)
		self.lbl_dbname = QLabel('')
		self.btn_changedb = QPushButton('更换题库')
		self.btn_changedb.clicked.connect(self.btn_changedb_clicked)
		self.btn_newdb = QPushButton('新建题库')
		self.btn_newdb.clicked.connect(self.btn_newdb_clicked)
		# fm = QFontMetrics(self.btn_changedb.font())
		# self.btn_changedb.setFixedWidth(fm.width(self.btn_changedb.text())+20)
		layout_db.addWidget(self.lbl_dbnamelabel, 0, Qt.AlignLeft)
		layout_db.addWidget(self.lbl_dbname)
		layout_db.addWidget(self.btn_changedb, 0, Qt.AlignRight)
		layout_db.addWidget(self.btn_newdb, 0, Qt.AlignRight)
		# layout_db.setSpacing(5)
		self.DBDisplayBox.setLayout(layout_db)
		self.UserBox = QGroupBox('')
		layout_user = QHBoxLayout()
		self.lbl_userlabel = QLabel('操作人：')
		self.combo_user = QComboBox()
		self.combo_user.currentIndexChanged.connect(self.combo_user_changed)
		layout_user.addWidget(self.lbl_userlabel)
		layout_user.addWidget(self.combo_user)
		self.UserBox.setLayout(layout_user)
		self.InfoLayout = QHBoxLayout()
		self.InfoLayout.addWidget(self.DBDisplayBox)
		self.InfoLayout.addWidget(self.UserBox)


	def createTotalQuestionsNumBox(self):
		self.TotalQuestionsNumBox = QGroupBox('各类型题目总数')
		layout = QVBoxLayout()
		self.tbl_total_questions_num = QTableWidget()
		self.tbl_total_questions_num.setRowCount(1)
		self.tbl_total_questions_num.setColumnCount(6)
		self.tbl_total_questions_num.verticalHeader().setVisible(False)
		self.tbl_total_questions_num.setHorizontalHeaderLabels(['单选题数','多选题数','判断题数','填空题数','计算题数','证明题数'])
		self.tbl_total_questions_num.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
		self.tbl_total_questions_num.setEditTriggers(QAbstractItemView.NoEditTriggers)
		self.tbl_total_questions_num.setSelectionMode(QAbstractItemView.NoSelection)
		# self.update_total_questions_sum()
		self.tbl_total_questions_num.setFixedHeight(60)
		self.tbl_total_questions_num.setStyleSheet('''QTableWidget { border: 0; }''')
		self.tbl_total_questions_num.setGridStyle(0)
		layout.addWidget(self.tbl_total_questions_num)
		self.TotalQuestionsNumBox.setLayout(layout)
		self.TotalQuestionsNumBox.setMaximumHeight(self.tbl_total_questions_num.width()+20)
		
	def createBrowseBox(self):
		self.chapters_selected_previously = []
		self.selected_sectionsid_in_BrowseBox = []

		self.BrowseBox = QGroupBox('浏览题目')
		layout = QGridLayout()
		self.tree_sections_in_BrowseBox = QTreeWidget()
		self.tree_sections_in_BrowseBox.setColumnCount(1)
		self.tree_sections_in_BrowseBox.setMinimumWidth(250)
		self.tree_sections_in_BrowseBox.setMaximumWidth(400)
		self.tree_sections_in_BrowseBox.setSelectionMode(QAbstractItemView.MultiSelection)
		self.tree_sections_in_BrowseBox.setHeaderLabels(['选择章节(可多选)'])
		self.tree_sections_in_BrowseBox.clicked.connect(self.tree_sections_clicked)
		layout.addWidget(self.tree_sections_in_BrowseBox, 0, 0, 2, 1)

		layout2 = QGridLayout()
		self.chk_schoice_in_BrowseBox = QCheckBox('单选题')
		self.chk_mchoice_in_BrowseBox = QCheckBox('多选题')
		self.chk_tof_in_BrowseBox = QCheckBox('判断题')
		self.chk_blank_in_BrowseBox = QCheckBox('填空题')
		self.chk_calculation_in_BrowseBox = QCheckBox('计算题')
		self.chk_proof_in_BrowseBox = QCheckBox('证明题')
		self.chk_schoice_in_BrowseBox.setChecked(True)
		self.chk_mchoice_in_BrowseBox.setChecked(True)
		self.chk_tof_in_BrowseBox.setChecked(True)
		self.chk_blank_in_BrowseBox.setChecked(True)
		self.chk_calculation_in_BrowseBox.setChecked(True)
		self.chk_proof_in_BrowseBox.setChecked(True)
		self.chk_schoice_in_BrowseBox.clicked.connect(self.update_preview_in_BrowseBox)
		self.chk_mchoice_in_BrowseBox.clicked.connect(self.update_preview_in_BrowseBox)
		self.chk_tof_in_BrowseBox.clicked.connect(self.update_preview_in_BrowseBox)
		self.chk_blank_in_BrowseBox.clicked.connect(self.update_preview_in_BrowseBox)
		self.chk_calculation_in_BrowseBox.clicked.connect(self.update_preview_in_BrowseBox)
		self.chk_proof_in_BrowseBox.clicked.connect(self.update_preview_in_BrowseBox)
		layout2.addWidget(self.chk_schoice_in_BrowseBox, 0, 0)
		layout2.addWidget(self.chk_mchoice_in_BrowseBox, 0, 1)
		layout2.addWidget(self.chk_tof_in_BrowseBox, 0, 2)
		layout2.addWidget(self.chk_blank_in_BrowseBox, 1, 0)
		layout2.addWidget(self.chk_calculation_in_BrowseBox, 1, 1)
		layout2.addWidget(self.chk_proof_in_BrowseBox, 1, 2)
		layout.addLayout(layout2, 0, 1)

		self.webView_in_BrowseBox = QWebEngineView()
		self.webView_in_BrowseBox.setMinimumSize(600, 400)
		self.webView_in_BrowseBox.setContextMenuPolicy(0) # 禁止右键菜单
		self.update_preview_in_BrowseBox()
		layout.addWidget(self.webView_in_BrowseBox, 1, 1)
		layout.setHorizontalSpacing(20)
		layout.setRowStretch(0, 1)
		layout.setRowStretch(1, 3)
		self.BrowseBox.setLayout(layout)

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
		self.btn_addcalculation = QPushButton('添加计算题')
		self.btn_addcalculation.clicked.connect(self.btn_addcalculation_clicked)
		self.btn_addproof = QPushButton('添加证明题')
		self.btn_addproof.clicked.connect(self.btn_addproof_clicked)
		layout.setSpacing(10)
		layout.addWidget(self.btn_addschoice)
		layout.addWidget(self.btn_addmchoice)
		layout.addWidget(self.btn_addtof)
		layout.addWidget(self.btn_addblank)
		layout.addWidget(self.btn_addcalculation)
		layout.addWidget(self.btn_addproof)
		self.AddQuestionBox.setLayout(layout)

	def createModifyQuestionBox(self):
		self.ModifyQuestionBox = QGroupBox('修改题目')
		self.sectionid_selected_in_ModifyBox = 0 # 当前选择的章节id，0表示未选择
		self.questionid_in_ModifyBox = 0 # 当前显示的问题的id，0表示未选择
		self.questionids_in_ModifyBox = [] # 当前显示的章节下符合条件的全部问题的id
		self.question_data_in_ModifyBox = [] # 当前显示的问题的详细数据

		layout = QGridLayout()
		self.tree_sections_in_ModifyBox = QTreeWidget()
		self.tree_sections_in_ModifyBox.setColumnCount(1)
		self.tree_sections_in_ModifyBox.setMinimumWidth(250)
		self.tree_sections_in_ModifyBox.setMaximumWidth(400)
		self.tree_sections_in_ModifyBox.setSelectionMode(QAbstractItemView.SingleSelection)
		self.tree_sections_in_ModifyBox.setHeaderLabels(['选择节(单选子节点)'])
		layout.addWidget(self.tree_sections_in_ModifyBox, 0, 0, 3, 1)

		layout2 = QHBoxLayout()
		self.list_type_of_question_in_ModifyBox = QComboBox()
		self.list_type_of_question_in_ModifyBox.addItems(['单选题','多选题','判断题','填空题','计算题','证明题'])
		self.list_type_of_question_in_ModifyBox.setCurrentIndex(0)
		self.list_type_of_question_in_ModifyBox.currentIndexChanged.connect(self.retrieve_questionids_in_ModifyBox)
		self.lbl_sequence_in_ModifyBox = QLabel('题目序列：0/0')
		self.lbl_sequence_in_ModifyBox.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
		layout2.addWidget(self.list_type_of_question_in_ModifyBox)
		layout2.addWidget(self.lbl_sequence_in_ModifyBox)
		layout.addLayout(layout2, 0, 1, 1, 3)

		self.webView_in_ModifyBox = QWebEngineView()
		self.webView_in_ModifyBox.setMinimumSize(600, 400)
		self.webView_in_ModifyBox.setContextMenuPolicy(0) # 禁止右键菜单
		layout.addWidget(self.webView_in_ModifyBox, 1, 1, 1, 3)

		layout_navi_btn = QHBoxLayout()
		self.btn_previous = QPushButton('上一题(&Z)')
		self.btn_next = QPushButton('下一题(&X)')
		self.btn_modify = QPushButton('修改(&M)')
		self.btn_copy = QPushButton('复制(&C)')
		self.btn_delete = QPushButton('删除(&D)')
		fm = QFontMetrics(self.btn_modify.font())
		margin = 4
		self.btn_previous.setFixedWidth(fm.width(self.btn_previous.text()) + margin)
		self.btn_next.setFixedWidth(fm.width(self.btn_next.text()) + margin)
		self.btn_modify.setFixedWidth(fm.width(self.btn_modify.text()) + margin)
		self.btn_copy.setFixedWidth(fm.width(self.btn_copy.text()) + margin)
		self.btn_delete.setFixedWidth(fm.width(self.btn_delete.text()) + margin)
		self.btn_previous.setEnabled(False)
		self.btn_modify.setEnabled(False)
		self.btn_next.setEnabled(False)
		self.btn_delete.setEnabled(False)
		self.btn_copy.setEnabled(False)
		self.btn_previous.clicked.connect(self.btn_previous_clicked)
		self.btn_next.clicked.connect(self.btn_next_clicked)
		self.btn_modify.clicked.connect(self.btn_modify_clicked)
		self.btn_delete.clicked.connect(self.btn_delete_clicked)
		self.btn_copy.clicked.connect(self.btn_copy_clicked)
		layout_navi_btn.addWidget(self.btn_previous)
		layout_navi_btn.addWidget(self.btn_modify)
		layout_navi_btn.addWidget(self.btn_copy)
		layout_navi_btn.addWidget(self.btn_delete)
		layout_navi_btn.addWidget(self.btn_next)

		self.update_preview_in_ModifyBox()
		self.tree_sections_in_ModifyBox.itemSelectionChanged.connect(self.tree_sections_in_ModifyBox_changed)
		
		layout.addLayout(layout_navi_btn,2,2)
		layout.setHorizontalSpacing(20)
		layout.setRowStretch(0, 1)
		layout.setRowStretch(1, 100)
		self.ModifyQuestionBox.setLayout(layout)	

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

	def createExportOptionsBox(self):
		layout_number = QGridLayout()
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
		self.ed_calculation = QLineEdit('0')
		self.ed_proof = QLineEdit('0')
		regex = QRegExp("^[1-9]\d*|0$")
		validator = QRegExpValidator(regex)
		self.ed_schoice.setValidator(validator)
		self.ed_mchoice.setValidator(validator)
		self.ed_tof.setValidator(validator)
		self.ed_blank.setValidator(validator)
		self.ed_calculation.setValidator(validator)
		self.ed_proof.setValidator(validator)
		self.ed_schoice.setAlignment(Qt.AlignRight)
		self.ed_mchoice.setAlignment(Qt.AlignRight)
		self.ed_tof.setAlignment(Qt.AlignRight)
		self.ed_blank.setAlignment(Qt.AlignRight)
		self.ed_calculation.setAlignment(Qt.AlignRight)
		self.ed_proof.setAlignment(Qt.AlignRight)
		self.ed_schoice.setFixedWidth(100)
		self.ed_mchoice.setFixedWidth(100)
		self.ed_tof.setFixedWidth(100)
		self.ed_blank.setFixedWidth(100)
		self.ed_calculation.setFixedWidth(100)
		self.ed_proof.setFixedWidth(100)
		self.ed_schoice.textChanged.connect(self.ed_num_changed)
		self.ed_mchoice.textChanged.connect(self.ed_num_changed)
		self.ed_tof.textChanged.connect(self.ed_num_changed)
		self.ed_blank.textChanged.connect(self.ed_num_changed)
		self.ed_calculation.textChanged.connect(self.ed_num_changed)
		self.ed_proof.textChanged.connect(self.ed_num_changed)
		self.ed_schoice.installEventFilter(self)
		self.ed_mchoice.installEventFilter(self)
		self.ed_tof.installEventFilter(self)
		self.ed_blank.installEventFilter(self)
		self.ed_calculation.installEventFilter(self)
		self.ed_proof.installEventFilter(self)
		layout_number.addWidget(self.lbl_schoice, 0, 0)
		layout_number.addWidget(self.lbl_mchoice, 1, 0)
		layout_number.addWidget(self.lbl_tof, 2, 0)
		layout_number.addWidget(self.lbl_blank, 3, 0)
		layout_number.addWidget(self.lbl_calculate, 4, 0)
		layout_number.addWidget(self.lbl_prove, 5, 0)
		layout_number.addWidget(self.ed_schoice, 0, 1)
		layout_number.addWidget(self.ed_mchoice, 1, 1)
		layout_number.addWidget(self.ed_tof, 2, 1)
		layout_number.addWidget(self.ed_blank, 3, 1)
		layout_number.addWidget(self.ed_calculation, 4, 1)
		layout_number.addWidget(self.ed_proof, 5, 1)

		layout_options = QGridLayout()
		self.chk_solution = QCheckBox('包含解答')
		self.chk_solution.setToolTip('默认解答在所有题目之后显示')
		self.chk_random = QCheckBox('打乱题目顺序')
		self.chk_randomchoice = QCheckBox('打乱选择题选项顺序')
		self.chk_white = QCheckBox('主观题后留空')
		self.chk_follow = QCheckBox('解答跟随题干')
		self.chk_notsure = QCheckBox('未知难度')
		self.chk_easy = QCheckBox('简单难度')
		self.chk_medium = QCheckBox('中等难度')
		self.chk_hard = QCheckBox('困难难度')
		self.chk_hell = QCheckBox('地狱难度')
		self.chk_solution.setChecked(True)
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
		layout_options.addWidget(self.chk_random, 0, 1)
		layout_options.addWidget(self.chk_randomchoice, 1, 1)
		
		self.ed_title = QLineEdit()
		self.ed_title.setPlaceholderText('在此输入导出习题集的标题')
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
		self.btn_export_to_latex = QPushButton('导出 LaTeX')
		self.btn_export_to_latex.clicked.connect(self.export_questions_to_latex)
		self.btn_switch = QPushButton('切换至自由选题')
		self.btn_switch.clicked.connect(self.btn_switch_clicked)
		self.btn_export_to_html = QPushButton('导出 HTML')
		self.btn_export_to_html.clicked.connect(self.export_questions_to_html)
		layout_btn.addWidget(self.btn_export_to_latex)
		layout_btn.addWidget(self.btn_switch)
		layout_btn.addWidget(self.btn_export_to_html)

		layout = QGridLayout()
		layout.addLayout(layout_number, 0, 0, 2, 1)
		layout.addLayout(layout_options, 0, 1)
		layout.addLayout(layout_btn, 1, 1)
		layout.setColumnStretch(0, 1)
		layout.setColumnStretch(1, 5)
		layout.setHorizontalSpacing(30)

		self.ExportOptionsBox = QGroupBox('导出选项')
		self.ExportOptionsBox.setLayout(layout)

	def createSelectedNumBox(self): # 当前选中题目的数目
		self.SelectedNumBox = QGroupBox('当前选中各类型题目总数')
		layout = QVBoxLayout()
		self.tbl_selected_num = QTableWidget()
		self.tbl_selected_num.setRowCount(1)
		self.tbl_selected_num.setColumnCount(6)
		self.tbl_selected_num.verticalHeader().setVisible(False)
		self.tbl_selected_num.setHorizontalHeaderLabels(['单选题数','多选题数','判断题数','填空题数','计算题数','证明题数'])
		self.tbl_selected_num.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
		self.tbl_selected_num.setEditTriggers(QAbstractItemView.NoEditTriggers)
		self.tbl_selected_num.setSelectionMode(QAbstractItemView.NoSelection)
		# self.update_total_questions_sum()
		self.tbl_selected_num.setFixedHeight(60)
		self.tbl_selected_num.setStyleSheet('''QTableWidget { border: 0; }''')
		self.tbl_selected_num.setGridStyle(0)
		layout.addWidget(self.tbl_selected_num)
		self.SelectedNumBox.setLayout(layout)
		self.SelectedNumBox.setMaximumHeight(self.tbl_selected_num.width()+20)
	
	def createSelectQuestionBox(self):
		self.SelectQuestionBox = QGroupBox('选择题目')
		self.sectionid_selected_in_SelectQuestionBox = 0 # 当前选择的章节id，0表示未选择
		self.questionid_in_SelectQuestionBox = 0 # 当前显示的问题的id，0表示未选择
		self.questionids_in_SelectQuestionBox = [] # 当前显示的章节下符合条件的全部问题的id
		self.question_data_in_SelectQuestionBox = [] # 当前显示的问题的详细数据
		self.schoiceid_prepare = [] # 自由选择问题导出标签页中待导出的所有单选题id
		self.mchoiceid_prepare = [] # 自由选择问题导出标签页中待导出的所有多选题id
		self.tofid_prepare = [] # 自由选择问题导出标签页中待导出的所有判断题id
		self.blankid_prepare = [] # 自由选择问题导出标签页中待导出的所有填空题id
		self.calculationid_prepare = [] # 自由选择问题导出标签页中待导出的所有计算题id
		self.proofid_prepare = [] # 自由选择问题导出标签页中待导出的所有证明题id
		self.schoice_choiceseq_prepare = [] # 自由选择问题导出标签页中待导出的所有单选题选项顺序
		self.mchoice_choiceseq_prepare = [] # 自由选择问题导出标签页中待导出的所有多选题选项顺序

		layout = QGridLayout()
		self.tree_sections_in_SelectQuestionBox = QTreeWidget()
		self.tree_sections_in_SelectQuestionBox.setColumnCount(1)
		self.tree_sections_in_SelectQuestionBox.setMinimumWidth(250)
		self.tree_sections_in_SelectQuestionBox.setMaximumWidth(400)
		self.tree_sections_in_SelectQuestionBox.setSelectionMode(QAbstractItemView.SingleSelection)
		self.tree_sections_in_SelectQuestionBox.setHeaderLabels(['选择节(单选子节点)'])
		layout.addWidget(self.tree_sections_in_SelectQuestionBox, 0, 0, 3, 1)

		layout2 = QHBoxLayout()
		self.list_type_of_question_in_SelectQuestionBox = QComboBox()
		self.list_type_of_question_in_SelectQuestionBox.addItems(['单选题','多选题','判断题','填空题','计算题','证明题'])
		self.list_type_of_question_in_SelectQuestionBox.setCurrentIndex(0)
		self.list_type_of_question_in_SelectQuestionBox.currentIndexChanged.connect(self.retrieve_questionids_in_SelectQuestionBox)
		self.lbl_sequence_in_SelectQuestionBox = QLabel('题目序列：0/0')
		self.lbl_sequence_in_SelectQuestionBox.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
		layout2.addWidget(self.list_type_of_question_in_SelectQuestionBox)
		layout2.addWidget(self.lbl_sequence_in_SelectQuestionBox)
		layout.addLayout(layout2, 0, 1, 1, 3)

		self.webView_in_SelectQuestionBox = QWebEngineView()
		self.webView_in_SelectQuestionBox.setMinimumSize(600, 400)
		self.webView_in_SelectQuestionBox.setContextMenuPolicy(0) # 禁止右键菜单
		layout.addWidget(self.webView_in_SelectQuestionBox, 1, 1, 1, 3)

		layout_navi_btn = QHBoxLayout()
		self.btn_import_id = QPushButton('导入...')
		self.btn_preview = QPushButton('预览导出')
		self.btn_preview.clicked.connect(self.btn_preview_clicked)
		self.btn_previous_in_SelectQuestionBox = QPushButton('上一题(&Z)')
		self.btn_next_in_SelectQuestionBox = QPushButton('下一题(&X)')
		self.chk_select_in_SelectQuestionBox = QCheckBox('选中(&S)')
		fm = QFontMetrics(self.btn_import_id.font())
		margin = 20
		self.btn_previous_in_SelectQuestionBox.setFixedWidth(fm.width(self.btn_previous_in_SelectQuestionBox.text()) + margin)
		self.btn_next_in_SelectQuestionBox.setFixedWidth(fm.width(self.btn_next_in_SelectQuestionBox.text()) + margin)
		self.btn_import_id.setFixedWidth(fm.width(self.btn_import_id.text()) + margin)
		self.btn_preview.setFixedWidth(fm.width(self.btn_preview.text()) + margin)
		self.btn_previous_in_SelectQuestionBox.setEnabled(False)
		self.chk_select_in_SelectQuestionBox.setEnabled(False)
		self.btn_next_in_SelectQuestionBox.setEnabled(False)
		self.btn_import_id.clicked.connect(self.btn_import_id_clicked)
		self.btn_previous_in_SelectQuestionBox.clicked.connect(self.btn_previous_in_SelectQuestionBox_clicked)
		self.btn_next_in_SelectQuestionBox.clicked.connect(self.btn_next_in_SelectQuestionBox_clicked)
		self.chk_select_in_SelectQuestionBox.clicked.connect(self.chk_select_in_SelectQuestionBox_clicked)
		layout_navi_btn.addWidget(self.btn_import_id)
		layout_navi_btn.addWidget(self.btn_previous_in_SelectQuestionBox)
		layout_navi_btn.addWidget(self.chk_select_in_SelectQuestionBox)
		layout_navi_btn.addWidget(self.btn_next_in_SelectQuestionBox)
		layout_navi_btn.addWidget(self.btn_preview)
		layout_navi_btn.setSpacing(10)

		self.update_preview_in_SelectQuestionBox()
		self.tree_sections_in_SelectQuestionBox.itemSelectionChanged.connect(self.tree_sections_in_SelectQuestionBox_changed)
		
		layout.addLayout(layout_navi_btn,2,2)
		layout.setHorizontalSpacing(20)
		layout.setRowStretch(0, 1)
		layout.setRowStretch(1, 100)
		self.SelectQuestionBox.setLayout(layout)

	def btn_changesections_clicked(self):
		if not self.check_settings():
			return
		self.select_sections_ui = SelectSections(self.mydb)
		self.select_sections_ui.signal.connect(self.update_sections_in_ExportBox)
		self.singal_sectionid.connect(self.select_sections_ui.initialize)
		self.singal_sectionid.emit(self.selected_sectionids_in_ExportBox)
		self.select_sections_ui.show()

	def btn_addschoice_clicked(self):
		if not self.check_settings():
			return
		self.add_schoice_ui = AddSingleChoice(self.mydb)
		self.transmit_settings(self.add_schoice_ui)
		self.add_schoice_ui.show()

	def btn_addmchoice_clicked(self):
		if not self.check_settings():
			return
		self.add_mchoice_ui = AddMultipleChoice(self.mydb)
		self.transmit_settings(self.add_mchoice_ui)
		self.add_mchoice_ui.show()

	def btn_addtof_clicked(self):
		if not self.check_settings():
			return
		self.add_tof_ui = AddToF(self.mydb)
		self.transmit_settings(self.add_tof_ui)
		self.add_tof_ui.show()
	
	def btn_addblank_clicked(self):
		if not self.check_settings():
			return
		self.add_blank_ui = AddFillinBlanks(self.mydb)
		self.transmit_settings(self.add_blank_ui)
		self.add_blank_ui.show()

	def btn_addcalculation_clicked(self):
		if not self.check_settings():
			return
		self.add_calculation_ui = AddCalculation(self.mydb)
		self.transmit_settings(self.add_calculation_ui)
		self.add_calculation_ui.show()

	def btn_addproof_clicked(self):
		if not self.check_settings():
			return
		self.add_proof_ui = AddProof(self.mydb)
		self.transmit_settings(self.add_proof_ui)
		self.add_proof_ui.show()

	def btn_previous_clicked(self):
		index = self.questionids_in_ModifyBox.index(self.questionid_in_ModifyBox)
		if index != 0:
			self.questionid_in_ModifyBox = self.questionids_in_ModifyBox[index-1]
		self.update_preview_in_ModifyBox()

	def btn_next_clicked(self):
		index = self.questionids_in_ModifyBox.index(self.questionid_in_ModifyBox)
		if index != len(self.questionids_in_ModifyBox)-1:
			self.questionid_in_ModifyBox = self.questionids_in_ModifyBox[index+1]
		self.update_preview_in_ModifyBox()
	
	def btn_modify_clicked(self):
		if self.list_type_of_question_in_ModifyBox.currentText() == '单选题':
			self.add_schoice_ui = AddSingleChoice(self.mydb)
			self.add_schoice_ui.input_question.setPlainText(myfun.transform_latex_to_plaintext(self.question_data_in_ModifyBox[0]))
			self.add_schoice_ui.input_answerA.setPlainText(myfun.transform_latex_to_plaintext(self.question_data_in_ModifyBox[1]))
			self.add_schoice_ui.input_answerB.setPlainText(myfun.transform_latex_to_plaintext(self.question_data_in_ModifyBox[2]))
			self.add_schoice_ui.input_answerC.setPlainText(myfun.transform_latex_to_plaintext(self.question_data_in_ModifyBox[3]))
			self.add_schoice_ui.input_answerD.setPlainText(myfun.transform_latex_to_plaintext(self.question_data_in_ModifyBox[4]))
			if self.question_data_in_ModifyBox[5] == 'A':
				self.add_schoice_ui.btn_A.setChecked(True)
				self.add_schoice_ui.clickA()
			elif self.question_data_in_ModifyBox[5] == 'B':
				self.add_schoice_ui.btn_B.setChecked(True)
				self.add_schoice_ui.clickB()
			elif self.question_data_in_ModifyBox[5] == 'C':
				self.add_schoice_ui.btn_C.setChecked(True)
				self.add_schoice_ui.clickC()
			elif self.question_data_in_ModifyBox[5] == 'D':
				self.add_schoice_ui.btn_D.setChecked(True)
				self.add_schoice_ui.clickD()
			self.add_schoice_ui.input_explain.setPlainText(myfun.transform_latex_to_plaintext(self.question_data_in_ModifyBox[6]))
			i = 0
			while self.question_data_in_ModifyBox[7] != self.sections[i][0]:
				i += 1
			self.add_schoice_ui.list_section.setCurrentIndex(i)
			i = 0
			while self.question_data_in_ModifyBox[8] != self.difficulties[i][0]:
				i += 1
			self.add_schoice_ui.list_difficulty.setCurrentIndex(i)
			i = 0
			while self.question_data_in_ModifyBox[9] != self.sources[i][0]:
				i += 1
			self.add_schoice_ui.list_source.setCurrentIndex(i)
			self.add_schoice_ui.other_settings.connect(self.update_after_modification)
			self.add_schoice_ui.modification = self.questionid_in_ModifyBox
			self.add_schoice_ui.current_userid = self.current_userid
			self.add_schoice_ui.btn_add.setText('修改题目')
			self.add_schoice_ui.setWindowTitle('修改单选题')
			self.add_schoice_ui.show()
		if self.list_type_of_question_in_ModifyBox.currentText() == '多选题':
			self.add_mchoice_ui = AddMultipleChoice(self.mydb)
			self.add_mchoice_ui.input_question.setPlainText(myfun.transform_latex_to_plaintext(self.question_data_in_ModifyBox[0]))
			self.add_mchoice_ui.input_answerA.setPlainText(myfun.transform_latex_to_plaintext(self.question_data_in_ModifyBox[1]))
			self.add_mchoice_ui.input_answerB.setPlainText(myfun.transform_latex_to_plaintext(self.question_data_in_ModifyBox[2]))
			self.add_mchoice_ui.input_answerC.setPlainText(myfun.transform_latex_to_plaintext(self.question_data_in_ModifyBox[3]))
			self.add_mchoice_ui.input_answerD.setPlainText(myfun.transform_latex_to_plaintext(self.question_data_in_ModifyBox[4]))
			self.add_mchoice_ui.btn_A.setCurrentIndex(self.question_data_in_ModifyBox[5])
			self.add_mchoice_ui.btn_B.setCurrentIndex(self.question_data_in_ModifyBox[6])
			self.add_mchoice_ui.btn_C.setCurrentIndex(self.question_data_in_ModifyBox[7])
			self.add_mchoice_ui.btn_D.setCurrentIndex(self.question_data_in_ModifyBox[8])
			self.add_mchoice_ui.input_explain.setPlainText(myfun.transform_latex_to_plaintext(self.question_data_in_ModifyBox[9]))
			i = 0
			while self.question_data_in_ModifyBox[10] != self.sections[i][0]:
				i += 1
			self.add_mchoice_ui.list_section.setCurrentIndex(i)
			i = 0
			while self.question_data_in_ModifyBox[11] != self.difficulties[i][0]:
				i += 1
			self.add_mchoice_ui.list_difficulty.setCurrentIndex(i)
			i = 0
			while self.question_data_in_ModifyBox[12] != self.sources[i][0]:
				i += 1
			self.add_mchoice_ui.list_source.setCurrentIndex(i)
			self.add_mchoice_ui.other_settings.connect(self.update_after_modification)
			self.add_mchoice_ui.modification = self.questionid_in_ModifyBox
			self.add_mchoice_ui.current_userid = self.current_userid
			self.add_mchoice_ui.btn_add.setText('修改题目')
			self.add_mchoice_ui.setWindowTitle('修改多选题')
			self.add_mchoice_ui.show()
		if self.list_type_of_question_in_ModifyBox.currentText() == '判断题':
			self.add_tof_ui = AddToF(self.mydb)
			self.add_tof_ui.input_question.setPlainText(myfun.transform_latex_to_plaintext(self.question_data_in_ModifyBox[0]))
			self.add_tof_ui.list_answer.setCurrentIndex(myfun.transform_latex_to_plaintext(self.question_data_in_ModifyBox[1]))
			self.add_tof_ui.input_explain.setPlainText(myfun.transform_latex_to_plaintext(self.question_data_in_ModifyBox[2]))
			i = 0
			while self.question_data_in_ModifyBox[3] != self.sections[i][0]:
				i += 1
			self.add_tof_ui.list_section.setCurrentIndex(i)
			i = 0
			while self.question_data_in_ModifyBox[4] != self.difficulties[i][0]:
				i += 1
			self.add_tof_ui.list_difficulty.setCurrentIndex(i)
			i = 0
			while self.question_data_in_ModifyBox[5] != self.sources[i][0]:
				i += 1
			self.add_tof_ui.list_source.setCurrentIndex(i)
			self.add_tof_ui.other_settings.connect(self.update_after_modification)
			self.add_tof_ui.modification = self.questionid_in_ModifyBox
			self.add_tof_ui.current_userid = self.current_userid
			self.add_tof_ui.btn_add.setText('修改题目')
			self.add_tof_ui.setWindowTitle('修改判断题')
			self.add_tof_ui.show()
		if self.list_type_of_question_in_ModifyBox.currentText() == '填空题':
			self.add_blank_ui = AddFillinBlanks(self.mydb)
			self.add_blank_ui.input_question.setPlainText(myfun.transform_latex_to_plaintext(self.question_data_in_ModifyBox[0]))
			self.add_blank_ui.input_answer1.setPlainText(myfun.transform_latex_to_plaintext(self.question_data_in_ModifyBox[1]))
			self.add_blank_ui.input_answer2.setPlainText(myfun.transform_latex_to_plaintext(self.question_data_in_ModifyBox[2]))
			self.add_blank_ui.input_answer3.setPlainText(myfun.transform_latex_to_plaintext(self.question_data_in_ModifyBox[3]))
			self.add_blank_ui.input_answer4.setPlainText(myfun.transform_latex_to_plaintext(self.question_data_in_ModifyBox[4]))
			self.add_blank_ui.input_explain.setPlainText(myfun.transform_latex_to_plaintext(self.question_data_in_ModifyBox[5]))
			i = 0
			while self.question_data_in_ModifyBox[6] != self.sections[i][0]:
				i += 1
			self.add_blank_ui.list_section.setCurrentIndex(i)
			i = 0
			while self.question_data_in_ModifyBox[7] != self.difficulties[i][0]:
				i += 1
			self.add_blank_ui.list_difficulty.setCurrentIndex(i)
			i = 0
			while self.question_data_in_ModifyBox[8] != self.sources[i][0]:
				i += 1
			self.add_blank_ui.list_source.setCurrentIndex(i)
			self.add_blank_ui.other_settings.connect(self.update_after_modification)
			self.add_blank_ui.modification = self.questionid_in_ModifyBox
			self.add_blank_ui.current_userid = self.current_userid
			self.add_blank_ui.btn_add.setText('修改题目')
			self.add_blank_ui.setWindowTitle('修改填空题')
			self.add_blank_ui.show()
		if self.list_type_of_question_in_ModifyBox.currentText() == '计算题':
			self.add_calculation_ui = AddCalculation(self.mydb)
			self.add_calculation_ui.input_question.setPlainText(myfun.transform_latex_to_plaintext(self.question_data_in_ModifyBox[0]))
			self.add_calculation_ui.input_answer.setPlainText(myfun.transform_latex_to_plaintext(self.question_data_in_ModifyBox[1]))
			i = 0
			while self.question_data_in_ModifyBox[2] != self.sections[i][0]:
				i += 1
			self.add_calculation_ui.list_section.setCurrentIndex(i)
			i = 0
			while self.question_data_in_ModifyBox[3] != self.difficulties[i][0]:
				i += 1
			self.add_calculation_ui.list_difficulty.setCurrentIndex(i)
			i = 0
			while self.question_data_in_ModifyBox[4] != self.sources[i][0]:
				i += 1
			self.add_calculation_ui.list_source.setCurrentIndex(i)
			self.add_calculation_ui.other_settings.connect(self.update_after_modification)
			self.add_calculation_ui.modification = self.questionid_in_ModifyBox
			self.add_calculation_ui.current_userid = self.current_userid
			self.add_calculation_ui.btn_add.setText('修改题目')
			self.add_calculation_ui.setWindowTitle('修改计算题')
			self.add_calculation_ui.show()
		if self.list_type_of_question_in_ModifyBox.currentText() == '证明题':
			self.add_proof_ui = AddProof(self.mydb)
			self.add_proof_ui.input_question.setPlainText(myfun.transform_latex_to_plaintext(self.question_data_in_ModifyBox[0]))
			self.add_proof_ui.input_answer.setPlainText(myfun.transform_latex_to_plaintext(self.question_data_in_ModifyBox[1]))
			i = 0
			while self.question_data_in_ModifyBox[2] != self.sections[i][0]:
				i += 1
			self.add_proof_ui.list_section.setCurrentIndex(i)
			i = 0
			while self.question_data_in_ModifyBox[3] != self.difficulties[i][0]:
				i += 1
			self.add_proof_ui.list_difficulty.setCurrentIndex(i)
			i = 0
			while self.question_data_in_ModifyBox[4] != self.sources[i][0]:
				i += 1
			self.add_proof_ui.list_source.setCurrentIndex(i)
			self.add_proof_ui.other_settings.connect(self.update_after_modification)
			self.add_proof_ui.modification = self.questionid_in_ModifyBox
			self.add_proof_ui.current_userid = self.current_userid
			self.add_proof_ui.btn_add.setText('修改题目')
			self.add_proof_ui.setWindowTitle('修改证明题')
			self.add_proof_ui.show()

	def btn_delete_clicked(self):
		reply = QMessageBox.question(self, u'询问', u'确认删除当前题目？', QMessageBox.Yes, QMessageBox.No)
		if reply == QMessageBox.Yes:
			if self.list_type_of_question_in_ModifyBox.currentText() == '单选题':
				deletestring = ('delete from schoice where id = %d' % (self.questionid_in_ModifyBox))
			if self.list_type_of_question_in_ModifyBox.currentText() == '多选题':
				deletestring = ('delete from mchoice where id = %d' % (self.questionid_in_ModifyBox))
			if self.list_type_of_question_in_ModifyBox.currentText() == '判断题':
				deletestring = ('delete from tof where id = %d' % (self.questionid_in_ModifyBox))
			if self.list_type_of_question_in_ModifyBox.currentText() == '填空题':
				deletestring = ('delete from blank where id = %d' % (self.questionid_in_ModifyBox))
			if self.list_type_of_question_in_ModifyBox.currentText() == '计算题':
				deletestring = ('delete from calculation where id = %d' % (self.questionid_in_ModifyBox))
			if self.list_type_of_question_in_ModifyBox.currentText() == '证明题':
				deletestring = ('delete from proof where id = %d' % (self.questionid_in_ModifyBox))
			if self.mydb.insert(deletestring):
				QMessageBox.about(self, '通知', '删除成功！')
				index = self.questionids_in_ModifyBox.index(self.questionid_in_ModifyBox)
				self.questionids_in_ModifyBox.remove(self.questionid_in_ModifyBox)
				if len(self.questionids_in_ModifyBox) == 0:
					self.questionid_in_ModifyBox = 0 # 如果删除后当前题目列表为空，则问题id清0
				elif index == len(self.questionids_in_ModifyBox): # 如果删除的是当前题目列表中最后一个，则设置问题 id 为删除后列表中最后一个
					self.questionid_in_ModifyBox = self.questionids_in_ModifyBox[index - 1]
				else:
					self.questionid_in_ModifyBox = self.questionids_in_ModifyBox[index]
				self.update_preview_in_ModifyBox()
				self.update_preview_in_BrowseBox()
				self.update_preview_in_SelectQuestionBox()
				self.update_sections_in_ExportBox(self.selected_sectionids_in_ExportBox) # 更新按章节导出标签面上的题目数量
			else:
				QMessageBox.about(self, '通知', '删除失败！')

	def btn_copy_clicked(self):
		if self.list_type_of_question_in_ModifyBox.currentText() == '单选题':
			self.add_schoice_ui = AddSingleChoice(self.mydb)
			self.add_schoice_ui.input_question.setPlainText(myfun.transform_latex_to_plaintext(self.question_data_in_ModifyBox[0]))
			self.add_schoice_ui.input_answerA.setPlainText(self.question_data_in_ModifyBox[1].replace('\\\\\n','\n'))
			self.add_schoice_ui.input_answerB.setPlainText(self.question_data_in_ModifyBox[2].replace('\\\\\n','\n'))
			self.add_schoice_ui.input_answerC.setPlainText(self.question_data_in_ModifyBox[3].replace('\\\\\n','\n'))
			self.add_schoice_ui.input_answerD.setPlainText(self.question_data_in_ModifyBox[4].replace('\\\\\n','\n'))
			if self.question_data_in_ModifyBox[5] == 'A':
				self.add_schoice_ui.btn_A.setChecked(True)
				self.add_schoice_ui.clickA()
			elif self.question_data_in_ModifyBox[5] == 'B':
				self.add_schoice_ui.btn_B.setChecked(True)
				self.add_schoice_ui.clickB()
			elif self.question_data_in_ModifyBox[5] == 'C':
				self.add_schoice_ui.btn_C.setChecked(True)
				self.add_schoice_ui.clickC()
			elif self.question_data_in_ModifyBox[5] == 'D':
				self.add_schoice_ui.btn_D.setChecked(True)
				self.add_schoice_ui.clickD()
			self.add_schoice_ui.input_explain.setPlainText(myfun.transform_latex_to_plaintext(self.question_data_in_ModifyBox[6]))
			i = 0
			while self.question_data_in_ModifyBox[7] != self.sections[i][0]:
				i += 1
			self.add_schoice_ui.list_section.setCurrentIndex(i)
			i = 0
			while self.question_data_in_ModifyBox[8] != self.difficulties[i][0]:
				i += 1
			self.add_schoice_ui.list_difficulty.setCurrentIndex(i)
			i = 0
			while self.question_data_in_ModifyBox[9] != self.sources[i][0]:
				i += 1
			self.add_schoice_ui.list_source.setCurrentIndex(i)
			self.add_schoice_ui.other_settings.connect(self.update_after_insertion)
			self.add_schoice_ui.show()
		if self.list_type_of_question_in_ModifyBox.currentText() == '多选题':
			self.add_mchoice_ui = AddMultipleChoice(self.mydb)
			self.add_mchoice_ui.input_question.setPlainText(myfun.transform_latex_to_plaintext(self.question_data_in_ModifyBox[0]))
			self.add_mchoice_ui.input_answerA.setPlainText(self.question_data_in_ModifyBox[1].replace('\\\\\n','\n'))
			self.add_mchoice_ui.input_answerB.setPlainText(self.question_data_in_ModifyBox[2].replace('\\\\\n','\n'))
			self.add_mchoice_ui.input_answerC.setPlainText(self.question_data_in_ModifyBox[3].replace('\\\\\n','\n'))
			self.add_mchoice_ui.input_answerD.setPlainText(self.question_data_in_ModifyBox[4].replace('\\\\\n','\n'))
			self.add_mchoice_ui.btn_A.setCurrentIndex(self.question_data_in_ModifyBox[5])
			self.add_mchoice_ui.btn_B.setCurrentIndex(self.question_data_in_ModifyBox[6])
			self.add_mchoice_ui.btn_C.setCurrentIndex(self.question_data_in_ModifyBox[7])
			self.add_mchoice_ui.btn_D.setCurrentIndex(self.question_data_in_ModifyBox[8])
			self.add_mchoice_ui.input_explain.setPlainText(myfun.transform_latex_to_plaintext(self.question_data_in_ModifyBox[9]))
			i = 0
			while self.question_data_in_ModifyBox[10] != self.sections[i][0]:
				i += 1
			self.add_mchoice_ui.list_section.setCurrentIndex(i)
			i = 0
			while self.question_data_in_ModifyBox[11] != self.difficulties[i][0]:
				i += 1
			self.add_mchoice_ui.list_difficulty.setCurrentIndex(i)
			i = 0
			while self.question_data_in_ModifyBox[12] != self.sources[i][0]:
				i += 1
			self.add_mchoice_ui.list_source.setCurrentIndex(i)
			self.add_mchoice_ui.other_settings.connect(self.update_after_insertion)
			self.add_mchoice_ui.show()
		if self.list_type_of_question_in_ModifyBox.currentText() == '判断题':
			self.add_tof_ui = AddToF(self.mydb)
			self.add_tof_ui.input_question.setPlainText(myfun.transform_latex_to_plaintext(self.question_data_in_ModifyBox[0]))
			self.add_tof_ui.list_answer.setCurrentIndex(self.question_data_in_ModifyBox[1])
			self.add_tof_ui.input_explain.setPlainText(myfun.transform_latex_to_plaintext(self.question_data_in_ModifyBox[2]))
			i = 0
			while self.question_data_in_ModifyBox[3] != self.sections[i][0]:
				i += 1
			self.add_tof_ui.list_section.setCurrentIndex(i)
			i = 0
			while self.question_data_in_ModifyBox[4] != self.difficulties[i][0]:
				i += 1
			self.add_tof_ui.list_difficulty.setCurrentIndex(i)
			i = 0
			while self.question_data_in_ModifyBox[5] != self.sources[i][0]:
				i += 1
			self.add_tof_ui.list_source.setCurrentIndex(i)
			self.add_tof_ui.other_settings.connect(self.update_after_insertion)
			self.add_tof_ui.show()
		if self.list_type_of_question_in_ModifyBox.currentText() == '填空题':
			self.add_blank_ui = AddFillinBlanks(self.mydb)
			self.add_blank_ui.input_question.setPlainText(myfun.transform_latex_to_plaintext(self.question_data_in_ModifyBox[0]))
			self.add_blank_ui.input_answer1.setPlainText(self.question_data_in_ModifyBox[1].replace('\\\\\n','\n'))
			self.add_blank_ui.input_answer2.setPlainText(self.question_data_in_ModifyBox[2].replace('\\\\\n','\n'))
			self.add_blank_ui.input_answer3.setPlainText(self.question_data_in_ModifyBox[3].replace('\\\\\n','\n'))
			self.add_blank_ui.input_answer4.setPlainText(self.question_data_in_ModifyBox[4].replace('\\\\\n','\n'))
			self.add_blank_ui.input_explain.setPlainText(myfun.transform_latex_to_plaintext(self.question_data_in_ModifyBox[5]))
			i = 0
			while self.question_data_in_ModifyBox[6] != self.sections[i][0]:
				i += 1
			self.add_blank_ui.list_section.setCurrentIndex(i)
			i = 0
			while self.question_data_in_ModifyBox[7] != self.difficulties[i][0]:
				i += 1
			self.add_blank_ui.list_difficulty.setCurrentIndex(i)
			i = 0
			while self.question_data_in_ModifyBox[8] != self.sources[i][0]:
				i += 1
			self.add_blank_ui.list_source.setCurrentIndex(i)
			self.add_blank_ui.other_settings.connect(self.update_after_insertion)
			self.add_blank_ui.show()
		if self.list_type_of_question_in_ModifyBox.currentText() == '计算题':
			self.add_calculation_ui = AddCalculation(self.mydb)
			self.add_calculation_ui.input_question.setPlainText(myfun.transform_latex_to_plaintext(self.question_data_in_ModifyBox[0]))
			self.add_calculation_ui.input_answer.setPlainText(myfun.transform_latex_to_plaintext(self.question_data_in_ModifyBox[1]))
			i = 0
			while self.question_data_in_ModifyBox[2] != self.sections[i][0]:
				i += 1
			self.add_calculation_ui.list_section.setCurrentIndex(i)
			i = 0
			while self.question_data_in_ModifyBox[3] != self.difficulties[i][0]:
				i += 1
			self.add_calculation_ui.list_difficulty.setCurrentIndex(i)
			i = 0
			while self.question_data_in_ModifyBox[4] != self.sources[i][0]:
				i += 1
			self.add_calculation_ui.list_source.setCurrentIndex(i)
			self.add_calculation_ui.other_settings.connect(self.update_after_insertion)
			self.add_calculation_ui.show()
		if self.list_type_of_question_in_ModifyBox.currentText() == '证明题':
			self.add_proof_ui = AddProof(self.mydb)
			self.add_proof_ui.input_question.setPlainText(myfun.transform_latex_to_plaintext(self.question_data_in_ModifyBox[0]))
			self.add_proof_ui.input_answer.setPlainText(myfun.transform_latex_to_plaintext(self.question_data_in_ModifyBox[1]))
			i = 0
			while self.question_data_in_ModifyBox[2] != self.sections[i][0]:
				i += 1
			self.add_proof_ui.list_section.setCurrentIndex(i)
			i = 0
			while self.question_data_in_ModifyBox[3] != self.difficulties[i][0]:
				i += 1
			self.add_proof_ui.list_difficulty.setCurrentIndex(i)
			i = 0
			while self.question_data_in_ModifyBox[4] != self.sources[i][0]:
				i += 1
			self.add_proof_ui.list_source.setCurrentIndex(i)
			self.add_proof_ui.other_settings.connect(self.update_after_insertion)
			self.add_proof_ui.show()

	def btn_previous_in_SelectQuestionBox_clicked(self):
		index = self.questionids_in_SelectQuestionBox.index(self.questionid_in_SelectQuestionBox)
		if index != 0:
			self.questionid_in_SelectQuestionBox = self.questionids_in_SelectQuestionBox[index-1]
		self.update_preview_in_SelectQuestionBox()

	def btn_next_in_SelectQuestionBox_clicked(self):
		index = self.questionids_in_SelectQuestionBox.index(self.questionid_in_SelectQuestionBox)
		if index != len(self.questionids_in_SelectQuestionBox)-1:
			self.questionid_in_SelectQuestionBox = self.questionids_in_SelectQuestionBox[index+1]
		self.update_preview_in_SelectQuestionBox()

	def btn_import_id_clicked(self):
		if not self.check_settings():
			return
		folder = QDir.currentPath() + '/exports/'
		filename, _ = QFileDialog.getOpenFileName(self, '请选择文件', folder, "txt files (*.txt)")
		if not filename:
			return
		f = open(filename, 'r', encoding='utf-8')
		f_list = f.readlines()
		f_list = [line.strip() for line in f_list]
		try:
			schoice_index = f_list.index('[schoice]')
			mchoice_index = f_list.index('[mchoice]')
			tof_index = f_list.index('[tof]')
			blank_index = f_list.index('[blank]')
			calculation_index = f_list.index('[calculation]')
			proof_index = f_list.index('[proof]')
		except Exception as e:
			print(e)
			QMessageBox.about(self, '错误', '读取id出错！')
			return
		self.schoiceid_prepare.clear()
		self.schoice_choiceseq_prepare.clear()
		self.mchoiceid_prepare.clear()
		self.mchoice_choiceseq_prepare.clear()
		self.tofid_prepare.clear()
		self.blankid_prepare.clear()
		self.calculationid_prepare.clear()
		self.proofid_prepare.clear()
		for i in range(schoice_index+1, mchoice_index):
			items = f_list[i].split(',')
			self.schoiceid_prepare.append(int(items[0]))
			self.schoice_choiceseq_prepare.append([int(items[i]) for i in range(1,5)])
		for i in range(mchoice_index+1, tof_index):
			items = f_list[i].split(',')
			self.mchoiceid_prepare.append(int(items[0]))
			self.mchoice_choiceseq_prepare.append([int(items[i]) for i in range(1,5)])
		for i in range(tof_index+1, blank_index):
			self.tofid_prepare.append(int(f_list[i]))
		for i in range(blank_index+1, calculation_index):
			self.blankid_prepare.append(int(f_list[i]))
		for i in range(calculation_index+1, proof_index):
			self.calculationid_prepare.append(int(f_list[i]))
		for i in range(proof_index+1, len(f_list)):
			self.proofid_prepare.append(int(f_list[i]))
		self.update_checkStatus_in_SelectQuestionBox()
		self.update_selectedNum()

	def btn_preview_clicked(self):
		self.preview_ui = PreviewQuestions(self.mydb)
		self.preview_ui.schoiceid = self.schoiceid_prepare
		self.preview_ui.mchoiceid = self.mchoiceid_prepare
		self.preview_ui.tofid = self.tofid_prepare
		self.preview_ui.blankid = self.blankid_prepare
		self.preview_ui.calculationid = self.calculationid_prepare
		self.preview_ui.proofid = self.proofid_prepare
		self.preview_ui.schoice_seq = self.schoice_choiceseq_prepare
		self.preview_ui.mchoice_seq = self.mchoice_choiceseq_prepare
		self.options['title'] = self.ed_title.text().strip()
		self.preview_ui.options = self.options
		self.preview_ui.createPreview()
		self.preview_ui.show()

	def btn_switch_clicked(self):
		[passed,schoiceid,mchoiceid,tofid,blankid,calculationid,proofid]=self.get_questionid_in_ExportbySection()
		if not passed:
			return
		self.schoiceid_prepare = schoiceid
		self.mchoiceid_prepare = mchoiceid
		self.tofid_prepare = tofid
		self.blankid_prepare = blankid
		self.calculationid_prepare = calculationid
		self.proofid_prepare = proofid
		self.update_selectedNum()
		self.update_checkStatus_in_SelectQuestionBox()
		self.tabs.setCurrentWidget(self.tab_export_by_question)

	def btn_add_source_in_settings_clicked(self):
		text, ok = QInputDialog.getText(self,'添加题目来源','请输入要添加的题目来源')
		if ok:
			exist = False
			for item in self.sources:
				if item[1] == text.strip():
					exist = True
					break
			if exist:
				QMessageBox.about(self, u'警告', u'题库中已有该来源！')
			else:
				insertstring = f'INSERT INTO "main"."sources" ("source") VALUES ("{text.strip()}");'
				if not self.mydb.insert(insertstring):
					QMessageBox.about(self, u'警告', u'添加失败，请联系管理员！')
				else:
					self.update_list_source_in_settings()
			
	def btn_modify_source_in_settings_clicked(self):
		selected_row = self.list_source_in_settings.currentRow()
		if selected_row == -1:
			QMessageBox.about(self, u'警告', u'请选中要修改的条目！')
			return
		text, ok = QInputDialog.getText(self,'修改题目来源','请输入新的题目来源', QLineEdit.Normal, self.list_source_in_settings.currentItem().text())
		if ok:
			exist = False
			for item in self.sources:
				if item[1] == text.strip():
					exist = True
					break
			if exist:
				QMessageBox.about(self, u'警告', u'题库中已有该来源！')
				return
			else:
				updatestring = 'UPDATE "main"."sources" SET source="' + text.strip() + '" where id=%d;' % (self.sources[self.list_source_in_settings.currentRow()][0])
				if not self.mydb.insert(updatestring):
					QMessageBox.about(self, u'警告', u'修改失败，请联系管理员！')
				else:
					self.update_list_source_in_settings()
		

	def btn_delete_source_in_settings_clicked(self):
		selected_row = self.list_source_in_settings.currentRow()
		if selected_row == -1:
			QMessageBox.about(self, u'警告', u'请选中要删除的条目！')
			return
		source_id = self.sources[self.list_source_in_settings.currentRow()][0]
		countstring = f'''SELECT sum(num) from (
						SELECT count(*) as num from schoice where source={source_id}
						UNION ALL
						SELECT count(*) as num from mchoice where source={source_id}
						UNION ALL
						SELECT count(*) as num from tof where source = {source_id}
						UNION ALL
						SELECT count(*) as num from blank where source = {source_id}
						UNION ALL
						SELECT count(*) as num from calculation where source = {source_id}
						UNION ALL
						SELECT count(*) as num from proof where source = {source_id}
						) as total'''
		num = self.mydb.search(countstring)
		if num[0][0] > 0:
			QMessageBox.about(self, u'警告', f'题库中有 {num[0][0]} 道当前来源题目，不能删除该题目来源！')
			return
		deletestring = 'delete from sources where id=%d;' % (self.sources[self.list_source_in_settings.currentRow()][0])
		if not self.mydb.insert(deletestring):
			QMessageBox.about(self, u'警告', u'删除失败，请联系管理员！')
		else:
			self.update_list_source_in_settings()
	
	def btn_add_chap_in_settings_clicked(self):
		text, ok = QInputDialog.getText(self,'添加章','请输入要添加的章标题')
		if ok:
			exist = False
			for item in self.chapters:
				if item[1] == text.strip():
					exist = True
					break
			if exist:
				QMessageBox.about(self, u'警告', u'题库中已有相同的章标题！')
				return
			else:
				insertstring = 'INSERT INTO "main"."chapters" ("chapter") VALUES ("' + text.strip() + '");'
				if not self.mydb.insert(insertstring):
					QMessageBox.about(self, u'警告', u'添加失败，请联系管理员！')
				else:
					self.update_tree_sections()

	def btn_add_sec_in_settings_clicked(self):
		if self.chapterid_selected_in_settings == 0 and self.sectionid_selected_in_settings == 0:
			QMessageBox.about(self, u'警告', u'请选中父级章标题或同级节标题！')
			return
		text, ok = QInputDialog.getText(self,'添加节','请输入要添加的节标题')
		if ok:
			exist = False
			for item in self.sections:
				if item[2] == self.chapterid_selected_in_settings and item[1] == text.strip():
					exist = True
					break
			if exist:
				QMessageBox.about(self, u'警告', u'选中的章中已有相同的节标题！')
				return
			else:
				insertstring = f'INSERT INTO "main"."sections" ("section", "chapter") VALUES ("{text.strip()}", {self.chapterid_selected_in_settings});'
				if not self.mydb.insert(insertstring):
					QMessageBox.about(self, u'警告', u'添加失败，请联系管理员！')
					return
				else:
					self.update_tree_sections()
	
	def btn_modify_chap_sec_in_settings_clicked(self):
		if self.chapterid_selected_in_settings == 0 and self.sectionid_selected_in_settings == 0: # 如果章和节标题都没选中
			QMessageBox.about(self, u'警告', u'请选中章标题或节标题！')
			return
		if self.sectionid_selected_in_settings == 0: # 如果没选中节标题(即当前选中的是章标题)
			text, ok = QInputDialog.getText(self,'修改章标题','请输入新的章标题')
			if ok:
				exist = False
				for item in self.chapters:
					if item[1] == text.strip():
						exist = True
						break
				if exist:
					QMessageBox.about(self, u'警告', u'题库中已有相同的章标题！')
					return
				else:
					updatestring = (f'UPDATE chapters SET chapter="{text.strip()}" where id={self.chapterid_selected_in_settings};')
					if not self.mydb.insert(updatestring):
						QMessageBox.about(self, u'警告', u'修改失败，请联系管理员！')
						return
					else:
						self.update_tree_sections()
						self.update_sections_in_ExportBox(self.selected_sectionids_in_ExportBox)
		elif self.sectionid_selected_in_settings != 0: # 如果选中了节标题
			text, ok = QInputDialog.getText(self,'修改节标题','请输入新的节标题')
			if ok:
				exist = False
				for item in self.sections:
					if item[2] == self.chapterid_selected_in_settings and item[1] == text.strip():
						exist = True
						break
				if exist:
					QMessageBox.about(self, u'警告', u'选中的章中已有相同的节标题！')
					return
				else:
					updatestring = (f'UPDATE sections SET section="{text.strip()}" where id={self.sectionid_selected_in_settings};')
					if not self.mydb.insert(updatestring):
						QMessageBox.about(self, u'警告', u'修改失败，请联系管理员！')
						return
					else:
						self.update_tree_sections()
						self.update_sections_in_ExportBox(self.selected_sectionids_in_ExportBox)

	def btn_delete_chap_sec_in_settings_clicked(self):
		if self.chapterid_selected_in_settings == 0 and self.sectionid_selected_in_settings == 0: # 如果章和节标题都没选中
			QMessageBox.about(self, u'警告', u'请选中章标题或节标题！')
			return
		if self.sectionid_selected_in_settings == 0: # 如果没选中节标题(即当前选中的是章标题)
			searchstring = f'Select count(*) from sections where chapter={self.chapterid_selected_in_settings}'
			num = self.mydb.search(searchstring)
			if num[0][0] > 0:
				QMessageBox.about(self, u'警告', f'选中的章标题下有 {num[0][0]} 个节标题，不能删除！')
				return
			deletestring = f'delete from chapters where id={self.chapterid_selected_in_settings}'
			if not self.mydb.insert(deletestring):
				QMessageBox.about(self, u'警告', u'删除失败，请联系管理员！')
			else:
				self.update_tree_sections()
		elif self.sectionid_selected_in_settings != 0: # 如果选中了节标题
			countstring = f'''SELECT sum(num) from (
						SELECT count(*) as num from schoice where section={self.sectionid_selected_in_settings}
						UNION ALL
						SELECT count(*) as num from mchoice where section={self.sectionid_selected_in_settings}
						UNION ALL
						SELECT count(*) as num from tof where section={self.sectionid_selected_in_settings}
						UNION ALL
						SELECT count(*) as num from blank where section={self.sectionid_selected_in_settings}
						UNION ALL
						SELECT count(*) as num from calculation where section={self.sectionid_selected_in_settings}
						UNION ALL
						SELECT count(*) as num from proof where section={self.sectionid_selected_in_settings}
						) as total'''
			num = self.mydb.search(countstring)
			if num[0][0] > 0:
				QMessageBox.about(self, u'警告', f'选中的节标题下有 {num[0][0]} 道题目，不能删除！')
				return
			deletestring = f'delete from sections where id={self.sectionid_selected_in_settings}'
			if not self.mydb.insert(deletestring):
				QMessageBox.about(self, u'警告', u'删除失败，请联系管理员！')
			else:
				# 以下不能交换顺序
				if self.selected_sectionids_in_ExportBox.count(self.sectionid_selected_in_settings) != 0:
					self.selected_sectionids_in_ExportBox.remove(self.sectionid_selected_in_settings)
					self.update_sections_in_ExportBox(self.selected_sectionids_in_ExportBox)
				self.update_tree_sections()

	def btn_add_user_in_settings_clicked(self):
		text, ok = QInputDialog.getText(self,'添加操作人','请输入操作人姓名')
		if ok:
			exist = False
			for item in self.users:
				if item[1] == text.strip():
					exist = True
					break
			if exist:
				QMessageBox.about(self, u'警告', u'题库中已有同名操作人！')
			else:
				insertstring = f'INSERT INTO "main"."users" ("name") VALUES ("{text.strip()}");'
				if not self.mydb.insert(insertstring):
					QMessageBox.about(self, u'警告', u'添加失败，请联系管理员！')
				else:
					self.update_combo_users()
					self.update_list_users_in_settings()
			
	def btn_modify_user_in_settings_clicked(self):
		selected_row = self.list_users_in_settings.currentRow()
		if selected_row == -1:
			QMessageBox.about(self, u'警告', u'请选中要修改的条目！')
			return
		text, ok = QInputDialog.getText(self,'修改操作人姓名','请输入新的操作人', QLineEdit.Normal, self.list_users_in_settings.currentItem().text())
		if ok:
			exist = False
			for item in self.users:
				if item[1] == text.strip():
					exist = True
					break
			if exist:
				QMessageBox.about(self, u'警告', u'题库中已有同名操作人！')
				return
			else:
				updatestring = f'UPDATE "main"."users" SET name="{text.strip()}" where id={self.users[self.list_users_in_settings.currentRow()][0]};'
				if not self.mydb.insert(updatestring):
					QMessageBox.about(self, u'警告', u'修改失败，请联系管理员！')
				else:
					self.update_combo_users()
					self.update_list_users_in_settings()
		

	def btn_delete_user_in_settings_clicked(self):
		selected_row = self.list_users_in_settings.currentRow()
		if selected_row == -1:
			QMessageBox.about(self, u'警告', u'请选中要删除的条目！')
			return
		user_id = self.users[self.list_users_in_settings.currentRow()][0]
		countstring = f'''SELECT sum(num) from (
						SELECT count(*) as num from schoice where inputuser={user_id} or modifyuser={user_id}
						UNION ALL
						SELECT count(*) as num from mchoice where inputuser={user_id} or modifyuser={user_id}
						UNION ALL
						SELECT count(*) as num from tof where inputuser = {user_id} or modifyuser={user_id}
						UNION ALL
						SELECT count(*) as num from blank where inputuser = {user_id} or modifyuser={user_id}
						UNION ALL
						SELECT count(*) as num from calculation where inputuser = {user_id} or modifyuser={user_id}
						UNION ALL
						SELECT count(*) as num from proof where inputuser = {user_id} or modifyuser={user_id}
						) as total'''
		num = self.mydb.search(countstring)
		if num[0][0] > 0:
			QMessageBox.about(self, u'警告', f'题库中有 {num[0][0]} 道题目由选中操作人录入或修改，不能删除该操作人！')
			return
		deletestring = f'delete from users where id={user_id};'
		if not self.mydb.insert(deletestring):
			QMessageBox.about(self, u'警告', u'删除失败，请联系管理员！')
		else:
			self.update_combo_users()
			self.update_list_users_in_settings()

	def chk_select_in_SelectQuestionBox_clicked(self):
		if self.list_type_of_question_in_SelectQuestionBox.currentText() == '单选题':
			if self.chk_select_in_SelectQuestionBox.isChecked():
				self.schoiceid_prepare.append(self.questionid_in_SelectQuestionBox)
				self.schoice_choiceseq_prepare.append([1,2,3,4])
			else:
				index = self.schoiceid_prepare.index(self.questionid_in_SelectQuestionBox)
				del self.schoiceid_prepare[index]
				del self.schoice_choiceseq_prepare[index]
		elif self.list_type_of_question_in_SelectQuestionBox.currentText() == '多选题':
			if self.chk_select_in_SelectQuestionBox.isChecked():
				self.mchoiceid_prepare.append(self.questionid_in_SelectQuestionBox)
				self.mchoice_choiceseq_prepare.append([1,2,3,4])
			else:
				index = self.mchoiceid_prepare.index(self.questionid_in_SelectQuestionBox)
				del self.mchoiceid_prepare[index]
				del self.mchoice_choiceseq_prepare[index]
		elif self.list_type_of_question_in_SelectQuestionBox.currentText() == '判断题':
			if self.chk_select_in_SelectQuestionBox.isChecked():
				self.tofid_prepare.append(self.questionid_in_SelectQuestionBox)
			else:
				self.tofid_prepare.remove(self.questionid_in_SelectQuestionBox)
		elif self.list_type_of_question_in_SelectQuestionBox.currentText() == '填空题':
			if self.chk_select_in_SelectQuestionBox.isChecked():
				self.blankid_prepare.append(self.questionid_in_SelectQuestionBox)
			else:
				self.blankid_prepare.remove(self.questionid_in_SelectQuestionBox)
		elif self.list_type_of_question_in_SelectQuestionBox.currentText() == '计算题':
			if self.chk_select_in_SelectQuestionBox.isChecked():
				self.calculationid_prepare.append(self.questionid_in_SelectQuestionBox)
			else:
				self.calculationid_prepare.remove(self.questionid_in_SelectQuestionBox)
		elif self.list_type_of_question_in_SelectQuestionBox.currentText() == '证明题':
			if self.chk_select_in_SelectQuestionBox.isChecked():
				self.proofid_prepare.append(self.questionid_in_SelectQuestionBox)
			else:
				self.proofid_prepare.remove(self.questionid_in_SelectQuestionBox)
		self.update_selectedNum()

	def chk_solution_clicked(self):
		if not self.chk_solution.isChecked():
			self.chk_follow.setChecked(False)
		self.chk_follow.setEnabled(self.chk_solution.isChecked())
		self.setoptions()

	# def chk_white_clicked(self):
	# 	if self.chk_white.isChecked():
	# 		self.chk_follow.setChecked(False)
	# 	self.setoptions()

	# def chk_follow_clicked(self):
	# 	if self.chk_follow.isChecked():
	# 		self.chk_white.setChecked(False)
	# 	self.setoptions()
	
	def ed_num_changed(self):
		if self.sender().text() == '':
			self.sender().setText('0')
		pass

	def eventFilter(self, object, event):
		# 当输入数字时输入框中是0，则删去0，输入数字
		if object == self.ed_schoice or object == self.ed_mchoice or object == self.ed_tof or object == self.ed_blank or object == self.ed_calculation or object == self.ed_proof:
			if event.type() == QEvent.KeyPress:
				key = QKeyEvent(event)
				if key.key() >=49 and key.key() <=57 and object.text() == '0':
					object.setText(key.text())
					return True
		return QWidget.eventFilter(self, object, event)

	def tree_sections_clicked(self):
		currentItem = self.tree_sections_in_BrowseBox.currentItem()
		if currentItem.parent() == None: # 如果点击的是章
			if (not currentItem.isSelected()) and (currentItem in self.chapters_selected_previously): # 如果上次选中，这次没选中，则设置所有子节点未选中
				self.chapters_selected_previously.remove(currentItem)
				for i in range(currentItem.childCount()):
					currentItem.child(i).setSelected(False)
			elif (currentItem.isSelected()) and (currentItem not in self.chapters_selected_previously): # 如果上次未选中，这次选中，则设置所有子节点选中
				self.chapters_selected_previously.append(currentItem)
				for i in range(currentItem.childCount()):
					currentItem.child(i).setSelected(True)
		else: # 如果点击的是节
			if (not currentItem.isSelected()) and currentItem.parent().isSelected(): # 如果点击的节取消选中，且其父节点章被选中，则设置父节点为未选中
				currentItem.parent().setSelected(False)
				self.chapters_selected_previously.remove(currentItem.parent())
		items = self.tree_sections_in_BrowseBox.selectedItems()
		self.selected_sectionsid_in_BrowseBox = []
		for item in items:
			if item.parent() != None: # 不是父节点的话
				i = 0
				while item.text(0) != self.sections[i][1]:
					i = i + 1
				self.selected_sectionsid_in_BrowseBox.append(self.sections[i][0])
			else:
				pass
		self.update_preview_in_BrowseBox()

	def tree_sections_in_ModifyBox_changed(self):
		currentItem = self.tree_sections_in_ModifyBox.currentItem()
		if currentItem.isSelected():
			if currentItem.parent() != None:
				i = 0
				while currentItem.text(0) != self.sections[i][1]:
					i += 1
				self.sectionid_selected_in_ModifyBox = self.sections[i][0]
			else:
				self.sectionid_selected_in_ModifyBox = 0
		else:
			self.sectionid_selected_in_ModifyBox = 0
		self.retrieve_questionids_in_ModifyBox()

	def tree_sections_in_SelectQuestionBox_changed(self):
		currentItem = self.tree_sections_in_SelectQuestionBox.currentItem()
		if currentItem.isSelected():
			if currentItem.parent() != None:
				i = 0
				while currentItem.text(0) != self.sections[i][1]:
					i += 1
				self.sectionid_selected_in_SelectQuestionBox = self.sections[i][0]
			else:
				self.sectionid_selected_in_SelectQuestionBox = 0
		else:
			self.sectionid_selected_in_SelectQuestionBox = 0
		self.retrieve_questionids_in_SelectQuestionBox()

	def tree_sections_in_settings_changed(self):
		currentItem = self.tree_sections_in_settings.currentItem()
		if currentItem.isSelected(): # 如果选中
			if currentItem.parent() != None: # 如果选择的是节
				i = 0
				while currentItem.text(0) != self.sections[i][1]:
					i += 1
				self.sectionid_selected_in_settings = self.sections[i][0]
				self.chapterid_selected_in_settings = self.sections[i][2]
			else: # 如果选择的是章
				i = 0
				while currentItem.text(0) != self.chapters[i][1]:
					i += 1
				self.sectionid_selected_in_settings = 0
				self.chapterid_selected_in_settings = self.chapters[i][0]
		else: # 如果没选中
			self.sectionid_selected_in_settings = 0
			self.chapterid_selected_in_settings = 0

	def update_total_questions_sum(self): # 更新当前各类问题总数
		searchstring = ('select count(*) from schoice')
		num_schoice = self.mydb.search(searchstring)[0][0]
		newItem = QTableWidgetItem(str(num_schoice))
		newItem.setTextAlignment(Qt.AlignHCenter)
		self.tbl_total_questions_num.setItem(0, 0, newItem)
		searchstring = ('select count(*) from mchoice')
		num_mchoice = self.mydb.search(searchstring)[0][0]
		newItem = QTableWidgetItem(str(num_mchoice))
		newItem.setTextAlignment(Qt.AlignHCenter)
		self.tbl_total_questions_num.setItem(0, 1, newItem)
		searchstring = ('select count(*) from tof')
		num_tof = self.mydb.search(searchstring)[0][0]
		newItem = QTableWidgetItem(str(num_tof))
		newItem.setTextAlignment(Qt.AlignHCenter)
		self.tbl_total_questions_num.setItem(0, 2, newItem)
		searchstring = ('select count(*) from blank')
		num_blank = self.mydb.search(searchstring)[0][0]
		newItem = QTableWidgetItem(str(num_blank))
		newItem.setTextAlignment(Qt.AlignHCenter)
		self.tbl_total_questions_num.setItem(0, 3, newItem)
		searchstring = ('select count(*) from calculation')
		num_calculation = self.mydb.search(searchstring)[0][0]
		newItem = QTableWidgetItem(str(num_calculation))
		newItem.setTextAlignment(Qt.AlignHCenter)
		self.tbl_total_questions_num.setItem(0, 4, newItem)
		searchstring = ('select count(*) from proof')
		num_proof = self.mydb.search(searchstring)[0][0]
		newItem = QTableWidgetItem(str(num_proof))
		newItem.setTextAlignment(Qt.AlignHCenter)
		self.tbl_total_questions_num.setItem(0, 5, newItem)

	def update_after_insertion(self, other_settings): # 添加题目后主界面更新
		self.last_added_section_id = other_settings[0]
		self.last_added_difficulty_id = other_settings[1]
		self.last_added_source_id = other_settings[2]
		self.update_total_questions_sum()
		self.update_preview_in_BrowseBox()
		self.retrieve_questionids_in_ModifyBox()
		self.update_sections_in_ExportBox(self.selected_sectionids_in_ExportBox)

	def update_after_modification(self, other_settings): # 修改题目后主界面更新
		if self.sectionid_selected_in_ModifyBox != other_settings[0]:
			index = self.questionids_in_ModifyBox.index(self.questionid_in_ModifyBox)
			self.questionids_in_ModifyBox.remove(self.questionid_in_ModifyBox)
			if len(self.questionids_in_ModifyBox) == 0:
				self.questionid_in_ModifyBox = 0
			elif index == len(self.questionids_in_ModifyBox):
				self.questionid_in_ModifyBox = self.questionids_in_ModifyBox[index - 1]
			else:
				self.questionid_in_ModifyBox = self.questionids_in_ModifyBox[index]
		self.update_preview_in_BrowseBox()
		self.update_preview_in_ModifyBox()
		self.update_preview_in_SelectQuestionBox()
		self.update_sections_in_ExportBox(self.selected_sectionids_in_ExportBox)
		
	def update_selectedNum(self): # 更新自由选题导出标签页上当前选中题目数
		newItem = QTableWidgetItem(str(len(self.schoiceid_prepare)))
		newItem.setTextAlignment(Qt.AlignHCenter)
		self.tbl_selected_num.setItem(0, 0, newItem)
		newItem = QTableWidgetItem(str(len(self.mchoiceid_prepare)))
		newItem.setTextAlignment(Qt.AlignHCenter)
		self.tbl_selected_num.setItem(0, 1, newItem)
		newItem = QTableWidgetItem(str(len(self.tofid_prepare)))
		newItem.setTextAlignment(Qt.AlignHCenter)
		self.tbl_selected_num.setItem(0, 2, newItem)
		newItem = QTableWidgetItem(str(len(self.blankid_prepare)))
		newItem.setTextAlignment(Qt.AlignHCenter)
		self.tbl_selected_num.setItem(0, 3, newItem)
		newItem = QTableWidgetItem(str(len(self.calculationid_prepare)))
		newItem.setTextAlignment(Qt.AlignHCenter)
		self.tbl_selected_num.setItem(0, 4, newItem)
		newItem = QTableWidgetItem(str(len(self.proofid_prepare)))
		newItem.setTextAlignment(Qt.AlignHCenter)
		self.tbl_selected_num.setItem(0, 5, newItem)

	def update_sections_in_ExportBox(self, sectionids): # 更新按章节导出标签页上章节题目数
		self.selected_sectionids_in_ExportBox = sectionids
		self.tbl_selectedsections.setRowCount(len(sectionids))
		total_num_schoice = 0
		total_num_mchoice = 0
		total_num_tof = 0
		total_num_blank = 0
		total_num_calculation = 0
		total_num_proof = 0
		for i in range(len(sectionids)):
			j = 0
			while self.sections[j][0] != sectionids[i]:
				j = j + 1
			newItem = QTableWidgetItem(self.sections[j][1])
			self.tbl_selectedsections.setItem(i, 0, newItem)
			searchstring = ('select count(*) from schoice where section=%d' % (sectionids[i]))
			num_schoice = self.mydb.search(searchstring)[0][0]
			total_num_schoice = total_num_schoice + num_schoice
			newItem = QTableWidgetItem(str(num_schoice))
			newItem.setTextAlignment(Qt.AlignHCenter)
			self.tbl_selectedsections.setItem(i, 1, newItem)
			searchstring = ('select count(*) from mchoice where section=%d' % (sectionids[i]))
			num_mchoice = self.mydb.search(searchstring)[0][0]
			total_num_mchoice = total_num_mchoice + num_mchoice
			newItem = QTableWidgetItem(str(num_mchoice))
			newItem.setTextAlignment(Qt.AlignHCenter)
			self.tbl_selectedsections.setItem(i, 2, newItem)
			searchstring = ('select count(*) from tof where section=%d' % (sectionids[i]))
			num_tof = self.mydb.search(searchstring)[0][0]
			total_num_tof = total_num_tof + num_tof
			newItem = QTableWidgetItem(str(num_tof))
			newItem.setTextAlignment(Qt.AlignHCenter)
			self.tbl_selectedsections.setItem(i, 3, newItem)
			searchstring = ('select count(*) from blank where section=%d' % (sectionids[i]))
			num_blank = self.mydb.search(searchstring)[0][0]
			total_num_blank = total_num_blank + num_blank
			newItem = QTableWidgetItem(str(num_blank))
			newItem.setTextAlignment(Qt.AlignHCenter)
			self.tbl_selectedsections.setItem(i, 4, newItem)
			searchstring = ('select count(*) from calculation where section=%d' % (sectionids[i]))
			num_calculation = self.mydb.search(searchstring)[0][0]
			total_num_calculation = total_num_calculation + num_calculation
			newItem = QTableWidgetItem(str(num_calculation))
			newItem.setTextAlignment(Qt.AlignHCenter)
			self.tbl_selectedsections.setItem(i, 5, newItem)
			searchstring = ('select count(*) from proof where section=%d' % (sectionids[i]))
			num_proof = self.mydb.search(searchstring)[0][0]
			total_num_proof = total_num_proof + num_proof
			newItem = QTableWidgetItem(str(num_proof))
			newItem.setTextAlignment(Qt.AlignHCenter)
			self.tbl_selectedsections.setItem(i, 6, newItem)
		self.ed_schoice.setText(str(total_num_schoice))
		self.ed_mchoice.setText(str(total_num_mchoice))
		self.ed_tof.setText(str(total_num_tof))
		self.ed_blank.setText(str(total_num_blank))
		self.ed_calculation.setText(str(total_num_calculation))
		self.ed_proof.setText(str(total_num_proof))

	def update_preview_in_ModifyBox(self):
		# print('sectionid:%d,questionid:%d' % (self.sectionid_selected_in_ModifyBox,self.questionid_in_ModifyBox))
		if self.sectionid_selected_in_ModifyBox == 0 or self.questionid_in_ModifyBox == 0:
			self.btn_next.setEnabled(False)
			self.btn_previous.setEnabled(False)
			self.btn_modify.setEnabled(False)
			self.btn_delete.setEnabled(False)
			self.btn_copy.setEnabled(False)
			self.lbl_sequence_in_ModifyBox.setText('题目序列：0/0')
			self.webView_in_ModifyBox.setHtml(myfun.gethtml(self.webView_in_ModifyBox.width()))
			return
		if self.list_type_of_question_in_ModifyBox.currentText() == '单选题':
			searchstring = ('select "question", "A", "B", "C", "D", "answer", "explain", "section", "difficulty", "source" from schoice where id=%d' % (self.questionid_in_ModifyBox))
		if self.list_type_of_question_in_ModifyBox.currentText() == '多选题':
			searchstring = ('select "question", "A", "B", "C", "D", "pos_A", "pos_B", "pos_C", "pos_D", "explain", "section", "difficulty", "source" from mchoice where id=%d' % (self.questionid_in_ModifyBox))
		if self.list_type_of_question_in_ModifyBox.currentText() == '判断题':
			searchstring = ('select "question", "correct", "explain", "section", "difficulty", "source" from tof where id=%d' % (self.questionid_in_ModifyBox))
		if self.list_type_of_question_in_ModifyBox.currentText() == '填空题':
			searchstring = ('select "question", "answer1", "answer2", "answer3", "answer4", "explain", "section", "difficulty", "source" from blank where id=%d' % (self.questionid_in_ModifyBox))
		if self.list_type_of_question_in_ModifyBox.currentText() == '计算题':
			searchstring = ('select "question", "answer", "section", "difficulty", "source" from calculation where id=%d' % (self.questionid_in_ModifyBox))
		if self.list_type_of_question_in_ModifyBox.currentText() == '证明题':
			searchstring = ('select "question", "answer", "section", "difficulty", "source" from proof where id=%d' % (self.questionid_in_ModifyBox))
		thisquestion = self.mydb.search(searchstring)
		self.question_data_in_ModifyBox = [i for i in thisquestion[0]]
		questionstring = myfun.format_questiondata_to_html(self.question_data_in_ModifyBox, self.list_type_of_question_in_ModifyBox.currentText(), fromdatabase=1)
		pageSourceContent = questionstring
		# print(myfun.gethtml(self.webView_in_ModifyBox.width(), pageSourceContent))
		self.webView_in_ModifyBox.setHtml(myfun.gethtml(self.webView_in_ModifyBox.width(), pageSourceContent))
		index = self.questionids_in_ModifyBox.index(self.questionid_in_ModifyBox)
		self.btn_previous.setEnabled(index != 0)
		self.btn_modify.setEnabled(True)
		self.btn_delete.setEnabled(True)
		self.btn_copy.setEnabled(True)
		self.btn_next.setEnabled(index != len(self.questionids_in_ModifyBox)-1)
		self.lbl_sequence_in_ModifyBox.setText('题目序列：%d/%d' % (index+1, len(self.questionids_in_ModifyBox)))

	def update_preview_in_SelectQuestionBox(self):
		# print('sectionid:%d,questionid:%d' % (self.sectionid_selected_in_SelectQuestionBox,self.questionid_in_SelectQuestionBox))
		if self.sectionid_selected_in_SelectQuestionBox == 0 or self.questionid_in_SelectQuestionBox == 0:
			self.btn_next_in_SelectQuestionBox.setEnabled(False)
			self.btn_previous_in_SelectQuestionBox.setEnabled(False)
			self.chk_select_in_SelectQuestionBox.setEnabled(False)
			self.lbl_sequence_in_SelectQuestionBox.setText('题目序列：0/0')
			self.webView_in_SelectQuestionBox.setHtml(myfun.gethtml(self.webView_in_SelectQuestionBox.width()))
			return
		if self.list_type_of_question_in_SelectQuestionBox.currentText() == '单选题':
			searchstring = ('select "question", "A", "B", "C", "D", "answer", "explain", "section", "difficulty", "source" from schoice where id=%d' % (self.questionid_in_SelectQuestionBox))
		if self.list_type_of_question_in_SelectQuestionBox.currentText() == '多选题':
			searchstring = ('select "question", "A", "B", "C", "D", "pos_A", "pos_B", "pos_C", "pos_D", "explain", "section", "difficulty", "source" from mchoice where id=%d' % (self.questionid_in_SelectQuestionBox))
		if self.list_type_of_question_in_SelectQuestionBox.currentText() == '判断题':
			searchstring = ('select "question", "correct", "explain", "section", "difficulty", "source" from tof where id=%d' % (self.questionid_in_SelectQuestionBox))
		if self.list_type_of_question_in_SelectQuestionBox.currentText() == '填空题':
			searchstring = ('select "question", "answer1", "answer2", "answer3", "answer4", "explain", "section", "difficulty", "source" from blank where id=%d' % (self.questionid_in_SelectQuestionBox))
		if self.list_type_of_question_in_SelectQuestionBox.currentText() == '计算题':
			searchstring = ('select "question", "answer", "section", "difficulty", "source" from calculation where id=%d' % (self.questionid_in_SelectQuestionBox))
		if self.list_type_of_question_in_SelectQuestionBox.currentText() == '证明题':
			searchstring = ('select "question", "answer", "section", "difficulty", "source" from proof where id=%d' % (self.questionid_in_SelectQuestionBox))
		thisquestion = self.mydb.search(searchstring)
		self.question_data_in_SelectQuestionBox = [i for i in thisquestion[0]]
		questionstring = myfun.format_questiondata_to_html(self.question_data_in_SelectQuestionBox, self.list_type_of_question_in_SelectQuestionBox.currentText(), fromdatabase=1)
		pageSourceContent = questionstring
		self.webView_in_SelectQuestionBox.setHtml(myfun.gethtml(self.webView_in_SelectQuestionBox.width(), pageSourceContent))
		index = self.questionids_in_SelectQuestionBox.index(self.questionid_in_SelectQuestionBox)
		self.btn_previous_in_SelectQuestionBox.setEnabled(index != 0)
		self.chk_select_in_SelectQuestionBox.setEnabled(True)
		self.btn_next_in_SelectQuestionBox.setEnabled(index != len(self.questionids_in_SelectQuestionBox)-1)
		self.lbl_sequence_in_SelectQuestionBox.setText('题目序列：%d/%d' % (index+1, len(self.questionids_in_SelectQuestionBox)))
		self.update_checkStatus_in_SelectQuestionBox()

	def update_checkStatus_in_SelectQuestionBox(self):
		if self.list_type_of_question_in_SelectQuestionBox.currentText() == '单选题':
			self.chk_select_in_SelectQuestionBox.setChecked(self.questionid_in_SelectQuestionBox in self.schoiceid_prepare)
		elif self.list_type_of_question_in_SelectQuestionBox.currentText() == '多选题':
			self.chk_select_in_SelectQuestionBox.setChecked(self.questionid_in_SelectQuestionBox in self.mchoiceid_prepare)
		elif self.list_type_of_question_in_SelectQuestionBox.currentText() == '判断题':
			self.chk_select_in_SelectQuestionBox.setChecked(self.questionid_in_SelectQuestionBox in self.tofid_prepare)
		elif self.list_type_of_question_in_SelectQuestionBox.currentText() == '填空题':
			self.chk_select_in_SelectQuestionBox.setChecked(self.questionid_in_SelectQuestionBox in self.blankid_prepare)
		elif self.list_type_of_question_in_SelectQuestionBox.currentText() == '计算题':
			self.chk_select_in_SelectQuestionBox.setChecked(self.questionid_in_SelectQuestionBox in self.calculationid_prepare)
		elif self.list_type_of_question_in_SelectQuestionBox.currentText() == '证明题':
			self.chk_select_in_SelectQuestionBox.setChecked(self.questionid_in_SelectQuestionBox in self.proofid_prepare)

	def update_tree_sections(self):
		self.retrieve_data()
		self.tree_sections_in_BrowseBox.clear()
		for i in range(len(self.chapters)):
			root = QTreeWidgetItem(self.tree_sections_in_BrowseBox)
			root.setText(0, self.chapters[i][1])
			secs_in_this_chp = []
			j = 0
			for j in range(len(self.sections)):
				if self.sections[j][2] == self.chapters[i][0]:
					secs_in_this_chp.append(self.sections[j][1])
			for j in range(len(secs_in_this_chp)):
				child = QTreeWidgetItem(root)
				child.setText(0, secs_in_this_chp[j])
			self.tree_sections_in_BrowseBox.addTopLevelItem(root)
		self.tree_sections_in_ModifyBox.clear()
		for i in range(len(self.chapters)):
			root = QTreeWidgetItem(self.tree_sections_in_ModifyBox)
			root.setText(0, self.chapters[i][1])
			secs_in_this_chp = []
			j = 0
			for j in range(len(self.sections)):
				if self.sections[j][2] == self.chapters[i][0]:
					secs_in_this_chp.append(self.sections[j][1])
			for j in range(len(secs_in_this_chp)):
				child = QTreeWidgetItem(root)
				child.setText(0, secs_in_this_chp[j])
			self.tree_sections_in_ModifyBox.addTopLevelItem(root)
		self.tree_sections_in_SelectQuestionBox.clear()
		for i in range(len(self.chapters)):
			root = QTreeWidgetItem(self.tree_sections_in_SelectQuestionBox)
			root.setText(0, self.chapters[i][1])
			secs_in_this_chp = []
			j = 0
			for j in range(len(self.sections)):
				if self.sections[j][2] == self.chapters[i][0]:
					secs_in_this_chp.append(self.sections[j][1])
			for j in range(len(secs_in_this_chp)):
				child = QTreeWidgetItem(root)
				child.setText(0, secs_in_this_chp[j])
			self.tree_sections_in_SelectQuestionBox.addTopLevelItem(root)
		self.tree_sections_in_settings.clear()
		for i in range(len(self.chapters)):
			root = QTreeWidgetItem(self.tree_sections_in_settings)
			root.setText(0, self.chapters[i][1])
			secs_in_this_chp = []
			j = 0
			for j in range(len(self.sections)):
				if self.sections[j][2] == self.chapters[i][0]:
					secs_in_this_chp.append(self.sections[j][1])
			for j in range(len(secs_in_this_chp)):
				child = QTreeWidgetItem(root)
				child.setText(0, secs_in_this_chp[j])
			self.tree_sections_in_settings.addTopLevelItem(root)
			
	# 更新预览
	def update_preview_in_BrowseBox(self):
		if not self.selected_sectionsid_in_BrowseBox:
			self.webView_in_BrowseBox.setHtml(myfun.gethtml(self.webView_in_BrowseBox.width()))
			return
		sectionstring = (' where section=' + str(self.selected_sectionsid_in_BrowseBox[0]))
		for i in self.selected_sectionsid_in_BrowseBox:
			sectionstring = sectionstring + ' or section=' + str(i)
		# 读单选题表
		if self.chk_schoice_in_BrowseBox.isChecked():
			searchstring = ('select "id" from schoice' + sectionstring)
			searchresult = self.mydb.search(searchstring)
			schoiceid = [i[0] for i in searchresult]
		else:
			schoiceid = []
		num_schoice = len(schoiceid)
		# 读多选题表
		if self.chk_mchoice_in_BrowseBox.isChecked():
			searchstring = ('select "id" from mchoice' + sectionstring)
			searchresult = self.mydb.search(searchstring)
			mchoiceid = [i[0] for i in searchresult]
		else:
			mchoiceid = []
		num_mchoice = len(mchoiceid)
		# 读判断题表
		if self.chk_tof_in_BrowseBox.isChecked():
			searchstring = ('select "id" from tof' + sectionstring)
			searchresult = self.mydb.search(searchstring)
			tofid = [i[0] for i in searchresult]
		else:
			tofid = []
		num_tof = len(tofid)
		# 读填空题表
		if self.chk_blank_in_BrowseBox.isChecked():
			searchstring = ('select "id" from blank' + sectionstring)
			searchresult = self.mydb.search(searchstring)
			blankid = [i[0] for i in searchresult]
		else:
			blankid = []
		num_blank = len(blankid)
		# 读计算题表
		if self.chk_calculation_in_BrowseBox.isChecked():
			searchstring = ('select "id" from calculation' + sectionstring)
			searchresult = self.mydb.search(searchstring)
			calculationid = [i[0] for i in searchresult]
		else:
			calculationid = []
		num_calculation = len(calculationid)
		# 读证明题表
		if self.chk_proof_in_BrowseBox.isChecked():
			searchstring = ('select "id" from proof' + sectionstring)
			searchresult = self.mydb.search(searchstring)
			proofid = [i[0] for i in searchresult]
		else:
			proofid = []
		num_proof = len(proofid)

		# if not (num_schoice or num_mchoice or num_tof or num_blank or num_calculation or num_proof):
		# 	self.webView_in_BrowseBox.setHtml(myfun.gethtml(self.webView_in_BrowseBox.width()))
		# 	return
		
		pageSourceContent,_,_ = myfun.generate_html_body(self.mydb,schoiceid,mchoiceid,tofid,blankid,calculationid,proofid)

		self.webView_in_BrowseBox.setHtml(myfun.gethtml(self.webView_in_BrowseBox.width(), pageSourceContent))

	def update_list_source_in_settings(self):
		self.list_source_in_settings.clear()
		self.retrieve_data()
		if self.sources:
			for row in self.sources:
				self.list_source_in_settings.addItem(row[1])

	def update_list_users_in_settings(self):
		self.list_users_in_settings.clear()
		self.retrieve_data()
		if self.users:
			for row in self.users:
				self.list_users_in_settings.addItem(row[1])

	def retrieve_data(self):
		searchstring = 'select * from chapters'
		self.chapters = self.mydb.search(searchstring)
		searchstring = 'select * from sections'
		self.sections = self.mydb.search(searchstring)
		searchstring = 'select * from difficulties'
		self.difficulties = self.mydb.search(searchstring)
		searchstring = 'select * from sources'
		self.sources = self.mydb.search(searchstring)

	def retrieve_questionids_in_ModifyBox(self):
		if self.sectionid_selected_in_ModifyBox == 0:
			self.update_preview_in_ModifyBox()
			return
		if self.list_type_of_question_in_ModifyBox.currentText() == '单选题':
			searchstring = ('select "id" from schoice where section = %d' % (self.sectionid_selected_in_ModifyBox))
			schoice = self.mydb.search(searchstring)
			self.questionids_in_ModifyBox = [i[0] for i in schoice] # 指定章节指定题型的所有id列表
		if self.list_type_of_question_in_ModifyBox.currentText() == '多选题':
			searchstring = ('select "id" from mchoice where section = %d' % (self.sectionid_selected_in_ModifyBox))
			mchoice = self.mydb.search(searchstring)
			self.questionids_in_ModifyBox = [i[0] for i in mchoice] # 指定章节指定题型的所有id列表
		if self.list_type_of_question_in_ModifyBox.currentText() == '判断题':
			searchstring = ('select "id" from tof where section = %d' % (self.sectionid_selected_in_ModifyBox))
			tof = self.mydb.search(searchstring)
			self.questionids_in_ModifyBox = [i[0] for i in tof] # 指定章节指定题型的所有id列表
		if self.list_type_of_question_in_ModifyBox.currentText() == '填空题':
			searchstring = ('select "id" from blank where section = %d' % (self.sectionid_selected_in_ModifyBox))
			blank = self.mydb.search(searchstring)
			self.questionids_in_ModifyBox = [i[0] for i in blank] # 指定章节指定题型的所有id列表
		if self.list_type_of_question_in_ModifyBox.currentText() == '计算题':
			searchstring = ('select "id" from calculation where section = %d' % (self.sectionid_selected_in_ModifyBox))
			calculation = self.mydb.search(searchstring)
			self.questionids_in_ModifyBox = [i[0] for i in calculation] # 指定章节指定题型的所有id列表
		if self.list_type_of_question_in_ModifyBox.currentText() == '证明题':
			searchstring = ('select "id" from proof where section = %d' % (self.sectionid_selected_in_ModifyBox))
			proof = self.mydb.search(searchstring)
			self.questionids_in_ModifyBox = [i[0] for i in proof] # 指定章节指定题型的所有id列表
		if self.questionids_in_ModifyBox:
			self.questionid_in_ModifyBox = self.questionids_in_ModifyBox[0]
		else:
			self.questionid_in_ModifyBox = 0
		self.update_preview_in_ModifyBox()

	def retrieve_questionids_in_SelectQuestionBox(self):
		if self.sectionid_selected_in_SelectQuestionBox == 0:
			self.update_preview_in_SelectQuestionBox()
			return
		if self.list_type_of_question_in_SelectQuestionBox.currentText() == '单选题':
			searchstring = ('select "id" from schoice where section = %d' % (self.sectionid_selected_in_SelectQuestionBox))
			schoice = self.mydb.search(searchstring)
			self.questionids_in_SelectQuestionBox = [i[0] for i in schoice] # 指定章节指定题型的所有id列表
		if self.list_type_of_question_in_SelectQuestionBox.currentText() == '多选题':
			searchstring = ('select "id" from mchoice where section = %d' % (self.sectionid_selected_in_SelectQuestionBox))
			mchoice = self.mydb.search(searchstring)
			self.questionids_in_SelectQuestionBox = [i[0] for i in mchoice] # 指定章节指定题型的所有id列表
		if self.list_type_of_question_in_SelectQuestionBox.currentText() == '判断题':
			searchstring = ('select "id" from tof where section = %d' % (self.sectionid_selected_in_SelectQuestionBox))
			tof = self.mydb.search(searchstring)
			self.questionids_in_SelectQuestionBox = [i[0] for i in tof] # 指定章节指定题型的所有id列表
		if self.list_type_of_question_in_SelectQuestionBox.currentText() == '填空题':
			searchstring = ('select "id" from blank where section = %d' % (self.sectionid_selected_in_SelectQuestionBox))
			blank = self.mydb.search(searchstring)
			self.questionids_in_SelectQuestionBox = [i[0] for i in blank] # 指定章节指定题型的所有id列表
		if self.list_type_of_question_in_SelectQuestionBox.currentText() == '计算题':
			searchstring = ('select "id" from calculation where section = %d' % (self.sectionid_selected_in_SelectQuestionBox))
			calculation = self.mydb.search(searchstring)
			self.questionids_in_SelectQuestionBox = [i[0] for i in calculation] # 指定章节指定题型的所有id列表
		if self.list_type_of_question_in_SelectQuestionBox.currentText() == '证明题':
			searchstring = ('select "id" from proof where section = %d' % (self.sectionid_selected_in_SelectQuestionBox))
			proof = self.mydb.search(searchstring)
			self.questionids_in_SelectQuestionBox = [i[0] for i in proof] # 指定章节指定题型的所有id列表
		if self.questionids_in_SelectQuestionBox:
			self.questionid_in_SelectQuestionBox = self.questionids_in_SelectQuestionBox[0]
		else:
			self.questionid_in_SelectQuestionBox = 0
		self.update_preview_in_SelectQuestionBox()

	def transmit_settings(self, ui): # 将设置传递给打开的子窗口
		ui.other_settings.connect(self.update_after_insertion)
		i = 0
		for j in range(len(self.sections)):
			if self.last_added_section_id == self.sections[j][0]:
				i = j
				break
		ui.list_section.setCurrentIndex(i)
		i = 0
		for j in range(len(self.difficulties)):
			if self.last_added_difficulty_id == self.difficulties[j][0]:
				i = j
				break
		ui.list_difficulty.setCurrentIndex(i)
		i = 0
		for j in range(len(self.sources)):
			if self.last_added_source_id == self.sources[j][0]:
				i = j
				break
		ui.current_userid = self.current_userid
		ui.list_source.setCurrentIndex(i)
	
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
		[passed,schoiceid,mchoiceid,tofid,blankid,calculationid,proofid]=self.get_questionid_in_ExportbySection()
		if not passed:
			return
		num_schoice = len(schoiceid)
		num_mchoice = len(mchoiceid)
		num_tof = len(tofid)
		num_blank = len(blankid)
		num_calculation = len(calculationid)
		num_proof = len(proofid)

		if not (num_schoice or num_mchoice or num_tof or num_blank or num_calculation or num_proof):
			QMessageBox.about(self, u'通知', u'当前章节中没有题目！')
			return
		
		self.options['title'] = self.ed_title.text().strip()
		result = myfun.export_to_latex(self.mydb,schoiceid,mchoiceid,tofid,blankid,calculationid,proofid,self.options)
		if result[0]:
			QMessageBox.about(self, u'通知', (u'导出文件 %s.tex 成功！' % (result[1])))
		else:
			QMessageBox.about(self, u'错误', u'导出失败！')
			print(result[1])

	# 调整窗口大小事件
	def resizeEvent(self, event):#调整窗口尺寸时，该方法被持续调用。event参数包含QResizeEvent类的实例，通过该类的下列方法获得窗口信息：
		self.update_preview_in_BrowseBox()
		self.update_preview_in_ModifyBox()
		self.update_preview_in_SelectQuestionBox()

	def export_questions_to_html(self):
		[passed,schoiceid,mchoiceid,tofid,blankid,calculationid,proofid]=self.get_questionid_in_ExportbySection()
		if not passed:
			return
		num_schoice = len(schoiceid)
		num_mchoice = len(mchoiceid)
		num_tof = len(tofid)
		num_blank = len(blankid)
		num_calculation = len(calculationid)
		num_proof = len(proofid)

		if not (num_schoice or num_mchoice or num_tof or num_blank or num_calculation or num_proof):
			QMessageBox.about(self, u'通知', u'当前章节中没有题目！')
			return
		
		self.options['title'] = self.ed_title.text().strip()
		result = myfun.export_to_html(self.mydb,schoiceid,mchoiceid,tofid,blankid,calculationid,proofid,self.options)
		if result[0]:
			QMessageBox.about(self, u'通知', (u'导出文件 %s.html 成功！' % (result[1])))
		else:
			QMessageBox.about(self, u'错误', u'导出失败！')
			print(result[1])

	def get_questionid_in_ExportbySection(self):
		if not self.selected_sectionids_in_ExportBox:
			QMessageBox.about(self, u'通知', u'请先选择章节！')
			return False,[],[],[],[],[],[]
		flag = [] # 记录每个题型的填写数量是否超出已有数量
		num_of_filled = [] # 用户填写的每个题型的数量
		num_of_filled.append(int(self.ed_schoice.text()))
		num_of_filled.append(int(self.ed_mchoice.text()))
		num_of_filled.append(int(self.ed_tof.text()))
		num_of_filled.append(int(self.ed_blank.text()))
		num_of_filled.append(int(self.ed_calculation.text()))
		num_of_filled.append(int(self.ed_proof.text()))
		for col in range(6):
			num_of_sections = len(self.selected_sectionids_in_ExportBox)
			total_num_of_questions = 0
			for i in range(num_of_sections):
				total_num_of_questions += int(self.tbl_selectedsections.item(i,col+1).text())
			flag.append(total_num_of_questions<num_of_filled[col]) # 填写的超出实际的
		errortype=[] # 数量填写有误的题目类型
		if flag[0] == True:
			errortype.append('单选题')
		if flag[1] == True:
			errortype.append('多选题')
		if flag[2] == True:
			errortype.append('判断题')
		if flag[3] == True:
			errortype.append('填空题')
		if flag[4] == True:
			errortype.append('计算题')
		if flag[5] == True:
			errortype.append('证明题')
		if errortype:
			QMessageBox.about(self, u'错误', u'您填写的%s数量超出所选章节中的题目数量，请重新填写！' % ('、'.join(errortype)))
			return False,[],[],[],[],[],[]

		# 根据填写的题目数量获取并筛选单选题id
		schoiceid = self.drop_questions('schoice', int(self.ed_schoice.text()))
		# 根据填写的题目数量获取并筛选多选题id
		mchoiceid = self.drop_questions('mchoice', int(self.ed_mchoice.text()))
		# 根据填写的题目数量获取并筛选判断题id
		tofid = self.drop_questions('tof', int(self.ed_tof.text()))
		# 根据填写的题目数量获取并筛选填空题id
		blankid = self.drop_questions('blank', int(self.ed_blank.text()))
		# 根据填写的题目数量获取并筛选计算题id
		calculationid = self.drop_questions('calculation', int(self.ed_calculation.text()))
		# 根据填写的题目数量获取并筛选证明题id
		proofid = self.drop_questions('proof', int(self.ed_proof.text()))
		
		return True,schoiceid,mchoiceid,tofid,blankid,calculationid,proofid

	def drop_questions(self, question_type, num_target): # 根据填写的题目数量获取并筛选题目id
		difficulties = []
		if self.chk_notsure.isChecked():
			difficulties.append('1')
		if self.chk_easy.isChecked():
			difficulties.append('2')
		if self.chk_medium.isChecked():
			difficulties.append('3')
		if self.chk_hard.isChecked():
			difficulties.append('4')
		if self.chk_hell.isChecked():
			difficulties.append('5')
		if difficulties:
			difficultystring = ' and (difficulty =' + ' or difficulty='.join(difficulties) + ')'
		else:
			difficultystring = ''
		id_by_sections = []
		num_id_by_sections = []
		for i in range(0, len(self.selected_sectionids_in_ExportBox)):
			sectionstring = (' where (section=' + str(self.selected_sectionids_in_ExportBox[i]) + ')')
			searchstring = ('select "id" from ' + question_type + sectionstring + difficultystring)
			searchresult = self.mydb.search(searchstring)
			id_by_sections.append([i[0] for i in searchresult])
			num_id_by_sections.append(len(id_by_sections[-1]))
		while sum(num_id_by_sections) > num_target:
			interval = [num_id_by_sections[i]/sum(num_id_by_sections) for i in range(len(num_id_by_sections))]
			for j in range(1,len(interval)):
				interval[j] += interval[j-1]
			indicator = random.random()
			for j in range(len(interval)):
				if num_id_by_sections[j] == 0:
					continue
				if indicator<=interval[j]:
					num_id_by_sections[j] -= 1
					break
		questionid = []
		for i in range(len(id_by_sections)):
			ids = id_by_sections[i]
			diff = len(ids)-num_id_by_sections[i]
			for j in range(diff):
				index = random.randint(0,len(ids)-1)
				ids.pop(index)
			for j in ids:
				questionid.append(j)
		return questionid

	def ask_update(self, remote_ver):
		if remote_ver > self.ver:
			reply = QMessageBox.question(
				self, '升级', f'检测到新版本{remote_ver}，当前版本为{self.ver}，是否前往下载更新？',
				QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
			if reply == QMessageBox.Yes:
				webopen('http://www.jhanmath.com/?page_id=228')

class Thread_update(QThread):
	res = pyqtSignal(str)

	def __init__(self, parent=None):
		super(Thread_update, self).__init__(parent)

	def setCurrentVer(self, ver):
		self.ver = ver

	def run(self):
		url = 'http://www.jhanmath.com/wp-content/uploads/softwares/questions/README.md'
		try:
			res = requests.get(url)
			if res.status_code == requests.codes.ok:
				pattern = r"ver. \d{4}.\d{2}.\d{2}"
				remote_ver = regex.search(pattern, res.text)
				self.res.emit(remote_ver.group()[-10:])
		except Exception:
			pass