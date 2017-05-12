# from __future__ import unicode_literals

# try:
#     # Python 2.6-2.7 
#     from HTMLParser import HTMLParser
# except ImportError:
#     # Python 3
#     from html.parser import HTMLParser

# from googleapiclient.discovery import build

# from dojo.transform import SparkTransform


# class GoogleTranslationsTransform(SparkTransform):

#     OUTPUT = {
#         'fields': [
#             {'name': 'from_language', 'type': 'string'},
#             {'name': 'from_value', 'type': 'string'},
#             {'name': 'to_language', 'type': 'string'},
#             {'name': 'to_value', 'type': 'string'}
#         ]
#     }

#     MAX_SEGMENTS = 32

#     def process(self, inputs):
#         from_values = []
#         for name, df in inputs.items():
#             if name in self.config['fields']:
#                 fields = self.config['fields'][name]
#                 from_values += df.rdd\
#                                  .flatMap(lambda r: [r[k].lower().strip() for k in fields])\
#                                  .distinct()\
#                                  .collect()
#         from_values = list(sorted(set(from_values)))
#         rows = []
#         for chunk_from_values in self._chunks(from_values, self.MAX_SEGMENTS):
#             chunk_from_values = list(chunk_from_values)
#             service = build('translate', 'v2', developerKey=self.secrets['google_api_key'])
#             to_language = self.config.get('to_language', 'en')
#             resp = service.translations().list(target=to_language, q=chunk_from_values).execute()
#             for from_value, translation in zip(chunk_from_values, resp['translations']):
#                 rows.append({
#                     'from_language': translation['detectedSourceLanguage'].lower(),
#                     'from_value': from_value,
#                     'to_language': to_language,
#                     'to_value': HTMLParser().unescape(translation['translatedText']).lower()
#                 })
#         return rows

#     def _chunks(self, l, n):
#         for i in range(0, len(l), n):
#             yield l[i:i + n]
