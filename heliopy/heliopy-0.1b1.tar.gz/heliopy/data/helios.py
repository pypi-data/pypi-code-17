"""
Methods for importing Helios data.

In general the data are available form a number of sources (replace 'helios1'
with 'helios2' in url to change probe):

* Distribution functions - Not publically available
* Merged plasma/mangetic field - |merged_url|
* 6 second cadence magnetic field - |6s_mag_url|
* Trajectory - |traj_url|

.. |merged_url| replace::
    ftp://cdaweb.gsfc.nasa.gov/pub/data/helios/helios1/merged/
.. |6s_mag_url| replace::
    ftp://cdaweb.gsfc.nasa.gov/pub/data/helios/helios1/mag/6sec_ness/
.. |traj_url| replace::
    ftp://cdaweb.gsfc.nasa.gov/pub/data/helios/helios1/traj/

If the data is publically available, it will be dowloaded automatically if it
doesn't exist locally.
"""
import pandas as pd
import numpy as np
from datetime import date, time, datetime, timedelta
import os
import warnings
from urllib.error import URLError
from heliopy import config
from heliopy.data import helper
import heliopy.vector.transformations as spacetrans
import heliopy.time as spacetime
import heliopy.constants as constants
data_dir = config['DEFAULT']['download_dir']
use_hdf = config['DEFAULT']['use_hdf']
helios_dir = os.path.join(data_dir, 'helios')


def dtime2ordinal(dtime):
    """Consistent method to convert datetime to ordinal"""
    if type(dtime) == datetime:
        dtime = pd.Series(dtime)
    return pd.DatetimeIndex(dtime).astype(np.int64)


def _check_probe(probe):
    probe = str(probe)
    assert probe == '1' or probe == '2', 'Probe number must be 1 or 2'
    return probe


def _dist_file_dir(probe, year, doy):
    yearstring = str(year)[-2:]
    return os.path.join(helios_dir,
                        'helios' + probe,
                        'dist',
                        'h' + probe + yearstring,
                        'Y' + yearstring + 'D' + str(doy).zfill(3))


def _loaddistfile(probe, year, doy, hour, minute, second):
    """
    Method to load a Helios distribution file.

    Returns opened file and location of file if file exists. If file doesn't
    exist raises an OSError.

    Parameters
    ----------
    probe : int, string
        Helios probe to import data from. Must be 1 or 2.
    year : int
        Year
    doy : int
        Day of year
    hour : int
        Hour.
    minute : int
        Minute
    second : int
        Second

    Returns
    -------
    f : file
        Opened distribution function file
    filename : string
        Filename of opened file
    """
    probe = _check_probe(probe)
    # Work out location of file
    yearstring = str(year)[-2:]
    filedir = _dist_file_dir(probe, year, doy)
    filename = os.path.join(filedir,
                            'h' + probe + 'y' + yearstring +
                            'd' + str(doy).zfill(3) +
                            'h' + str(hour).zfill(2) +
                            'm' + str(minute).zfill(2) +
                            's' + str(second).zfill(2) + '_')

    # Try to open distribution file
    for extension in ['hdm.0', 'hdm.1', 'ndm.0', 'ndm.1']:
        try:
            f = open(filename + extension)
            filename += extension
        except OSError:
            continue

    if 'f' not in locals():
        raise OSError('Could not find file with name ' +
                      filename[:-1])
    else:
        return f, filename


def _dist_filename_to_hms(path):
    """Given distribution filename, extract hour, minute, second"""
    # year = int(path[-21:-19]) + 1900
    # doy = int(path[-18:-15])
    hour = int(path[-14:-12])
    minute = int(path[-11:-9])
    second = int(path[-8:-6])
    return hour, minute, second


