#!/usr/bin/env python
"""
Types4YAML
==========

Types4YAML is a simple type schema system for JSON/YAML documents.

JSON/YAML objects are hugely convenient for passing around data
across environments/languages/programs. Their ease of construction and
flexibility are a one of their great benefits, but when passing them
across APIs it is convenient to check that they conform to the expected
structure.

To this end, we present the Types4YAML library, which provides classes
for reading type schemas (which are themselves written in JSON/YAML)
and validating JSON/YAML documents against them.

Type Schemas
------------

A type schema is a JSON/YAML document which describes a vocabulary
of conformant objects.  Type schemas contain two kinds of element:
atomic types and constructed types. Atomic types describe indivisible
data objects; constructed types describe objects that are composed of
objects of one or more component types.

The supported atomic types are:

any
    Any data object. Any JSON/YAML data which is well formed satisfies
    the ``any`` type.

boolean
    A data object that may be interpreted as a boolean.

string
    Any string object.

date
    A string of the form ``YYYY/MM/DD``.

time
    A string of the form ``HH:mm:ss[.s+]``. Note that fractional seconds
    may be present, but if none are present, a trailing decimal point
    (``.``) should not be present.

datetime
    A string of the form ``YYYY/MM/DD HH:mm:ss[.s+]``. Note that
    fractional seconds may be present, but if none are present, a trailing
    decimal point (``.``) should not be present.

number
    A number data object. This includes integers and floating point
    numbers.  In some libraries, floating point numbers are sometimes
    serialized as strings, so a string which can be converted to a number
    also types correctly.

Constructed types are represented as dictionary object with a single key,
which names the kind of composite object being constructed, and whose
value describes the constituent types, the details of which depend on
the kind of composite object as described below:

oneof: enum
    Describes an enumeration of string values. The value is a list of strings
    that constitute valid values. E.g. ``{'oneof':['heads', 'tails']}``

regex: regex
    Describes a constrained string value. The value is a string comprising
    a regular expression (Python ``re`` flavour), which a data string
    must match to be valid. E.g. ``{'string':'^[A-Z][A-Z]:[0-9][0-9]$'}``.

list: type
    Describes a list value of arbitrary length. The value is a type to
    whichThe elements of the list must all conform to for the list to
    be valid. E.g. ``{'list':'string'}``.  Note that in Python, the list
    type also describes native tuples as well as lists.

tuple: types
    Describes a list of fixed length in which the elements may take on
    different types. The value is a list of types which describes the
    types of the constituent fields. Note that in Python, the tuple type
    also describes native tuples as well as lists.

dict: defn
    Describes a dictionary/map object. The value is a dictionary: the keys
    denote the valid keys in the map, and the values, are the type of the
    data object corresponding to the key. Optional keys are denoted with a
    ``?`` suffix. The special key ``*`` indicates that data objects may
    contain additional keys, whose values conform to the corresponding type.
    E.g. ``{'dict':{'foo':'string', 'bar?':'number', '*':'any'}}``.

union: alts
    Describes an undiscriminated union of types. The value is a list of
    types.  A data object that satisfies any one of the types satisfies
    the union type.  Note: the code for testing whether a data object
    satisfies the union should be assumed to test the data object against
    the given types in order, by default, which could have implications
    for performance.  E.g. ``{'union':['string', {'list':'number'}]}``.

d_u: defn
    Describes a discriminated union type. Discriminated union types are
    equivalent to dictionaries in which all keys are optional, exactly
    one of which must be present in a valid data object. The value is
    a dictionary object, the keys of which are the discriminators (or tags),
    and the corresponding values are the element types associated with
    that discriminator. E.g. ``{'d_u':{'qux':'number', 'wombat':'string'}}``.

with: defns
    Bind names to one or more types, and yield a type. The value is
    a list of length 2 (a tuple). The first element is a dictionary,
    the keys of which are the defined types. The second element is the
    resulting type.  Redefinition of names in nested ``with`` types is
    not currently supported.  E.g. ``{'with': [{'foo':'number'}, {'named':'foo'}]}``

named: name
    Use a named type. The type must be in scope.

The following YAML document specifies the type schema for valid type schemas::

    with:
    -   dictionary: {dict: {'*': {named: type}}}
        types: {list: {named: type}}
        type:
            union:
            - null
            - oneof: [any, boolean, string, date, time, datetime, number]
            - d_u:
                oneof:  {list: string}
                regex:  string
                list:   {named: type}
                tuple:  {named: types}
                dict:   {named: dictionary}
                d_u:    {named: dictionary}
                union:  {named: types}
                with:
                    tuple:
                    - {named: dictionary}
                    - {named: type}
                named:  string
    -   named: type
"""

