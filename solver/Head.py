import numpy as np
from solver.Phases_classes import Phase
from solver.Postprocessor import formalization
import time


def get_input(input_data, coor_data, polygons_data, lines_data):
  list_node_line = {}

  for i in range(len(lines_data)):
    for j in range(len(lines_data[i])):
      list_node_line[lines_data[i][0]] = lines_data[i][1]

  for i in list_node_line.keys():
    for j in list_node_line[i]:
      j.pop(0)

  list_node_polygon = {}
  for i in range(len(polygons_data)):
    for j in range(len(polygons_data[i])):
      list_node_polygon[polygons_data[i][0]] = polygons_data[i][1]

  for i in list_node_polygon.keys():
    for j in list_node_polygon[i]:
      j.pop(0)

  list_node_coor = []

  for i in list_node_polygon.keys():
    list_node_polygon[i] = np.asarray(list_node_polygon[i])

  for i in range(len(coor_data)):
    list_node_coor.append(coor_data[i][1])
    list_node_coor[i].pop(0)
  list_node_coor = np.asarray(list_node_coor)
  return input_data, list_node_coor, list_node_polygon, list_node_line


def solver(input_data, list_node_coor, list_node_polygon, list_node_line):
  print('=============================================================================')
  print('Начинается работа функции get_input!')
  start = time.perf_counter()

  input_data, list_node_coor, list_node_polygon, list_node_line = get_input(
    input_data, list_node_coor, list_node_polygon, list_node_line)

  finish = time.perf_counter()
  print(f'Время работы get_input: {str(finish - start)}')

  d_x = {}

  print('=============================================================================')
  print(f'Фазы: {input_data.keys()}')

  for i in input_data.keys():
    print('=============================================================================')
    print('Начинается работа функции le_solve в цикле!')
    start = time.perf_counter()

    d_x[i] = Phase(phase=input_data[i]).le_solve(
      list_node_coor, list_node_polygon, list_node_line)

    finish = time.perf_counter()
    print(f'Время работы le_solve: {str(finish - start)}')

  print('=============================================================================')
  print('Начинается работа функции formalization!')
  start = time.perf_counter()

  geometry_points, geometry_nodes, result = formalization(
    input_data, list_node_polygon, d_x, list_node_coor)

  finish = time.perf_counter()
  print(f'Время работы formalization: {str(finish - start)}')
  print('=============================================================================')

  return geometry_points, geometry_nodes, result
