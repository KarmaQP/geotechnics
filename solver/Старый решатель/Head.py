import numpy as np
from solver.Phases_classes import PhasePlastic


# Вспомогательные функции для визуализации
def list_nodes_triang(polygons_node_list):
  list_nodes = list(polygons_node_list.values())
  v = np.zeros((1, len(list_nodes[0][0])), dtype=np.int_)
  for i in range(len(list_nodes)):
    v = np.vstack([v, list_nodes[i]])
  list_nodes = np.delete(v, 0, axis=0)

  m, l = list_nodes.shape
  list_nodes_tri = np.zeros((m * 4, 3))
  for i in range(m):
    list_nodes_tri[4 * i, 0] = list_nodes[i, 0]
    list_nodes_tri[4 * i, 1] = list_nodes[i, 3]
    list_nodes_tri[4 * i, 2] = list_nodes[i, 5]

    list_nodes_tri[4 * i + 1, 0] = list_nodes[i, 3]
    list_nodes_tri[4 * i + 1, 1] = list_nodes[i, 1]
    list_nodes_tri[4 * i + 1, 2] = list_nodes[i, 4]

    list_nodes_tri[4 * i + 2, 0] = list_nodes[i, 5]
    list_nodes_tri[4 * i + 2, 1] = list_nodes[i, 4]
    list_nodes_tri[4 * i + 2, 2] = list_nodes[i, 2]

    list_nodes_tri[4 * i + 3, 0] = list_nodes[i, 3]
    list_nodes_tri[4 * i + 3, 1] = list_nodes[i, 4]
    list_nodes_tri[4 * i + 3, 2] = list_nodes[i, 5]
  return list_nodes_tri


def coor_mid_calc(list_coor, polygons_node_list):
  list_nodes = list(polygons_node_list.values())
  v = np.zeros((1, len(list_nodes[0][0])), dtype=np.int_)
  for i in range(len(list_nodes)):
    v = np.vstack([v, list_nodes[i]])
  list_nodes = np.delete(v, 0, axis=0)
  num_el = len(list_nodes)

  # Вычисление координат точек интегрирования и карт связности промежуточных треугольников
  list_coor_mid = np.zeros((num_el * 4, 2), dtype=np.float32)
  list_node_mid = np.zeros((4 * num_el, 3), dtype=np.int_)
  for i in range(num_el):
    # 0 точка интегрирования
    list_coor_mid[4 * i, 0] = (list_coor[list_nodes[i, 0], 0] + list_coor[list_nodes[i, 4], 0] + list_coor[
        list_nodes[i, 3], 0]) / 3
    list_coor_mid[4 * i, 1] = (list_coor[list_nodes[i, 0], 1] + list_coor[list_nodes[i, 4], 1] + list_coor[
        list_nodes[i, 3], 1]) / 3
    list_node_mid[4 * i] = np.array([list_nodes[i, 0],
                                    list_nodes[i, 4], list_nodes[i, 3]])
    # 1 точка интегрирования
    list_coor_mid[4 * i + 1, 0] = (list_coor[list_nodes[i, 4], 0] + list_coor[list_nodes[i, 1], 0] + list_coor[
        list_nodes[i, 5], 0]) / 3
    list_coor_mid[4 * i + 1, 1] = (list_coor[list_nodes[i, 4], 1] + list_coor[list_nodes[i, 1], 1] + list_coor[
        list_nodes[i, 5], 1]) / 3
    list_node_mid[4 * i +
                  1] = np.array([list_nodes[i, 4], list_nodes[i, 1], list_nodes[i, 5]])
    # 2 точка интегрирования
    list_coor_mid[4 * i + 2, 0] = (list_coor[list_nodes[i, 3], 0] + list_coor[list_nodes[i, 5], 0] + list_coor[
        list_nodes[i, 2], 0]) / 3
    list_coor_mid[4 * i + 2, 1] = (list_coor[list_nodes[i, 3], 1] + list_coor[list_nodes[i, 5], 1] + list_coor[
        list_nodes[i, 2], 1]) / 3
    list_node_mid[4 * i +
                  2] = np.array([list_nodes[i, 3], list_nodes[i, 5], list_nodes[i, 2]])
    # # средний треугольник
    list_node_mid[4 * i +
                  3] = np.array([list_nodes[i, 4], list_nodes[i, 5], list_nodes[i, 3]])
  return list_coor_mid, list_node_mid, num_el


def solver(num_nodes, input_data, list_coor, polygons_node_list, lines_node_list):
  u = PhasePlastic(cur_phase=input_data).le_solve(
    list_coor, polygons_node_list, lines_node_list)
  coor_x = list_coor[:, 0]
  coor_y = list_coor[:, 1]
  u_x = np.zeros(num_nodes)
  u_y = np.zeros(num_nodes)
  for i in range(num_nodes):
    u_x[i] = u[2 * i]
    u_y[i] = u[2 * i + 1]
  list_nodes = list_nodes_triang(polygons_node_list)
  list_coor_mid, list_node_mid, num_el = coor_mid_calc(
    list_coor, polygons_node_list)

  epsilon = np.ones((4 * num_el, 3), dtype=np.float64)
  sigma = np.ones((4 * num_el, 3), dtype=np.float64)
  stress_points = np.zeros((4 * num_el), dtype=np.float64)

  geometry_points = {'x': coor_x, 'y': coor_y, 'map': list_nodes}
  geometry_nodes = {
    'x_mid': list_coor_mid[:, 0], 'y_mid': list_coor_mid[:, 1], 'map_mid': list_node_mid}
  result = {'u_x': u_x, 'u_y': u_y,
            'eps_XX': epsilon[:, 0], 'eps_YY': epsilon[:, 1], 'eps_XY': epsilon[:, 2],
            'sigma_XX': sigma[:, 0], 'sigma_YY': sigma[:, 1], 'sigma_XY': sigma[:, 2],
            'stress_points': stress_points}
  return geometry_points, geometry_nodes, result
