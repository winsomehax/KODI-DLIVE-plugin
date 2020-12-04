import routing
from xbmcplugin import addDirectoryItem, endOfDirectory, setContent
from xbmcgui import ListItem, Dialog, INPUT_ALPHANUM
import xbmcaddon
import dlive_query as dq

plugin = routing.Plugin()

def valid_user():
    global query
    if not query.validated_user_id:
        # Warn the user that it's not a valid user and resort to winsomehax so the add-on at least runs
        dialog = Dialog()
        ok = dialog.ok("Warning",
                       "The DLIVE add-on has not found your user on DLIVE")
        return False
    
    return True
        

@plugin.route('/')
def index():
    build_main_menu()


@plugin.route('/followed_live')
def followed_live():

    if not valid_user:
        return

    build_followed_live()


@plugin.route('/followed_replay')
def followed_replay():
    if not valid_user:
        return

    build_followed_replay()


@plugin.route('/followed_replay_user/<user>')
def followed_replay_user(user):

    if not valid_user:
        return

    build_followed_replay_user(user)


@plugin.route('/livestreams_search')
def livestreams_search():
    build_livestreams_search()


@plugin.route('/all_livestreams')
def livestreams_all():
    build_all_livestreams()


@plugin.route('/open_settings')
def open_settings():
    build_open_settings()


def build_main_menu():
    display_user = get_dlive_userid()

    h = plugin.handle

    setContent(h, "videos")
    li = ListItem("Your DLIVE username is: " + display_user, iconImage="")
    li.setProperty('IsPlayable', 'False')
    addDirectoryItem(h, plugin.url_for(open_settings),
                     listitem=li, isFolder=True)

    li = ListItem("Currently live streamers you follow", iconImage="")
    li.setProperty('IsPlayable', 'False')
    addDirectoryItem(h, plugin.url_for(followed_live),
                     listitem=li, isFolder=True)

    li = ListItem('Replays of streamers you follow', iconImage="")
    li.setProperty('IsPlayable', 'False')
    addDirectoryItem(h, plugin.url_for(followed_replay),
                     listitem=li, isFolder=True)

    li = ListItem('View all currently live streams', iconImage="")
    li.setProperty('IsPlayable', 'False')
    addDirectoryItem(h, plugin.url_for(livestreams_all),
                     listitem=li, isFolder=True)

    li = ListItem('Search currently live streams', iconImage="")
    li.setProperty('IsPlayable', 'False')
    addDirectoryItem(h, plugin.url_for(livestreams_search),
                     listitem=li, isFolder=True)

    endOfDirectory(h)


def build_followed_live():

    h = plugin.handle
    setContent(h, "videos")

    global query
    live_streams = query.get_following_live_streams()

    if 0==len(live_streams):
        li = ListItem(
            "** NONE OF THE STREAMERS YOU FOLLOW ARE LIVE **", iconImage="")
        li.setProperty('IsPlayable', 'False')
        addDirectoryItem(h, "", listitem=li, isFolder=False)
    else:
        for stream in live_streams:
            li = ListItem(stream.displayName + ": " + stream.title, iconImage=stream.thumbURL)
            li.setProperty('IsPlayable', 'True')
            addDirectoryItem(h, stream.playURL, listitem=li, isFolder=False)

    endOfDirectory(h)


def build_followed_replay():
    h = plugin.handle
    setContent(h, "videos")

    global query
    
    following = query.get_following()

    if 0==len(following):
        li = ListItem("** YOU ARE NOT FOLLOWING ANYONE **", iconImage="")
        li.setProperty('IsPlayable', 'False')
        addDirectoryItem(h, "", listitem=li, isFolder=False)
    else:
        for user in following:
            url = plugin.url_for(followed_replay_user, user=user.user_id)
            li = ListItem(user.displayName, iconImage="")
            li.setProperty('IsPlayable', 'False')
            addDirectoryItem(h, url, listitem=li, isFolder=True)

    endOfDirectory(h)


