import librosa


def calcChroma_stft(wav_path):
    y, sr = librosa.load(wav_path)
    chroma_stft = librosa.feature.chroma_stft(y=y, sr=sr)
    return chroma_stft


def calcChroma_cqt(wav_path):
    y, sr = librosa.load(wav_path)
    chroma_cqt = librosa.feature.chroma_cqt(y=y, sr=sr)
    return chroma_cqt


def calcChroma_cens(wav_path):
    y, sr = librosa.load(wav_path)
    chroma_cens = librosa.feature.chroma_cens(y=y, sr=sr)
    return chroma_cens


def calcTonnetz(wav_path):
    y, sr = librosa.load(wav_path)
    y = librosa.effects.harmonic(y)
    tonnetz = librosa.feature.tonnetz(y=y, sr=sr)
    return tonnetz
