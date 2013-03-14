#!/usr/bin/env python
# DcAdmin.py
import xmlrpclib, rsa, sys
rpcport = 8772

class DcAdmin:
	def __init__(self, dst):
		self.senssionkey = None
		try:
			self.rpcclient = xmlrpclib.ServerProxy("http://%s:%s" % (dst, rpcport))
			self.pubkey = self.get_pubkey()
		except:
			print "Can NOT connect to DeskCloud Server through XMLRPC Way"
			sys.exit(1)
	def get_pubkey(self):
		''''Get public key from the server'''
		n, e = self.rpcclient.getPubkey()
		publickey = rsa.PublicKey(int(n), int(e))
		return publickey
	def login_admin(self, name, passwd):
		'''Admin user login interface'''
		encryptName = rsa.transform.bytes2int(rsa.encrypt(name, self.pubkey))
		encryptPasswd = rsa.transform.bytes2int(rsa.encrypt(passwd, self.pubkey))
		encryptName = str(encryptName)
		encryptPasswd = str(encryptPasswd)
		print encryptName
		if not self.rpcclient.loginAdmin(encryptName, encryptPasswd):
			print "login failed!"
		else:
			print "login successed"

	def add_admin(self, name, passwd):
		'''Add user to the server'''
		'''@TODO: Encrypy the passwd and verify user'id by the server side'''
		if not self.rpcclient.addAdmin(name, passwd):
			print "Add admin user %s failed" % name
		else:
			print "Add admin user %s successed" % name

if __name__ == '__main__':
	host = '10.107.10.100'
	dcadmin = DcAdmin(host)
	dcadmin.login_admin('anzigly', '123456')