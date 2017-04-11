# -*- coding: utf-8 -*-
# Copyright 2016 LasLabs Inc.
# License MIT (https://opensource.org/licenses/MIT).

""" This library allows you to interact with a remote Red October Instance using Python.

Red October is a cryptographically-secure implementation of the two-person rule to
protect sensitive data. From a technical perspective, Red October is a software-based
encryption and decryption server. The server can be used to encrypt a payload in such
a way that no one individual can decrypt it. The encryption of the payload is
cryptographically tied to the credentials of the authorized users.

Authorized persons can delegate their credentials to the server for a period of time.
The server can decrypt any previously-encrypted payloads as long as the appropriate number
of people have delegated their credentials to the server.

This architecture allows Red October to act as a convenient decryption service. Other
systems, including CloudFlare’s build system, can use it for decryption and users can
delegate their credentials to the server via a simple web interface. All communication
with Red October is encrypted with TLS, ensuring that passwords are not sent in the clear.

* `Read more on the CloudFlare blog
  <https://blog.cloudflare.com/red-october-cloudflares-open-source-implementation-of-the-two-man-rule/>`_.
* `View the Red October source
  <https://github.com/cloudflare/redoctober>`_.
"""


from .red_october import RedOctober
