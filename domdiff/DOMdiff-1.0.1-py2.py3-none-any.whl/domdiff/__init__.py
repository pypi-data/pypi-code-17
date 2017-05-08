#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
This module provides functions to find subtrees of a DOM that got removed/added
between two HTML pages, (e.g. after an update of a website).
'''


from bs4 import BeautifulSoup, Tag, NavigableString, Comment


def diff(page1, page2):
    '''
    Returns a tuple (removals, additions) where removals are dom tree elements
    that exist in `page1` but not `page2` and additions are the reverse.

    :param page1: The first HTML page.
    :type page1: str or :py:class:`bs4.BeautifulSoup`
    :param page2: The second HTML page.
    :type page2: str or :py:class:`bs4.BeautifulSoup`
    :returns: A tuple of lists of :py:class:`bs4.Tag` objects.
    :rtype: Tuple
    '''
    soup1 = _soupify(page1)
    soup2 = _soupify(page2)
    return removals(soup1.html, soup2.html), additions(soup1.html, soup2.html)


def additions(soup1, soup2):
    '''
    Returns a list of :py:class:`bs4.Tag` objects that got exist in `soup2`
    but not in `soup1`, i.e. additions in `soup2`.

    :param soup1: The first HTML page as the root html tag.
    :type soup1: :py:class:`bs4.Tag`
    :param soup2: The second HTML page as the root html tag.
    :type soup2: :py:class:`bs4.Tag`
    :returns: A list of dom subtrees as their top tag that got added.
    :rtype: list
    '''
    path_element_list1 = _generate_path_list(soup1)
    paths1 = {path:element for path, element in path_element_list1}
    result = []
    for element in _find_new_domparts(soup2, paths1):
        if element not in result:
            result.append(element)
    nested_elements = []
    for element in result:
        for parent in element.parents:
            if parent in result:
                nested_elements.append(element)
    for element in nested_elements:
        result.remove(element)
    return result


def removals(soup1, soup2):
    '''
    Invocates additions with reverse order.

    :param soup1: The first HTML page as the root html tag.
    :type soup1: :py:class:`bs4.Tag`
    :param soup2: The second HTML page as the root html tag.
    :type soup2: :py:class:`bs4.Tag`
    :returns: A list of dom subtrees as their top tag that got removed.
    :rtype: list
    '''
    return additions(soup2, soup1)


def _generate_path_list(element):
    '''
    Recursively generate a list of tuples containing a string-representation
    of the DOM element represented by a `bs4.Tag` object and the `bs4.Tag`
    element itself.

    :param element: The :py:class:`bs4.Tag` object from which downwards to
        generate the list.
    :type element: Any :py:class:`bs4.*` object
    :returns: A generator of (str, :py:class:`bs4.Tag`) typles.
    :rtype: iterable
    '''
    path = _path_representation(element)
    if path:
        yield path, element
    if isinstance(element, Tag):
        for child in element.children:
            for path, _ in _generate_path_list(child):
                if path:
                    yield path, child


def _path_representation(element):
    '''
    Create a string representation of the `element`'s path up to the root
    of the DOM tree.

    :param element: The element of which to create the string representation.
    :type element: Any :py:class:`bs4.*` object
    :returns: A string representing the path.
    :rtype: str
    '''
    path = []
    string_repr = _stringify(element)
    if string_repr:
        path.append(string_repr)
    for parent in element.parents:
        if parent.name == '[document]':
            continue
        path.append(parent.name)
    return '.'.join(reversed(path))


def _stringify(element):
    '''
    Create a string representation of the element, including all attributes.
    Returns `None` for elements of neither `bs4.Tag` or `bs4.NavigableString`
    type.

    :param element: Element for which to create the string representation.
    :type element: Any :py:class:`bs4.*` object
    :returns: A string representation.
    :rtype: str
    '''
    if isinstance(element, Tag):
        attrs = ';'.join(
            ['%s=%s' % (name, 
                        ','.join(values) if isinstance(values, list) else values)
             for name, values in element.attrs.iteritems()]
        )
        if attrs:
            return '/'.join([element.name,attrs])
        else:
            return element.name
    elif isinstance(element, NavigableString):
        return element.string.strip()
    else:
        return None


def _find_new_domparts(element, paths):
    '''
    Recursively iterates through the descendants of `element` and yields
    those descendants whose string representation is not in paths. If this
    is the case for a `bs4.NavigableString`, the string's parent element
    is yielded.

    :param element: Element whose descendants to check.
    :type element: Any :py:class:`bs4.*` object
    :param paths: A dict mapping elements' string representation to
        `bs4.*` objects
    :type paths: dict
    :returns: An iterator of newly added `bs4.Tag` elements.
    :rtype: iterable
    '''
    path = _path_representation(element)
    if path:
        if path in paths:
            if isinstance(element, Tag):
                for child in element.children:
                    for element in _find_new_domparts(child, paths):
                        yield element
        else:
            if isinstance(element, Tag):
                yield element
            elif isinstance(element, NavigableString):
                yield element.parent


def _soupify(page):
    '''
    Check if the object `page` is already a BeautifulSoup object.
    If not, it is assumed to be an HTML string and a soup of it is returned.

    :param page: The object to convert to `BeautifulSoup` if necessary.
    :type page: str or BeautifulSoup.
    :returns: A BeautifulSoup representation of the page
    :rtype: :py:class:`bs4.BeautifulSoup`
    '''
    if not isinstance(page, BeautifulSoup):
        return BeautifulSoup(page, 'html.parser')
    return page
