import sys
import xbmc, xbmcgui, xbmcplugin, xbmcaddon
from shotwell import *

# plugin constants
__plugin__ = "shotwell"
__author__ = "jaumem"
__url__ = "http://code.google.com/p/xbmc-addons/"
__svn_url__ = "http://xbmc-addons.googlecode.com/svn/trunk/plugins/pictures/flickr"
__version__ = "1.5.4"
__settings__ = xbmcaddon.Addon(id='plugin.image.shotwell')

# codi en si                

def llistat_categories():
    handle=int(sys.argv[1])
    xbmcplugin.addDirectoryItem(handle,url=sys.argv[0]+"?events",isFolder=True,totalItems=3,listitem=xbmcgui.ListItem("Events",iconImage="",thumbnailImage=""))
    xbmcplugin.addDirectoryItem(handle,url=sys.argv[0]+"?tags",isFolder=True,totalItems=3,listitem=xbmcgui.ListItem("Tags",iconImage="",thumbnailImage=""))
    xbmcplugin.addDirectoryItem(handle,url=sys.argv[0]+"?favorits",isFolder=True,totalItems=3,listitem=xbmcgui.ListItem("Favorits",iconImage="",thumbnailImage=""))
    xbmcplugin.endOfDirectory(handle, cacheToDisc=False)

def llistat_events():
    # TODO: connectar a la BD per veure els events disponibles
    handle=int(sys.argv[1])
    xbmcplugin.addDirectoryItem(handle,url=sys.argv[0]+"?event=ev1",isFolder=True,totalItems=2,listitem=xbmcgui.ListItem("Event1",iconImage="",thumbnailImage=""))
    xbmcplugin.addDirectoryItem(handle,url=sys.argv[0]+"?event=ev2",isFolder=True,totalItems=2,listitem=xbmcgui.ListItem("Event2",iconImage="",thumbnailImage=""))
    xbmcplugin.endOfDirectory(handle, cacheToDisc=False)

def llistat_tags():
    # TODO: connectar a la BD per veure els tags disponibles
    handle=int(sys.argv[1])
    xbmcplugin.addDirectoryItem(handle,url=sys.argv[0]+"?tag=tag1",isFolder=True,totalItems=2,listitem=xbmcgui.ListItem("Tag1",iconImage="",thumbnailImage=""))
    xbmcplugin.addDirectoryItem(handle,url=sys.argv[0]+"?tag=tag2",isFolder=True,totalItems=2,listitem=xbmcgui.ListItem("Tag2",iconImage="",thumbnailImage=""))
    xbmcplugin.endOfDirectory(handle, cacheToDisc=False)

def llistat_tag(tag):
    # TODO: obtenir les fotos del tag que em passen
    handle=int(sys.argv[1])
    shotwell=Shotwell()
    l=shotwell.picture_list()
    print l
    for f in l:
        listitem=xbmcgui.ListItem(f['filename'], 
	    iconImage=f['icon'], 
	    thumbnailImage=f['thumbnail'])
        xbmcplugin.addDirectoryItem(handle,f['filename'],isFolder=False,totalItems=len(l),listitem=listitem)
    xbmcplugin.endOfDirectory(handle, cacheToDisc=False)
#        listitem=xbmcgui.ListItem(f['filename'], 
#	    iconImage=f['icon']"/home/jaumem/.shotwell/thumbs/thumbs128/thumb000000000000000a.jpg", 
#	    thumbnailImage="/home/jaumem/.shotwell/thumbs/thumbs360/thumb000000000000000a.jpg")


def llistat_favorits():
    # TODO: obtenir les fotos favorites
    llistat_tag("favo")

def llistat_event(event):
    # TODO: obtenir les fotos de l'event que em passen.
    # Per aixo farem una classe shotwell que obtingui aquesta informacio com a llistes de fotos, i les fotos tindran les dades que volem.
    # A partir d'aquestes llistes, muntarem els "listitems" que calguin.
    llistat_tag(event)


if ( __name__ == "__main__" ):
    xbmc.log("Hello world del plugin")
    # sys.argv[0] es la URL del plugin
    # sys.argv[2] es el parametre que li ha arribat al plugin
    # Quan un element de la llista es de tipus carpeta, li passem la URL del plugin i concatenat amb un "?", la resta de parametres
    # que li volem passar. En aquest cas, el parametres seran:
    # events | favorits | tags | tag=nom_del_tag | event=nom_del_event 
    # exemple:
    #   plugin://pictures/fspot/?tag=platges
    if ( "events" in sys.argv[2] ):
	llistat_events()
    elif ( "favorits" in sys.argv[2] ):
	llistat_favorits()
    elif ( "tags" in sys.argv[2] ):
	llistat_tags()
    elif ( "tag=" in sys.argv[2] ):
	llistat_tag(sys.argv[2][5:])
    elif ( "event=" in sys.argv[2] ):
	llistat_event(sys.argv[2][6:])
    else:	
	llistat_categories()

