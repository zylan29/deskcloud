#!/usr/bin/env python
# dcUser.py
'''
User of DeskCloud System
'''
__author__ = 'liziyang'
__version__ = '0.1'

class DcUser:
	def __init__(self, conn):
		self.conn = conn

	#def get_all_images(self):
	#	return self.conn.get_all_images()

	def get_instance_reservations(self):
		return self.conn.get_all_instances()
		
	def get_all_instances(self):
		instances = []
		reservations = self.get_instance_reservations()
		for reservation in reservations:
			for instance in reservation.instances:
				instances.append(instance)
		return instances