def integrated_dists(probe, starttime, endtime):
    """
    Returns the integrated distributions from experiments i1a and i1b in Helios
    distribution function files.

    The distributions are integrated over all angles and given as a function
    of proton velocity.

    Parameters
    ----------
    probe : int
        Helios probe to import data from. Must be 1 or 2.
    starttime : datetime
        Start of interval
    endtime : datetime
        End of interval

    Returns
    -------
    distinfo : Series
        Infromation stored in the top of distribution function files.
    """
    extensions = ['hdm.0', 'hdm.1', 'ndm.0', 'ndm.1']
    distlist = {'a': [], 'b': []}

    # Loop through each day
    while starttime < endtime + timedelta(days=1):
        year = starttime.year
        doy = starttime.strftime('%j')
        # Directory for today's distribution files
        dist_dir = _dist_file_dir(probe, year, doy)
        # Locaiton of hdf file to save to/load from
        hdffile = 'h' + probe + str(year) + str(doy).zfill(3) +\
            'integrated_dists.hdf'
        hdffile = os.path.join(dist_dir, hdffile)
        todays_dists = {'a': [], 'b': []}
        if os.path.isfile(hdffile):
            for key in todays_dists:
                todays_dists[key] = pd.read_hdf(hdffile, key=key)
        else:
            # Get every distribution function file present for this day
            for f in os.listdir(dist_dir):
                path = os.path.join(dist_dir, f)
                # Check for distribution function
                if path[-5:] in extensions:
                    hour, minute, second = _dist_filename_to_hms(path)
                    try:
                        a, b = integrated_dists_single(probe, year, doy,
                                                       hour, minute, second)
                    except RuntimeError as err:
                        strerr = 'No ion distribution function data in file'
                        if str(err) == strerr:
                            continue
                        raise err

                    t = datetime.combine(starttime.date(),
                                         time(hour, minute, second))
                    dists = {'a': a, 'b': b}
                    for key in dists:
                        dist = dists[key]
                        dist['Time'] = t
                        dist = dist.set_index(['Time', 'v'], drop=True)
                        todays_dists[key].append(dist)
            for key in todays_dists:
                todays_dists[key] = pd.concat(todays_dists[key])
                if use_hdf:
                    todays_dists[key].to_hdf(hdffile, key=key, mode='a')
        for key in distlist:
            distlist[key].append(todays_dists[key])
        starttime += timedelta(days=1)

    # The while loop will only stop after we have overshot
    starttime -= timedelta(days=1)
    for key in distlist:
        distlist[key] = helper.timefilter(distlist[key], starttime, endtime)
    return distlist


def integrated_dists_single(probe, year, doy, hour, minute, second):
    """
    Returns the integrated distributions from experiments i1a and i1b in Helios
    distribution function files.

    The distributions are integrated over all angles and given as a function
    of proton velocity.

    Parameters
    ----------
    probe : int, string
        Helios probe to import data from. Must be 1 or 2.
    year : int
        Year
    doy : int
        Day of year
    hour : int
        Hour
    minute : int
        Minute.
    second : int
        Second

    Returns
    -------
    i1a : DataFrame
        i1a integrated distribution function.
    i1b : DataFrame
        i1b integrated distribution function.
    """
    probe = _check_probe(probe)
    f, _ = _loaddistfile(probe, year, doy, hour, minute, second)
    for line in f:
        if line[0:19] == ' 1-D i1a integrated':
            break
    # i1a distribution function
    i1adf = f.readline().split()
    f.readline()
    i1avs = f.readline().split()
    f.readline()
    # i1b distribution file
    i1bdf = f.readline().split()
    f.readline()
    i1bvs = f.readline().split()

    i1a = pd.DataFrame({'v': i1avs, 'df': i1adf}, dtype=float)
    i1b = pd.DataFrame({'v': i1bvs, 'df': i1bdf}, dtype=float)
    return i1a, i1b


def electron_dist(probe, year, doy, hour, minute, second, remove_advect=False):
    """
    Read in 2D electron distribution function.

    Parameters
    ----------
    probe : int, string
        Helios probe to import data from. Must be 1 or 2.
    year : int
        Year
    doy : int
        Day of year
    hour : int
        Hour.
    minute : int
        Minute
    second : int
        Second
    remove_advect : bool, optional
        If ``False``, the distribution is returned in
        the spacecraft frame.

        If ``True``, the distribution is
        returned in the solar wind frame, by subtracting the spacecraft
        velocity from the velcoity of each bin. Note this significantly
        slows down reading in the distribution.

    Returns
    -------
    dist : DataFrame
        2D electron distribution function
    """
    probe = _check_probe(probe)
    f, filename = _loaddistfile(probe, year, doy, hour, minute, second)
    startline = None
    for i, line in enumerate(f):
        # Find start of electron distribution function
        if line[0:4] == ' 2-D':
            startline = i + 2
            # Throw away next line (just has max of distribution)
            f.readline()
            # Throw away next line (just has table headings)
            if f.readline()[0:27] == ' no electron data available':
                return None
            break
    nlines = None
    for i, line in enumerate(f):
        if line[:30] == ' -1.2 Degree, Pizzo correction':
            break
    nlines = i + 1
    if startline is None:
        return None
    ##########################################
    # Read and process electron distribution #
    ##########################################
    # Arguments for reading in data
    readargs = {'usecols': [0, 1, 2, 3, 4, 5],
                'names': ['Az', 'E_bin', 'pdf', 'counts', 'vx', 'vy'],
                'delim_whitespace': True,
                'skiprows': startline,
                'nrows': nlines}
    # Read in data
    dist = pd.read_table(filename, **readargs)
    if dist.empty:
        return None

    # Remove spacecraft abberation
    # Assumes that spacecraft motion is always in the ecliptic (x-y)
    # plane
    if remove_advect:
        params = distparams_single(probe, year, doy, hour, minute, second)
        dist['vx'] += params['helios_vr']
        dist['vy'] += params['helios_v']
    # Convert to SI units
    dist[['vx', 'vy']] *= 1e3
    dist['pdf'] *= 1e12
    # Calculate spherical coordinates of energy bins
    dist['|v|'], _, dist['phi'] =\
        spacetrans.cart2sph(dist['vx'], dist['vy'], 0)
    # Calculate bin energy assuming particles are electrons
    dist['E_electron'] = 0.5 * constants.m_e *\
        ((dist['|v|']) ** 2)

    # Convert to multi-index using Azimuth and energy bin
    dist = dist.set_index(['E_bin', 'Az'])
    return dist


