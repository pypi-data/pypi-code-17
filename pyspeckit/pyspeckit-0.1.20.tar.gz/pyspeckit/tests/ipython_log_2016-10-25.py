########################################################
# Started Logging At: 2016-10-25 11:14:46
########################################################

import specutils
spec=specutils.io.fits.read_fits_spectrum1d('test.fits')
spec=specutils.io.fits.read_fits_spectrum1d('test_GHz.fits')
spec=specutils.io.fits.read_fits_spectrum1d('test_GHz.fits', dispersion_unit='GHz')
spec=specutils.io.fits.read_fits_spectrum1d('sample_13CO.fits')
spec
sp = pyspeckit.Spectrum.from_spectrum1d(spec)                     
#sp.baseline(xmin=2200,xmax=3600,exclude=[2500,2800],subtract=False,highlight_fitregion=True,order=2)
import pyspeckit
sp = pyspeckit.Spectrum.from_spectrum1d(spec)
sp.plotter()
sp.baseline(xmin=00000,xmax=150000,exclude=[60000,80000],subtract=False,highlight_fitregion=True,order=2)
get_ipython().magic('history ')
