"""
Contains the V5 API wrapper.
"""

import typing

from aiopixiv.wrapper import BaseAPI


class PixivAPIv5(BaseAPI):
    """
    Methods for API v5.

    v5 is an authenticated API, and requires auth for all endpoints. It is also superior to v6.
    """
    BASE_URL = "https://public-api.secure.pixiv.net/v1"
    WORKS_URL = BASE_URL + "/works/{}.json"
    USER_URL = BASE_URL + "/users/{}.json"

    LATEST_WORKS_URL = BASE_URL + "/works.json"

    RANKING_URL = BASE_URL + "/ranking/{}.json"

    USER_FEEDS_URL = BASE_URL + "/users/{}/feeds.json"
    USER_WORKS_URL = BASE_URL + "/users/{}/works.json"

    # Specific URLs for ourselves.

    ME_URL = BASE_URL + "/me"
    ME_FEEDS_URL = ME_URL + "/feeds.json"
    ME_FAVOURITES_URL = ME_URL + "/favorite_works.json"
    ME_FOLLOWING_URL = ME_URL + "/following.json"
    ME_FAVOURITE_USERS_URL = ME_URL + "/favorite-users.json"

    async def make_request(self, method: str, url: str, params: dict = None, data: dict = None,
                           headers: dict = None,
                           hit_400=False):
        if headers is None:
            headers = {}

        headers['User-Agent'] = 'PixivIOSApp/5.8.7'
        return await super().make_request(method, url, params, data, headers, hit_400)

    async def get_work_information(self, work_id: int):
        """
        Gets information about a piece of work.

        :param work_id: The ID of the work.
        :return: A dict containing the information.
        """
        url = self.WORKS_URL.format(work_id)
        params = {
            'image_sizes': 'px_128x128,small,medium,large,px_480mw',
            'include_stats': 'true',
        }

        return await self.make_request("GET", url, params=params)

    async def get_user_information(self, user_id: int):
        """
        Gets information about a user.

        :param user_id: The ID of the user.
        :return: A dict containing the information.
        """

        url = self.USER_URL.format(user_id)
        params = {
            'profile_image_sizes': 'px_170x170,px_50x50',
            'image_sizes': 'px_128x128,small,medium,large,px_480mw',
            'include_stats': "1",
            'include_profile': "1",
            'include_workspace': "1",
            'include_contacts': "1",
        }
        return await self.make_request("GET", url, params=params)

    # Self-requests.
    async def get_my_feeds(self, *, show_r18: bool = True, max_id=None):
        """
        Gets the list of your current feeds.

        :param show_r18: Should R-18 content be shown?
        :param max_id: Unknown.
        :return: A dict, containing your feeds.
        """
        params = {
            'relation': 'all',
            'type': 'touch_nottext',
            'show_r18': "1" if show_r18 else "0",
        }
        if max_id:
            params["max_id"] = str(max_id)

        return await self.make_request("GET", self.ME_FEEDS_URL, params=params)

    async def get_my_favourites(self, *, page: int = 1, per_page: int = 50,
                                publicity: str = "public",
                                image_sizes: typing.Iterable = ('px_128x128', 'px_480mw', 'large')):
        """
        Gets the list of your favourites.

        :param page: The page of favourites to fetch.
        :param per_page: The number of favourites per page to return.
        :param publicity: Which type of favourites should be returned ("public" or "private")
        :param image_sizes: An iterable of valid image sizes to return.
        :return: A dict, containing your favourites.
        """
        params = {
            'page': str(page),
            'per_page': str(per_page),
            'publicity': publicity,
            'image_sizes': ','.join(image_sizes),
        }
        return await self.make_request("GET", self.ME_FAVOURITES_URL, params=params)

    async def add_favourite(self, work_id: int, *, publicity: str = "public"):
        """
        Adds a favourite to your list of favourites.
        Unfortunately, this only supports adding one favourite per call.

        :param work_id: The work ID to add.
        :param publicity: The publicity ("public" or "private").
        """
        params = {
            'work_id': str(work_id),
            'publicity': publicity,
        }
        return await self.make_request("POST", self.ME_FAVOURITES_URL, params=params)

    async def delete_favourite(self, *ids, publicity="public"):
        """
        Deletes a favourite from your list of favourites.
        This allows passing in multiple IDs to delete multiple at a time.

        :param ids: The IDs of the works to delete.
        :param publicity: The publicity ("public" or "private).
        """
        params = {
            'publicity': publicity
        }
        if len(ids) == 1:
            params["ids"] = str(ids[0])
        else:
            params["ids"] = ",".join(map(str, ids))

        return await self.make_request("DELETE", self.ME_FAVOURITES_URL, params=params)

    async def get_my_following_works(self, *, page: int = 1, per_page: int = 30,
                                     image_sizes=('px_128x128', 'px_480mw', 'large')):
        """
        Gets a list of works from the artists you follow.

        :param page: The page of works to return.
        :param per_page: The number of items per page.
        :param image_sizes: An iterable of valid image sizes.
        :return: A list containing Work objects.
        """
        params = {
            'page': str(page),
            'per_page': str(per_page),
            'image_sizes': ','.join(image_sizes),
            'include_stats': "true",
            'include_sanity_level': "true",
        }

        return await self.make_request("GET", self.ME_FOLLOWING_URL, params=params)

    async def follow_user(self, user_id: int, *, publicity: str = "public"):
        """
        Follows a user.

        :param user_id: The user ID of the user you wish to follow.
        :param publicity: The publicity of the follow.
        """
        params = {
            'target_user_id': str(user_id),
            'publicity': publicity
        }

        return await self.make_request("POST", self.ME_FAVOURITE_USERS_URL, params=params)

    async def unfollow_user(self, *ids, publicity: str = "public"):
        """
        Unfollows a user.

        :param ids: An iterable of user IDs to unfollow.
        :param publicity: The publicity of the follow.
        """
        params = {
            'publicity': publicity
        }

        if len(ids) == 1:
            params['delete_ids'] = str(ids[0])
        else:
            params['delete_ids'] = ','.join(map(str, ids))

        return await self.make_request("DELETE", self.ME_FAVOURITE_USERS_URL, params=params)

    async def get_user_works(self, user_id: int, *, page: int = 1, per_page=30,
                             image_sizes=('px_128x128', 'px_480mw', 'large')):
        """
        Gets the list of works for a user.

        :param user_id: The user ID to find the works for.
        :param page: The page of works to fetch.
        :param per_page: The number of works per page to fetch.
        :param image_sizes: The valid image sizes.
        """
        url = self.USER_WORKS_URL.format(user_id)
        params = {
            'page': page,
            'per_page': per_page,
            'include_stats': "true",
            'include_sanity_level': "true",
            'image_sizes': ','.join(image_sizes),
        }

        return await self.make_request("GET", url, params=params)

    async def get_user_feeds(self, user_id: int, *, show_r18: bool = True,
                             max_id: int = None):
        """
        Gets the list of feeds for a user.

        :param user_id: The user ID to get the feeds for.
        :param show_r18: If R-18 content is included or not.
        :param max_id: Unknown.
        """
        url = self.USER_FEEDS_URL.format(user_id)
        params = {
            "show_r18": "1" if show_r18 else "0",
            "relation": "all",
            "type": "touch_nottext"
        }

        return await self.make_request("GET", url, params=params)

    # Non-specific user actions.

    async def search_works(self, query, *, page=1, per_page=30, mode='text',
                           period='all', order='desc', sort='date',
                           types=('illustration', 'manga', 'ugoira')):
        """
        Searches Pixiv for works matching the given query.

        :param query: The query or tags to search for.
        :param page: The page of results to return.
        :param per_page: The number of items to return per page of results.
        :param mode: Unknown.
        :param period: The period of time in which to search.
        :param order: The sorting order of the results, by date.
        :param sort: How the results are sorted. Possible values are unknown.
        :param types: What types can be returned. 
            Valid items are: ('illustration', 'manga', 'ugoira')
        :return: A dict, containing an `illustrations`` key which has a list of Illustration objects.
        """
        url = 'https://public-api.secure.pixiv.net/v1/search/works.json'
        params = {
            'q': query,
            'page': str(page),
            'per_page': str(per_page),
            'period': period,
            'order': order,
            'sort': sort,
            'mode': mode,
            'types': ','.join(types),
            'include_stats': "true",
            'include_sanity_level': "true",
            'image_sizes': ','.join(['px_128x128', 'px_480mw', 'large']),
        }
        return await self.make_request("GET", url, params=params)

    async def get_rankings(self, ranking_type: str = 'all', *, mode: str = 'daily',
                           page: int = 1, per_page: int = 50, date: str = None):
        """
        Gets the current works rankings for the specified types of items.

        :param ranking_type: The type to fetch.
            Valid types: [all, illust, manga, ugoira]

        :param mode: The mode to call with.
           for 'illust' & 'manga': [daily, weekly, monthly, rookie, daily_r18, weekly_r18, r18g]
           for 'ugoira': [daily, weekly, daily_r18, weekly_r18],

        :param page: The page of results to fetch.
        :param per_page: The number of results per page.
        :param date: The date (in ISO format) to return rankings from.
        """
        url = self.RANKING_URL.format(ranking_type)
        params = {
            'mode': mode,
            'page': str(page),
            'per_page': str(per_page),
            'include_stats': "true",
            'include_sanity_level': "true",
            'image_sizes': ','.join(['px_128x128', 'px_480mw', 'large']),
            'profile_image_sizes': ','.join(['px_170x170', 'px_50x50']),
        }
        if date:
            params["date"] = date

        i = await self.make_request("GET", url, params=params)

        # unfuck the response
        r = {
            "response": i["response"][0]["works"]
        }
        return r

    async def get_latest_works(self, *, page=1, per_page=30):
        """
        Gets the latest works.

        :param page: The page of results to return.
        :param per_page: The number of items per page.
        """
        params = {
            'page': str(page),
            'per_page': str(per_page),
            'include_stats': "true",
            'include_sanity_level': "true",
            'image_sizes': ','.join(['px_128x128', 'px_480mw', 'large']),
            'profile_image_sizes': ','.join(['px_170x170', 'px_50x50']),
        }
        return await self.make_request("GET", url=self.LATEST_WORKS_URL, params=params)