def distparams(probe, starttime, endtime):
    """
    Read in distribution parameters found in the header of distribution files.

    Parameters
    ----------
    probe : int
        Helios probe to import data from. Must be 1 or 2.
    starttime : datetime
        Start of interval
    endtime : datetime
        End of interval

    Returns
    -------
    distinfo : Series
        Infromation stored in the top of distribution function files
    """
    extensions = ['hdm.0', 'hdm.1', 'ndm.0', 'ndm.1']
    paramlist = []

    # Loop through each day
    while starttime < endtime:
        year = starttime.year
        doy = starttime.strftime('%j')
        # Directory for today's distribution files
        dist_dir = _dist_file_dir(probe, year, doy)
        # Locaiton of hdf file to save to/load from
        hdffile = 'h' + probe + str(year) + str(doy).zfill(3) +\
            'distparams.hdf'
        hdffile = os.path.join(dist_dir, hdffile)
        if os.path.isfile(hdffile):
            todays_params = pd.read_hdf(hdffile)
        else:
            todays_params = []
            # Get every distribution function file present for this day
            for f in os.listdir(dist_dir):
                path = os.path.join(dist_dir, f)
                # Check for distribution function
                if path[-5:] in extensions:
                    hour, minute, second = _dist_filename_to_hms(path)
                    p = distparams_single(probe, year, doy,
                                          hour, minute, second)
                    todays_params.append(p)

            todays_params = pd.concat(todays_params,
                                      ignore_index=True, axis=1).T
            todays_params = todays_params.set_index('Time', drop=False)
            if use_hdf:
                todays_params.to_hdf(hdffile, key='distparams', mode='w')

        paramlist.append(todays_params)
        starttime += timedelta(days=1)

    return helper.timefilter(paramlist, starttime, endtime)


