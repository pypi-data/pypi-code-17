import asyncio

import aiohttp


class Jisho:
    """The class that makes the API requests. A class is necessary to safely
    handle the aiohttp ClientSession."""
    api_url = 'http://jisho.org/api/v1/search/words'

    def __init__(self):
        self.loop = asyncio.get_event_loop()
        self.session = aiohttp.ClientSession(loop=self.loop)

    def __del__(self):
        self.session.close()

    async def lookup(self, word, **kwargs):
        """Search Jisho.org for a word. Returns a list of dicts with keys
        readings, words, english, parts_of_speech."""
        params = {'keyword': word}
        params.update(kwargs)
        async with self.session.get(self.api_url, params=params) as resp:
            response = (await resp.json())['data']

        results = []

        for data in response:
            readings = []
            words = []

            for kanji in data['japanese']:
                reading = kanji.get('reading')
                if reading:
                    readings.append(reading)

                word = kanji.get('word')
                if word and word not in words:
                    words.append(kanji['word'])

            senses = {'english': [], 'parts_of_speech': []}

            for sense in data['senses']:
                senses['english'].extend(sense['english_definitions'])
                senses['parts_of_speech'].extend(sense['parts_of_speech'])

            try:
                senses['parts_of_speech'].remove('Wikipedia defintition')
            except ValueError:
                pass

            result = {'readings': readings, 'words': words}
            result.update(senses)
            results.append(result)

        return results
