# Only export very specific items
from .lpc import lpc_freq, lpc_freqtrack
from .lsharm import lsharm_freqtrack
from .peaktracing import quadratic_peak_interpolation, windowed_peaktracing, guided_peaktracing
from .maxpeak import max_peak

# Cleanup module filenames
del lpc
del lsharm
del peaktracing
del maxpeak
