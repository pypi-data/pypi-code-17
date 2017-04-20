
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

	def _retrieve_albums(self):
		user_id = self._get_safe('user_id')

		if user_id:
			albums = api.request('/user/' + user_id + '/albums', method='GET')

			if albums:
				self.albums = [
					Album(meta={'album': album}) for album in albums['albums']
				]
				return True
			else:
				return False
		else:
			return False

	def get_albums(self):
		albums = self._get_safe('albums')

		# If albums not found, try to retrieve them.
		if not albums: self._retrieve_albums()

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

	def get_followers(self, offset = 0, hard = False):
		hasGotten = self._get_safe('followers')

		if hasGotten and not hard and offset == 0:
			return hasGotten
		else:
			user_id = self._get_safe('user_id')

			if user_id:
				followers = api.request('/user/' + user_id + "/followers", method="GET", params=dict(
					user=user_id,
					offset=offset
				))

				if followers:
					self.followers = [User(meta={'user': follower}) for follower in followers['users']]
					return self.followers
				else:
					return False
			else:
				return False

	def get_following(self, offset = 0, hard = False):
		hasGotten = self._get_safe('followers')

		if hasGotten and not hard and offset == 0:
			return hasGotten
		else:
			user_id = self._get_safe('user_id')

			if user_id:
				followers = api.request('/user/' + user_id + "/following", method="GET", params=dict(
					user=user_id,
					offset=offset
				))

				if followers:
					self.followers = [User(meta={'user': follower}) for follower in followers['users']]
					return self.followers
				else:
					return False
			else:
				return False

	def is_following(self, other_username):
		user_id = self._get_safe('user_id')

		if user_id:
			request = api.request('/user/' + user_id + '/follow', method="GET", params=dict(
				otherUser=other_username.get_user_id()
			))

			if request:
				return request['isFollowing']
			else:
				return False
		else:
			return False

	def is_blocked(self, other_username):
		user_id = self._get_safe('user_id')

		if user_id:
			request = api.request(
				'/user/' + user_id + '/block/' + other_username.get_user_id(),
				method="GET"
			)

			if request:
				return request['blocked']
			else:
				return False
		else:
			return False

	def get_videos(self, session=None, order="video_id", limit=0, private=0, offset=0, hard=False):
		hasGotten = self._get_safe('user_videos')

		if hasGotten and not hard and offset == 0:
			return hasGotten
		else:
			user_id = self._get_safe('user_id')

			if user_id:
				token = None
				if session:
					token = session.get_token()

				videos = api.request('/videos/list', method="GET", params=dict(
					private=private,
					order=order,
					token=token,
					offset=offset,
					limit=limit,
					user=user_id
				))

				if videos:
					from Video import Video

					self.user_videos = [Video(meta={'video': video}) for video in videos['videos']]
					return self.user_videos
				else:
					return False
			else:
				return False
