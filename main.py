import routing
from xbmcplugin import addDirectoryItem, endOfDirectory, setContent
from xbmcgui import ListItem, Dialog, INPUT_ALPHANUM
import xbmcaddon
import dlivequery

plugin = routing.Plugin()
# kp = kf.KodiPlugin()
dq = dlivequery.DliveInfo()


@plugin.route('/')
def index():
	h = plugin.handle
	setContent(h, "videos")

	dq_user = xbmcaddon.Addon().getSetting("user")

	li = ListItem("Your DLIVE username is: " + dq_user, iconImage="")
	li.setProperty('IsPlayable', 'False')
	addDirectoryItem(h, plugin.url_for(open_settings), listitem=li, isFolder=True)

	li = ListItem("Live streamers you follow", iconImage="")
	li.setProperty('IsPlayable', 'False')
	addDirectoryItem(h, plugin.url_for(followed_live), listitem=li, isFolder=True)

	li = ListItem('Replays of followed streamers', iconImage="")
	li.setProperty('IsPlayable', 'False')
	addDirectoryItem(h, plugin.url_for(followed_replay), listitem=li, isFolder=True)

	li = ListItem('Search current live streams', iconImage="")
	li.setProperty('IsPlayable', 'False')
	addDirectoryItem(h, plugin.url_for(livestreams_search), listitem=li, isFolder=True)

	endOfDirectory(h)


@plugin.route('/followed_live')
def followed_live():
	anylive = False
	h = plugin.handle
	setContent(h, "videos")
	f = dq.following_live_streams(xbmcaddon.Addon().getSetting("user"))

	for u in f:
		name = u[0]
		url = u[1]
		thumb = u[2]
		streamer = u[3]

		li = ListItem(streamer + ": " + name, iconImage=thumb)
		li.setProperty('IsPlayable', 'True')
		addDirectoryItem(h, url, listitem=li, isFolder=False)

		anylive = True

	if not anylive:
		li = ListItem("** NONE OF THE STREAMERS YOU FOLLOW ARE LIVE **", iconImage="")
		li.setProperty('IsPlayable', 'False')
		addDirectoryItem(h, "", listitem=li, isFolder=False)

	endOfDirectory(h)


@plugin.route('/followed_replay')
def followed_replay():
	any_followed = False

	h = plugin.handle
	setContent(h, "videos")
	f = dq.following(xbmcaddon.Addon().getSetting("user"))

	for u in f:
		name = u[0]
		url = plugin.url_for(followed_replay_user, user=u[1])

		li = ListItem(name, iconImage="")
		li.setProperty('IsPlayable', 'False')
		addDirectoryItem(h, url, listitem=li, isFolder=True)

		any_followed = True

	if not any_followed:
		li = ListItem("** YOU ARE NOT FOLLOWING ANYONE **", iconImage="")
		li.setProperty('IsPlayable', 'False')
		addDirectoryItem(h, "", listitem=li, isFolder=False)

	endOfDirectory(h)


@plugin.route('/followed_replay_user/<user>')
def followed_replay_user(user):
	any_replays = False

	h = plugin.handle
	setContent(h, "videos")
	f = dq.replays(user, xbmcaddon.Addon().getSetting("user"))

	for u in f:
		title = u[0]
		length = u[1]
		thumb = u[2]
		playback_url = u[3]

		li = ListItem(title, iconImage=thumb)
		li.setProperty('IsPlayable', 'True')
		li.setInfo("video", {'mediatype': 'video', 'duration': length})
		li.addStreamInfo('video', {'duration': length})
		li.setArt({'icon': thumb})
		li.setArt({'poster': thumb})
		li.setArt({'thumb': thumb})
		li.setArt({'banner': thumb})

		addDirectoryItem(h, playback_url, listitem=li, isFolder=False)

		any_replays = True

	if not any_replays:
		li = ListItem("** NO REPLAYS FOUND **", iconImage="")
		li.setProperty('IsPlayable', 'False')
		addDirectoryItem(h, "", listitem=li, isFolder=False)

	endOfDirectory(h)


@plugin.route('/livestreams_search')
def livestreams_search():
	search_for = Dialog().input("Enter search", "", INPUT_ALPHANUM, 0, 0).upper()

	any_replays = False

	h = plugin.handle
	setContent(h, "videos")
	f = dq.all_live_streams()

	for u in f:
		title = u[0]
		playback_url = u[1]
		thumb = u[2]
		user = u[3]

		if search_for in title.upper():
			li = ListItem(user + ": " + title, iconImage=thumb)
			li.setProperty('IsPlayable', 'True')
			li.setInfo("video", {'mediatype': 'video', 'duration': 0})
			li.addStreamInfo('video', {'duration': 0})
			li.setArt({'icon': thumb})
			li.setArt({'poster': thumb})
			li.setArt({'thumb': thumb})
			li.setArt({'banner': thumb})

			addDirectoryItem(h, playback_url, listitem=li, isFolder=False)

			any_replays = True

	if not any_replays:
		li = ListItem("** NO LIVE STREAMS FOUND **", iconImage="")
		li.setProperty('IsPlayable', 'False')
		addDirectoryItem(h, "", listitem=li, isFolder=False)

	endOfDirectory(h)


@plugin.route('/open_settings')
def open_settings():
	xbmcaddon.Addon().openSettings()


if __name__ == '__main__':
	# logging.basicConfig(filename='/tmp/example.log', level=logging.DEBUG

	plugin.run()
# menubuilders.runme()
