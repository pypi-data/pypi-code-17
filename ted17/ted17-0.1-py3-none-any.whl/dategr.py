# -*- coding: utf-8 -*-
"""Module dategr.py"""
import datetime


def date2gr(date, removezero=False):
    '''
    date : iso date yyyy-mm-dd
    returns date: dd/mm/yyyy
    '''
    def remove_zero(stra):
        """Remove trailing zeros"""
        if len(stra) > 1 and stra[0] == '0':
            return stra[1:]
        else:
            return stra
    if not date:
        return ''
    year, month, day = date.split('-')
    if removezero:
        return '%s/%s/%s' % (remove_zero(day), remove_zero(month), year)
    else:
        return '%s/%s/%s' % (day, month, year)


def grdate2iso(greek_date):
    """Return iso date (yyy-mm-dd) from greek date(dd/mm/yyyy)"""
    assert len(greek_date) in (8, 9, 10)
    assert len(greek_date.replace('/', '')) + 2 == len(greek_date)
    day, month, year = greek_date.split('/')
    if len(day) == 1:
        day = '0%s' % day
    if len(month) == 1:
        month = '0%s' % month
    return '%s-%s-%s' % (year, month, day)


def getymd_from_iso(isodate):
    '''
    Year, month, date From isodate
    '''
    assert isodate[4] == '-'
    assert isodate[7] == '-'
    year, month, date = isodate.split('-')
    return int(year), int(month), int(date)


def saizon(iso_date, startmonth=10):
    '''
    Επιστρέφει ετήσιο διάστημα από μήνα
    dat : Ημερομηνία
    startmonth : Μήνας που αρχίζει η σαιζόν
    '''
    startmonth = int(startmonth)  # Make sure startmonth is integer
    assert startmonth <= 12
    year, month, _ = getymd_from_iso(iso_date)
    if int(month) >= startmonth:
        return '%s-%s(%s)' % (year, year+1, startmonth)
    else:
        return '%s-%s(%s)' % (year-1, year, startmonth)


def week(iso_date):
    '''
    returns year-weekNumber
    '''
    year, month, day = getymd_from_iso(iso_date)
    week_number = '%s' % datetime.date(year, month, day).isocalendar()[1]
    if len(week_number) == 1:
        week_number = '0' + week_number
    return '%sw%s' % (year, week_number)


def period(date, diast=2):
    '''
    επιστρέφει δίμηνο, τρίμηνο, τετράμηνο, εξάμηνο
    '''
    assert diast in (2, 3, 4, 6)
    dval = {2: u'οΔίμ', 3: u'οΤρίμ', 4: u'οΤετρ', 6: u'οΕξάμ'}
    year, month, date = getymd_from_iso(date)
    imonth = int(month)
    aperiod = imonth // diast
    ypoloipo = imonth % diast
    if ypoloipo > 0:
        aperiod += 1
    return '%s-%s%s' % (year, aperiod, dval[diast])


def group_selector(adate, per='m'):
    """Selector"""
    if per == 'd':  # Όλη η ημερομηνία
        dat = adate[:10]
    elif per == 'm':  # Έτος + μήνας ####-##
        dat = adate[:7]
    elif per == 'y':  # Έτος μόνο
        dat = adate[:4]
    elif per == 'm2':
        dat = period(adate, 2)
    elif per == 'm3':
        dat = period(adate, 3)
    elif per == 'm4':
        dat = period(adate, 4)
    elif per == 'm6':
        dat = period(adate, 6)
    elif per == 'w':
        dat = week(adate)
    elif per == 's':
        dat = saizon(adate)
    else:  # Default is Year
        dat = adate[:4]
    return dat
