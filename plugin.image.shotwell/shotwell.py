'''
Classe que permet accedir a la BD de Shotwell
'''

import sys
import os
import xbmc
from pysqlite2 import dbapi2 as sqlite

bd="/home/jaumem/.shotwell/data/photo.db"

class Shotwell:

	def __init__( self ):
		self.conn=sqlite.connect(bd)
		self.conn.isolation_level = None

	def picture_list(self):
		cursor=self.conn.cursor()
		rows=cursor.execute('select filename from phototable')
		l=[]
		for row in rows:
			# TODO: fet que el icon i el thumbnail sigui el que toca
			# com es relacionen amb el nom? no esta a la taula!!!
			l.append({'filename':row[0],'icon':row[0],'thumbnail':row[0]})
		return l
