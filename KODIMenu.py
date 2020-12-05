from xbmcplugin import addDirectoryItem, endOfDirectory, setContent
from xbmcgui import ListItem

class KODIMenu():

    def __init__(self, plugin):
        self.plugin=plugin
        self.h = plugin.handle

    def start_folder(self):
        setContent(self.h, "videos")

    def new_info_item(self, info):
        li = ListItem(info, iconImage="")
        li.setProperty('IsPlayable', 'False')
        addDirectoryItem(self.h, "", listitem=li, isFolder=False)

    def new_video_item(self, displayName, title, playURL, thumbURL, duration):

        li = ListItem(displayName + ": " + title, playURL, iconImage=thumbURL)

        li.setProperty('IsPlayable', 'True')
        li.setInfo("video", {'mediatype': 'video', 'duration': 0})
        li.addStreamInfo('video', {'duration': duration})
        li.setArt({'icon': thumbURL})
        li.setArt({'poster': thumbURL})
        li.setArt({'thumb': thumbURL})
        li.setArt({'banner': thumbURL})

        addDirectoryItem(self.h, playURL, listitem=li, isFolder=False)

    def new_folder_item(self, item_name, item_val, func):

        li = ListItem(item_name, iconImage="")
        li.setProperty('IsPlayable', 'False')
        addDirectoryItem(self.h, self.plugin.url_for(func, item_val=item_val),
                         listitem=li, isFolder=True)

    def end_folder(self):
        endOfDirectory(self.h)
