"""
@file
@brief Record a couple of seconds and returns the raw stream.
"""
import io
import wave
from pyquickhelper.loghelper import noLOG


def record_speech(RECORD_SECONDS=5, CHUNK=1024, FORMAT=None,
                  CHANNELS=2, RATE=44100,
                  WAVE_OUTPUT_FILENAME=None, fLOG=noLOG):
    """
    Records 5 seconds by default and returns the bytes which
    contains that sound.

    @param      RECORD_SECONDS          number of seconds to record
    @param      WAVE_OUTPUT_FILENAME    if not None, also saves the result as a filename
    @return                             bytes

    See `pyaudio <http://people.csail.mit.edu/hubert/pyaudio/>`_
    for the others parameters.
    """
    import pyaudio
    if FORMAT is None:
        FORMAT = pyaudio.paInt16
    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    fLOG("* recording")

    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    fLOG("* done recording")

    stream.stop_stream()
    stream.close()
    p.terminate()

    if WAVE_OUTPUT_FILENAME is not None:
        wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()

    st = io.BytesIO()
    wf = wave.open(st, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    return st.getvalue()


def play_speech(filename_or_bytes, CHUNK=1024):
    """
    Play a way

    @param      filename_or_bytes  wav file or bytes

    See `pyaudio <http://people.csail.mit.edu/hubert/pyaudio/>`_
    for the others parameters.
    """

    if isinstance(filename_or_bytes, str):
        wf = wave.open(filename_or_bytes, 'rb')
    else:
        st = io.BytesIO(filename_or_bytes)
        wf = wave.open(st, 'rb')

    import pyaudio
    p = pyaudio.PyAudio()

    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    data = wf.readframes(CHUNK)

    while len(data) > 0:
        stream.write(data)
        data = wf.readframes(CHUNK)

    stream.stop_stream()
    stream.close()

    p.terminate()
