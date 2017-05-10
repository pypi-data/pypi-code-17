from math import log, exp

def bounded_sigmoid(x, lower_bound=35., upper_bound=35.):
    return 1. \
           / (1. + exp(-max(min(x, lower_bound), -upper_bound)))

def log_loss(p, y):
    p = max(min(p, 1. - 10e-15), 10e-15)
    return -log(p) if y == 1. else -log(1. - p)