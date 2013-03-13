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
	def add_admin(self, name, passwd):
		'''Add user to the server'''
		if not self.rpcclient.addAdmin(name, passwd):
			print "Add admin user %s failed" % name
		else:
			print "Add admin user %s successed" % name

if __name__ == '__main__':
	host = '10.0.17.110'
	dcadmin = DcAdmin(host)