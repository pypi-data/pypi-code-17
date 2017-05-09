#-*- coding: utf-8 -*-
"""
@file
@brief Small functions.
"""
import datetime


def convert_into_days(date, lang="fr", format="%Y-%m-%dT%H:%M:%S"):
    """
    Convert a date into the number of days from today.

    @param      date        str or datetime
    @param      lang        language
    @param      format      format to use
    @return                 string
    """
    if lang != "fr":
        raise NotImplementedError(
            "Language '{0}' is not supported.".format(lang))
    now = datetime.datetime.now()
    if isinstance(date, str):
        date = datetime.datetime.strptime(date, format)
    delta = now - date
    delay = delta.days
    if delay == 0:
        hour = delta.seconds // 3600
        if hour <= 1:
            return "il y a moins d'une heure"
        elif hour <= 2:
            return "il y a deux heures"
        elif hour <= 3:
            return "il y a trois heures"
        elif hour <= 6:
            return "il y a six heures"
        elif hour <= 12:
            return "il y a douze heures"
        else:
            return "aujourd'hui"
    elif delay == 1:
        return "hier"
    elif delay == 2:
        return "avant-hier"
    elif delay < 0:
        return "dans le futur"
    else:
        return "il y a {0} jours".format(delay)


_int_values = dict(un=1, deux=2, trois=3, quatre=4, cinq=5, six=6, sept=7,
                   huit=8, neuf=9, dix=10, onze=11, douze=12, vingt=20, cent=100,
                   cents=100, mille=1000)


def parse_string_int(text: str) -> int:
    """
    Converts a string into an integer.
    It can also be a string like *'un'*.

    @param      text        text to convert
    @return                 number
    """
    if not text:
        raise ValueError("Text to convert cannot be empty.")
    if not isinstance(text, str):
        raise ValueError("Text to convert cannot be a string.")
    try:
        return int(text)
    except ValueError:
        if text in _int_values:
            return _int_values[text]
        else:
            raise ValueError("Unable to convert '{0}' into int.".format(text))
