#/usr/bin/env python
#-*- coding:utf-8 -*-
# loginWin.py
import sys
from PyQt4 import QtGui, QtCore
import dclib

class LoginWin(QtGui.QWidget):
	def __init__(self, parent=None):
		QtGui.QWidget.__init__(self, parent)
		self.windowTitle = dclib.getunicode(u'PDL虚拟桌面云系统')
		self.setWindowTitle(self.windowTitle)

		serverLabel = QtGui.QLabel(dclib.getunicode(u'服务器：'))
		serverEdit = QtGui.QLineEdit()

		grid = QtGui.QGridLayout()
		grid.setSpacing(10)

		grid.addWidget(serverLabel,1,0)
		grid.addWidget(serverEdit,1,1)

		self.setLayout(grid)

if __name__ == '__main__':
	app = QtGui.QApplication(sys.argv)
	loginwin = LoginWin()
	loginwin.show()
	sys.exit(app.exec_())