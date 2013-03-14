#/usr/bin/env python
#-*- coding:utf-8 -*-

from PyQt4 import QtCore

def getunicode(chinesestr):
	return unicode(QtCore.QString(chinesestr).toLocal8Bit(), 'gbk', 'ignore')