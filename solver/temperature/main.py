import numpy as np
import mpld3
from mpld3 import plugins
import matplotlib.pyplot as plt
import matplotlib.tri as tri
import pandas as pd


def isofields_temp(nodes, data_fig, elem, step):
  x = nodes[:, 1]
  y = nodes[:, 2]

  fig, ax = plt.subplots()

  triang = tri.Triangulation(x, y, elem.astype(int), mask=None)

  "Создаем графическое отображение результатов."

  pc = ax.tripcolor(triang, list(data_fig.values())[step], cmap='jet')
  pc1 = ax.scatter(x, y, c=list(data_fig.values())
                   [step], s=0, cmap='jet', alpha=1)
  fig.colorbar(pc1, ax=ax)
  ax.set(title=list(data_fig.keys())[step], xlabel='X Axis', ylabel='Y Axis')
  ax.set_aspect('equal', 'box')

  min_max_values = {}

  print(f'Максимальное {list(data_fig.keys())[step]}:', max(
    list(data_fig.values())[step]))
  print(f'Минимальное {list(data_fig.keys())[step]}:', min(
    list(data_fig.values())[step]))

  min_max_values[f"temperature1"] = {
      "min": round(min(list(data_fig.values())[step]), 3),
      "max": round(max(list(data_fig.values())[step]), 3),
  }

  df = pd.DataFrame(index=range(len(x)))

  df['x'] = x
  df['y'] = y
  df['Значение'] = list(data_fig.values())[step]

  labels = []
  for i in range(len(x)):
    label = round(df.iloc[[i], 2:3].T, 3)
    # label.columns = ['№{0}'.format(i)]
    # print(str(label.to_html()))
    # print(label)
    labels.append(str(label.to_html()))

  points = ax.plot(df.x, df.y, 'o', color='b',
                   mec='k', ms=15, mew=1, alpha=0)

  tooltip = plugins.PointHTMLTooltip(points[0], labels,
                                     voffset=10, hoffset=10)
  plugins.connect(fig, tooltip)

  mpld3.save_json(fig, f'static/src/dist/results/temperature/isofields.json')

  return min_max_values


def generate_data(coord, polygons, lines_data):

  list_node_polygon = {}

  for i in range(len(polygons)):
    list_node_polygon[f'{polygons[i][0]}'] = polygons[i][1]

  list_node_line = {}

  for i in range(len(lines_data)):
    list_node_line[f'{lines_data[i][0]}'] = lines_data[i][1]

  return coord, list_node_polygon, list_node_line


def create_data_temp(coord, list_node_line, list_node_polygon, data_2):

  nn = len(coord)
  ne = 0
  nodes = np.zeros((nn, 3))

  surfaces_all = list(list_node_polygon.values())

  for i in range(len(list_node_polygon)):

    ne = ne + len(surfaces_all[i])

  elem = np.zeros((ne, 3), dtype='int64')
  propertires = np.zeros((ne, 3), dtype='float64')

  for i in range(nn):
    nodes[i, 0] = coord[i][1][0]
    nodes[i, 1] = coord[i][1][1]
    nodes[i, 2] = coord[i][1][2]

  for i in range(len(list_node_polygon)):

    if i == 0:
      k = 0
    else:
      k = k + len(surfaces_all[i - 1])

    for j in range(len(surfaces_all[i])):
      elem[k + j][:3] = surfaces_all[i][j][1:4]
      data_list = list(data_2.get('soils')[i].get('material').values())
      propertires[k + j][0] = data_list[0].get('tempCoef')
      propertires[k + j][1] = data_list[0].get('tempHeat')
      propertires[k + j][2] = data_list[0].get('tempDensity')

  nodes_s = np.zeros((ne, 2))

  for i in range(ne):
    nodes_s[i][0] = (nodes[elem[i][0]][1] + nodes[elem[i]
                     [1]][1] + nodes[elem[i][2]][1]) / 3
    nodes_s[i][1] = (nodes[elem[i][0]][2] + nodes[elem[i]
                     [1]][2] + nodes[elem[i][2]][2]) / 3

  return nn, ne, nodes, elem, propertires, nodes_s


def bc_temp(elem, ne, list_node_line, input_data):

  boundary_lines = []
  bcwater = []
  bc_water_nodes = []
  H_water_lines_value2 = []
  d_ind = np.zeros((ne, 6))

  for i in range(len(input_data.get('lines'))):
    try:
      input_data.get('lines')[
          i]['propertyParams']['boundaryTemp']
    except KeyError:
      continue
    else:
      boundary_lines.append(input_data.get('lines')[i]['name'])
      boundary_lines.append(input_data.get('lines')[
          i]['propertyParams']['boundaryTemp'])

  for i in range(len(boundary_lines)):
    if type(boundary_lines[i]) is str:
      bcwater.append(list_node_line[boundary_lines[i]])
      bcwater.append(boundary_lines[i + 1])

  for i in range(len(bcwater)):
    if type(bcwater[i]) is list:
      for j in range(len(bcwater[i])):
        bc_water_nodes.append(bcwater[i][j][1])
        bc_water_nodes.append(bcwater[i][j][2])
        H_water_lines_value2.append(bcwater[i + 1])
        H_water_lines_value2.append(bcwater[i + 1])

  for i in range(ne):
    for j in range(3):
      for k in range(len(bc_water_nodes)):
        if elem[i][j] == bc_water_nodes[k]:
          d_ind[i][j] = 1
          d_ind[i][j + 3] = H_water_lines_value2[k]

  return d_ind


