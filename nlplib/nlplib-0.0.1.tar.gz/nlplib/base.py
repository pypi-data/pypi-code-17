# -*- coding: utf-8 -*-
import langid


def language_langid(text):
    """Detect language of content

    Args:
        text (unicode): Input text

    Returns:
        str: Language"""
    if text is None:
        return None
    lang, value = langid.classify(text)
    return lang
