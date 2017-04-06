def backwards_search(p, cl, rank, total_length):
    """Perform backwards search using pattern p, count lookup cl and rank rank

    reference http://alexbowe.com/fm-index/"""

    start = 0
    end = total_length - 1
    
    for i in range(len(p)-1,-1,-1):
        if end < start:
            break
        
        char = p[i]
        count_for_char = cl[char]
        
        start = count_for_char + rank.rank(start-1, char)
        end = count_for_char + rank.rank(end, char) - 1

    return start, end
