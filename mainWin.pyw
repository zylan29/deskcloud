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

		self.setWindowTitle(u'PDL虚拟桌面云系统')

		exit = QtGui.QAction(u'退出', self)
		exit.setShortcut('Ctrl+Q')
		exit.setStatusTip('Exitapplication')
		exit.connect(exit,QtCore.SIGNAL('triggered()'), QtGui.qApp, QtCore.SLOT('quit()'))

		menu = self.menuBar()
		file = menu.addMenu(u'文件')
		file.addAction(exit)
		self.statusBar()
		
		tabwidget = QtGui.QTabWidget()

		self.instances = self.user.get_all_instances()
		instancelist = QtGui.QListWidget()
		instancelist.addItems(self.__objlist2strlist(self.instances))
		instancelist.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
		self.connect(instancelist, QtCore.SIGNAL('currentItemChanged(QListWidgetItem *,QListWidgetItem *)'), self.select_changed_instancelist)
		tabwidget.addTab(instancelist, u'虚拟机实例')

		#self.images = self.user.get_all_images()
		#imagelist = QtGui.QListWidget()
		#imagelist.addItems(self.__objlist2strlist(self.images))
		#self.connect(imagelist, QtCore.SIGNAL('currentItemChanged(QListWidgetItem *,QListWidgetItem *)'), self.select_changed_imagelist)
		#tabwidget.addTab(imagelist, u'映像')
		
		tabwidget.setMovable(True)

		welcomelab = QtGui.QLabel(u"<font color=blue size=4><b>欢迎来到PDL虚拟桌面云系统</b></font>")
		welcomelab.setAlignment(QtCore.Qt.AlignCenter)
		self.startbtn = QtGui.QPushButton(u'启动')
		self.startbtn.setHidden(True)
		self.shutbtn = QtGui.QPushButton(u'关机')
		self.shutbtn.setHidden(True)

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
		self.resize(550, 550)

	#def select_changed_imagelist(self, current, previous):
	#	img_info = []
	#	image_id = current.text()
	#	for img in self.images:
	#		if image_id == img.id:
	#			img_info = [u'映像名：\t%s'%img.name, u'映像ID：\t%s'%img.id]
	#			break
	#	self.detaillist.clear()
	#	self.detaillist.addItems(img_info)

	def select_changed_instancelist(self, current, previous):
		instance_info = []
		instance_name = current.text()
		for ins in self.instances:
			if instance_name == ins.id:
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