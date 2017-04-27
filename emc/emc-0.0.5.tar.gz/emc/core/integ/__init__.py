from numpy import set_printoptions

float_formatter = lambda x: "%.4f" %x
set_printoptions(formatter={'float_kind':float_formatter})