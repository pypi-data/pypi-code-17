#-*- coding: utf-8 -*-
"""
@file
@brief Look into the mail box
"""
import wikipedia
import wptools
import re
from .mokadi_exceptions import WikipediaException


def definition_wikipedia(query, summary=True, lang="fr"):
    """
    Search for the definition of something on wikipedia.

    @param      query       what to search for
    @param      summary     summary or long definition
    @param      lang        language
    @return                 definition
    """
    wikipedia.set_lang("fr")
    if summary:
        res = wikipedia.summary(query, sentences=1)
        return res.strip("# ")
    else:
        res = wikipedia.search(query, results=1)
        if len(res) == 0:
            raise WikipediaException(
                "Unable to find a page for '{0}'".format(query))
        title = res[0]
        page = wikipedia.page(title)
        if page is None or not hasattr(page, "content"):
            raise WikipediaException(
                "Unable to find a page for '{0}' (2)".format(page))
        page = page.content
        if lang == "fr":
            if "== Notes et références ==" in page:
                page = page.split("== Notes et références ==")[0]
            if "== Voir aussi ==" in page:
                page = page.split("== Notes et références ==")[0]
        return page


def suggestions_wikipedia(query, lang="fr"):
    """
    Suggestions for something on wikipedia.

    @param      query       what to search for
    @param      lang        language
    @return                 definition
    """
    wikipedia.set_lang("fr")
    return wikipedia.search(query, results=10)


def synonyms_wiktionary(name, lang="fr"):
    """
    Returns the definition from Wiktionary.

    @param      name        name to look for
    @param      lang        language
    @return                 definition

    `Wiktionay API <https://en.wiktionary.org/w/api.php>`_.
    """
    page = wptools.page(name, wiki='{0}.wiktionary.org'.format(
        lang), lang=lang, silent=True)
    page.get_parse()
    text = page.wikitext
    syn = "==== {{S|synonymes}} ===="
    if syn not in text:
        return None
    text = text.split(syn)[1].split("====")[0]
    reg = re.compile("[[]{2}(.*?)[]]{2}")
    res = reg.findall(text)
    return res
