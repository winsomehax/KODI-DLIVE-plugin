from requests import post
import json


"""
Data class - unsure if @dataclass is allowed in Kodi
"""
class LiveStream():

    def __init__(self, title, playURL, thumbURL, displayName):
        self.title = title
        self.playURL = playURL
        self.thumbURL = thumbURL
        self.displayName = displayName


"""
Data class - unsure if @dataclass is allowed in Kodi
"""
class ReplayStream():

    def __init__(self, title, playURL, thumbURL, length):
        self.title = title
        self.playURL = playURL
        self.thumbURL = thumbURL
        self.length = length


"""
Data class - unsure if @dataclass is allowed in Kodi
"""
class User():

    def __init__(self, displayName, user_id):
        self.displayName = displayName
        self.user_id = user_id


"""
Query class for DLIVE - funnel all 
"""
class Query():

    def __init__(self):
        self.endpoint = 'https://graphigo.prd.dlive.tv/'
        self.token = None
        self.headername = None
        self.user_id = ""
        self.display_name = ""
        self.validated_user_id = False

    def __execute(self, query, variables=None):
        return self.__send(query, variables)

    def __inject_token(self, token, headername='Authorization'):
        self.token = token
        self.headername = headername

    def __send(self, query, variables):
        data = {'query': query, 'variables': variables}
        headers = {'Accept': 'application/json',
                   'Content-Type': 'application/json'}

        if self.token is not None:
            headers[self.headername] = '{}'.format(self.token)

        #        response = request("POST", url, data=payload)
        req = post(self.endpoint, data=json.dumps(
            data).encode('utf-8'), headers=headers)
        j = req.json()
        return j

    """
    Given a dlive.tv display name, function makes a call to the API and returns the blockchain user_id (which never changes)
    or None
    """

    def set_user_id(self, display_name):

        result = self.__execute(
            '''query { userByDisplayName ( displayname: "'''+display_name+'''") { username } }''')

        m = result["data"]["userByDisplayName"]

        if m is None:
            self.validated_user_id = False
            self.user_id = ""
            self.display_name = ""
            return False

        self.user_id = m["username"]
        self.display_name = display_name
        self.validated_user_id = True
        return True

    """
    Returns the graphql structure from dlive given the blockchain user id. The returned structure contains livestreams,
    past broadcasts and who the person is following.
    """

    def __get_user_info(self, user_id):

        print ("USER ID: ", user_id)
        result = self.__execute(
            ''' query { user(username: "''' + user_id + '''") { following { totalCount list { displayname username 
            livestream { thumbnailUrl title } pastBroadcasts { list { title length thumbnailUrl playbackUrl } } } } } 
            } ''')

        if result["data"]["user"] is None:
            result = None

        return result

    """
    Returns all the live streams after a certain point
    """

    def __get_all_live_streams_after(self, after):

        result = self.__execute(
            '''query { livestreams (input: {showNSFW: true, order: TRENDING, after: "'''+after+'''"}) { pageInfo { startCursor, endCursor, 
            hasNextPage, hasPreviousPage} list { id, permlink, ageRestriction, thumbnailUrl, disableAlert, title, 
            createdAt, totalReward, watchingCount, creator {username, displayname}, view } } }''')

        return result

    """
    Returns a list of all the extant live streams on DLIVE - by making multiple calls if necessary
    """

    def get_all_live_streams(self):
        result = []

        after_cursor = "0"
        next_page = True

        while next_page:
            r = self.__get_all_live_streams_after(after_cursor)
            next_page = r["data"]["livestreams"]["pageInfo"]["hasNextPage"]
            after_cursor = r["data"]["livestreams"]["pageInfo"]["endCursor"]

            for u in r["data"]["livestreams"]["list"]:
                record = LiveStream(title=u["title"],
                                    playURL='https://live.prd.dlive.tv/hls/live/' +
                                    u["creator"]["username"] + '.m3u8',
                                    thumbURL=u["thumbnailUrl"],
                                    displayName=u["creator"]["displayname"])

                result.append(record)

        return result

    """
    Get the graphql information for user (A) and then parse it into a list of that (A) is following and are
    currently live
    """

    def get_following_live_streams(self):

        user_info = self.__get_user_info(self.user_id)

        result = []

        print ("***************** ", str(user_info))

        for stream in user_info["data"]["user"]["following"]["list"]:
            if stream["livestream"] is not None:
                record = LiveStream(title=stream["livestream"]["title"],
                                    playURL='https://live.prd.dlive.tv/hls/live/' +
                                    stream["username"] + '.m3u8',
                                    thumbURL=stream["livestream"]["thumbnailUrl"],
                                    displayName=stream["displayname"])

                result.append(record)

        return result

    """
    Returns a list of users (blockchain id and display_name) that the user is following.
    """

    def get_following(self):
        r = self.__get_user_info(self.user_id)

        result = []

        for u in r["data"]["user"]["following"]["list"]:
            record = User(displayName=u["displayname"],
                          user_id=u["username"])
            result.append(record)

        return result

    """
    """

    def get_replays(self, username):
        r = self.__get_user_info(self.user_id)
        result = []

        for u in r["data"]["user"]["following"]["list"]:
            if username == u["username"]:
                for s in u["pastBroadcasts"]["list"]:
                    record = ReplayStream(
                        title=s["title"], playURL=s["playbackUrl"], thumbURL=s["thumbnailUrl"], length=s["length"])
                    result.append(record)

        return result
