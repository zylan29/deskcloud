#/usr/bin/env python
import xmlrpclib, sys

class DcConnection():
	def __init__(self, uri, transport=None, encoding=None, verbose=0, allow_none=0, use_datetime=0):
		self.rpcclient = xmlrpclib.ServerProxy(uri, transport=None, encoding=None, verbose=0, allow_none=0, use_datetime=0)
		self.sessionkey = None

	def __getattr__(self, name):
		print name
		glob = {'n':10}
		local = {}
		func = 'self.rpcclient.test'
		print sys.argv
		print locals
		c = compile(func,'','eval')
		return eval(c)
		#return eval(func, glob, local)




if __name__ == '__main__':
	rpcclient = DcConnection("http://192.168.0.135:8772")
	print rpcclient.t(1)