# -*- coding: utf-8 -*-

from ted17.w_checkbox import Checkbox
from ted17.w_date import Date
from ted17.w_date_or_empty import Date_or_empty
from ted17.w_integer import Integer
from ted17.w_integer_spin import Integer_spin
from ted17.w_numeric import Numeric
from ted17.w_numeric_spin import Numeric_spin
from ted17.w_text import Text
from ted17.w_text_button import Text_button
from ted17.w_text_combo import Combo
from ted17.w_textline import Text_line
from ted17.w_textline_numbers_only import Textline_numbers_only
from ted17.w_weekdays import Weekdays
from ted17.w_yesno_combo import Yes_no_combo


def qtfield(typ, parent, name):
    '''
    Factory for fld classes.
    '''
    typo = typ.upper()
    if typo == 'BOOLEAN':
        return Checkbox(parent)
    elif typo == 'DATE':
        return Date(parent)
    elif typo == 'DATEN':
        return Date_or_empty(parent)
    elif typo == 'INTEGER':
        return Integer(parent)
    elif typo == 'INTEGERS':
        return Integer_spin(parent)
    elif typo == 'NUMERIC':
        return Numeric(parent)
    elif typo == 'NUMERICS':
        return Numeric_spin(parent)
    elif typo == 'TEXT':
        return Text(parent)
    elif typo == 'IDBUTTON':
        assert(name.endswith('_id'))
        return Text_button(parent, name)
    elif typo == 'IDCOMBO':
        assert(name.endswith('_id'))
        return Combo(parent, name)
    elif typo == 'VARCHAR':
        return Text_line(parent)
    elif typo == 'VARCHARN':
        return Textline_numbers_only(parent)
    elif typo == 'WEEKDAYS':
        return Weekdays(parent)
    elif typo == 'YESNO':
        return Yes_no_combo(parent)
    else:
        return Text_line(parent)