def distparams_single(probe, year, doy, hour, minute, second):
    """
    Read in parameters from a single distribution function measurement.

    Parameters
    ----------
    probe : int, string
        Helios probe to import data from. Must be 1 or 2.
    year : int
        Year
    doy : int
        Day of year
    hour : int
        Hour
    minute : int
        Minute
    second : int
        Second

    Returns
    -------
    distparams : Series
        Distribution parameters from top of distribution function file.
    """
    probe = _check_probe(probe)
    f, _ = _loaddistfile(probe, year, doy, hour, minute, second)

    _, month, day = spacetime.doy2ymd(year, doy)
    dtime = datetime(year, month, day, hour, minute, second)
    distparams = pd.Series(dtime, index=['Time'], dtype=object)
    # Ignore the Pizzo et. al. correction at top of file
    for _ in range(0, 3):
        f.readline()
    # Line of flags
    flags = f.readline().split()
    distparams['imode'] = int(flags[0])
    # Alternating energy/azimuth shift on?
    distparams['ishift'] = bool(flags[1])
    # Possibly H2 abberation shift?
    distparams['iperihelion_shift'] = bool(flags[2])
    # Indicates a HDM file which contained bad data (frames), but could be
    # handled as NDM file
    distparams['minus'] = int(flags[3])
    # 0 = no instrument, 1 = i1a, 2 = I3
    distparams['ion_instrument'] = int(flags[4])

    # 2 lines of Helios location information
    location = f.readline().split()
    distparams['r_sun'] = float(location[0])     # Heliospheric distance (AU)
    distparams['clong'] = float(location[1])    # Carrington longitude (deg)
    distparams['clat'] = float(location[2])     # Carrington lattitude (deg)
    distparams['carrot'] = int(f.readline().split()[0])   # Carrington cycle

    # 2 lines of Earth location information
    earth_loc = f.readline().split()
    # Heliospheric distance (AU)
    distparams['earth_rsun'] = float(earth_loc[0])
    # Carrington longitude (deg)
    distparams['earth_clong'] = float(earth_loc[1])
    # Carrington lattitude (deg)
    distparams['earth_clat'] = float(earth_loc[2])
    earth_loc = f.readline().split()
    # Angle between Earth and Helios (deg)
    distparams['earth_he_angle'] = float(earth_loc[0])
    # Carrington rotation
    distparams['earth_carrot'] = int(earth_loc[1])

    # Helios velocity information
    helios_v = f.readline().split()
    # Helios radial velocity (km/s)
    distparams['helios_vr'] = float(helios_v[0]) * 1731
    # Helios tangential velocity (km/s)
    distparams['helios_v'] = float(helios_v[1]) * 1731

    # i1a integrated ion parameters
    i1a_proton_params = f.readline().split()
    # Proton number density (cm^-3)
    distparams['np_i1a'] = float(i1a_proton_params[0])
    # Proton velocity (km/s)
    distparams['vp_i1a'] = float(i1a_proton_params[1])
    # Proton temperature (K)
    distparams['Tp_i1a'] = float(i1a_proton_params[2])
    i1a_proton_params = f.readline().split()
    # Proton azimuth flow angle (deg)
    distparams['v_az_i1a'] = float(i1a_proton_params[0])
    # Proton elevation flow angle (deg)
    distparams['v_el_i1a'] = float(i1a_proton_params[1])
    assert distparams['v_az_i1a'] < 360,\
        'Flow azimuth must be less than 360 degrees'

    # i1a integrated alpha parameters (possibly all zero?)
    i1a_alpha_params = f.readline().split()
    # Alpha number density (cm^-3)
    distparams['na_i1a'] = float(i1a_alpha_params[0])
    # Alpha velocity (km/s)
    distparams['va_i1a'] = float(i1a_alpha_params[1])
    # Alpha temperature (K)
    distparams['Ta_i1a'] = float(i1a_alpha_params[2])

    # i1b integrated ion parameters
    i1b_proton_params = f.readline().split()
    # Proton number density (cm^-3)
    distparams['np_i1b'] = float(i1b_proton_params[0])
    # Proton velocity (km/s)
    distparams['vp_i1b'] = float(i1b_proton_params[1])
    # Proton temperature (K)
    distparams['Tp_i1b'] = float(i1b_proton_params[2])

    # Magnetic field (out by a factor of 10 in data files for some reason)
    B = f.readline().split()
    distparams['Bx'] = float(B[0]) / 10
    distparams['By'] = float(B[1]) / 10
    distparams['Bz'] = float(B[2]) / 10
    sigmaB = f.readline().split()
    distparams['sigmaBx'] = float(sigmaB[0]) / 10
    distparams['sigmaBy'] = float(sigmaB[1]) / 10
    distparams['sigmaBz'] = float(sigmaB[2]) / 10

    # Replace bad values with nans
    to_replace = {'Tp_i1a': [-1.0, 0],
                  'np_i1a': [-1.0, 0],
                  'vp_i1a': [-1.0, 0],
                  'Tp_i1b': [-1.0, 0],
                  'np_i1b': [-1.0, 0],
                  'vp_i1b': [-1.0, 0],
                  'sigmaBx': -0.01, 'sigmaBy': -0.01, 'sigmaBz': -0.01,
                  'Bx': 0.0, 'By': 0.0, 'Bz': 0.0,
                  'v_az_i1a': [-1, 0], 'v_el_i1a': [-1, 0],
                  'na_i1a': [-1, 0], 'va_i1a': [-1, 0], 'Ta_i1a': [-1, 0]}
    distparams = distparams.replace(to_replace, np.nan)
    return distparams


