import numpy as np
from sklearn.preprocessing import Binarizer

def clasificar_por_umbral_custom(y_probs, umbral):
    binarizer = Binarizer(threshold=umbral)
    return binarizer.transform(y_probs)