__docformat__ = 'restructuredtext'

import datetime
import re
import StringIO

import yaml

type_definition_of_types = \
"""
with:
-   dictionary: {dict: {'*': {named: type}}}
    types: {list: {named: type}}
    type:
        union:
        - null
        - oneof: [any, boolean, string, date, time, datetime, number]
        - d_u:
            oneof:  {list: string}
            regex:  string
            list:   {named: type}
            tuple:  {named: types}
            dict:   {named: dictionary}
            union:  {named: types}
            d_u:    {named: dictionary}
            with:
                tuple:
                - {named: dictionary}
                - {named: type}
            named:  string
-   named: type
"""

type_of_types = yaml.safe_load(StringIO.StringIO(type_definition_of_types))

class BadType(Exception):
    """
    ``BadType`` exceptions are thrown when the type itself is
    malformed in some way. Examples include ``oneof`` types with
    no elements, ``named`` references to undeclared types, and so
    on.
    """
    def __init__(self, arg):
        self.args = arg

class _UsageError(Exception):
    def __init__(self, arg):
        self.args = arg

booleanValues = {
    'y':    True,
    'Y':    True,
    'yes':  True,
    'Yes':  True,
    'YES':  True,
    'n':    False,
    'N':    False,
    'no':   False,
    'No':   False,
    'NO':   False,
    'true': True,
    'True': True,
    'TRUE': True,
    'false':False,
    'False':False,
    'FALSE':False,
    'on':   True,
    'On':   True,
    'ON':   True,
    'off':  False,
    'Off':  False,
    'OFF':  False,
    1:      True,
    0:      False,
    True:   True,
    False:  False
}

class _Context(object):
    def __init__(self):
        self.defs = []
        self.errs = []
        self.ctxt = ['']
        self.scope = []

    def push_defs(self, defs):
        self.defs.append(defs)

    def pop_defs(self):
        self.defs.pop()

    def lookup(self, name):
        i = len(self.defs)
        while i > 0:
            i -= 1
            if name in self.defs[i]:
                return self.defs[i][name]
        raise BadType, '%s: undefined type %s' % (self.ctxt[-1], name)

    def error(self, msg):
        self.errs.append('%s: %s' % (self.ctxt[-1], msg))

    def enter(self, ctx, defs=None):
        p = self.ctxt[-1]
        self.ctxt.append(p + ctx)
        if defs is None:
            self.scope.append(False)
        else:
            self.scope.append(True)
            self.defs.append(defs)
        return self

    def __enter__(self):
        return None

    def __exit__(self, *args):
        self.ctxt.pop()
        if self.scope.pop():
            self.defs.pop()

