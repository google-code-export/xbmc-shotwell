'''
Shotwell BD Access
'''

import os
import sqlite3
import datetime

bd=os.path.expanduser("~/.shotwell/data/photo.db")
thumbs128=os.path.expanduser("~/.shotwell/thumbs/thumbs128")
thumbs360=os.path.expanduser("~/.shotwell/thumbs/thumbs360")

class Shotwell:

	def __init__( self ):
		self.conn=sqlite3.connect(bd)
		self.conn.isolation_level = None

	def picture_list (self,sql, flagged=False):
		if flagged:
			sql+=" and flags=16"
		sql=sql+" order by id";
		cursor=self.conn.cursor()
		rows=cursor.execute(sql)
		l=[]
		for row in rows:
		    id=row[0]
		    filename=row[1]
		    l.append({
				'id': id,
				'name': os.path.basename(filename),
				'filename':filename,
				'icon':'%s/thumb%016x.jpg' % (thumbs128,id),
				'thumbnail': '%s/thumb%016x.jpg' % (thumbs360,id)
		    })
		cursor.close()
		return l

	def picture_list_flagged(self):
		return self.picture_list('select id, filename from phototable where 1=1',True)

	def picture_list_event(self,event_id,flagged):
		return self.picture_list('select id, filename from phototable where event_id=%s' % (event_id), flagged)

	def picture_list_last(self,flagged):
		return self.picture_list('select id, filename from phototable where import_id = (select max(import_id) from phototable)',flagged)

	def picture_list_tag(self,tag_id,flagged):
        # get a comma separated thumbnail list from a database field
		cursor=self.conn.cursor()
		cursor.execute('select photo_id_list from tagtable where id=%i' % (tag_id))
		row=cursor.fetchone()
		cursor.close()
		thumbs=row[0].split(",")
		thumbs.pop()
	    # and transform to a decimal number list after converting it from hexadecimal
		l=[]
		for f in thumbs:
			l.append(str(int(f[6:],16)))
		return self.picture_list('select id, filename from phototable where id in (%s)' % (','.join(l)),flagged)


	def event_list(self):
		cursor=self.conn.cursor()
		rows=cursor.execute('''
			select e.id, name, min(timestamp) as start,max(timestamp) as end, primary_source_id
			from eventtable e,phototable p where event_id=e.id 
			group by event_id order by 3 desc
		''');
		l=[]
		for row in rows:
			l.append({
				'id':row[0],
				'name':row[1],
				'start':datetime.datetime.fromtimestamp(row[2]),
				'end':datetime.datetime.fromtimestamp(row[3]),
				'icon':'%s/%s.jpg' % (thumbs128,row[4]),
				'thumbnail': '%s/%s.jpg' % (thumbs360,row[4])
			})
		return l

	def tag_list(self):
		cursor=self.conn.cursor()
		rows=cursor.execute('select id, name from tagtable')
		l=[]
		for row in rows:
			l.append({
				'id':row[0],
				'name':row[1]
			})
		return l