def build_followed_replay_user(user):

    h = plugin.handle
    setContent(h, "videos")

    global query
    replays=query.get_replays(user)

    if 0==len(replays):
        li = ListItem("** NO REPLAYS FOUND **", iconImage="")
        li.setProperty('IsPlayable', 'False')
        addDirectoryItem(h, "", listitem=li, isFolder=False)
    else:
        for stream in replays:
            li = ListItem(stream.title, iconImage=stream.thumbURL)
            li.setProperty('IsPlayable', 'True')
            li.setInfo("video", {'mediatype': 'video', 'duration': stream.length})
            li.addStreamInfo('video', {'duration': stream.length})
            li.setArt({'icon': stream.thumbURL})
            li.setArt({'poster': stream.thumbURL})
            li.setArt({'thumb': stream.thumbURL})
            li.setArt({'banner': stream.thumbURL})

            addDirectoryItem(h, stream.playURL, listitem=li, isFolder=False)

    endOfDirectory(h)


def build_all_livestreams():

    h = plugin.handle
    setContent(h, "videos")

    global query
    streams = query.get_all_live_streams()

    if 0==len(streams):
        li = ListItem("** NO LIVE STREAMS FOUND **", iconImage="")
        li.setProperty('IsPlayable', 'False')
        addDirectoryItem(h, "", listitem=li, isFolder=False)
    else:
        for stream in streams:

            li = ListItem(stream.displayName + ": " + stream.title, iconImage=stream.thumbURL)

            li.setProperty('IsPlayable', 'True')
            li.setInfo("video", {'mediatype': 'video', 'duration': 0})
            li.addStreamInfo('video', {'duration': 0})
            li.setArt({'icon': stream.thumbURL})
            li.setArt({'poster': stream.thumbURL})
            li.setArt({'thumb': stream.thumbURL})
            li.setArt({'banner': stream.thumbURL})

            addDirectoryItem(h, stream.playURL, listitem=li, isFolder=False)

    endOfDirectory(h)


def build_livestreams_search():

    search_for = Dialog().input("Enter search", "", INPUT_ALPHANUM, 0, 0).upper()

    h = plugin.handle
    setContent(h, "videos")

    global query
    streams = query.get_all_live_streams()

    if 0==len(streams):
        li = ListItem("** NO LIVE STREAMS FOUND **", iconImage="")
        li.setProperty('IsPlayable', 'False')
        addDirectoryItem(h, "", listitem=li, isFolder=False)
    else:

        for stream in streams:

            if search_for in stream.title.upper():
                li = ListItem(stream.displayName + ": " + stream.title, iconImage=stream.thumbURL)
                li.setProperty('IsPlayable', 'True')
                li.setInfo("video", {'mediatype': 'video', 'duration': 0})
                li.addStreamInfo('video', {'duration': 0})
                li.setArt({'icon': stream.thumbURL})
                li.setArt({'poster': stream.thumbURL})
                li.setArt({'thumb': stream.thumbURL})
                li.setArt({'banner': stream.thumbURL})

                addDirectoryItem(h, stream.playURL, listitem=li, isFolder=False)

    endOfDirectory(h)


def build_open_settings():
    xbmcaddon.Addon().openSettings()
    get_dlive_userid()



def get_dlive_userid():
    global query
    display_name = xbmcaddon.Addon().getSetting("user")   # What is the Display Name set as in the add-on settings
                 
    if not query.set_user_id(display_name):               # set the query object if it has a valid blockchain user-id
    
        # Warn the user that it's not a valid user and resort to winsomehax so the add-on at least runs
        dialog = Dialog()
        ok = dialog.ok("Unable to find your DLIVE user",
                       "The DLIVE add-on cannot find the Display Name specified in settings. Using the default: winsomehax")
        
        query.set_user_id("winsomehax")                   # set it as winsomehax
        xbmcaddon.Addon().setSetting(id="user", value="winsomehax") # Write that to the settings

    return display_name

query = dq.Query()
get_dlive_userid()
