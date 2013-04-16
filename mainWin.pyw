#/usr/bin/env python
#-*- coding:utf-8 -*-
# mainWin.py

import sys
from PyQt4 import QtGui, QtCore
import boto
from boto.ec2.regioninfo import RegionInfo
import loginWin, dcUser, dcIcos


class MainWin(QtGui.QMainWindow):
	def __init__(self, conn, parent=None):
		QtGui.QMainWindow.__init__(self, parent)

		self.user = dcUser.DcUser(conn)
		self.instances = []
		self.selected_ins = None

		self.setWindowTitle(u'PDL虚拟桌面云系统')

		exitact = QtGui.QAction(u'退出', self)
		exitact.setShortcut('Ctrl+Q')
		exitact.setStatusTip('Exit Application')
		exitact.connect(exitact, QtCore.SIGNAL('triggered()'), QtGui.qApp, QtCore.SLOT('quit()'))

		aboutact = QtGui.QAction(u'关于', self)
		self.connect(aboutact, QtCore.SIGNAL('triggered()'), self.about)

		self.startact = QtGui.QAction(QtGui.QIcon('icos/start.ico'), u'启动', self)
		self.connect(self.startact, QtCore.SIGNAL('triggered()'), self.start_ins)
		self.stopact = QtGui.QAction(QtGui.QIcon('icos/stop.ico'), u'关机', self)
		self.connect(self.stopact, QtCore.SIGNAL('triggered()'), self.shut_ins)
		self.startact.setDisabled(True)
		self.stopact.setDisabled(True)


		menu = self.menuBar()
		filemenu = menu.addMenu(u'文件')
		filemenu.addAction(exitact)
		filemenu.addAction(aboutact)



		toolbar = QtGui.QToolBar()
		toolbar.addAction(self.startact)
		toolbar.addAction(self.stopact)

		self.addToolBar(toolbar)
		
		self.statusBar()
		
		tabwidget = QtGui.QTabWidget()
		self.instancelist = QtGui.QListWidget()
		self.instancelist.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
		self.connect(self.instancelist, QtCore.SIGNAL('currentItemChanged(QListWidgetItem *,QListWidgetItem *)'), self.select_changed_instancelist)
		tabwidget.addTab(self.instancelist, u'虚拟机实例')

		tabwidget.setMovable(True)

	
		self.detaillist = QtGui.QListWidget()
		vbox = QtGui.QVBoxLayout()
		
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

	def about(self):
		about_str = u'PDL虚拟桌面云系统\n版本： 0.1alpha\n作者：李紫阳'
		QtGui.QMessageBox.information(self, u'关于', about_str, QtGui.QMessageBox.Yes)

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
			current_item = self.instancelist.item(current_row)
			self.select_changed_instancelist(current_item, current_item)

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
			return
		instance_info = []
		instance_name = current.text()
		for ins in self.instances:
			if instance_name == ins.id:
				self.selected_ins = ins
				if ins.state == 'running':
					self.startact.setIcon(QtGui.QIcon('icos/reboot.ico'))
					self.startact.setText(u'重启')
					self.startact.setDisabled(False)
					self.stopact.setIconText(u'关机')
					self.stopact.setDisabled(False)
				elif ins.state == 'stopped':
					self.startact.setIcon(QtGui.QIcon('icos/start.ico'))
					self.startact.setText(u'开机')
					self.stopact.setDisabled(True)
				else:
					self.startact.setDisabled(True)
					self.stopact.setDisabled(True)

				instance_info = [u'虚拟机ID：\t%s'%ins.id, u'状态：\t%s'%ins.state, u'IP地址：\t%s'%ins.ip_address, u'启动时间：\t%s'%ins.launch_time]
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