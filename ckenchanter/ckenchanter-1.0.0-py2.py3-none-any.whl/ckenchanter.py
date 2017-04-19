import enchant
import urlparse
import urllib
from enchant.checker import SpellChecker


class CKEnchanter(SpellChecker):
    def __init__(self, word_list_path=None):
        """
        Initialize a new CKEnchanter object
        """
        # If a word list was given, add it to the default dictionary
        if word_list_path:
            self.master_dict = enchant.DictWithPWL("en_US", word_list_path)
        else:
            self.master_dict = enchant.Dict("en_US")

        # Finish creating a pyenchant spellchecker
        SpellChecker.__init__(self, self.master_dict)

    def _get_data_val(self, data, key):
        """
        Get a key out of the data string
        """
        val = data.get(key, [])
        if len(val) > 0:
            return val[0]
        return ''

    def parse_ckeditor_request(self, request_data):
        """
        Parses a request from CKEdtior and prepares the appropriate response
        """
        # Break apart the query string
        data = urlparse.parse_qs(request_data)

        if self._get_data_val(data, 'cmd') == 'getbanner':
            # CKEditor banner response
            return {"banner": True}
        elif self._get_data_val(data, 'cmd') == 'get_lang_list':
            # CKEditor langList response
            return {
                "langList": {
                    "ltr": {
                        "en_US": "American English",
                    },
                    "rtl": {}
                },
                "verLang": 6
            }
        elif self._get_data_val(data, 'cmd') == 'check_spelling':
            # Ok, now we're actually checking the words
            text = urllib.unquote(self._get_data_val(data, 'text')).replace(',', ' ')
            return self.spellcheck(text)

        # For safety
        return {}

    def spellcheck(self, text):
        # Run the spellchecker
        self.set_text(text)

        errors = []
        for err in self:
            suggestions = self.master_dict.suggest(err.word)
            result = {
                'word': err.word,
                'ud': 'false',
                'suggestions': suggestions
            }
            errors.append(result)

        return errors
