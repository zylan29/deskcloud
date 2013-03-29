#!/usr/bin/env python
import boto
from boto.ec2.regioninfo import RegionInfo

EC2_ACCESS_KEY = 'acf6ce0848d946f68a9d4c71f0d9bdc6'
EC2_SECRET_KEY = 'c64e94fe179c4346964e39217d3c1767'
REGION_NAME = 'myregion'
REGION_ENDPOINT = '10.107.10.100'
REGION_PORT=8773
REGION_PATH='/services/Cloud'

region = RegionInfo(name=REGION_NAME, endpoint=REGION_ENDPOINT)

conn = boto.connect_ec2(EC2_ACCESS_KEY, EC2_SECRET_KEY, region=region, port=REGION_PORT, path=REGION_PATH, is_secure=False)
reservations = conn.get_all_instances()
def operate():
    for reservation in reservations:
        for instance in reservation.instances:
            state = instance.state
            print "id:%s,state:%s,ip:%s" % (instance.id, state, instance.ip_address)
operate()