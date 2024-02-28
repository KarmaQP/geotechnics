import numpy as np


class ModelLE:
  # Класс модели Linear Elastic
  def __init__(self, weight=None, e_ur=None, v_ur=None):
    self.weight = weight
    self.e_ur = e_ur
    self.v_ur = v_ur

  def d_matrix(self):
    d_e = self.e_ur / ((1 - 2 * self.v_ur) * (1 + self.v_ur)) * np.array([[1 - self.v_ur, self.v_ur, 0],
                                                                          [self.v_ur, 1 -
                                                                           self.v_ur, 0],
                                                                          [0, 0, (1 - 2 * self.v_ur) / 2]])
    return d_e


class ModelMC(ModelLE):
  # Класс модели Mohr-Coulomb
  def __init__(self, c, fi, weight, e_ur, v_ur):
    super().__init__(weight, e_ur, v_ur)
    self.c = c
    self.fi = fi


def soil_model_get(soil):
  material = None
  for i in soil['material'].keys():
    name_mat = i
  if soil['material'][name_mat]['mechParameter'] == 'linear-elastic':
    material = ModelLE(weight=soil['material'][name_mat]['weight'],
                       e_ur=soil['material'][name_mat]['elasticModulus'],
                       v_ur=soil['material'][name_mat]['poisson'])
  return material
