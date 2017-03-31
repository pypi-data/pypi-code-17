def p(l, indent=False, lvl=0):
    for f in l:
        if isinstance(f, list):
            p(f, indent, lvl+1)
        else:
            if indent:
                for ts in range(lvl):
                    print('\t', end='')
            print(f)