class _Type(object):
    def __init__(self, _type, validate = True):
        """
        Create a new type object out of a native python object.
        If validate is True, then the type object is validated
        against the type schema for types.
        """

        if validate:
            tot = _TypeType(type_of_types)
            (_, errs) = tot.check(_type)
            if len(errs) > 0:
                raise BadType, errs

        self._type = _type

    def valid(self, x):
        """
        Ignore error messages, just check if a value is conformant.
        """
        (y, errs) = self.check(x)
        return len(errs) == 0

    def check(self, x, *t):
        """
        Check a data object to see if it conforms to the type.
        Returns a tuple of the normalized value and a list of error messages.
        """
        if len(t) == 0:
            tp = self._type
            ctx = _Context()
        else:
            (tp, ctx) = t

        if tp is None:
            if x is not None:
                ctx.error('expected None, got ' + repr(type(x)))
            y = None
        elif isinstance(tp, basestring):
            m = 'check_atom_' + tp
            y = getattr(self, m)(x, ctx)
        else:
            assert type(tp) == type({}) and len(tp) == 1
            (k, v) = tp.items()[0]
            m = 'check_cons_' + k
            y = getattr(self, m)(x, v, ctx)

        if len(t) == 0:
            return (y, ctx.errs)
        else:
            return y

    def check_atom_any(self, x, ctx):
        return x

    def check_atom_boolean(self, x, ctx):
        if not isinstance(x, (basestring, int, long, bool)):
            ctx.error('expected boolean, got ' + repr(type(x)))
            return None
        if x not in booleanValues:
            ctx.error('expected boolean, got ' + str(x))
            return None
        return booleanValues[x]

    def check_atom_string(self, x, ctx):
        if not isinstance(x, basestring):
            ctx.error('expected string, got ' + repr(type(x)))
            return None
        return x

    def check_atom_date(self, x, ctx):
        if not isinstance(x, basestring):
            ctx.error('expected date, got ' + repr(type(x)))
            return None
        m = re.match('(\d\d\d\d)/(\d\d)/(\d\d)$', x)
        if m is None:
            ctx.error('expected date, got malformed string "' + x + '"')
            return None
        try:
            yy = int(m.group(1))
            mm = int(m.group(2))
            dd = int(m.group(3))
            d = datetime.date(yy, mm, dd)
            return d
        except:
            ctx.error('invalid date ' + x)
            return None

    def check_atom_time(self, x, ctx):
        if not isinstance(x, basestring):
            ctx.error('expected time, got ' + repr(type(x)))
            return None
        m = re.match('(\d\d):(\d\d):(\d\d)(\.[0-9]+)?$', x)
        if m is None:
            ctx.error('expected time, got malformed string "' + x + '"')
            return None
        hh = int(m.group(1))
        mm = int(m.group(2))
        ss = int(m.group(3))
        us = 0
        if m.group(4) is not None:
            us = int(1e6*float('0' + m.group(4)))

        ok = True
        if hh < 0 or hh >= 24:
            ok = False
        if mm < 0 or mm >= 60:
            ok = False
        if ss < 0 or ss >= 60:
            ok = False
        assert 0 <= us and us < 1000000
        if not ok:
            ctx.error('invalid time ' + x)
            return None
        return datetime.time(hh, mm, ss, us)

    def check_atom_datetime(self, x, ctx):
        if not isinstance(x, basestring):
            ctx.error('expected datetime, got ' + repr(type(x)))
            return None
        m = re.match('(\d\d\d\d/\d\d/\d\d) (\d\d:\d\d:\d\d(\.[0-9]+)?)$', x)
        if m is None:
            ctx.error('expected datetime, got malformed string "' + x + '"')
            return None
        d = self.check_atom_date(m.group(1), ctx)
        t = self.check_atom_time(m.group(2), ctx)
        if d is None or t is None:
            return None
        return  datetime.datetime.combine(d, t)

    def check_atom_number(self, x, ctx):
        if isinstance(x, (int, long, float)):
            return x
        try:
            return float(x)
        except:
            ctx.error('expected number, got ' + repr(type(x)))
            return None

    def check_cons_oneof(self, x, t, ctx):
        if not isinstance(x, basestring):
            ctx.error('in oneof, expected string, got ' + repr(type(x)))
            return None
        if x not in t:
            ctx.error('in oneof, unexpected value "' + x + '"')
            return None
        return x

    def check_cons_regex(self, x, t, ctx):
        if not isinstance(x, basestring):
            ctx.error('in regex, expected string, got ' + repr(type(x)))
            return None
        try:
            if not re.match(t, x):
                ctx.error('regex "%s" did not match "%s"' % (t, x))
                return None
            return x
        except:
            raise BadType, 'unevaluable regex: ', t

    def check_cons_list(self, x, t, ctx):
        if type(x) != type([]) and type(x) != type((1,2)):
            ctx.error('expected list or tuple, got ' + repr(type(x)))
            return None
        y = []
        for i in xrange(len(x)):
            with ctx.enter('[%d]' % (i,)):
                y.append(self.check(x[i], t, ctx))
        if type(x) == type([]):
            return y
        else:
            return tuple(y)

    def check_cons_tuple(self, x, t, ctx):
        if type(x) != type([]) and type(x) != type((1,2)):
            ctx.error('expected list or tuple, got ' + repr(type(x)))
            return None
        if len(x) != len(t):
            ctx.error('expected %d-tuple, got %d-tuple' % (len(t), len(x)))
            return None
        y = []
        for i in xrange(len(t)):
            with ctx.enter('[%d]' % (i,)):
                y.append(self.check(x[i], t[i], ctx))
        return tuple(y)

    def check_cons_dict(self, x, t, ctx):
        if type(x) != type({}):
            ctx.error('expected dict, got ' + repr(type(x)))
            return None
        mand = {}
        opts = {}
        extra = None
        for (k,u) in t.items():
            if k == '*':
                extra = u
            elif k.endswith('?'):
                opts[k[:-1]] = u
            else:
                mand[k] = u
        y = {}
        for (k,v) in x.items():
            with ctx.enter('.' + k):
                if k in mand:
                    y[k] = self.check(v, mand[k], ctx)
                    continue
                if k in opts:
                    y[k] = self.check(v, opts[k], ctx)
                    continue
                if extra is not None:
                    y[k] = self.check(v, extra, ctx)
                    continue
        n = 0
        for k in set(mand.keys()) - set(x.keys()):
            n += 1
            ctx.error('unexpected key ' + k)
        if n > 0:
            return None
        return y

    def check_cons_d_u(self, x, t, ctx):
        if type(x) != type({}):
            ctx.error('in discriminated union, expected dict, got ' + repr(type(x)))
            return None
        if len(x) != 1:
            ctx.error('in discriminated union, expected single key, got ' + str(len(x)))
            return None
        (k, v) = x.items()[0]
        if k not in t:
            ctx.error('in discriminated union, unexpected key "' + k + '"')
            return None
        with ctx.enter('.' + k):
            return {k: self.check(v, t[k], ctx)}

    def check_cons_union(self, x, t, ctx):
        errs = ctx.errs
        best = None
        for u in t:
            ctx.errs = []
            y = self.check(x, u, ctx)
            if len(ctx.errs) == 0:
                ctx.errs = errs
                return y
            if best is None or len(ctx.errs) < len(best):
                best = ctx.errs
        ctx.errs = errs + best
        return None

    def check_cons_with(self, x, t, ctx):
        if len(t) != 2:
            raise BadType, 'badly formed "with" block'
        defs = t[0]
        u = t[1]
        with ctx.enter('with', defs):
            y = self.check(x, u, ctx)
        return y

    def check_cons_named(self, x, t, ctx):
        u = ctx.lookup(t)
        return self.check(x, u, ctx)

