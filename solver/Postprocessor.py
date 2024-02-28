import numpy as np
from solver.Phases_classes import Phase


def list_nodes_triang(polygons_node_list):
  list_nodes = list(polygons_node_list.values())
  v = np.zeros((1, len(list_nodes[0][0])), dtype=np.int_)
  for i in range(len(list_nodes)):
    v = np.vstack([v, list_nodes[i]])
  list_nodes = np.delete(v, 0, axis=0)

  r, c = list_nodes.shape
  list_nodes_tri = np.zeros((r * 4, 3))
  for i in range(r):
    list_nodes_tri[4 * i, 0] = list_nodes[i, 5]
    list_nodes_tri[4 * i, 1] = list_nodes[i, 4]
    list_nodes_tri[4 * i, 2] = list_nodes[i, 2]

    list_nodes_tri[4 * i + 1, 0] = list_nodes[i, 0]
    list_nodes_tri[4 * i + 1, 1] = list_nodes[i, 3]
    list_nodes_tri[4 * i + 1, 2] = list_nodes[i, 5]

    list_nodes_tri[4 * i + 2, 0] = list_nodes[i, 3]
    list_nodes_tri[4 * i + 2, 1] = list_nodes[i, 1]
    list_nodes_tri[4 * i + 2, 2] = list_nodes[i, 4]

    list_nodes_tri[4 * i + 3, 0] = list_nodes[i, 4]
    list_nodes_tri[4 * i + 3, 1] = list_nodes[i, 5]
    list_nodes_tri[4 * i + 3, 2] = list_nodes[i, 3]
  return list_nodes_tri


def coor_mid_calc(list_node_polygon, list_node_coor):
  list_nodes = list(list_node_polygon.values())
  v = np.zeros((1, len(list_nodes[0][0])), dtype=np.int_)
  for i in range(len(list_nodes)):
    v = np.vstack([v, list_nodes[i]])
  list_nodes = np.delete(v, 0, axis=0)
  num_el = len(list_nodes)

  # Вычисление координат точек интегрирования и карт связности промежуточных треугольников
  list_coor_mid = np.zeros((num_el * 3, 2), dtype=np.float32)
  for i in range(num_el):
    # 0 точка интегрирования
    list_coor_mid[3 * i, 0] = (list_node_coor[list_nodes[i, 0], 0] + list_node_coor[list_nodes[i, 3], 0] +
                               list_node_coor[list_nodes[i, 5], 0]) / 3
    list_coor_mid[3 * i, 1] = (list_node_coor[list_nodes[i, 0], 1] + list_node_coor[list_nodes[i, 3], 1] +
                               list_node_coor[list_nodes[i, 5], 1]) / 3
    # 1 точка интегрирования
    list_coor_mid[3 * i + 1, 0] = (list_node_coor[list_nodes[i, 3], 0] + list_node_coor[list_nodes[i, 1], 0] +
                                   list_node_coor[list_nodes[i, 4], 0]) / 3
    list_coor_mid[3 * i + 1, 1] = (list_node_coor[list_nodes[i, 3], 1] + list_node_coor[list_nodes[i, 1], 1] +
                                   list_node_coor[list_nodes[i, 4], 1]) / 3
    # 2 точка интегрирования
    list_coor_mid[3 * i + 2, 0] = (list_node_coor[list_nodes[i, 2], 0] + list_node_coor[list_nodes[i, 5], 0] +
                                   list_node_coor[list_nodes[i, 4], 0]) / 3
    list_coor_mid[3 * i + 2, 1] = (list_node_coor[list_nodes[i, 2], 1] + list_node_coor[list_nodes[i, 5], 1] +
                                   list_node_coor[list_nodes[i, 4], 1]) / 3
  return list_coor_mid, num_el


def eps_reformat(input_data, list_node_polygon, list_node_coor, d_x):
  phases_val = {}
  for i in input_data.keys():
    phases_val[i] = Phase(phase=input_data[i]).epsilon(
      d_x[i], list_node_polygon, list_node_coor)
  return phases_val


def sig_reformat(input_data, list_node_polygon, list_node_coor, d_x):
  phases_val = {}
  for i in input_data.keys():
    phases_val[i] = Phase(phase=input_data[i]).sigma(
      d_x[i], list_node_polygon, list_node_coor)
  return phases_val


def dict_in_array(dictionary):
  array = None
  k = 0
  for i in dictionary.keys():
    if k == 0:
      array = np.zeros_like(dictionary[i][0])
    k += 1
    array = np.row_stack([array, dictionary[i]])
  array = np.delete(array, 0, 0)
  return array


def mid_value_add(array):
  mid_array = array
  k = 0
  for i in range(2, len(array), 3):
    k += 1
    middle = np.mean(array[(i - 2):i + 1], axis=1)
    mid_array = np.insert(mid_array, i + k, middle, axis=0)
  return mid_array


def formalization(input_data, list_node_polygon, d_x, list_node_coor):
  num_nodes = len(list_node_coor[:, 0])
  coor_x = list_node_coor[:, 0]
  coor_y = list_node_coor[:, 1]

  u_x = {}
  u_y = {}
  disp_x = np.zeros(num_nodes, dtype=np.float64)
  disp_y = np.zeros(num_nodes, dtype=np.float64)
  for i in d_x.keys():
    for j in range(num_nodes):
      disp_x[j] = d_x[i][2 * j]
      disp_y[j] = d_x[i][2 * j + 1]
    u_x[i] = disp_x
    u_y[i] = disp_y

  list_nodes = list_nodes_triang(list_node_polygon)
  list_coor_mid, num_el = coor_mid_calc(list_node_polygon, list_node_coor)
  eps = eps_reformat(input_data, list_node_polygon, list_node_coor, d_x)
  sig = sig_reformat(input_data, list_node_polygon, list_node_coor, d_x)
  epsilon = {}
  sigma = {}
  for i in input_data.keys():
    epsilon[i] = dict_in_array(eps[i])
    sigma[i] = dict_in_array(sig[i])

  stress_points = {}
  for i in input_data.keys():
    stress_points[i] = np.zeros((4 * num_el), dtype=np.float64)

  geometry_points = {'x': coor_x, 'y': coor_y, 'map': list_nodes}
  geometry_nodes = {'x_mid': list_coor_mid[:, 0], 'y_mid': list_coor_mid[:, 1]}

  result = {}
  for i in input_data.keys():
    result[i] = {'u_x': u_x[i], 'u_y': u_y[i],
                 'eps_XX': epsilon[i][:, 0], 'eps_YY': epsilon[i][:, 1], 'eps_XY': epsilon[i][:, 2],
                 'sigma_XX': sigma[i][:, 0], 'sigma_YY': sigma[i][:, 1], 'sigma_XY': sigma[i][:, 2],
                 'stress_points': stress_points[i]}
  return geometry_points, geometry_nodes, result
