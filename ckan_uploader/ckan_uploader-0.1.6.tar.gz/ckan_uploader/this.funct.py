import responses
from ckan_uploader.ckan_uploader import CKANUploader
import json
from os import path
from ckan_uploader.models import Dataset

here = path.dirname(path.abspath(__file__))
CKAN_APIKEY = 'b110b824-dd96-46f0-b25c-bed1fc21bcfa'
CKAN_HOST = 'http://localhost:5000'

EXAMPLE_DATASET = json.load(open(path.join(here, 'testing_data/dataset.ok.json')))
EXAMPLE_BAD_DATASET = json.load(open(path.join(here, 'testing_data/dataset.fail.json')))
DISTRIBUTION_OK = json.load(open(path.join(here, 'testing_data/distribution.ok.json')))

my_mock_responses = {
    'package_list':
        {
            'case1': json.dumps(json.load(open(path.join(here, 'testing_data/package_list-case1.json'))))
        },
    'package_show':
        {
            'case1': json.dumps(json.load(open(path.join(here, 'testing_data/package_show-case1.json'))))
        },
    'package_search':
        {
            'case1': json.dumps(json.load(open(path.join(here, 'testing_data/package_search-case1.json'))))
        }
}

# Preparo mock de CKAN-response: package_list.
responses.add(**{
    'method': responses.POST,
    'url': 'http://localhost:5000/api/action/package_list',
    'body': my_mock_responses['package_list']['case1'],
    'content_type': 'application/json'

})
# Preparo mock de CKAN-response: package_show.
responses.add(**{
    'method': responses.POST,
    'url': 'http://localhost:5000/api/action/package_show',
    'body': my_mock_responses['package_show']['case1'],
    'content_type': 'application/json'
})
cl = CKANUploader(CKAN_HOST, CKAN_APIKEY)
print cl.exists('mi-recurso-del-ejemplo', search_for_datasets=False, _fformat='JPG')