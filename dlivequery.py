import graphql


class DliveInfo():
	_info = {}

	def __init__(self):
		pass

	def following(self, uname):
		self.refresh(uname)
		following = []

		if not (self._info is None):

			for u in self._info["data"]["user"]["following"]["list"]:
				following.append((u["displayname"], u["username"]))

		return following

	def replays(self, username, uname):
		self.refresh(uname)
		replays = []

		if not (self._info is None):
			for u in self._info["data"]["user"]["following"]["list"]:
				if u["username"] == username:
					for s in u["pastBroadcasts"]["list"]:
						replays.append((s["title"], s["length"], s["thumbnailUrl"], s["playbackUrl"]))

		return replays

	def following_live_streams(self, uname):
		self.refresh(uname)
		streams = []

		if not (self._info is None):
			for u in self._info["data"]["user"]["following"]["list"]:
				if u["livestream"] is not None:
					streams.append(
						(u["livestream"]["title"], 'https://live.prd.dlive.tv/hls/live/' + u["username"] + '.m3u8',
						 u["livestream"]["thumbnailUrl"], u["displayname"]))

		return streams

	def refresh(self, uname):
		client = graphql.GraphQLClient('https://graphigo.prd.dlive.tv/')

		if uname == "":
			uname = "winsomehax"

		result = client.execute('''
query {
    user(username: "''' + uname + '''")
    {
        following{
            totalCount
            list {
                displayname
                username
                livestream {
                    thumbnailUrl
                    title
                }
                pastBroadcasts {
                    list {
                        title
                        length
                        thumbnailUrl
                        playbackUrl
                    }
                }
            }
        }
    }
}

		''')

		#		result = client.execute('''
		#		query {
		#		    user(username: "winsomehax")
		#		    {
		#		        following{
		#		            totalCount
		#		            list {
		#		                displayname
		#		                username
		#		                livestream {
		#		                    thumbnailUrl
		#		                    title
		#		                }
		#		                pastBroadcasts {
		#		                    list {
		#		                        title
		#		                        length
		#		                        thumbnailUrl
		#		                        playbackUrl
		#		                    }
		#		                }
		#		            }
		#		        }
		#		    }
		#		}
		#
		#				''')

		if result["data"]["user"] == None:
			self._info = None
		else:
			self._info = result
		return result