def ion_dists(probe, starttime, endtime, remove_advect=False):
    """
    Return 3D ion distributions between *starttime* and *endtime*

    Parameters
    ----------
    probe : int
        Helios probe to import data from. Must be 1 or 2.
    starttime : datetime
        Start of interval
    endtime : datetime
        End of interval
    remove_advect : bool, optional
        If *False*, the distribution is returned in
        the spacecraft frame.

        If *True*, the distribution is
        returned in the solar wind frame, by subtracting the spacecraft
        velocity from the velcoity of each bin. Note this significantly
        slows down reading in the distribution.

    Returns
    -------
    distinfo : Series
        Infromation stored in the top of distribution function files.
    """
    extensions = ['hdm.0', 'hdm.1', 'ndm.0', 'ndm.1']
    distlist = []

    # Loop through each day
    while starttime < endtime:
        year = starttime.year
        doy = starttime.strftime('%j')
        # Directory for today's distribution files
        dist_dir = _dist_file_dir(probe, year, doy)
        # Locaiton of hdf file to save to/load from
        hdffile = 'h' + probe + str(year) + str(doy).zfill(3) +\
            'ion_dists.hdf'
        hdffile = os.path.join(dist_dir, hdffile)
        if os.path.isfile(hdffile):
            todays_dist = pd.read_hdf(hdffile)
        else:
            todays_dist = []
            # Get every distribution function file present for this day
            for f in os.listdir(dist_dir):
                path = os.path.join(dist_dir, f)
                # Check for distribution function
                if path[-5:] in extensions:
                    hour, minute, second = _dist_filename_to_hms(path)
                    try:
                        d = ion_dist_single(probe, year, doy,
                                            hour, minute, second)
                    except RuntimeError as err:
                        strerr = 'No ion distribution function data in file'
                        if str(err) == strerr:
                            continue
                        raise err

                    t = datetime.combine(starttime.date(),
                                         time(hour, minute, second))
                    d['Time'] = t
                    todays_dist.append(d)
            todays_dist = pd.concat(todays_dist)
            todays_dist = todays_dist.set_index('Time', append=True)
            if use_hdf:
                todays_dist.to_hdf(hdffile, key='ion_dist', mode='w')

        distlist.append(todays_dist)
        starttime += timedelta(days=1)

    # The while loop will only stop after we have overshot
    starttime -= timedelta(days=1)
    return helper.timefilter(distlist, starttime, endtime)


def ion_dist_single(probe, year, doy, hour, minute, second,
                    remove_advect=False):
    """
    Read in ion distribution function.

    Parameters
    ----------
    probe : int, string
        Helios probe to import data from. Must be 1 or 2.
    year : int
        Year
    doy : int
        Day of year
    hour : int
        Hour
    minute : int
        Minute.
    second : int
        Second
    remove_advect : bool, optional
        If *False*, the distribution is returned in
        the spacecraft frame.

        If *True*, the distribution is
        returned in the solar wind frame, by subtracting the spacecraft
        velocity from the velcoity of each bin. Note this significantly
        slows down reading in the distribution.

    Returns
    -------
    dist : DataFrame
        3D ion distribution function
    """
    probe = _check_probe(probe)
    f, filename = _loaddistfile(probe, year, doy, hour, minute, second)

    nionlines = None   # Number of lines in ion distribution
    linesread = 0  # Stores the total number of lines read in the file
    # Loop through file to find end of ion distribution function
    for i, line in enumerate(f):
        # Find start of proton distribution function
        if line[0:23] == 'Maximum of distribution':
            ionstartline = i + 1
        # Find number of lines in ion distribution function
        if line[0:4] == ' 2-D':
            nionlines = i - ionstartline
            break

    linesread += i
    # Bizzare case where there are two proton distributions in one file,
    # or there's no electron data available
    for i, line in enumerate(f):
        if line[0:23] == 'Maximum of distribution' or\
           line[0:30] == '  1.2 Degree, Pizzo correction' or\
           line[0:30] == ' -1.2 Degree, Pizzo correction':
            warnings.warn("More than one ion distribution function found",
                          RuntimeWarning)
            # NOTE: Bodge
            linesread -= 1
            break

    f.close()

    # If there's no electron data to get number of lines, set end of ion
    # distribution function to end of file
    if nionlines is None:
        nionlines = i - ionstartline + 1

    #####################################
    # Read and process ion distribution #
    #####################################
    # If no ion data in file
    if nionlines < 1:
        raise RuntimeError('No ion distribution function data in file')

    # Arguments for reading in data
    readargs = {'usecols': [0, 1, 2, 3, 4, 5, 6, 7],
                'names': ['Az', 'El', 'E_bin', 'pdf', 'counts',
                          'vx', 'vy', 'vz'],
                'delim_whitespace': True,
                'skiprows': ionstartline,
                'nrows': nionlines}
    # Read in data
    dist = pd.read_table(filename, **readargs)

    # Remove spacecraft abberation
    # Assumes that spacecraft motion is always in the ecliptic (x-y)
    # plane
    if remove_advect:
        params = distparams_single(probe, year, doy, hour, minute, second)
        dist['vx'] += params['helios_vr']
        dist['vy'] += params['helios_v']
    # Convert to SI units
    dist[['vx', 'vy', 'vz']] *= 1e3
    dist['pdf'] *= 1e12
    # Calculate magnitude, elevation and azimuth of energy bins
    dist['|v|'], dist['theta'], dist['phi'] =\
        spacetrans.cart2sph(dist['vx'], dist['vy'], dist['vz'])
    # Calculate bin energy assuming particles are protons
    dist['E_proton'] = 0.5 * constants.m_p * ((dist['|v|']) ** 2)

    # Convert to multi-index using azimuth, elevation, and energy bins
    dist = dist.set_index(['E_bin', 'El', 'Az'])
    return dist


