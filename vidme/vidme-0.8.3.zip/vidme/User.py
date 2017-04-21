
import api
from Album import Album

class User:

	def __init__(self, username = "", **kwargs):
		if "username" in kwargs:
			self.username = kwargs['username']
		elif username:
			self.username = username
		else:
			self.username = ""

		if "user_id" in kwargs:
			self.user_id = kwargs['user_id']
		else:
			self.user_id = ""

		if 'meta' in kwargs:
			self.set_meta(kwargs['meta'])
		elif self.user_id or self.username:
			self.set_meta(self.retrieve_meta())

	def retrieve_meta(self):
		user = False

		if self.user_id:
			user = api.request('/user/' + str(self.user_id), method="GET")
		elif self.username:
			user = api.request('/userByUsername', method="GET", params=dict(
				username=self.username
			))

		return user

	def set_meta(self, meta):
		# Confirm meta is good
		self.meta = meta

		if 'user' in meta:
			user = meta['user']

			for key, value in user.items():
				# Add item to class
				setattr(self, key, value)
				# Add getter for item
				setattr(self, 'get_' + key, lambda v=value: v)

	def _retrieve_albums(self, limit=20, offset=0):
		user_id = self._get_safe('user_id')

		if user_id:
			albums = api.request('/user/' + user_id + '/albums', method='GET',
				params=dict(
					limit=limit,
					offset=offset,
				))

			if albums:
				return [
					Album(meta={'album': album}) for album in albums['albums']
				]
				return True
			else:
				return False
		else:
			return False

	def _yield_albums(self, limit, offset):
		self.albums = []

		while True:
			albums = self._retrieve_albums(limit, offset)
			if albums and len(albums) > 0:
				self.albums.extend(albums)
				offset += limit
				yield albums
			else:
				break

	def get_albums(self, refresh=False, limit=15, offset=0):
		albums = self._get_safe('albums')

		# If albums not found, try to retrieve them.
		if refresh or not albums:
			return self._yield_albums(limit, offset)

		albums = self._get_safe('albums')

		if albums:
			return albums
		else:
			return False

	def _get_safe(self, name):
		if hasattr(self, name):
			return getattr(self, name)
		else:
			return False

	def _api_call(self, session, action, args = {}):
		user_id = self._get_safe('user_id')

		args['token'] = session.get_token()

		if user_id:
			video_action = api.request('/user/' + user_id + '/' + action, data=args)

			if video_action:
				self.set_meta(video_action)
				return True
			else:
				return False
		return False

	def set_username(self, session, username):
		return self._api_call(session, 'edit', dict(username=username))

	def set_password(self, session, password, passwordCurrent):
		return self._api_call(session, 'edit', dict(password=password, passwordCurrent=passwordCurrent))

	def set_bio(self, session, bio):
		return self._api_call(session, 'edit', dict(bio=bio))

	def set_displayname(self, session, displayname):
		return self._api_call(session, 'edit', dict(displayname=displayname))

	def set_email(self, session, email):
		return self._api_call(session, 'edit', dict(email=email))

	def follow_user(self, session, user):
		return self._api_call(session, 'follow', dict(user=user.get_user_id()))

	def unfollow_user(self, session, user):
		return self._api_call(session, 'unfollow', dict(user=user.get_user_id()))

	def unsubscribe_user(self, session, user):
		return self._api_call(session, 'unsubscribe', dict(user=user.get_user_id()))

	def _retrieve_followers(self, limit=20, offset=0):
		user_id = self._get_safe('user_id')

		if user_id:
			followers = api.request('/user/' + user_id + "/followers", method="GET", params=dict(
					user=user_id,
					offset=offset,
					limit=limit,
				))

			if followers:
				return [
					User(meta={'user': follower}) for follower in followers['users']
				]
			else:
				return False
		else:
			return False

	def _yield_followers(self, limit, offset):
		self.followers = []

		while True:
			followers = self._retrieve_followers(limit, offset)
			if followers and len(followers) > 0:
				self.followers.extend(followers)
				offset += limit
				yield followers
			else:
				break

	def get_followers(self, refresh=False, limit=15, offset=0):
		followers = self._get_safe('followers')

		# If followers not found, try to retrieve them.
		if refresh or not followers:
			return self._yield_followers(limit, offset)

		followers = self._get_safe('followers')

		if followers:
			return followers
		else:
			return False

	def _retrieve_following(self, limit=20, offset=0):
		user_id = self._get_safe('user_id')

		if user_id:
			following = api.request('/user/' + user_id + "/following", method="GET", params=dict(
					user=user_id,
					offset=offset,
					limit=limit,
				))

			if following:
				return [
					User(meta={'user': following}) for following in following['users']
				]
			else:
				return False
		else:
			return False

	def _yield_following(self, limit, offset):
		self.following = []

		while True:
			following = self._retrieve_following(limit, offset)
			if following and len(following) > 0:
				self.following.extend(following)
				offset += limit
				yield following
			else:
				break

	def get_following(self, refresh=False, limit=15, offset=0):
		following = self._get_safe('following')

		# If following not found, try to retrieve them.
		if refresh or not following:
			return self._yield_following(limit, offset)

		following = self._get_safe('following')

		if following:
			return following
		else:
			return False

	def is_following(self, ouser):
		user_id = self._get_safe('user_id')

		if user_id:
			request = api.request('/user/' + user_id + '/follow', method="GET", params=dict(
				otherUser=ouser.get_user_id()
			))

			if request:
				return request['isFollowing']
			else:
				return False
		else:
			return False

	def is_blocked(self, ouser):
		user_id = self._get_safe('user_id')

		if user_id:
			request = api.request(
				'/user/' + user_id + '/block/' + ouser.get_user_id(),
				method="GET"
			)

			if request:
				return request['blocked']
			else:
				return False
		else:
			return False

	def _retrieve_videos(self, limit=20, offset=0, session=None, order=None, private=0):
		from Video import Video
		
		user_id = self._get_safe('user_id')

		token = None

		if session:
			token = session.get_token()

		if user_id:
			videos = api.request('/videos/list', method="GET", params=dict(
					private=private,
					order=order,
					token=token,
					offset=offset,
					limit=limit,
					user=user_id
				))

			if videos:
				return [
					Video(meta={'video': video}) for video in videos['videos']
				]
			else:
				return False
		else:
			return False

	def _yield_videos(self, limit, offset, session=None, order=None, private=0):
		self.videos = []

		while True:
			videos = self._retrieve_videos(limit, offset, session, order, private)
			if videos and len(videos) > 0:
				self.videos.extend(videos)
				offset += limit
				yield videos
			else:
				break
	def get_videos(self, refresh=False, limit=15, offset=0, session=None, order="video_id", private=0):
		videos = self._get_safe('videos')

		# If videos not found, try to retrieve them.
		if refresh or not videos:
			return self._yield_videos(limit, offset)

		videos = self._get_safe('videos')

		if videos:
			return videos
		else:
			return False
