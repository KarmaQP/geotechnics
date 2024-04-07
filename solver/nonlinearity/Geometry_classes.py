import numpy as np
import scipy as sp


class FE6:
  def __init__(self, list_node_coor, list_nodes, material=None, sigma=None, index=None):
    self.list_node_coor = list_node_coor
    self.list_nodes = list_nodes
    self.material = material
    self.sigma = sigma
    self.index = index

  # Класс 6-ти узлового плоского КЭ

  def loc_coor_calc(self):
    x_loc = np.zeros((len(self.list_nodes)), dtype=np.float64)
    y_loc = np.zeros((len(self.list_nodes)), dtype=np.float64)
    for k in range(len(self.list_nodes)):
      x_loc[k] = self.list_node_coor[self.list_nodes[k], 0]
      y_loc[k] = self.list_node_coor[self.list_nodes[k], 1]
    return x_loc, y_loc

  def square_calc(self):
    x_loc, y_loc = self.loc_coor_calc()[0:2]
    s = abs((x_loc[1] - x_loc[0]) * (y_loc[2] - y_loc[0]) -
            (x_loc[2] - x_loc[0]) * (y_loc[1] - y_loc[0])) / 2
    return s

  def b1_calc(self):
    b = np.zeros((3, 12), dtype=np.float64)
    x, y = self.loc_coor_calc()
    b[0, 0] = -5 / 3 * (y[2] - y[1])
    b[1, 1] = -5 / 3 * (x[1] - x[2])
    b[0, 2] = -1 / 3 * (y[2] - y[0])
    b[1, 3] = -1 / 3 * (x[0] - x[2])
    b[0, 4] = -1 / 3 * (y[0] - y[1])
    b[1, 5] = -1 / 3 * (x[1] - x[0])
    b[0, 6] = 2 * y[2] + 2 / 3 * y[1] - 8 / 3 * y[0]
    b[1, 7] = 8 / 3 * x[0] - 2 * x[2] - 2 / 3 * x[1]
    b[0, 8] = 2 / 3 * (y[2] - y[1])
    b[1, 9] = 2 / 3 * (x[1] - x[2])
    b[0, 10] = 8 / 3 * y[0] - 2 * y[1] - 2 / 3 * y[2]
    b[1, 11] = 2 * x[1] + 2 / 3 * x[2] - 8 / 3 * x[0]
    for j in range(12):
      if j % 2 == 0:
        b[2, j] = b[1, j + 1]
      if j % 2 == 1:
        b[2, j] = b[0, j - 1]
    b = 1 / ((y[2] - y[0]) * (x[1] - x[0]) - (y[1] - y[0]) * (x[2] - x[0])) * b
    return b

  def b2_calc(self):
    b = np.zeros((3, 12), dtype=np.float64)
    x, y = self.loc_coor_calc()
    b[0, 0] = 1 / 3 * (y[2] - y[1])
    b[1, 1] = 1 / 3 * (x[1] - x[2])
    b[0, 2] = 5 / 3 * (y[2] - y[0])
    b[1, 3] = 5 / 3 * (x[0] - x[2])
    b[0, 4] = -1 / 3 * (y[0] - y[1])
    b[1, 5] = -1 / 3 * (x[1] - x[0])
    b[0, 6] = 8 / 3 * y[1] - 2 / 3 * y[0] - 2 * y[2]
    b[1, 7] = 2 / 3 * x[0] - 8 / 3 * x[1] + 2 * x[2]
    b[0, 8] = 2 * y[0] - 8 / 3 * y[1] + 2 / 3 * y[2]
    b[1, 9] = 8 / 3 * x[1] - 2 * x[0] - 2 / 3 * x[2]
    b[0, 10] = 2 / 3 * (y[0] - y[2])
    b[1, 11] = 2 / 3 * (x[2] - x[0])
    for j in range(12):
      if j % 2 == 0:
        b[2, j] = b[1, j + 1]
      if j % 2 == 1:
        b[2, j] = b[0, j - 1]
    b = 1 / ((y[2] - y[0]) * (x[1] - x[0]) - (y[1] - y[0]) * (x[2] - x[0])) * b
    return b

  def b3_calc(self):
    b = np.zeros((3, 12), dtype=np.float64)
    x, y = self.loc_coor_calc()
    b[0, 0] = 1 / 3 * (y[2] - y[1])
    b[1, 1] = 1 / 3 * (x[1] - x[2])
    b[0, 2] = -1 / 3 * (y[2] - y[0])
    b[1, 3] = -1 / 3 * (x[0] - x[2])
    b[0, 4] = 5 / 3 * (y[0] - y[1])
    b[1, 5] = 5 / 3 * (x[1] - x[0])
    b[0, 6] = 2 / 3 * (y[1] - y[0])
    b[1, 7] = 2 / 3 * (x[0] - x[1])
    b[0, 8] = 8 / 3 * y[2] - 2 / 3 * y[1] - 2 * y[0]
    b[1, 9] = 2 * x[0] + 2 / 3 * x[1] - 8 / 3 * x[2]
    b[0, 10] = 2 / 3 * y[0] + 2 * y[1] - 8 / 3 * y[2]
    b[1, 11] = 8 / 3 * x[2] - 2 * x[1] - 2 / 3 * x[0]
    for j in range(12):
      if j % 2 == 0:
        b[2, j] = b[1, j + 1]
      if j % 2 == 1:
        b[2, j] = b[0, j - 1]
    b = 1 / ((y[2] - y[0]) * (x[1] - x[0]) - (y[1] - y[0]) * (x[2] - x[0])) * b
    return b

  def matrix_csc_transform(self, k_loc):
    # функция составления разреженной матрицы жесткости сжато-столбцового формата CSC
    num_nodes = len(self.list_node_coor[:, 0])
    rrows, ccols = k_loc.shape
    data = k_loc.reshape(rrows * ccols, order='C')
    rows = np.zeros((rrows * ccols))
    for i in range(rrows * ccols):
      rows[i] = self.list_nodes[(i // 2) % (rrows // 2)] * 2 + i % 2
    cols = np.zeros((rrows * ccols))
    for i in range(rrows * ccols):
      cols[i] = self.list_nodes[(i // rrows) // 2] * 2 + (i // rrows) % 2

    transf_matrix = sp.sparse.csc_matrix(
      (data, (cols, rows)), shape=(num_nodes * 2, num_nodes * 2))
    return transf_matrix

  def k_matrix_calc(self):
    b_1 = self.b1_calc()
    b_2 = self.b2_calc()
    b_3 = self.b3_calc()
    s = self.square_calc()
    d1 = self.material.d_matrix(self.sigma[0], self.index[0])
    d2 = self.material.d_matrix(self.sigma[1], self.index[1])
    d3 = self.material.d_matrix(self.sigma[2], self.index[2])
    k_loc = 1 / 3 * s * (b_1.T @ d1 @ b_1 + b_2.T @
                         d2 @ b_2 + b_3.T @ d3 @ b_3)
    return self.matrix_csc_transform(k_loc)

  def r_vector_calc(self):
    num_nodes = len(self.list_node_coor[:, 0])
    s = self.square_calc()
    r_vector = np.zeros((num_nodes * 2), dtype=np.float64)
    for i in range(3):
      r_vector[2 * self.list_nodes[i + 3] + 1] = - \
        self.material.weight * s * 1 / 3
    return r_vector

  def sigma_calc(self, delta):
    b_1 = self.b1_calc()
    b_2 = self.b2_calc()
    b_3 = self.b3_calc()
    delta = delta.reshape((12, 1))
    eps1 = b_1 @ delta
    eps2 = b_2 @ delta
    eps3 = b_3 @ delta
    eps1 = [eps1[0][0], eps1[1][0], eps1[2][0]]
    eps2 = [eps2[0][0], eps2[1][0], eps2[2][0]]
    eps3 = [eps3[0][0], eps3[1][0], eps3[2][0]]

    sigma_int = np.zeros((3, 3), dtype=np.float64)
    index = np.zeros((3, 1), dtype=np.int_)
    tau = np.zeros((3, 1), dtype=np.float64)
    sigma_elast = np.zeros((3, 3), dtype=np.float64)

    sigma_int[0], index[0], tau[0], sigma_elast[0] = self.material.sigma_check(
      self.sigma[0], eps1, self.index[0])
    sigma_int[1], index[1], tau[1], sigma_elast[1] = self.material.sigma_check(
      self.sigma[1], eps2, self.index[1])
    sigma_int[2], index[2], tau[2], sigma_elast[2] = self.material.sigma_check(
      self.sigma[2], eps3, self.index[2])
    return sigma_int, index, tau, sigma_elast

  def epsilon_calc(self, delta):
    b_1 = self.b1_calc()
    b_2 = self.b2_calc()
    b_3 = self.b3_calc()
    delta = delta.reshape((12, 1))
    eps1 = b_1 @ delta
    eps2 = b_2 @ delta
    eps3 = b_3 @ delta
    eps = np.array([[eps1[0][0], eps1[1][0], eps1[2][0]],
                    [eps2[0][0], eps2[1][0], eps2[2][0]],
                    [eps3[0][0], eps3[1][0], eps3[2][0]]], dtype=np.float64)
    return eps

  def r_internal(self, sigma_int):
    num_nodes = len(self.list_node_coor[:, 0])
    b = np.array([self.b1_calc(), self.b2_calc(), self.b3_calc()])
    s = self.square_calc()
    r = np.zeros(12, dtype=np.float64)
    r_int = np.zeros((num_nodes * 2), dtype=np.float64)
    for i in range(3):
      r += 1 / 3 * s * b[i].T @ sigma_int[i]
    for i in range(6):
      r_int[2 * self.list_nodes[i]] = r[2 * i]
      r_int[2 * self.list_nodes[i] + 1] = r[2 * i + 1]
    return r_int


class Polygon:
  def __init__(self, list_coor, list_nodes, material=None, sigma=None, index=None):
    self.list_coor = list_coor
    self.list_nodes = list_nodes
    self.material = material
    self.sigma = sigma
    self.index = index
    self.stiff_mat = sp.sparse.csc_matrix(([0], ([0], [0])), shape=(
      len(self.list_coor[:, 0]) * 2, len(self.list_coor[:, 0]) * 2))
    self.stiff_mat_2 = sp.sparse.csc_matrix(([0], ([0], [0])),
                                            shape=(len(self.list_coor[:, 0]) * 2, len(self.list_coor[:, 0]) * 2))

  def stiff_matrix(self):
    stif_matrix = sp.sparse.csc_matrix(([0], ([0], [0])),
                                       shape=(len(self.list_coor[:, 0]) * 2, len(self.list_coor[:, 0]) * 2))
    for i in range(len(self.list_nodes[:, 0])):
      stif_matrix += FE6(self.list_coor, self.list_nodes[i], self.material,
                         self.sigma[3 * i: 3 * i + 3], self.index[3 * i: 3 * i + 3]).k_matrix_calc()

    return stif_matrix

  def r_glob_vector(self):
    num_nodes = len(self.list_coor[:, 0])
    num_el = len(self.list_nodes[:, 0])
    r_glob = np.zeros((2 * num_nodes), dtype=np.float64)
    for i in range(num_el):
      r_glob += FE6(self.list_coor,
                    self.list_nodes[i], self.material).r_vector_calc()
    return r_glob

  def sigma_calc(self, delta):
    num = len(self.list_nodes[:, 0])
    sigma_int = np.zeros((3 * num, 3), dtype=np.float64)
    index = np.zeros((3 * num, 1), dtype=np.int_)
    tau = np.zeros((3 * num, 1), dtype=np.float64)
    sigma_elast = np.zeros((3 * num, 3), dtype=np.float64)
    for i in range(num):
      (sigma_int[3 * i: 3 * i + 3],
       index[3 * i: 3 * i + 3],
       tau[3 * i: 3 * i + 3],
       sigma_elast[3 * i: 3 * i + 3]) = (FE6(self.list_coor,
                                             self.list_nodes[i],
                                             self.material,
                                             self.sigma[3 * i: 3 * i + 3],
                                             self.index[3 * i: 3 * i + 3]).sigma_calc(delta[i]))
    return sigma_int, index, tau, sigma_elast

  def epsilon_calc(self, delta):
    num = len(self.list_nodes[:, 0])
    epsilon = np.zeros((3 * num, 3), dtype=np.float64)
    for i in range(num):
      epsilon[3 * i: 3 * i + 3] = FE6(self.list_coor,
                                      self.list_nodes[i]).epsilon_calc(delta[i])
    return epsilon

  def r_internal(self, sigma):
    num_nodes = len(self.list_coor[:, 0])
    r = np.zeros((2 * num_nodes), dtype=np.float64)
    num_el = len(self.list_nodes[:, 0])
    for i in range(num_el):
      r += FE6(self.list_coor,
               self.list_nodes[i]).r_internal(sigma[3 * i: 3 * i + 3])
    return r


class Line:
  def __init__(self, list_node_coor, list_nodes, data):
    self.list_node_coor = list_node_coor
    self.data = data
    self.list_nodes = list_nodes

  def stiff_matrix(self):
    pass

  def r_glob_vector(self):
    pass

  def bound_cond(self):
    bc_node_x = None
    bc_node_y = None
    bc = np.zeros((len(self.list_node_coor), 2), dtype=np.int8)

    if 'ux' in self.data["propertyParams"].keys():
      bc_node_x = self.list_nodes
    if 'uy' in self.data["propertyParams"].keys():
      bc_node_y = self.list_nodes

    bc_node_x = np.unique(bc_node_x)
    bc_node_y = np.unique(bc_node_y)

    for i in bc_node_x:
      bc[i, 0] = 1
    for i in bc_node_y:
      bc[i, 1] = 1
    return bc