def merged(probe, starttime, endtime, verbose=True, try_download=True):
    """
    Read in merged data set

    Parameters
    ----------
    probe : int, string
        Helios probe to import data from. Must be 1 or 2.
    starttime : datetime
        Interval start time
    endtime : datetime
        Interval end time
    verbose : bool
        If ``True``, print more information as data is loading

    Returns
    -------
    data : DataFrame
        Merged data set
    """
    probe = _check_probe(probe)

    daylist = spacetime.daysplitinterval(starttime, endtime)
    data = []
    floc = os.path.join(helios_dir,
                        'helios' + probe,
                        'merged',
                        'he' + probe + '_40sec')
    for day in daylist:
        this_date = day[0]
        # Check that data for this day exists
        if probe == '1':
            if this_date < date(1974, 12, 12) or this_date > date(1985, 9, 4):
                continue
        if probe == '2':
            if this_date < date(1976, 1, 17) or this_date > date(1980, 3, 8):
                continue

        doy = int(this_date.strftime('%j'))
        year = this_date.year

        hdfloc = os.path.join(floc,
                              'H' + probe + str(year - 1900) + '_' +
                              str(doy).zfill(3) + '.h5')
        # Data not processed yet, try to process and load it
        if not os.path.isfile(hdfloc):
            try:
                data.append(_merged_fromascii(probe, year, doy,
                            try_download=try_download))
                if verbose:
                    print(year, doy, 'Processed ascii file')
            except (FileNotFoundError, URLError) as err:
                if verbose:
                    print(str(err))
                    print(year, doy, 'No raw merged data')
        else:
            # Load data from already processed file
            data.append(pd.read_hdf(hdfloc, 'table'))
            if verbose:
                print(year, doy)

    if data == []:
        fmt = '%d-%m-%Y'
        raise ValueError('No data to import for probe ' + probe +
                         ' between ' + starttime.strftime(fmt) + ' and ' +
                         endtime.strftime(fmt))

    return helper.timefilter(data, starttime, endtime)


def _merged_fromascii(probe, year, doy, try_download):
    """
    Read in a single day of merged data.

    Data is loaded from orignal ascii files. and saved to a hdf file for faster
    access after first read in.

    Parameters
    ----------
    probe : int, string
        Helios probe to import data from. Must be 1 or 2.
    year : int
        Year
    doy : int
        Day of year

    Returns
    -------
    data : DataFrame
        Merged data set
    """
    probe = _check_probe(probe)
    local_dir = os.path.join(helios_dir,
                             'helios' + probe,
                             'merged',
                             'he' + probe + '_40sec/')
    remote_url = 'ftp://cdaweb.gsfc.nasa.gov/pub/data/helios/helios' +\
        probe + '/' + 'merged/he' + probe + '_40sec'
    filename = 'H' + probe + str(year - 1900) + '_' +\
        str(doy).zfill(3) + '.dat'
    asciiloc = os.path.join(local_dir, filename)

    # Make sure file is downloaded
    helper.load(filename, local_dir, remote_url, try_download=try_download)

    # Load data
    data = pd.read_table(asciiloc, delim_whitespace=True)

    # Process data
    data['year'] = data['year'].astype(int)
    # Convert date info to datetime
    data['Time'] = pd.to_datetime(data['year'], format='%Y') + \
        pd.to_timedelta(data['day'] - 1, unit='d') + \
        pd.to_timedelta(data['hour'], unit='h') + \
        pd.to_timedelta(data['min'], unit='m') + \
        pd.to_timedelta(data['sec'], unit='s')
    data['ordinal'] = pd.DatetimeIndex(data['Time']).astype(np.int64)

    data = data.drop(['year', 'day', 'hour', 'min', 'sec', 'dechr'], axis=1)
    # Set zero values to nans
    data.replace(0.0, np.nan, inplace=True)

    # Save data to a hdf store
    saveloc = os.path.join(local_dir, filename[:-4] + '.h5')
    data.to_hdf(saveloc, 'table', format='fixed', mode='w')
    return(data)


