import numpy as np
import scipy as sp
from solver.Geometry_classes import Polygon
from solver.Models_classes import soil_model_get


def boundary(lines_node_list, cur_phase, list_coor):
  num_nodes = len(list_coor)
  bc = np.zeros((num_nodes, 2))
  bc_node_x = []
  bc_node_y = []
  for i in cur_phase['lines']:
    if (i['phaseActivity']) and ('ux' in i['propertyParams'].keys()):
      bc_node_x += lines_node_list[i['name']]
    if (i['phaseActivity']) and ('uy' in i['propertyParams'].keys()):
      bc_node_y += lines_node_list[i['name']]
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


class PhasePlastic:
  def __init__(self, cur_phase):
    self.cur_phase = cur_phase

  def k_glob_sum(self, list_coor, polygons_node_list, lines_node_list):
    num_nodes = len(list_coor)
    k_glob = np.zeros((num_nodes * 2, num_nodes * 2), dtype=np.float64)
    bc = boundary(lines_node_list, self.cur_phase, list_coor)
    for i in self.cur_phase['soils']:
      if i['phaseActivity']:
        mat = soil_model_get(i)
        k_glob += Polygon.stiff_matrix(d_matrix=mat.d_matrix(),
                                       list_nodes=polygons_node_list[i['name']],
                                       node_bc=bc,
                                       list_coor=list_coor)
    return k_glob

  def r_glob_sum(self, list_coor, polygons_node_list, lines_node_list):
    num_nodes = len(list_coor)
    r_glob = np.zeros(num_nodes * 2, dtype=np.float64)
    bc = boundary(lines_node_list, self.cur_phase, list_coor)
    for i in self.cur_phase['soils']:
      if i['phaseActivity']:
        mat = soil_model_get(i)
        r_glob += Polygon.r_glob_vector(weight=mat.dead,
                                        list_nodes=polygons_node_list[i['name']],
                                        node_bc=bc,
                                        list_coor=list_coor)
    return r_glob

  def le_solve(self, list_coor, polygons_node_list, lines_node_list):
    k_matrix = self.k_glob_sum(list_coor, polygons_node_list, lines_node_list)
    d_r_vector = self.r_glob_sum(
      list_coor, polygons_node_list, lines_node_list)
    d_x_vector, exit_code = sp.sparse.linalg.bicg(k_matrix, d_r_vector)
    return d_x_vector
