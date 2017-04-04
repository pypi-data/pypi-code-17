import h5py
import time
import numpy
from PyMca5.PyMca import XASClass
from PyMca5.PyMcaIO import ConfigDict
import posixpath

t0Total = time.time()
analyzer = XASClass.XASClass()
outputFile = "testoutput.h5"
h5 = h5py.File("testdata.h5", "r")
out = h5py.File(outputFile, "w")
for entry0 in h5:
    data = h5[entry0]["data"].value
    energy = h5[entry0]["energy"].value
    firstSpectrum = data[0, 0, :]
    analyzer.setSpectrum(energy, firstSpectrum)
    ddict = analyzer.processSpectrum()
    # initialize the arrays from the first results
    usedEnergy = ddict["Energy"]
    usedMu = ddict["Mu"]
    normalizedIdx = (ddict["NormalizedEnergy"] >= ddict["NormalizedPlotMin"]) & \
          (ddict["NormalizedEnergy"] <= ddict["NormalizedPlotMax"])
    normalizedSpectrumX = ddict["NormalizedEnergy"][normalizedIdx]
    normalizedSpectrumY = ddict["NormalizedMu"][normalizedIdx]
    exafsIdx = (ddict["EXAFSKValues"] >= ddict["KMin"]) & \
               (ddict["EXAFSKValues"] <= ddict["KMax"])
    exafsSpectrumX = ddict["EXAFSKValues"][exafsIdx]
    exafsSpectrumY = ddict["EXAFSNormalized"][exafsIdx]
    xFT = ddict["FT"]["FTRadius"]
    yFT = ddict["FT"]["FTIntensity"]

    entry = posixpath.join(entry0, "XAS")
    e0Path = posixpath.join(entry, "edge")
    jumpPath = posixpath.join(entry, "jump")
    spectrumXPath = posixpath.join(entry, "spectrum", "energy")
    spectrumYPath = posixpath.join(entry, "spectrum", "mu")
    normalizedXPath = posixpath.join(entry, "normalized", "energy")
    normalizedYPath = posixpath.join(entry, "normalized", "mu")
    exafsXPath = posixpath.join(entry, "exafs", "k")
    exafsYPath = posixpath.join(entry, "exafs", "signal")
    ftXPath = posixpath.join(entry, "FT", "Radius")
    ftYPath = posixpath.join(entry, "FT", "Intensity")

    e0 = out.require_dataset(e0Path,
                             shape=data.shape[:-1],
                             dtype=numpy.float32,
                             chunks=None,
                             compression=None)
    jump = out.require_dataset(jumpPath,
                               shape=data.shape[:-1],
                               dtype=numpy.float32,
                               chunks=None,
                               compression=None)
    shape = list(data.shape[:-1]) + [usedEnergy.size]
    spectrumX = out.require_dataset(spectrumXPath,
                               shape=shape,
                               dtype=numpy.float32,
                               chunks=None,
                               compression=None)
    spectrumY = out.require_dataset(spectrumYPath,
                               shape=shape,
                               dtype=numpy.float32,
                               chunks=None,
                               compression=None)
    shape = list(data.shape[:-1]) + [normalizedSpectrumX.size]
    normalizedX = out.require_dataset(normalizedXPath,
                               shape=shape,
                               dtype=numpy.float32,
                               chunks=None,
                               compression=None)
    normalizedY = out.require_dataset(normalizedYPath,
                               shape=shape,
                               dtype=numpy.float32,
                               chunks=None,
                               compression=None)
    shape = list(data.shape[:-1]) + [exafsSpectrumX.size]
    exafsX = out.require_dataset(exafsXPath,
                                 shape=shape,
                                 dtype=numpy.float32,
                                 chunks=None,
                                 compression=None)
    exafsY = out.require_dataset(exafsYPath,
                                 shape=shape,
                                 dtype=numpy.float32,
                                 chunks=None,
                                 compression=None)
    shape = list(data.shape[:-1]) + [xFT.size]
    ftX = out.require_dataset(ftXPath,
                                 shape=shape,
                                 dtype=numpy.float32,
                                 chunks=None,
                                 compression=None)
    ftY = out.require_dataset(ftYPath,
                                 shape=shape,
                                 dtype=numpy.float32,
                                 chunks=None,
                                 compression=None)
    t0 = time.time()
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
        #for j in range(100):
            analyzer.setSpectrum(energy, data[i, j])
            ddict = analyzer.processSpectrum()
            e0[i, j] = ddict["Edge"]
            jump[i, j] = ddict["Jump"]
            normalizedX[i, j] = ddict["NormalizedEnergy"][normalizedIdx]
            normalizedX[i, j] = ddict["NormalizedMu"][normalizedIdx]
            exafsX[i, j] = ddict["EXAFSKValues"][exafsIdx]
            exafsY[i, j] = ddict["EXAFSNormalized"][exafsIdx]
            ftX[i, j] = ddict["FT"]["FTRadius"]
            ftY[i, j] = ddict["FT"]["FTIntensity"]
    elapsed = time.time() - t0
    print("Elapsed = ", elapsed)
    print("%.2f Spectra per second" % (data.shape[0] * data.shape[1]/elapsed))
out.flush()
out.close()
h5.close()
print("Total elapsed = ", time.time() - t0Total)