def mag_4hz(probe, starttime, endtime, verbose=True):
    """
    Read in 4Hz magnetic field data.

    Parameters
    ----------
    probe : int, string
        Helios probe to import data from. Must be 1 or 2.
    starttime : datetime
        Interval start time
    endtime : datetime
        Interval end time
    verbose : bool
        If ``True``, print more information as data is loading

    Returns
    -------
    data : DataFrame
        4Hz magnetic field data set
    """
    probe = _check_probe(probe)
    startdate = starttime.date()
    enddate = endtime.date()

    data = []
    # Loop through years
    for year in range(startdate.year, enddate.year + 1):
        floc = os.path.join(helios_dir,
                            'helios' + probe,
                            'mag',
                            '4hz')
        # Calculate start day of year
        if year == startdate.year:
            startdoy = int(startdate.strftime('%j'))
        else:
            startdoy = 1
        # Calculate end day of year
        if year == enddate.year:
            enddoy = int(enddate.strftime('%j'))
        else:
            enddoy = 366

        # Loop through days of year
        for doy in range(startdoy, enddoy + 1):
            hdfloc = os.path.join(floc,
                                  'he' + probe + '1s' + str(year - 1900) +
                                  str(doy).zfill(3) + '.h5')
            if not os.path.isfile(hdfloc):
                # Data not processed yet, try to process and load it
                try:
                    data.append(_fourHz_fromascii(probe, year, doy))
                    if verbose:
                        print(year, doy, '4Hz data processed')
                except ValueError as err:
                    if str(err)[0:15] == 'No raw mag data':
                        if verbose:
                            print(year, doy, 'No 4Hz raw mag data available'
                                  'for this day')
                    else:
                        raise
            else:
                # Load data from already processed file
                data.append(pd.read_hdf(hdfloc, 'table'))
    if data == []:
        raise ValueError('No raw mag data available')
    data = pd.concat(data, ignore_index=True)
    # Filter data between start and end times
    data = data[(data['Time'] > starttime) & (data['Time'] < endtime)]

    if data.empty:
        raise ValueError('No 4Hz raw mag data available for entire interval')
    return(data)


def _fourHz_fromascii(probe, year, doy):
    """
    Read in a single day of 4Hz magnetic field data.

    Parameters
    ----------
    probe : int, string
        Helios probe to import data from. Must be 1 or 2.
    year : int
        Year
    doy : int
        Day of year

    Returns
    -------
    data : DataFrame
        4Hz magnetic field data set
    """
    probe = _check_probe(probe)
    floc = os.path.join(helios_dir,
                        'helios' + probe,
                        'mag',
                        '4hz')
    fname = 'he' + probe + '1s' + str(year - 1900) + str(doy).zfill(3)
    # For some reason the last number in the filename is the hour at which
    # data starts from on that day... this means a loop to check each hour
    for i in range(0, 24):
        asciiloc = os.path.join(floc, fname + str(i).zfill(2) + '.asc')
        if os.path.isfile(asciiloc):
            break
        elif i == 23:
            raise ValueError('No raw mag data available for probe ' + probe +
                             ', Year: ' + str(year) + ' doy: ' + str(doy))

    # Read in data
    headings = ['Time', 'Bx', 'By', 'Bz']
    widths = [24, 16, 15, 15]
    data = pd.read_fwf(asciiloc, names=headings, header=None, widths=widths,
                       delim_whitespace=True)

    # Convert date info to datetime
    data['Time'] = pd.to_datetime(data['Time'], format='%Y-%m-%dT%H:%M:%S')
    data['ordinal'] = pd.DatetimeIndex(data['Time']).astype(np.int64)

    # Save data to a hdf store
    saveloc = os.path.join(floc, fname + '.h5')
    data.to_hdf(saveloc, 'table', format='fixed', mode='w')
    return(data)


def mag_ness(probe, starttime, endtime, verbose=True):
    """
    Read in 6 second magnetic field data.

    Parameters
    ----------
    probe : int, string
        Helios probe to import data from. Must be 1 or 2.
    starttime : datetime
        Interval start time
    endtime : datetime
        Interval end time
    verbose : bool, optional
        If ``True``, print more information as data is loading. Default is
        ``True``.

    Returns
    -------
    data : DataFrame
        6 second magnetic field data set
    """
    probe = _check_probe(probe)
    startdate = starttime.date()
    enddate = endtime.date()

    data = []
    # Loop through years
    for year in range(startdate.year, enddate.year + 1):
        floc = os.path.join(helios_dir,
                            'helios' + probe,
                            'mag',
                            '6sec_ness',
                            str(year))
        # Calculate start day
        startdoy = 1
        if year == startdate.year:
            startdoy = int(startdate.strftime('%j'))
        # Calculate end day
        enddoy = 366
        if year == enddate.year:
            enddoy = int(enddate.strftime('%j'))

        # Loop through days of year
        for doy in range(startdoy, enddoy + 1):
            hdfloc = os.path.join(floc, 'h' + probe + str(year - 1900) +
                                  str(doy).zfill(3) + '.hdf')
            if os.path.isfile(hdfloc):
                # Load data from already processed file
                data.append(pd.read_hdf(hdfloc))
                continue

            # Data not processed yet, try to process and load it
            try:
                data.append(_mag_ness_fromascii(probe, year, doy))
            except ValueError:
                if verbose:
                    print(year, doy, 'No raw mag data')

    return helper.timefilter(data, starttime, endtime)


