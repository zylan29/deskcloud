#!/usr/bin/env python
# DcAdmin.py
import xmlrpclib, rsa, sys
rpcport = 8772
keybits = 512

class DcAdmin:
	def __init__(self, dst):
		self.senssion_key = None
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

	def __encrypt2str(self, message):
		return str(rsa.transform.bytes2int(rsa.encrypt(message, self.pubkey)))

	def login_admin(self, name, passwd):
		'''Admin user login interface'''
		encryptName = self.__encrypt2str(name)
		encryptPasswd = self.__encrypt2str(passwd)
		(session_pubkey, self.senssion_key) = rsa.newkeys(keybits)
		if not self.rpcclient.loginAdmin(encryptName, encryptPasswd, str(session_pubkey.n), str(session_pubkey.e)):
			print "login failed!"
		else:
			print "login successed"

	def add_admin(self, name, passwd):
		'''Add Admin user'''
		'''@TODO: Encrypy the passwd and verify user'session key by the server side'''
		if not self.rpcclient.addAdmin(name, passwd):
			print "Add admin user %s failed" % name
		else:
			print "Add admin user %s successed" % name

	def add_user(self, name, passwd, access, secret, tenant_id, user_id):
		'''Add EC2 User'''
		'''@TODO:Encrypy the passwd and verify user'session key by the server side'''
		if not self.rpcclient.addUser(self.__encrypt2str(name), \
			self.__encrypt2str(passwd), self.__encrypt2str(access), \
			self.__encrypt2str(secret), self.__encrypt2str(tenant_id), \
			self.__encrypt2str(user_id)):
			print "Add EC2 user %s failed" % name
		else:
			print "Add EC2 user %s successed" % name

if __name__ == '__main__':
	host = '10.107.10.100'
	dcadmin = DcAdmin(host)
	#dcadmin.login_admin('anzigly', '123456')
	dcadmin.add_user('admin','admin','acf6ce0848d946f68a9d4c71f0d9bdc6','c64e94fe179c4346964e39217d3c1767','8e5834d7250b4897b140d4cdde3cea86','027112f0428940e9b889342f949eb30b')