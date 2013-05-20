#!/usr/bin/env python
# dcUser.py
'''
User of DeskCloud System
'''
__author__ = 'liziyang'
__version__ = '0.1'

class DcUser:
	def __init__(self, ec2conn, rpcconn):
		self.ec2conn = ec2conn
		self.rpcconn = rpcconn

	def get_instance_reservations(self):
		return self.ec2conn.get_all_instances()
		
	def get_all_instances(self):
		instances = []
		reservations = self.get_instance_reservations()
		for reservation in reservations:
			for instance in reservation.instances:
				instances.append(instance)
		return instances

	def reboot_instances(self, ins_id_list):
		self.ec2conn.reboot_instances(ins_id_list)

	def start_instances(self, ins_id_list):
		self.ec2conn.start_instances(ins_id_list)

	def stop_instances(self, ins_id_list):
		ret=self.ec2conn.stop_instances(ins_id_list)

	def get_display(self, ins_id):
		display = eval(self.rpcconn.getDisplay(ins_id))
		return display
