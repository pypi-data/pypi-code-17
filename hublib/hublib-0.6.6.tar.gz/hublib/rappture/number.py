from __future__ import print_function
from .. import ureg, Q_
from .node import Node

# Unit conversion
_units = [(" ** 2", "2"),
          (" ** 3", "3"),
          ("milli", "m"),
          ("centi", "c"),
          ("micro", "u"),
          ("nano", "n"),
          ("pico", "p"),
          ("femto", "f"),
          ("femto", "f"),
          ("atto", "a"),
          ("kilo", "k"),
          ("mega", "M"),
          ("giga", "G"),
          ("tera", "T"),
          ("peta", "P"),
          ("hour", "h"),
          ("day", "d"),
          ("degC", "C"),
          ("degF", "F"),
          ("degR", "R"),
          ("second", "s"),
          ("meter", "m"),
          ("minute", "min"),
          ("angstrom", "A"),
          ("inch", "in"),
          ("foot", "ft"),
          ("yard", "yd"),
          ("mile", "mi"),
          ("electron_volt", "eV"),
          ("joule", "J"),
          ("gallon", "gal"),
          ("liter", "L"),
          ("degree", "deg"),
          ("gram", "g"),
          ("atmosphere", "atm"),
          ("pascal", "Pa"),
          ("pound_force_per_square_inch", "psi"),
          ("mm_Hg", "mmHg"),
          ("newton", "N"),
          ("tesla", "T"),
          ("gauss", "G"),
          ("weber", "Wb"),
          ("maxwell", "Mx"),
          ("volt", "V"),
          ("mole", "mol"),
          ("hertz", "Hz"),
          ("atomic_mass_unit", "amu"),
          ("watt", "W"),
          ("kelvin", "K"),
          ("*","")
          ]

_runits = [('C', 'degC')]

# convert PINT units to Rappture string
def rap_unit(p_unit):
    val = str(p_unit)
    print("rap_units", val)
    for a,b in _units:
        val = val.replace(a,b)
    return val.replace(" ", "")

# parse rappture string . Returns PINT
def rap_parse(expr):
    val = str(expr)
    print("rap_parse", val)
    for a,b in _runits:
        val = val.replace(a,b)
    print("rap_parse2", val)
    return ureg.parse_expression(val)

# parse rappture units. Returns PINT
def rap_parse_units(expr):
    val = str(expr)
    print("rap_parse_u", val)
    for a,b in _runits:
        val = val.replace(a,b)
    print("rap_parse2_u", val)
    return ureg.parse_units(val)

# outputs Rappture-compatible string with units,
# Takes PINT value, int, or float. Preserves units if
# units is None.  Converts to units if necessary
def conv_rap(val, units=None):
    print("conv_rap", val, units)
    if type(units) == str:
        units = rap_parse_units(units)
        print("units=", units)

    if type(val) != Q_:
        if type(val) == int or type(val) == float:
            val = str(val)
        val = rap_parse(val)
        print("conv_rap", val)
    if units is not None:
        if hasattr(val, 'units'):
            print("foo", val)
            val = val.to(units)
            print("fooX", val)
        else:
            val = Q_(val, units)

    if hasattr(val, 'units'):
        print("val=", val)
        return "%s %s" % (val.magnitude, rap_unit(val.units))

    return str(val)


# Outputs PINT value, int, or float.
# Takes PINT value, int, float, or rappture string.  Preserves units if
# units is None.  Converts to units if necessary
def conv_pint(val, units=None):

    if type(units) == str:
        # Rappture compatibility. C is Celsius, not Coulombs
        if units == 'C':
            units = ureg.degC
        else:
            try:
                units = ureg.parse_expression(units).units
            except:
                ValueError("Unrecognized units:", units)

    try:
        if type(val) == str:
            val = ureg.parse_expression(val)
    except:
        raise ValueError("Bad input value:", val)

    if units is not None:
        if hasattr(val, 'units'):
            if val.units == ureg.coulomb and (units == ureg.K or units == ureg.degC):
                # C -> Celsius
                val = Q_(val.magnitude, ureg.degC)
            val = val.to(units)
        else:
            val = Q_(val, units)

    return val


class Number(Node):

    def text_to_number(self, magnitude=False, units=False):
        val = self.get_text()
        u = self.elem.find('units')
        if units:
            if u is None or u.text == '':
                return ''
            return ureg.parse_expression(u.text).units
        if u is None or u == '':
            return float(val)

        val = conv_pint(val, u.text, val)
        if magnitude:
            return val.magnitude
        return val

    @property
    def value(self):
        # print("GET NUMBER VALUE")
        return self.text_to_number()

    @value.setter
    def value(self, val):
        # print("SET NUMBER VALUE to", val)

        vunits = ''
        if hasattr(val, 'units'):
            vunits = val.units

        if vunits == '':
            # Not PINT, so just set to string value
            self.set_text(str(val))
            return

        uelem = elem.find('units')
        if uelem is None or uelem.text == '':
            # Rappture doesn't want units, but our expression has them!!!!
            raise ValueError("This Rappture element does not have Units!!")

        # Rappture wants units and we have them

        # convert Rappture units to PINT units
        if uelem.text == 'C':
            units = ureg.degC
        else:
            units = ureg.parse_expression(uelem.text).units

        # let PINT do the conversion
        val = val.to(units)

        # a Rappture-friendly string
        self.set_text('%s %s' % (val.magnitude, uelem.text))

    @property
    def magnitude(self):
        return self.text_to_number(magnitude=True)

    @property
    def units(self):
        return self.text_to_number(units=True)