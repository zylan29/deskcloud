#/usr/bin/env python
#-*- coding:utf-8 -*-
# mainWin.py

import sys
from PyQt4 import QtGui, QtCore
import boto
from boto.ec2.regioninfo import RegionInfo
import loginWin, dcUser


class MainWin(QtGui.QMainWindow):
	def __init__(self, conn, parent=None):
		QtGui.QMainWindow.__init__(self, parent)

		self.user = dcUser.DcUser(conn)
		self.instances = []
		self.selected_ins = None

		self.setWindowTitle(u'PDL虚拟桌面云系统')

		exit = QtGui.QAction(u'退出', self)
		exit.setShortcut('Ctrl+Q')
		exit.setStatusTip('Exitapplication')
		exit.connect(exit,QtCore.SIGNAL('triggered()'), QtGui.qApp, QtCore.SLOT('quit()'))

		menu = self.menuBar()
		filemenu = menu.addMenu(u'文件')
		filemenu.addAction(exit)
		self.statusBar()
		
		tabwidget = QtGui.QTabWidget()
		self.instancelist = QtGui.QListWidget()
		self.instancelist.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
		self.connect(self.instancelist, QtCore.SIGNAL('currentItemChanged(QListWidgetItem *,QListWidgetItem *)'), self.select_changed_instancelist)
		tabwidget.addTab(self.instancelist, u'虚拟机实例')

		tabwidget.setMovable(True)

		welcomelab = QtGui.QLabel(u"<font color=blue size=4><b>欢迎来到PDL虚拟桌面云系统</b></font>")
		welcomelab.setAlignment(QtCore.Qt.AlignCenter)
		self.startbtn = QtGui.QPushButton(u'启动')
		self.startbtn.setHidden(True)
		self.connect(self.startbtn, QtCore.SIGNAL('clicked()'), self.start_ins)

		self.shutbtn = QtGui.QPushButton(u'关机')
		self.shutbtn.setHidden(True)
		self.connect(self.shutbtn, QtCore.SIGNAL('clicked()'), self.shut_ins)

		hbox = QtGui.QHBoxLayout()

		hbox.addWidget(self.startbtn)
		hbox.addWidget(self.shutbtn)
		self.detaillist = QtGui.QListWidget()
		vbox = QtGui.QVBoxLayout()
		vbox.addWidget(welcomelab)
		vbox.addLayout(hbox)
		vbox.addWidget(self.detaillist)

		box = QtGui.QHBoxLayout()
		box.addWidget(tabwidget, 1)
		box.addLayout(vbox, 2)

		centralwidget = QtGui.QWidget()
		centralwidget.setLayout(box)
		self.setCentralWidget(centralwidget)
		self.resize(550, 500)

		self.update()

		self.update_timer = QtCore.QTimer(self)
		self.connect(self.update_timer, QtCore.SIGNAL('timeout()'), self.update)
		self.update_timer.start(1*1000)


	def update(self):
		self.update_ui()

	def update_instance_data(self):
		self.instances = self.user.get_all_instances()

	def __instances_differ(self, old_ins, new_ins):
		if len(old_ins) != len(new_ins):
			return True
		else:
			old_ins_ids = []
			for ins in old_ins:
				old_ins_ids.append(ins.id)
			old_ins_ids.sort()
			new_ins_ids = []
			for ins in new_ins:
				new_ins_ids.append(ins.id)
			new_ins_ids.sort()
			for i in range(len(old_ins_ids)):
				if old_ins_ids[i] != new_ins_ids[i]:
					return True
			return False

	def update_ui(self):
		old_ins = self.instances
		self.instances = self.user.get_all_instances()
		current_row = self.instancelist.currentRow()
		if self.__instances_differ(old_ins, self.instances):
			self.instancelist.clear()
			self.instancelist.addItems(self.__objlist2strlist(self.instances))
		if current_row != -1:
			self.instancelist.setCurrentRow(current_row)

	def start_ins(self):
		self.user.reboot_instances([self.selected_ins.id])
		self.update_instance_data()
		self.update_ui()

	def shut_ins(self):
		self.user.stop_instances([self.selected_ins.id])
		self.update_instance_data()
		self.update_ui()

	def select_changed_instancelist(self, current, previous):
		if current == None:
			print '111111'
			return
		instance_info = []
		instance_name = current.text()
		for ins in self.instances:
			if instance_name == ins.id:
				self.selected_ins = ins
				if ins.state == 'running':
					self.startbtn.setText(u'重启')
					self.startbtn.setHidden(False)
					self.startbtn.setDisabled(False)
					self.shutbtn.setText(u'关机')
					self.shutbtn.setHidden(False)
					self.startbtn.setDisabled(False)
				elif ins.state == 'stopped':
					self.startbtn.setText(u'开机')
					self.startbtn.setHidden(False)
					self.shutbtn.setDisabled(True)
					self.shutbtn.setHidden(True)
				else:
					self.startbtn.setDisabled(True)
					self.startbtn.setHidden(False)
					self.shutbtn.setDisabled(True)
					self.shutbtn.setHidden(False)

				instance_info = [u'虚拟机：\t%s'%ins.id, u'状态：\t%s'%ins.state, u'IP地址：\t%s'%ins.ip_address, u'Launch Time：\t%s'%ins.launch_time]
				break
		self.detaillist.clear()
		self.detaillist.addItems(instance_info)

	def __objlist2dict(self, objlist):
		self.__objlist2strlist()

	def __objlist2strlist(self, objlist):
		return [str(aobj).split(':')[1] for aobj in objlist]

if __name__ == '__main__':
	app = QtGui.QApplication(sys.argv)
	loginwindow = loginWin.LoginWin()
	while loginwindow.exec_() == QtGui.QDialog.Rejected:
		if loginwindow.closed == 1:
			sys.exit(0)
		loginwindow = None
		loginwindow = loginWin.LoginWin()
		loginwindow.show()
	mainwindow = MainWin(loginwindow.get_conn())
	mainwindow.show()

	sys.exit(app.exec_())