def _mag_ness_fromascii(probe, year, doy):
    """
    Read in a single day of 6 second magnetic field data.

    Data is read from orignal ascii files, and saved to a hdf file for faster
    access after the first read.

    Parameters
    ----------
    probe : int, string
        Helios probe to import data from. Must be 1 or 2.
    year : int
        Year
    doy : int
        Day of year

    Returns
    -------
    data : DataFrame
        6 second magnetic field data set
    """
    probe = _check_probe(probe)
    floc = os.path.join(helios_dir,
                        'helios' + probe,
                        'mag',
                        '6sec_ness',
                        str(year))
    fname = 'h' + probe + str(year - 1900) + str(doy).zfill(3)
    asciiloc = os.path.join(floc, fname + '.asc')
    if not os.path.isfile(asciiloc):
        raise ValueError('No raw mag data available for probe ' + probe +
                         ', Year: ' + str(year) + ' DOY: ' + str(doy))

    # Read in data
    headings = ['probe', 'year', 'doy', 'hour', 'minute', 'second', 'naverage',
                'Bx', 'By', 'Bz', '|B|', 'sigma_Bx', 'sigma_By', 'sigma_Bz']

    colspecs = [(1, 2), (2, 4), (4, 7), (7, 9), (9, 11), (11, 13), (13, 15),
                (15, 22), (22, 29), (29, 36), (36, 42), (42, 48), (48, 54),
                (54, 60)]
    data = pd.read_fwf(asciiloc, names=headings, header=None,
                       colspecs=colspecs)

    # Process data
    data['year'] += 1900
    # Convert date info to datetime
    data['Time'] = pd.to_datetime(data['year'], format='%Y') + \
        pd.to_timedelta(data['doy'] - 1, unit='d') + \
        pd.to_timedelta(data['hour'], unit='h') + \
        pd.to_timedelta(data['minute'], unit='m') + \
        pd.to_timedelta(data['second'], unit='s')
    data = data.drop(['year', 'doy', 'hour', 'minute', 'second'], axis=1)
    data = data.set_index('Time', drop=False)

    # Save data to a hdf store
    if use_hdf:
        saveloc = os.path.join(floc, fname + '.hdf')
        data.to_hdf(saveloc, 'mag', format='fixed', mode='w')
    return(data)


def trajectory(probe, starttime, endtime):
    """
    Read in trajectory data.

    Parameters
    ----------
    probe : int, string
        Helios probe to import data from. Must be 1 or 2.
    startdate : datetime
        Interval start date
    enddate : datetime
        Interval end date

    Returns
    -------
    data : DataFrame
        Trajectory data set
    """
    probe = _check_probe(probe)
    data = []
    headings = ['Year', 'doy', 'Hour', 'Carrrot', 'r', 'selat', 'selon',
                'hellat', 'hellon', 'hilon', 'escang', 'code']
    colspecs = [(0, 3), (4, 7), (8, 10), (11, 15), (16, 22), (23, 30),
                (31, 37), (38, 44), (45, 51), (52, 58), (59, 65), (66, 67)]
    # Loop through years
    for i in range(starttime.year, endtime.year + 1):
        floc = os.path.join(helios_dir,
                            'helios' + probe,
                            'traj')
        fname = 'he' + probe + 'trj' + str(i - 1900) + '.asc'

        # Read in data
        try:
            thisdata = pd.read_fwf(os.path.join(floc, fname),
                                   names=headings,
                                   header=None,
                                   colspecs=colspecs)
        except OSError:
            continue

        thisdata['Year'] += 1900

        # Convert date info to datetime
        thisdata['Time'] = pd.to_datetime(thisdata['Year'], format='%Y') + \
            pd.to_timedelta(thisdata['doy'] - 1, unit='d') + \
            pd.to_timedelta(thisdata['Hour'], unit='h')
        thisdata['ordinal'] = dtime2ordinal(thisdata['Time'])

        # Calculate cartesian positions
        thisdata['x'] = thisdata['r'] * np.cos(thisdata['selat']) *\
            np.cos(thisdata['selon'])
        thisdata['y'] = thisdata['r'] * np.cos(thisdata['selat']) *\
            np.sin(thisdata['selon'])
        thisdata['z'] = thisdata['r'] * np.sin(thisdata['selat'])

        thisdata = thisdata.drop(['Year', 'doy', 'Hour'], axis=1)
        data.append(thisdata)

    return helper.timefilter(data, starttime, endtime)
