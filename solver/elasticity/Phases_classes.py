import numpy as np
import scipy as sp
from solver.elasticity.Geometry_classes import Polygon
from solver.elasticity.Models_classes import soil_model_get
import time


class Phase:
  def __init__(self, phase):
    self.phase = phase

  def boundary(self, node_list, list_node_coor):
    num_nodes = len(list_node_coor)
    bc = np.zeros((num_nodes, 2))
    bc_node_x = []
    bc_node_y = []
    for i in self.phase['lines']:
      if (i['phaseActivity']) and ('ux' in i['propertyParams'].keys()):
        bc_node_x += node_list[i['name']]
      if (i['phaseActivity']) and ('uy' in i['propertyParams'].keys()):
        bc_node_y += node_list[i['name']]
    nodes_x = []
    nodes_y = []
    for i in bc_node_x:
      nodes_x += i
    for i in bc_node_y:
      nodes_y += i
    for i in nodes_x:
      bc[i, 0] = 1
    for i in nodes_y:
      bc[i, 1] = 1
    return bc

  def k_glob_sum(self, list_node_coor, list_node_polygon, list_node_line):
    num_nodes = len(list_node_coor[:, 0])
    k_glob = np.zeros((num_nodes * 2, num_nodes * 2), dtype=np.float64)
    for i in self.phase['soils']:
      if i['phaseActivity']:
        mat = soil_model_get(i)
        k_glob += Polygon.stiff_matrix(mat=mat, list_nodes=list_node_polygon[i['name']],
                                       node_bc=self.boundary(node_list=list_node_line,
                                                             list_node_coor=list_node_coor),
                                       list_node_coor=list_node_coor)
    return k_glob

  def r_glob_sum(self, list_node_coor, list_node_polygon, list_node_line):
    num_nodes = len(list_node_coor[:, 0])
    r_glob = np.zeros(num_nodes * 2, dtype=np.float64)
    for i in self.phase['soils']:
      if i['phaseActivity']:
        mat = soil_model_get(i)
        r_glob += Polygon.r_glob_vector(mat=mat, list_nodes=list_node_polygon[i['name']],
                                        node_bc=self.boundary(node_list=list_node_line,
                                                              list_node_coor=list_node_coor),
                                        list_node_coor=list_node_coor)
    return r_glob

  def le_solve(self, list_node_coor, list_node_polygon, list_node_line):
    print('=============================================================================')
    print('Начинается работа функции k_glob_sum (le_solve)!')
    start = time.perf_counter()

    k_matrix = self.k_glob_sum(
      list_node_coor, list_node_polygon, list_node_line)

    finish = time.perf_counter()
    print(f'Время работы k_glob_sum (le_solve): {str(finish - start)}')

    print('=============================================================================')
    print('Начинается работа функции r_glob_sum (le_solve)!')
    start = time.perf_counter()

    d_r_vector = self.r_glob_sum(
      list_node_coor, list_node_polygon, list_node_line)

    finish = time.perf_counter()
    print(f'Время работы r_glob_sum (le_solve): {str(finish - start)}')

    print('=============================================================================')
    print('Начинается работа функции scipy.sparce.lanalg.bicg (le_solve)!')
    start = time.perf_counter()

    d_x_vector, exit_code = sp.sparse.linalg.bicg(k_matrix, d_r_vector)

    finish = time.perf_counter()
    print(
      f'Время работы scipy.sparce.lanalg.bicg (le_solve): {str(finish - start)}')
    print('=============================================================================')
    return d_x_vector

  def delta(self, d_x, list_node_polygon):
    delta = {}
    for i in self.phase['soils']:
      if i['phaseActivity']:
        row, col = list_node_polygon[i['name']].shape
        delta[i['name']] = np.zeros((row, 2 * col), dtype=np.float64)
    for i in delta.keys():
      for j, string in enumerate(delta[i]):
        for k in range(6):
          delta[i][j, 2 * k] = d_x[2 * list_node_polygon[i][j, k]]
          delta[i][j, 2 * k + 1] = d_x[2 * list_node_polygon[i][j, k] + 1]
    return delta

  def epsilon(self, d_x, list_node_polygon, list_node_coor):
    delta = self.delta(d_x, list_node_polygon)
    epsilon = {}
    for i in self.phase['soils']:
      if i['phaseActivity']:
        epsilon[i['name']] = Polygon().epsilon(list_nodes=list_node_polygon[i['name']], delta=delta[i['name']],
                                               list_node_coor=list_node_coor)
    return epsilon

  def sigma(self, d_x, list_node_polygon, list_node_coor):
    delta = self.delta(d_x, list_node_polygon)
    sigma = {}
    mat = None
    for i in self.phase['soils']:
      if i['phaseActivity']:
        mat = soil_model_get(i)
        sigma[i['name']] = Polygon().sigma(list_nodes=list_node_polygon[i['name']], delta=delta[i['name']],
                                           list_node_coor=list_node_coor, d_e=mat.d_matrix())
    return sigma