def bc_T0(elem, ne, list_node_line, input_data):

  boundary_lines = []
  bcwater = []
  bc_water_nodes = []
  H_water_lines_value2 = []
  d_ind_T0 = np.zeros((ne, 6))

  for i in range(len(input_data.get('lines'))):
    try:
      input_data.get('lines')[
          i]['propertyParams']['initialTemp']
    except KeyError:
      continue
    else:
      boundary_lines.append(input_data.get('lines')[i]['name'])
      boundary_lines.append(input_data.get('lines')[
          i]['propertyParams']['initialTemp'])

  for i in range(len(boundary_lines)):
    if type(boundary_lines[i]) is str:
      bcwater.append(list_node_line[boundary_lines[i]])
      bcwater.append(boundary_lines[i + 1])

  for i in range(len(bcwater)):
    if type(bcwater[i]) is list:
      for j in range(len(bcwater[i])):
        bc_water_nodes.append(bcwater[i][j][1])
        bc_water_nodes.append(bcwater[i][j][2])
        H_water_lines_value2.append(bcwater[i + 1])
        H_water_lines_value2.append(bcwater[i + 1])

  for i in range(ne):
    for j in range(3):
      for k in range(len(bc_water_nodes)):
        if elem[i][j] == bc_water_nodes[k]:
          d_ind_T0[i][j] = 1
          d_ind_T0[i][j + 3] = H_water_lines_value2[k]

  return d_ind_T0


def gKr_temp(elem, nodes, ne, nn, d_ind, propertires, T, dt):

  K = np.zeros((nn, nn), dtype='float64')
  r = np.zeros(nn, dtype='float64')

  for i in range(0, ne):

    x = [nodes[elem[i][0]][1], nodes[elem[i][1]][1], nodes[elem[i][2]][1]]
    y = [nodes[elem[i][0]][2], nodes[elem[i][1]][2], nodes[elem[i][2]][2]]
    Tloc = [T[elem[i][0]], T[elem[i][1]], T[elem[i][2]]]

    d_loc = d_ind[i]

    lamda_C_po = propertires[i]

    Kloc, r_loc = local_temp(x, y, d_loc, lamda_C_po, dt, Tloc)

    for j in range(0, 3):
      r[elem[i][j]] += r_loc[j]
      for k in range(0, 3):
        K[elem[i][j], elem[i][k]] += Kloc[j, k]

  return K, r


def local_temp(x, y, d_loc, lamda_C_po, dt, Tloc):

  x1 = x[0]
  x2 = x[1]
  x3 = x[2]
  y1 = y[0]
  y2 = y[1]
  y3 = y[2]

  S = 0.5 * ((x2 - x1) * (y3 - y1) - (x3 - x1) * (y2 - y1))

  B = 1 / (2 * S) * np.array([[y2 - y3, y3 - y1, y1 - y2],
                              [x3 - x2, x1 - x3, x2 - x1]])

  A = np.array([[x2 - x1, x3 - x1],
                [y2 - y1, y3 - y1]])

  lamda = lamda_C_po[0]
  C = lamda_C_po[1]
  po = lamda_C_po[2]

  detA = np.linalg.det(A)
  Mloc = (1 / dt) * C * po * detA * np.array([[1 / 12, 1 / 24, 1 / 24],
                                              [1 / 24, 1 / 12, 1 / 24],
                                              [1 / 24, 1 / 24, 1 / 12]])

  Kloc = lamda * S * B.T @ B
  Kloc += Mloc

  r_loc = np.zeros(3)
  r_loc += Mloc @ Tloc

  for i in range(0, 3):
    if d_loc[i] == 1:
      Kloc[i] = 0
      Kloc[i, i] = 1
      r_loc[i] = d_loc[i + 3]

  return Kloc, r_loc


def inithial_param(N, t, T0):

  dt = t / N
  Tstep = []

  Tstep.append(T0)
  data_fig = {"Время расчета t=0, с": Tstep[0]}
  T = T0

  return N, dt, Tstep, data_fig, T


def gKr_T0(elem, nodes, ne, nn, d_ind_T0, propertires):

  K = np.zeros((nn, nn), dtype='float64')
  r = np.zeros(nn, dtype='float64')

  for i in range(0, ne):

    x = [nodes[elem[i][0]][1], nodes[elem[i][1]][1], nodes[elem[i][2]][1]]
    y = [nodes[elem[i][0]][2], nodes[elem[i][1]][2], nodes[elem[i][2]][2]]

    d_loc = d_ind_T0[i]

    lamda_C_po = propertires[i]

    Kloc, r_loc = local_T0(x, y, d_loc, lamda_C_po)

    for j in range(0, 3):
      r[elem[i][j]] += r_loc[j]
      for k in range(0, 3):
        K[elem[i][j], elem[i][k]] += Kloc[j, k]

  return K, r


def local_T0(x, y, d_loc, lamda_C_po):
  x1 = x[0]
  x2 = x[1]
  x3 = x[2]
  y1 = y[0]
  y2 = y[1]
  y3 = y[2]

  S = 0.5 * ((x2 - x1) * (y3 - y1) - (x3 - x1) * (y2 - y1))

  B = 1 / (2 * S) * np.array([[y2 - y3, y3 - y1, y1 - y2],
                              [x3 - x2, x1 - x3, x2 - x1]])

  lamda = lamda_C_po[0]

  Kloc = lamda * S * B.T @ B

  r_loc = np.zeros(3)

  for i in range(0, 3):
    if d_loc[i] == 1:
      Kloc[i] = 0
      Kloc[i, i] = 1
      r_loc[i] = d_loc[i + 3]

  return Kloc, r_loc
