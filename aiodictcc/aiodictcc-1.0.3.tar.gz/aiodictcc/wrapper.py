import functools
import re
from typing import List, Tuple

from lxml import etree

import aiohttp
import asyncio

AVAILABLE_LANGUAGES = {
    "en": "english",
    "de": "german",
    "fr": "french",
    "sv": "swedish",
    "es": "spanish",
    "bg": "bulgarian",
    "ro": "romanian",
    "it": "italian",
    "pt": "portuguese",
    "ru": "russian",
    "is": "icelandic",
    "hu": "hungarian",
    "la": "latin",
    "nl": "dutch",
    "sk": "slovakian",
    "hr": "croatian",
    "no": "norwegian",
    "cs": "czech",
    "fi": "finnish",
    "tr": "turkish",
    "da": "danish",
    "pl": "polish",
    "el": "greek",
    "sr": "serbian",
    "eo": "esperanto",
}

BASE_URL = "https://{subdomain}.dict.cc/?s={search}"


class UnavailableLanguageError(ValueError):
    """Thrown if a language is not supported."""


class Translate:
    @staticmethod
    def _filter(content):
        """Filter the parsed content by sanitizing and searching for `c1Arr` and `c2Arr`."""

        def sanitize(word):
            return re.sub("[\\\\\"]", "", word)

        match_pattern = "\"[^,]+\""
        in_list = []
        out_list = []

        for line in content.split("\\n"):
            if "var c1Arr" in line:
                in_list = map(sanitize, re.findall(match_pattern, line))
            elif "var c2Arr" in line:
                out_list = map(sanitize, re.findall(match_pattern, line))
        return zip(out_list, in_list)

    @staticmethod
    async def _make_request(request_url):
        """Internal function to request a page by using a given string"""
        session = aiohttp.ClientSession(
            headers={'User-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36'
                                   ' (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
        )

        async with session.get(request_url) as req:
            assert isinstance(req, aiohttp.ClientResponse)

            return await req.read()

    @staticmethod
    def _parse_page(content):
        """
        Internal function to parse a page by matching the xpath.
        """
        if content:
            data = etree.HTML(content)
            # Let's hope this doesn't break.
            _root = data.xpath('//*[@id="maincontent"]/script[2]/text()')
            return str(_root)

    @classmethod
    async def get_translation(cls, word: str, from_lang: str, to_lang: str) -> List[Tuple[str, str]]:
        """
        Requests a translation.
        Returns a list of tuples.
        """

        for unsupported_language in [l for l in [from_lang, to_lang] if l not in AVAILABLE_LANGUAGES.keys()]:
            raise UnavailableLanguageError("{} is not a supported language!".format(unsupported_language))

        subdomain = from_lang.lower() + to_lang.lower()

        req_url = BASE_URL.format(subdomain=subdomain, search=word)
        response = await cls._make_request(request_url=req_url)

        parse_part = functools.partial(cls._parse_page, response)
        event = asyncio.get_event_loop()
        parsed = await event.run_in_executor(None, parse_part)

        zipped_translation = cls._filter(parsed)

        return list(zipped_translation)
