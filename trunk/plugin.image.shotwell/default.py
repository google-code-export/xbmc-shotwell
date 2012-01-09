import sys
import xbmc, xbmcgui, xbmcplugin, xbmcaddon
from shotwell import *

# plugin constants
__plugin__ = "shotwell"
__author__ = "jaume.moral"
__url__ = "http://code.google.com/p/xbmc-shotwell/"
__svn_url__ = "http://xbmc-shotwell.googlecode.com/svn/trunk/"
__version__ = "1.0"
__settings__ = xbmcaddon.Addon(id='plugin.image.shotwell')

# code                

class XBMCShotwell:		

	def __init__(self):
		self.url=sys.argv[0]
		self.handle=int(sys.argv[1])
		self.parameters=sys.argv[2]
		self.shotwell=Shotwell()

	def home_menu(self):
		xbmcplugin.addDirectoryItem(
			self.handle,
			url=self.url+"?events",
			isFolder=True,
			totalItems=2,
			listitem=xbmcgui.ListItem("Events",iconImage="",thumbnailImage=""))
		xbmcplugin.addDirectoryItem(
			self.handle,
			url=self.url+"?tags",
			isFolder=True,
			totalItems=2,
			listitem=xbmcgui.ListItem("Tags",iconImage="",thumbnailImage=""))
		xbmcplugin.addDirectoryItem(
			self.handle,
			url=self.url+"?last",
			isFolder=True,
			totalItems=2,
			listitem=xbmcgui.ListItem("Last import",iconImage="",thumbnailImage=""))
		xbmcplugin.endOfDirectory(self.handle, cacheToDisc=False)

	def all_events(self):
		events=self.shotwell.event_list()
		for e in events:
			start=e['start'].strftime('%d/%m/%Y')
			end=e['end'].strftime('%d/%m/%Y')
			dates=start
			if start != end:
				dates="%s - %s" % (start,end)
			if e['name'] == None:
				name=dates
			else:
				name="%s (%s)" % (e['name'], dates)
			xbmcplugin.addDirectoryItem(
				self.handle,
				url="%s?event=%i" % (self.url,e['id']),
				isFolder=True,
				totalItems=len(events),
				listitem=xbmcgui.ListItem(name,iconImage=e['icon'],thumbnailImage=e['thumbnail'])
			)
		xbmcplugin.endOfDirectory(self.handle, cacheToDisc=False)

	def all_tags(self):
		tags=self.shotwell.tag_list()
		for t in tags:
		   	xbmcplugin.addDirectoryItem(
		      	self.handle,
		      	url="%s?tag=%i" % (self.url,t['id']),
		      	isFolder=True,
		      	totalItems=len(tags),
		      	listitem=xbmcgui.ListItem(t['name'],iconImage="",thumbnailImage="")
		   	)
		xbmcplugin.endOfDirectory(self.handle, cacheToDisc=False)

	def tag_pictures(self,tag_id):
		self.fill_picture_list(self.shotwell.picture_list_tag(tag_id))

	def last_pictures(self):
		self.fill_picture_list(self.shotwell.picture_list_last())

	def event_pictures(self,event_id):
		self.fill_picture_list(self.shotwell.picture_list_event(event_id))

	def fill_picture_list(self,l):
		for f in l:
		    xbmcplugin.addDirectoryItem(
				self.handle,
				f['filename'],
				isFolder=False,
				totalItems=len(l),
				listitem=xbmcgui.ListItem(f['name'], iconImage=f['icon'],thumbnailImage=f['thumbnail'])
		)
		xbmcplugin.endOfDirectory(self.handle, cacheToDisc=False)

	def execute(self):
		if ( "events" in self.parameters ):
			self.all_events()
		elif ( "tags" in self.parameters ):
			self.all_tags()
		elif ( "last" in self.parameters ):
			self.last_pictures()
		elif ( "tag=" in self.parameters ):
			self.tag_pictures(int(self.parameters.split("=")[1]))
		elif ( "event=" in self.parameters ):
			self.event_pictures(int(self.parameters.split("=")[1]))
		else:
			self.home_menu()


if ( __name__ == "__main__" ):
    # sys.argv[0] is plugin's URL 
    # sys.argv[1] is the handle
    # sys.argv[2] if the query string
    # Quan un element de la llista es de tipus carpeta, li passem la URL del plugin i concatenat amb un "?", la resta de parametres
    # que li volem passar. En aquest cas, el parametres seran:
    # events | favorits | tags | tag=tag_id | event=event_id 
    # exemple:
    #   plugin://plugin.image.shotwell/?tag=platges

    plugin=XBMCShotwell()
    plugin.execute()

