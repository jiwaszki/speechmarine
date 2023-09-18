import numpy as np


def gain_from_db(db_gain):
    return np.power(10, db_gain / 20)