class _TypeType(_Type):
    def __init__(self, _type):
        super(_TypeType, self).__init__(_type, False)

    def check_cons_d_u(self, x, t, ctx):

        # Check the basic constraints are satisfied.
        y = super(_TypeType, self).check_cons_d_u(x, t, ctx)
        if y is None:
            return None

        (k, v) = y.items()[0]

        if k == 'oneof':
            # oneof types must have at least one alternative.
            if len(v) == 0:
                ctx.error('oneof types must have at least 1 alternative')
                return None

        if k == 'regex':
            # regex types must have a vailid regex.
            try:
                p = re.compile(v)
            except:
                ctx.error('regex specification not well formed')
                return None

        return y

def make_type(**kwargs):
    """
    Construct a type schema object.  Exactly one of the following
    named arguments should be supplied:

    doc : string
        a string containing the YAML text of the type specification.

    file : file
        a file-like object from which the YAML text of the type
	    specification can be read.

    obj : object
        a native python object denoting the type.

    """
    if len(kwargs) > 1:
        raise _UsageError, kwargs
    if 'doc' in kwargs:
        stream = StringIO.StringIO(kwargs['doc'])
        t = yaml.load(stream)
        return _Type(t)
    if 'file' in kwargs:
        stream = kwargs['file']
        t = yaml.load(stream)
        return _Type(t)
    if 'obj' in kwargs:
        return _Type(kwargs['obj'])
    raise _UsageError, kwargs

