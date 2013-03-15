#/usr/bin/env python
#-*- coding:utf-8 -*-
# loginWin.py
import sys
from PyQt4 import QtGui, QtCore

class LoginWin(QtGui.QDialog):
	def __init__(self, parent=None):
		QtGui.QDialog.__init__(self, parent)

		self.closed = 0

		self.setWindowTitle(u'PDL虚拟桌面云系统')

		serverLabel = QtGui.QLabel(u'服务器：')
		self.serverEdit = QtGui.QComboBox()
		self.serverEdit.setEditable(True)
		self.serverEdit.autoCompletion = True

		userLabel = QtGui.QLabel(u'用户名：')
		self.userEdit = QtGui.QComboBox()
		self.userEdit.setEditable(True)
		self.userEdit.autoCompletion = True

		passwdLabel = QtGui.QLabel(u'密  码：')
		self.passwdEdit = QtGui.QLineEdit()

		self.autologin = QtGui.QCheckBox(u'自动登录')
		self.remeberpasswd = QtGui.QCheckBox(u'记住密码')

		loginBtn = QtGui.QPushButton(u'登陆')
		self.connect(loginBtn, QtCore.SIGNAL('clicked()'), self.login)

		grid = QtGui.QGridLayout()
		grid.setSpacing(10)
		grid.addWidget(serverLabel, 1, 0)
		grid.addWidget(self.serverEdit, 1, 1, 1, 4)
		grid.addWidget(userLabel, 2, 0)
		grid.addWidget(self.userEdit, 2, 1, 1, 4)
		grid.addWidget(passwdLabel, 3, 0)
		grid.addWidget(self.passwdEdit, 3, 1, 1, 4)
		grid.addWidget(self.autologin, 4, 1)
		grid.addWidget(self.remeberpasswd, 4, 3)
		grid.addWidget(loginBtn, 5, 1, 1, 4)

		self.setLayout(grid)
		self.resize(350, 100)

	def closeEvent(self, enven):
		self.closed = 1	

	def __login__(self, uri, user, passwd):
		return True

	def login(self):
		if self.__login__('10.107.10.100:8773', 'anzigly', '123456'):
			self.accept()
		else:
			self.reject()
			print "rejected"

if __name__ == '__main__':
	app = QtGui.QApplication(sys.argv)
	loginwin = LoginWin()
	loginwin.show()
	sys.exit(app.exec_())