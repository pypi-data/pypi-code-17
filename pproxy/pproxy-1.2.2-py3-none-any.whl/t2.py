def PiDigits():
    k, l, n, q, r, t = 1, 3, 3, 1, 0, 1
    nr = 16 * (r - t * n)
    n = 16 * (3 * q + r) // t - 16 * n
    q *= 16
    r = nr
    while 1:
        tn = t * n
        if 4 * q + r - t < tn:
            yield n
            nr = 16 * (r - tn)
            n = 16 * (3 * q + r) // t - 16 * n
            q *= 16
        else:
            t *= l
            nr = (2 * q + r) * l
            nn = (q * (7 * k) + 2 + r * l) // t
            q *= k
            l += 2
            k += 1
            n = nn
        r = nr
