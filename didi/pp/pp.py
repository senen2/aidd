import numpy as np
from apiML import *

a = np.array([[1, 1, 0, 0], [0, 1, 0, 0], [0, 1, 1, 1], [1, 1, 1, 1], ])
a = np.array([[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], ])
print bin_to_dec(a)
print np.binary_repr(8000, width=13)

