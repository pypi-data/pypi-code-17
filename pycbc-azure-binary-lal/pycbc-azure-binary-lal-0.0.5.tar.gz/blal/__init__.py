def azure_init():
    """ Initialize some of the settings needed for azure"""
    from pycbc.fft import backend_cpu
    backend_cpu.cpu_backend = 'numpy'
