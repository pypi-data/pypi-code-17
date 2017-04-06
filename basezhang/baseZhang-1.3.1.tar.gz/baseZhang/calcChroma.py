import fromLibrosa


def calcChroma_stft(wav_path):
    y, sr = fromLibrosa.load(wav_path)
    chroma_stft = fromLibrosa.chroma_stft(y=y, sr=sr)
    return chroma_stft


def calcChroma_cqt(wav_path):
    y, sr = fromLibrosa.load(wav_path)
    chroma_cqt = fromLibrosa.chroma_cqt(y=y, sr=sr)
    return chroma_cqt


def calcChroma_cens(wav_path):
    y, sr = fromLibrosa.load(wav_path)
    chroma_cens = fromLibrosa.chroma_cens(y=y, sr=sr)
    return chroma_cens


def calcTonnetz(wav_path):
    y, sr = fromLibrosa.load(wav_path)
    y = fromLibrosa.harmonic(y)
    tonnetz = fromLibrosa.tonnetz(y=y, sr=sr)
    return tonnetz
