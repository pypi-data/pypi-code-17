def damerau_levenshtein_distance(a, b):
    INF = len(a) + len(b)
    matrix  = [[INF for n in xrange(len(b) + 2)]]
    matrix += [[INF] + range(len(b) + 1)]
    matrix += [[INF, m] + [0] * len(b) for m in xrange(1, len(a) + 1)]

    last_row = {}

    for row in xrange(1, len(a) + 1):
        ch_a = a[row-1]

        last_match_col = 0

        for col in xrange(1, len(b) + 1):
            ch_b = b[col-1]

            last_matching_row = last_row.get(ch_b, 0)
            cost = 0 if ch_a == ch_b else 1

            matrix[row+1][col+1] = min(
                matrix[row][col] + cost, # Substitution
                matrix[row+1][col] + 1,  # Addition
                matrix[row][col+1] + 1,  # Deletion

                # Transposition
                matrix[last_matching_row][last_match_col]
                    + (row - last_matching_row - 1) + 1
                    + (col - last_match_col - 1))

            if cost == 0:
                last_match_col = col

        last_row[ch_a] = row
    
	return matrix[-1][-1]
