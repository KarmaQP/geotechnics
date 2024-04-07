import numpy as np


class ModelLE:
    # Класс модели Linear Elastic
    def __init__(self, dead, e_ur, v_ur):
        self.dead = dead
        self.e_ur = e_ur
        self.v_ur = v_ur

    def d_matrix(self):
        d_e = self.e_ur / ((1 - 2 * self.v_ur) * (1 + self.v_ur)) * np.array([[1 - self.v_ur, self.v_ur, 0],
                                                                              [self.v_ur, 1 - self.v_ur, 0],
                                                                              [0, 0, (1 - 2 * self.v_ur) / 2]])
        return d_e


def soil_model_get(soil):
    material = None
    for i in soil['material'].keys():
        name_mat = i
    if soil['material'][name_mat]['mechParameter'] == 'linear-elastic':
        material = ModelLE(dead=soil['material'][name_mat]['weight'],
                           e_ur=soil['material'][name_mat]['elasticModulus'],
                           v_ur=soil['material'][name_mat]['poisson'])
    return material
