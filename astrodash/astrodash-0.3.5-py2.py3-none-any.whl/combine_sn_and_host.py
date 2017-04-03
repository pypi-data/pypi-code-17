from dash.preprocessing import ReadSpectrumFile, ProcessingTools, PreProcessSpectrum


class CombineSnAndHost(object):
    def __init__(self, snFile, galFile, w0, w1, nw):
        self.w0 = w0
        self.w1 = w1
        self.nw = nw
        self.snReadSpectrumFile = ReadSpectrumFile(snFile, w0, w1, nw)
        self.galReadSpectrumFile = ReadSpectrumFile(galFile, w0, w1, nw).
        self.snSpectrum = self.snReadSpectrumFile.file_extension()
        self.galSpectrum = self.galReadSpectrumFile.file_extension()

    def _normalise_spectra(self):
        self.snSpectrum = self.

    def _overlapped_spectra(self):
        self.snIndexes = ProcessingTools(self.snSpectrum)
        self.galIndexes = ProcessingTools(self.galSpectrum)

        minIndex = min(self.snIndexes[0], self.galIndexes[0])
        maxIndex = max(self.snIndexes[1], self.galIndexes[1])

        return self.snIndexes[minIndex:maxIndex], self.galIndexes[minIndex:maxIndex]


    def sn_plus_gal(self, snCoeff, galCoeff):
        snSpectrumOverlapped, galSpectrumOverlapped = self._overlapped_spectra()

        combinedSpectrum = 0




