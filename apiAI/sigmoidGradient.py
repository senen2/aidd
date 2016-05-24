import numpy as np
import sigmoid as sig

def sigmoidGradient(z):
    return sig.sigmoid(z) * (1 - sig.sigmoid(z))