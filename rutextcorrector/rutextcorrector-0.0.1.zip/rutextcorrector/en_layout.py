# -*- coding: utf-8 -*-

en_ru_dict = {
    '~': u'Ё', "`": u'ё', '@': u'"', '#': u'№', '$': u';', '^': u':', '&': u'\?', 'Q': u'Й', 'q': u'й', 'W': u'Ц', 'w': u'ц',
    'E': u'У', 'e': u'у', 'R': u'К', 'r': u'к', 'T': u'Е', 't': u'е', 'Y': u'Н', 'y': u'н', 'U': u'Г', 'u': u'г',
    'I': u'Ш', 'i': u'ш', 'O': u'Щ', 'o': u'щ', 'P': u'З', 'p': u'з', '{': u'Х', '[': u'х', '}': u'Ъ', ']': u'ъ', '|': u'/',
    'A': u'Ф', 'a': u'ф', 'S': u'Ы', 's': u'ы', 'D': u'В', 'd': u'в', 'F': u'А', 'f': u'а', 'G': u'П', 'g': u'п',
    'H': u'Р', 'h': u'р', 'J': u'О', 'j': u'о', 'K': u'Л', 'k': u'л', 'L': u'Д', 'l': u'д',
    '\:': u'Ж', '\;': u'ж', '"': u'Э', "'": u'э', 'Z': u'Я', 'z': u'я', 'X': u'Ч', 'x': u'ч', 'C': u'С', 'c': u'с',
    'V': u'М', 'v': u'м', 'B': u'И', 'b': u'и', 'N': u'Т', 'n': u'т', 'M': u'Ь', 'm': u'ь', '<': u'Б', '\,': u'б',
    '>': u'Ю', '\.': u'ю', '\?': u'\,', '/': u'.'
}


def en_to_ru_layout(src):
    result = ''
    for c in src:
        result += en_ru_dict.get(c, c)
    return result


def run(src):
    """
    Run function for module
    :param src: 
    :return: 
    """
    return en_to_ru_layout(src)