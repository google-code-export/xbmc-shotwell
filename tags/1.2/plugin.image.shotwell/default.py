import sys
import xbmc, xbmcgui, xbmcplugin, xbmcaddon
from shotwell import *

# plugin constants
__plugin__ = "shotwell"
__author__ = "jaume.moral"
__url__ = "http://code.google.com/p/xbmc-shotwell/"
__svn_url__ = "http://xbmc-shotwell.googlecode.com/svn/trunk/"
__version__ = "1.1"
__settings__ = xbmcaddon.Addon(id='plugin.image.shotwell')
__language__ = __settings__.getLocalizedString
DATE_FORMAT = xbmc.getRegion('dateshort').lower()

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
			listitem=xbmcgui.ListItem(__language__(30000),iconImage="",thumbnailImage=""))
		xbmcplugin.addDirectoryItem(
			self.handle,
			url=self.url+"?tags",
			isFolder=True,
			totalItems=2,
			listitem=xbmcgui.ListItem(__language__(30001),iconImage="",thumbnailImage=""))
		xbmcplugin.addDirectoryItem(
			self.handle,
			url=self.url+"?last",
			isFolder=True,
			totalItems=2,
			listitem=xbmcgui.ListItem(__language__(30002),iconImage="",thumbnailImage=""))
		xbmcplugin.addDirectoryItem(
			self.handle,
			url=self.url+"?flagged",
			isFolder=True,
			totalItems=2,
			listitem=xbmcgui.ListItem(__language__(30003),iconImage="",thumbnailImage=""))
		xbmcplugin.endOfDirectory(self.handle, cacheToDisc=False)

	def all_events(self):
		events=self.shotwell.event_list()
		for e in events:
			start=e['start'].strftime(DATE_FORMAT)
			end=e['end'].strftime(DATE_FORMAT)
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

	def tag_pictures(self,tag_id,flagged):
		self.fill_picture_list(self.shotwell.picture_list_tag(tag_id,flagged),flagged)

	def last_pictures(self,flagged=False):
		self.fill_picture_list(self.shotwell.picture_list_last(flagged),flagged)

	def event_pictures(self,event_id,flagged):
		self.fill_picture_list(self.shotwell.picture_list_event(event_id,flagged),flagged)

	def all_flagged_pictures(self):
		self.fill_picture_list(self.shotwell.picture_list_flagged())

	def fill_picture_list(self,l,flagged=True):
		# add "Flagged" folder before pictures except in flagged is true
		if not flagged:
			xbmcplugin.addDirectoryItem(
				self.handle,
				url="%s?%s=flagged" % (self.url,self.parameters),
				isFolder=True,
				totalItems=len(l)+1,
				listitem=xbmcgui.ListItem(__language__(30003), iconImage="",thumbnailImage="")
			)
		for f in l:
		    xbmcplugin.addDirectoryItem(
				self.handle,
				f['filename'],
				isFolder=False,
				totalItems=len(l)+1,
				listitem=xbmcgui.ListItem(f['name'], iconImage=f['icon'],thumbnailImage=f['thumbnail'])
			)
		xbmcplugin.endOfDirectory(self.handle, cacheToDisc=False)

	def execute(self):
		flagged=False
		if ("flagged" in self.parameters):
			flagged=True

		if ( "events" in self.parameters ):
			self.all_events()
		elif ( "tags" in self.parameters ):
			self.all_tags()
		elif ( "last" in self.parameters ):
			self.last_pictures(flagged)
		elif ( "tag=" in self.parameters ):
			self.tag_pictures(int(self.parameters.split("=")[1]),flagged)
		elif ( "event=" in self.parameters ):
			self.event_pictures(int(self.parameters.split("=")[1]),flagged)
		else:
			if not flagged:
				self.home_menu()
			else: 
				self.all_flagged_pictures()


if ( __name__ == "__main__" ):
    # sys.argv[0] is plugin's URL 
    # sys.argv[1] is the handle
    # sys.argv[2] if the query string
    # When we click on a folter item in a list, plugin URL is called as it if was a web URL
    # Parameters are appened at the end of the URL after a "?"
    # Possible parameters are
    # - events
    # - last
	# - tags
    # - tag=tag_id
    # - event=event_id 
    # - as an optional parameter... flagged
    # Exemples:
    #   plugin://plugin.image.shotwell/?tag=mountains
    #   plugin://plugin.image.shotwell/?events

    plugin=XBMCShotwell()
    plugin.execute()
