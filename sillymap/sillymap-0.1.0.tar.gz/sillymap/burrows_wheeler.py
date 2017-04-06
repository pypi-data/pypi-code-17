
def burrows_wheeler(text):
    """Calculates the burrows wheeler transform of <text>.

    returns the burrows wheeler string and the suffix array indices
    The text is assumed to not contain the character $"""

    text += "$"
    all_permutations = []
    for i in range(len(text)):
        all_permutations.append((text[i:] + text[:i],i))

    all_permutations.sort()
    bw_l = [] # burrows wheeler as list
    sa_i = [] # suffix array indices

    for w,j in all_permutations:
        bw_l.append(w[-1])
        sa_i.append(j)

    return "".join(bw_l), sa_i
