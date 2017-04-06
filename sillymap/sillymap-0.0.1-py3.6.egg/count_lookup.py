from collections import Counter

def count_lookup(text):
    """Returns a lookup table for c, returning the 
    number of characthers in text lexically smaller than c.
    """
    char_count = Counter(text)
    lookup = {}

    current_count = 0
    for c in sorted(list(set(text))):
        lookup[c] = current_count
        current_count += char_count[c]

    return lookup
