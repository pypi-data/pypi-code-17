# -*- coding: utf-8 -*-
from uploader import CKANUploader
from models import Dataset, Distribution
import arrow


# cu = CKANUploader(ckan_url='http://localhost:5000', ckan_api_key='a6c204e7-0cdb-4326-92ba-e5be14c1d7c2')
# cu = CKANUploader(ckan_url='http://localhost:5000', ckan_api_key='b110b824-dd96-46f0-b25c-bed1fc21bcfa')
cu = CKANUploader(ckan_url='http://demo.ckan.org', ckan_api_key='c381dae0-fe59-48ee-b543-a240e0087dfa')

dist = {
    "state": 'active',
    "license_id": 'abc',
    "description": 'Description con muchas Ñññññ',
    "url": 'http://181.209.63.71/dataset/6897d435-8084-4685-b8ce-304b190755e4/resource/6145bf1c-a2fb-4bb5-b090-bb25f8419198/download/estructura-organica-3.csv',
    "name": 'Test At: n{}hrs.'.format(arrow.now().format('HH:mm'))}

dataset = {"license_title": "Creative Commons Attribution",
           "maintainer": "Jose A. Salgado(M)",
           "private": False,
           "maintainer_email": "jose.salgado.wrk@gmail.com",
           "id": "",
           "owner_org": "99920e14-6146-4cd1-8e57-d9d8c3b3190b",
           "author": "Jose A. Salgado",
           "author_email": "jose.salgad.wrk@gmail.com",
           "state": "active",
           "license_id": "cc-by",
           "type": "dataset",
           "groups": [],
           "name": "",
           "isopen": True,
           "url": "",
           "notes": "Dataset de prueba para testear la colocacion de puntos sobre un mapa de la IGN",
           "title": "Rocket Science",
           "license_url": "http://www.opendefinition.org/licenses/cc-by"}
d = Distribution(datadict=dist)
my_dataset = Dataset(datadict=dataset, _distributions=d)
if cu.save(my_dataset,
           only_metadata=True,
           _views=True):
    print "Dataset salvado con exito!!"
else:
    print "Oops... algo se rompio..."

