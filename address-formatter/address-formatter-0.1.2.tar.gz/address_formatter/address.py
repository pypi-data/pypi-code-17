# -*- coding: utf-8 -*-
import pycountry
from functools import wraps


try:
    bool(type(unicode))
except NameError:
    unicode = lambda s: str(s)


def upper(value):
    "A safe version of upper"
    if not value:
        return None
    return value.upper()


class requires(object):

    def __init__(self, *fields):
        self.fields = fields

    def __call__(self, f):
        @wraps(f)
        def wrapped_f(address, *args, **kwargs):
            for field in self.fields:
                if not getattr(address, field):
                    raise IncompleteAddress(field)
            return f(address, *args, **kwargs)
        return wrapped_f


class IncompleteAddress(Exception):
    pass


class Address(object):
    "An Address"

    def __init__(self, country_code,
                 name=None, company_name=None,
                 street=None, street2=None,
                 city=None, county=None,
                 postal_code=None,
                 subdivision_code=None):
        self.country_code = country_code
        self.name = name
        self.company_name = company_name
        self.street = street
        self.street2 = street2
        self.city = city
        self.county = county
        self.postal_code = postal_code
        self.subdivision_code = subdivision_code

    @property
    def country(self):
        return pycountry.countries.get(alpha_2=self.country_code)

    @property
    def country_name(self):
        return self.country.name

    @property
    def subdivision_name(self):
        try:
            return self.subdivision.name
        except KeyError:
            return None

    @property
    def subdivision(self):
        code = self.subdivision_code
        if code and len(code) < 5:
            code = u'%s-%s' % (self.country_code, code)
        return pycountry.subdivisions.get(code=code)

    def join(self, separator=u'\r\n', *args):
        return separator.join(map(unicode, filter(None, args)))

    def render(self, separator=u'\r\n'):
        country_renderer = 'render_%s' % self.country_code.lower()
        if hasattr(self, country_renderer):
            parts = getattr(self, country_renderer)()
        else:
            # no renderer defined for the country.
            # Just print it as safely as one could
            parts = [
                self.name,
                self.company_name,
                self.street,
                self.street2,
                self.city,
                self.county,
                self.postal_code,
                self.subdivision_name,
                self.country_name
            ]
        return self.join(separator, *parts)

    @requires('postal_code', 'city')
    def render_gb(self):
        "Great Britain"
        return [
            self.name,
            self.company_name,
            self.join(u' ', self.street, self.street2),
            self.join(u' ', self.county, self.subdivision_name),
            upper(self.city),
            upper(self.postal_code),
            self.country_name
        ]

    @requires('subdivision_code', 'postal_code')
    def render_us(self):
        "United States"
        return [
            self.name,
            self.company_name,
            self.join(u' ', self.street, self.street2),
            self.join(
                u' ', self.city, upper(self.subdivision_code[-2:]),
                self.postal_code
            ),
            self.country_name,
        ]

    @requires('postal_code')
    def render_ca(self):
        "Canada"
        if self.subdivision:
            subdivision = u'(%s)' % self.subdivision_name
        else:
            subdivision = None
        return [
            self.name,
            self.company_name,
            self.join(u'-', self.street2, self.street),
            self.join(u' ', self.city, subdivision, self.postal_code),
            self.country_name
        ]

    @requires('postal_code')
    def render_fr(self):
        "France"
        return [
            self.name,
            self.company_name,
            self.join(u' ', self.street, self.street2),
            self.join(u' ', self.postal_code, upper(self.city)),
            self.country_name
        ]

    @requires('postal_code')
    def render_de(self):
        "Germany"
        return [
            self.name,
            self.company_name,
            self.join(u' ', self.street2, self.street),
            self.join(u' ', self.postal_code, self.city),
            self.country_name
        ]

    @requires('postal_code', 'subdivision_code')
    def render_au(self):
        "Australia"
        return [
            self.name,
            self.company_name,
            self.join(u' ', self.street, self.street2),
            self.join(
                u' ', upper(self.city), upper(self.subdivision_code),
                self.postal_code
            ),
            self.country_name
        ]

    @requires('postal_code')
    def render_nl(self):
        "Netherlands"
        return [
            self.name,
            self.company_name,
            self.join(u' ', self.street, self.street2),
            self.join(u' ', self.postal_code, upper(self.city)),
            self.country_name,
        ]

    @requires('postal_code')
    def render_jp(self):
        "Japan"
        return [
            self.name,
            self.company_name,
            self.join(u', ', self.street, self.street2),
            self.join(u', ', self.subdivision_name, upper(self.city)),
            self.postal_code,
            self.country_name,
        ]

    @requires('postal_code')
    def render_co(self):
        "Norway"
        return [
            self.name,
            self.company_name,
            self.join(u' ', self.street, self.street2),
            self.join(u' ', self.postal_code, upper(self.city)),
            self.country_name
        ]
