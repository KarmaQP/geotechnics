import numpy as np
import scipy as sp


class FiniteElement6:
  # Класс 6-ти узлового плоского КЭ

  @staticmethod
  def loc_coor_calc(list_nodes, list_node_coor):
    x_loc = np.zeros((len(list_nodes)), dtype=np.float64)
    y_loc = np.zeros((len(list_nodes)), dtype=np.float64)
    for k in range(len(list_nodes)):
      x_loc[k] = list_node_coor[list_nodes[k], 0]
      y_loc[k] = list_node_coor[list_nodes[k], 1]
    return x_loc, y_loc

  def square_calc(self, list_nodes, list_node_coor):
    x_loc, y_loc = self.loc_coor_calc(list_nodes, list_node_coor)[0:2]
    s = abs((x_loc[1] - x_loc[0]) * (y_loc[2] - y_loc[0]) -
            (x_loc[2] - x_loc[0]) * (y_loc[1] - y_loc[0])) / 2
    return s

  def b1_calc(self, list_nodes, list_node_coor):
    b = np.zeros((3, 12), dtype=np.float64)
    x, y = self.loc_coor_calc(list_nodes, list_node_coor)
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

  def b2_calc(self, list_nodes, list_node_coor):
    b = np.zeros((3, 12), dtype=np.float64)
    x, y = self.loc_coor_calc(list_nodes, list_node_coor)
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

  def b3_calc(self, list_nodes, list_node_coor):
    b = np.zeros((3, 12), dtype=np.float64)
    x, y = self.loc_coor_calc(list_nodes, list_node_coor)
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

  @staticmethod
  def matrix_csc_transform(k_loc, list_nodes, list_node_coor):
    # функция составления разреженной матрицы жесткости сжато-столбцового формата CSC
    num_nodes = len(list_node_coor[:, 0])
    rrows, ccols = k_loc.shape
    data = k_loc.reshape(rrows * ccols, order='C')
    rows = np.zeros((rrows * ccols))
    for i in range(rrows * ccols):
      rows[i] = list_nodes[(i // 2) % (rrows // 2)] * 2 + i % 2
    cols = np.zeros((rrows * ccols))
    for i in range(rrows * ccols):
      cols[i] = list_nodes[(i // rrows) // 2] * 2 + (i // rrows) % 2

    transf_matrix = sp.sparse.csc_matrix(
      (data, (cols, rows)), shape=(num_nodes * 2, num_nodes * 2))
    return transf_matrix

  def k_local_matrix_calc(self, d_matrix, list_nodes, list_node_coor):
    b_1 = self.b1_calc(list_nodes, list_node_coor)
    b_2 = self.b2_calc(list_nodes, list_node_coor)
    b_3 = self.b3_calc(list_nodes, list_node_coor)
    s = self.square_calc(list_nodes, list_node_coor)
    k_loc = 1 / 3 * s * (b_1.T @ d_matrix @ b_1 + b_2.T @
                         d_matrix @ b_2 + b_3.T @ d_matrix @ b_3)
    return self.matrix_csc_transform(k_loc, list_nodes, list_node_coor)

  def r_loc_vector_calc(self, weight, list_nodes, list_node_coor):
    num_nodes = len(list_node_coor[:, 0])
    s = self.square_calc(list_nodes, list_node_coor)
    r_vector = np.zeros((num_nodes * 2), dtype=np.float64)
    for i in range(6):
      r_vector[2 * list_nodes[i] + 1] = weight * s * 1 / 6
    return r_vector

  def epsilon(self, list_nodes, delta, list_node_coor):
    b_1 = self.b1_calc(list_nodes, list_node_coor)
    b_2 = self.b2_calc(list_nodes, list_node_coor)
    b_3 = self.b3_calc(list_nodes, list_node_coor)
    delta = delta.reshape((12, 1))
    eps1 = b_1 @ delta
    eps2 = b_2 @ delta
    eps3 = b_3 @ delta
    eps1 = [eps1[0][0], eps1[1][0], eps1[2][0]]
    eps2 = [eps2[0][0], eps2[1][0], eps2[2][0]]
    eps3 = [eps3[0][0], eps3[1][0], eps3[2][0]]
    return eps1, eps2, eps3

  def sigma(self, list_nodes, delta, list_node_coor, d_e):
    b_1 = self.b1_calc(list_nodes, list_node_coor)
    b_2 = self.b2_calc(list_nodes, list_node_coor)
    b_3 = self.b3_calc(list_nodes, list_node_coor)
    delta = delta.reshape((12, 1))
    eps1 = b_1 @ delta
    eps2 = b_2 @ delta
    eps3 = b_3 @ delta
    sig1 = d_e @ eps1
    sig2 = d_e @ eps2
    sig3 = d_e @ eps3
    sig1 = [sig1[0][0], sig1[1][0], sig1[2][0]]
    sig2 = [sig2[0][0], sig2[1][0], sig2[2][0]]
    sig3 = [sig3[0][0], sig3[1][0], sig3[2][0]]
    return sig1, sig2, sig3


class Polygon:
  @staticmethod
  def stiff_matrix(mat, list_nodes, node_bc, list_node_coor):
    num_nodes = len(list_node_coor[:, 0])
    stiff_matrix = np.zeros((num_nodes * 2, num_nodes * 2), dtype=np.float64)
    for i in range(len(list_nodes[:, 0])):
      stiff_matrix += FiniteElement6().k_local_matrix_calc(mat.d_matrix(),
                                                           list_nodes[i], list_node_coor)
    for i in range(len(node_bc[:, 0])):
      if node_bc[i, 0] == 1:
        stiff_matrix[2 * i] = 0
        stiff_matrix[2 * i, 2 * i] = 1
      if node_bc[i, 1] == 1:
        stiff_matrix[2 * i + 1] = 0
        stiff_matrix[2 * i + 1, 2 * i + 1] = 1
    return stiff_matrix

  @staticmethod
  def r_glob_vector(mat, list_nodes, node_bc, list_node_coor):
    num_nodes = len(list_node_coor[:, 0])
    r_glob = np.zeros((2 * num_nodes), dtype=np.float64)
    el = None
    if len(list_nodes[0]) == 3:
      # el = FiniteElement3()
      pass
    elif len(list_nodes[0]) == 6:
      el = FiniteElement6()
    for i in range(len(list_nodes[:, 0])):
      r_glob += el.r_loc_vector_calc(mat.weight, list_nodes[i], list_node_coor)
    for i in range(len(node_bc[:, 0])):
      if node_bc[i, 0] == 1:
        r_glob[2 * i] = 0
      if node_bc[i, 1] == 1:
        r_glob[2 * i + 1] = 0
    return r_glob

  @staticmethod
  def epsilon(list_nodes, delta, list_node_coor):
    num = len(list_nodes[:, 0])
    eps = np.zeros((3 * num, 3), dtype=np.float64)
    for i in range(num):
      eps1, eps2, eps3 = FiniteElement6().epsilon(
        list_nodes[i], delta[i], list_node_coor)
      eps[3 * i] = eps1
      eps[3 * i + 1] = eps2
      eps[3 * i + 2] = eps3
    return eps

  @staticmethod
  def sigma(list_nodes, delta, list_node_coor, d_e):
    num = len(list_nodes[:, 0])
    sigma = np.zeros((3 * num, 3), dtype=np.float64)
    for i in range(num):
      sig1, sig2, sig3 = FiniteElement6().sigma(
        list_nodes[i], delta[i], list_node_coor, d_e)
      sigma[3 * i] = sig1
      sigma[3 * i + 1] = sig2
      sigma[3 * i + 2] = sig3
    return sigma
