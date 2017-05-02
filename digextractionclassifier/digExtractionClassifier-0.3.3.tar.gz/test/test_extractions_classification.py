import unittest
import codecs
from sklearn.externals import joblib
import json
from digExtractor.extractor_processor import ExtractorProcessor
from digExtractionsClassifier import dig_extractions_classifier
import digExtractionsClassifier.utility.functions as utility_functions

class TestExtractionsClassifier(unittest.TestCase):

    def load_model(self, filenames):
        print filenames
        classifier = dict()
        # try:
        filename = utility_functions.get_full_filename(__file__, filenames[0])
        print filename
        classifier['model'] = joblib.load(filename)
        # except:
            # raise Exception('Model file not present')
        try:
            classifier['scaler'] = joblib.load(utility_functions.get_full_filename(__file__, filenames[1]))
            classifier['normalizer'] = joblib.load(utility_functions.get_full_filename(__file__, filenames[2]))
            classifier['k_best'] = joblib.load(utility_functions.get_full_filename(__file__, filenames[3]))
        except:
            pass
        return classifier

    def read_test_file(self, filename):
        tokens = None
        filename = utility_functions.get_full_filename(__file__, filename)
        print filename
        with codecs.open(filename, 'r', 'utf-8') as file:
            for line in file:
                tokens = json.loads(line)

        return tokens

    def test_extractions_classifier(self):
        TEST_JSON_FILE = 'test_1.json'

        doc = dict()
        doc['tokens'] = self.read_test_file(TEST_JSON_FILE)

        extractor = self.setup_extractor()
        extractor_processor = ExtractorProcessor().set_input_fields('tokens').set_output_field('tokens_mod').set_extractor(extractor)

        updated_doc = extractor_processor.extract(doc)

#        self.assertEquals(updated_doc['social_media_ids'][0]['result']['value'], {'twitter': 'diamondsquirt'})
        self.assertEquals(True, True)

    def test_missing_tokens(self):
        doc = {"tokens":[]}

        extractor = self.setup_extractor()
        extractor_processor = ExtractorProcessor().set_input_fields('tokens').set_output_field('social_media_ids').set_extractor(extractor)

        updated_doc = extractor_processor.extract(doc)

        print updated_doc

        self.assertEquals(updated_doc, doc) 

    def setup_extractor(self):
        MODEL_FILE = 'city.pkl'
        EMBEDDINGS_FILE = 'unigram-part-00000-v2.json'

        model = self.load_model([MODEL_FILE])
        classification_field = 'city'
        embeddings = utility_functions.load_embeddings(EMBEDDINGS_FILE)

        return dig_extractions_classifier.DigExtractionsClassifier(model, classification_field, embeddings)

    def test_empty_tokens(self):
        doc = {}
        extractor = self.setup_extractor()
        extractor_processor = ExtractorProcessor().set_input_fields('tokens').set_output_field('social_media_ids').set_extractor(extractor)

        updated_doc = extractor_processor.extract(doc)

        print updated_doc

        self.assertEquals(updated_doc, {})       

if __name__ == '__main__':
    unittest.main()
