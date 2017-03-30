# -*- coding: utf-8 -*-
__author__ = u'Дмитрий'

from planfix import Planfix
from xml.dom.minidom import Document
import copy


p = Planfix('5d6af0896555cd47356c2c2afa6884e9', 'hunterhelp', '9efef835200ac9673e41fb9b79126e17')
p.auth("arsenal", "lema420821")
contact = {
    "email": "develop@hunterhelp.ru",
    "name": u"Develop",
    "lastName": u'Undevelop'
}
#contact_data = p.contact.add(contact)
#update_data = {
#    "post": "Developer",
#    "id": contact_data['contact']['id']
#}
#print p.contact.update(update_data)


print p.contact.get({
    "general": 1789999
})