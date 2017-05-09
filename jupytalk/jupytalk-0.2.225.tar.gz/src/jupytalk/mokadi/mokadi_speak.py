"""
@file
@brief Synthetize voice.
"""


def speak(text, lang="fr-FR", voice="", filename=None):
    """
    Text to speech.

    @param      text        text to speak
    @param      lang        language
    @param      voice       voice name
    @param      filename    filename (to save the results)

    See `SpeechSynthesizer <https://msdn.microsoft.com/fr-fr/library/system.speech.synthesis.speechsynthesizer(v=vs.110).aspx>`_.
    """
    from ensae_teaching_cs.pythonnet import vocal_synthesis
    vocal_synthesis(text, lang=lang, voice=voice, filename=filename)
