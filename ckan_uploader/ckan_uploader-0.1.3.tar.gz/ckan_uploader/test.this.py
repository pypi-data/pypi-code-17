# -*- coding: utf-8 -*-
from ckan_uploader import CKANUploader

cu = CKANUploader(ckan_url='http://localhost:5000', ckan_api_key='b110b824-dd96-46f0-b25c-bed1fc21bcfa')
# cu = CKANUploader(ckan_url='http://demo.ckan.org', ckan_api_key='c381dae0-fe59-48ee-b543-a240e0087dfa')

print cu.exists(id_or_name='example-upload', search_for_datasets=False)
print cu.get_resource_id('Example Upload.')
