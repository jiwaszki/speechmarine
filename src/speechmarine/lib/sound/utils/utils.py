import numpy as np


@profile
def gain_from_db(db_gain):
    return np.power(10, db_gain / 20)
