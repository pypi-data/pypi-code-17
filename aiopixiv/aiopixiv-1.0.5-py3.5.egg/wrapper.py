"""
Wrapper module

This module provides the API abstraction.
"""

import json
import logging

import aiohttp
from asyncio import AbstractEventLoop

import asyncio


class PixivError(Exception):
    """
    The base exception type.
    """


class PixivAuthFailed(PixivError):
    """
    Created when authentication failed.
    """


class BaseAPI(object):
    """
    Contains the base API object shared by the auth-required API and the public access API.

    :ivar sess: The :class:`aiohttp.ClientSession` used to make all HTTP requests.
        This is automatically closed at the end of the API's lifetime.

    :ivar access_token: The current OAuth2 access token used for making API requests.
    :ivar refresh_token: The refresh token used to get a new OAuth2 access token.
    :ivar user: The current user object associated with this API, if it is logged in.
    """

    def __init__(self, loop: AbstractEventLoop = None):
        self.access_token = None
        self.refresh_token = None

        self.user = None

        self.logger = logging.getLogger("aiopixiv")

        self.loop = loop
        if self.loop is None:
            self.loop = asyncio.get_event_loop()

        self.sess = aiohttp.ClientSession(loop=self.loop)

    async def _authenticate(self, username: str = None, password: str = None):
        """
        Authenticates with the Pixiv API.
        This will setup OAuth access.

        You should not use this method directly.

        :param username: The username to login with.
        :param password: The password to login with.
        """

        url = 'https://oauth.secure.pixiv.net/auth/token'

        oauth2_headers = {
            'App-OS': 'ios',
            'App-OS-Version': '9.3.3',
            'App-Version': '6.0.9',
            'User-Agent': 'PixivIOSApp/6.0.9 (iOS 9.3.3; iPhone8,1)',
        }

        # iOS app client ID/secret
        data = {
            'get_secure_url': 1,
            'client_id': 'bYGKuGVw91e0NMfPGp44euvGt59s',
            'client_secret': 'HP3RmkgAmEGro0gn1x9ioawQE8WMfvLXDz3ZqxpK',
        }
        if username is not None and password is not None:
            # Basic auth, use the password to login.
            self.logger.info("Logging into Pixiv with password auth")
            data['grant_type'] = 'password'
            data['username'] = username
            data['password'] = password

            self.__cached_login_info = {"username": username, "password": password}
        else:
            # Refresh OAuth2.
            self.logger.info("Refreshing OAuth token")
            data['grant_type'] = 'refresh_token'
            data['refresh_token'] = self.refresh_token

        # Call the token URL to get a new access token.
        async with self.sess.post(url, headers=oauth2_headers, data=data) as r:
            body = await r.text()
            if r.status not in [200, 301, 302]:
                d = await r.json()
                try:
                    if d["errors"]["system"]["code"] == 1508:
                        # invalid refresh token.
                        # login with the new password
                        await self._authenticate(**self.__cached_login_info)
                        return
                except KeyError:
                    pass

                raise PixivAuthFailed(await r.text())

            # Decode as JSON.
            data = json.loads(body)
            self.access_token = data["response"]["access_token"]
            self.user = data["response"]["user"]
            self.logger.info("Logged in as {}".format(self.user["id"]))
            self.refresh_token = data["response"]["refresh_token"]

    def __del__(self):
        self.sess.close()

    async def login(self, username: str, password: str):
        """
        Logs your account into Pixiv.

        This call is required at least once for API v5.

        :param username: Your account's username.
        :param password: Your account's password.
        """
        await self._authenticate(username, password)

    async def make_request(self, method: str, url: str, params: dict = None, data: dict = None, headers: dict = None,
                           hit_400=False):
        """
        Makes an authenticated request to pixiv.
        This will automatically retry if it hits a 400 by attempting to re-authorize with the refresh-token.

        This is an internal method, and should not be used by client code.

        :param method: The method to use.
        :param url: The URL to request.
        :param params: The parameters of the request.
        :param data: The body of the request.
        :param headers: The headers of the request.
        :param hit_400: Used in case a 400 UNAUTHORIZED was passed and we need to re-authorize.
        :return: A :class:`dict` containing the body, if appropriate.
        """
        # Run the request, but beware of 401s.
        if headers is None:
            headers = {}

        headers['Referer'] = 'http://spapi.pixiv.net/'
        headers['Authorization'] = 'Bearer %s' % self.access_token

        self.logger.info("{} {}".format(method, url))

        req = await self.sess.request(method, url, params=params, data=data, headers=headers)

        code = req.status
        try:
            d = json.loads(await req.text(encoding="utf-8"))
            if d.get("errors", {}).get("system", {}).get("message", "") == "The access token provided is invalid.":
                if hit_400:
                    # We already hit a 400, oh well.
                    raise PixivError(d)
                # Try again, with authentication.
                await self._authenticate()
                # Re-call the request.
                return await self.make_request(method, url, params, data, headers, True)
            elif code != 200:
                raise PixivError(await req.text())
            else:
                # Parse the body as JSON, and return it.
                return d
        finally:
            req.close()

    async def download_pixiv_image(self, image_url: str) -> bytes:
        """
        Downloads an image from Pixiv.

        Pixiv disables hotlinking or downloading the images directly without a Referer [sic] header with the correct
        location. This method automatically provides it.

        :param image_url: The image URL to get.
        :return: The bytes of the image.
        """
        headers = {
            "Referer": "http://spapi.pixiv.net/",
            "User-Agent": 'PixivIOSApp/6.0.9 (iOS 9.3.3; iPhone8,1)'
        }
        async with self.sess.get(image_url, headers=headers) as r:
            assert isinstance(r, aiohttp.ClientResponse)
            if r.status != 200:
                raise PixivError("Failed to download image {}".format(image_url))

            return await r.read()
