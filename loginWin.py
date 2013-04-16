#/usr/bin/env python
#-*- coding:utf-8 -*-
# loginWin.py
import sys
from PyQt4 import QtGui, QtCore
import xmlrpclib, rsa
import boto
from boto.ec2.regioninfo import RegionInfo

keybits = 512

class LoginWin(QtGui.QDialog):
	def __init__(self, parent=None):
		QtGui.QDialog.__init__(self, parent)

		self.closed = 0
		self.rpcclient = None
		self.pubkey = None
		self.sessionkey = None
		self.rpcport = 8772

		self.region_name = 'pdl'
		self.conn = None
		self.server = None
		self.region_port = '8773'
		self.region_path = '/services/Cloud'

		self.setWindowTitle(u'PDL虚拟桌面云系统')

		pic = QtGui.QPixmap('resources/zhangjiajie.jpg')
		pic = pic.scaledToWidth(350)
		piclabel = QtGui.QLabel()
		piclabel.setPixmap(pic)

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
		self.passwdEdit.setEchoMode(QtGui.QLineEdit.Password)

		self.autologin = QtGui.QCheckBox(u'自动登录')
		self.remeberpasswd = QtGui.QCheckBox(u'记住密码')

		self.serverEdit.addItem(u'http://10.0.17.110:8773/services/Cloud')
		self.userEdit.addItem(u'ec2')
		self.passwdEdit.setText(u'ec2')

		loginBtn = QtGui.QPushButton(u'登陆')
		self.connect(loginBtn, QtCore.SIGNAL('clicked()'), self.login)

		grid = QtGui.QGridLayout()
		grid.setSpacing(10)
		grid.addWidget(piclabel, 1, 0, 1, 5)
		grid.addWidget(serverLabel, 2, 0)
		grid.addWidget(self.serverEdit, 2, 1, 1, 4)
		grid.addWidget(userLabel, 3, 0)
		grid.addWidget(self.userEdit, 3, 1, 1, 4)
		grid.addWidget(passwdLabel, 4, 0)
		grid.addWidget(self.passwdEdit, 4, 1, 1, 4)
		grid.addWidget(self.autologin, 5, 1)
		grid.addWidget(self.remeberpasswd, 5, 3)
		grid.addWidget(loginBtn, 6, 1, 1, 4)

		self.setLayout(grid)
		self.resize(350, 100)

	def get_pubkey(self):
		''''Get public key from the server'''
		n, e = self.rpcclient.getPubkey()
		publickey = rsa.PublicKey(int(n), int(e))
		return publickey

	def get_conn(self):
		return self.conn

	def closeEvent(self, enven):
		self.closed = 1	

	def __decryptWithKey(self, crypto, prikey):
		return rsa.decrypt(rsa.transform.int2bytes(int(crypto)), prikey)

	def __decryptFromStr(self, crypto):
		return self.__decryptWithKey(crypto, self.senssion_key)

	def __encrypt2str(self, message):
		return str(rsa.transform.bytes2int(rsa.encrypt(message, self.pubkey)))

	def __login(self, username, passwd):
		encryptName = self.__encrypt2str(username)
		encryptPasswd = self.__encrypt2str(passwd)
		(session_pubkey, self.senssion_key) = rsa.newkeys(keybits)
		try:
			access, secret, tenant_id, user_id = (self.__decryptFromStr(x) for x in self.rpcclient.loginUser(encryptName, encryptPasswd, str(session_pubkey.n), str(session_pubkey.e)))
			region = RegionInfo(name=self.region_name, endpoint=self.server)
			self.conn = boto.connect_ec2(access, secret, region=region, port=int(self.region_port), path=self.region_path, is_secure=False)
			#TODO: Need to fix! when the connection is not correct, we need a timeout alert!
			self.conn.get_all_instances()
			return True
		except Exception, e:
			print 'c'
			QtGui.QMessageBox.warning(self, u'提示', u'连接服务器发生错误！', QtGui.QMessageBox.Yes)
			return False

	def parse_url(self, serverurl):
		http_head = 'http://'
		if serverurl.startswith(http_head):
			serverurl = serverurl[len(http_head):]
		ip, port = serverurl[:serverurl.find('/')].split(":")
		path = serverurl[serverurl.find('/'):]
		return ip, port, path

	def login(self):
		serverurl = str(self.serverEdit.currentText())
		self.server, self.region_port, self.region_path = self.parse_url(serverurl)
		username = str(self.userEdit.currentText())
		passwd = str(self.passwdEdit.text())

		if self.rpcclient == None:
			try:
				self.rpcclient = xmlrpclib.ServerProxy("http://%s:%s" % (self.server, self.rpcport))
				self.pubkey = self.get_pubkey()
			except:
				QtGui.QMessageBox.warning(self, u'提示', u'连接服务器发生错误！', QtGui.QMessageBox.Yes)
				self.reject()
				return
		if self.__login(username, passwd):
			self.accept()
		else:
			self.reject()