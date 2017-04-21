
import api

class Album:

	def __init__(self, album_id = "", meta = ""):
		self.album_id = album_id

		if meta:
			self.set_meta(meta)
		elif album_id:
			self.set_meta(self.retrieve_meta())

		self.videos = []

	def retrieve_meta(self):
		album = False

		if self.album_id:
			album = api.request('/album/' + str(self.album_id), method="GET")

		return album

	def set_meta(self, meta):
		# Confirm meta is good
		self.meta = meta

		if 'album' in meta:
			album = meta['album']

			for key, value in album.items():
				# Add item to class
				setattr(self, key, value)
				# Add getter for item
				setattr(self, 'get_' + key, lambda v=value: v)

	def _get_safe(self, name):
		if hasattr(self, name):
			return getattr(self, name)
		else:
			return False

	def _api_call(self, session, action, args = {}):
		album_id = self._get_safe('album_id')

		args['token'] = session.get_token()

		if album_id:
			video_action = api.request('/album/' + album_id + '/' + action, data=args)

			if video_action:
				self.set_meta(video_action)
				return True
			else:
				return False
		return False

	def set_title(self, session, title):
		return self._api_call(session, 'edit', dict(title=title))

	def set_description(self, session, description):
		return self._api_call(session, 'edit', dict(description=description))

	def set_url(self, session, url):
		return self._api_call(session, 'edit', dict(url=url))

	def add_video(self, session, video_id):
		album_id = self._get_safe('album_id')

		if album_id:
			video_action = api.request('/album/' + album_id + '/video/' + video_id, params=dict(
				token=session.get_token()
			))

			if video_action:
				from Video import Video
				self.videos.append(Video(video_id=video_action['albumVideo']['video_id']))
				return True
			else:
				return False
		return False

	def delete(self, session):
		album_id = self._get_safe('album_id')

		if album_id:
			video_action = api.request('/album/' + album_id, params=dict(
				token=session.get_token()
			), method='DELETE')

			if video_action:
				return True
			else:
				return False
		return False

	def create(self, session, title, description = "", url = ""):
		video_action = api.request('/album', data=dict(
			title=title,
			description=description,
			url=url,
			token=session.get_token()
		))

		if video_action:
			self.set_meta(video_action)
			return True
		else:
			return False
