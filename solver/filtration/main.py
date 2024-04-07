import numpy as np
import mpld3
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import pandas as pd
import matplotlib.tri as tri
from mpld3 import plugins


def create_data_wtf(coord, list_node_line, list_node_polygon, data_2):

  nn = len(coord)
  ne = 0
  nodes = np.zeros((nn, 3))

  surfaces_all = list(list_node_polygon.values())

  for i in range(len(list_node_polygon)):

    ne = ne + len(surfaces_all[i])

  elem = np.zeros((ne, 3), dtype='int64')
  propertires = np.zeros((ne, 2), dtype='float64')

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
      propertires[k + j][0] = data_list[0].get('filtrationX')
      propertires[k + j][1] = data_list[0].get('filtrationY')

  nodes_s = np.zeros((ne, 2))

  for i in range(ne):
    nodes_s[i][0] = (nodes[elem[i][0]][1] + nodes[elem[i]
                     [1]][1] + nodes[elem[i][2]][1]) / 3
    nodes_s[i][1] = (nodes[elem[i][0]][2] + nodes[elem[i]
                     [1]][2] + nodes[elem[i][2]][2]) / 3

  return nn, ne, nodes, elem, propertires, nodes_s


def gKr(elem, nodes, ne, nn, d_ind, propertires):

  K = np.zeros((nn, nn))
  r = np.zeros(nn)
  Bb = []

  for i in range(0, ne):

    x = [nodes[elem[i][0]][1], nodes[elem[i][1]][1], nodes[elem[i][2]][1]]
    y = [nodes[elem[i][0]][2], nodes[elem[i][1]][2], nodes[elem[i][2]][2]]

    d_loc = d_ind[i]

    kfxkfy = propertires[i]

    Kloc, r_loc, Bb = local(x, y, d_loc, kfxkfy, Bb)

    for j in range(0, 3):
      r[elem[i][j]] += r_loc[j]
      for k in range(0, 3):
        K[elem[i][j], elem[i][k]] += Kloc[j, k]

  return K, r, Bb


def local(x, y, d_loc, kfxkfy, Bb):
  x1 = x[0]
  x2 = x[1]
  x3 = x[2]
  y1 = y[0]
  y2 = y[1]
  y3 = y[2]

  S = 0.5 * ((x2 - x1) * (y3 - y1) - (x3 - x1) * (y2 - y1))

  B = 1 / (2 * S) * np.array([[y2 - y3, y3 - y1, y1 - y2],
                              [x3 - x2, x1 - x3, x2 - x1]])

  Bb.append(B)

  kfx = kfxkfy[0]
  kfy = kfxkfy[1]

  kf = np.array([[kfx, 0],
                [0, kfy]])

  O = np.array([[0, 1],
                [-1, 0]])

  Kloc = S * B.T @ O.T @ kf @ O @ B

  r_loc = np.zeros(3)

  for i in range(0, 3):
    if d_loc[i] == 1:
      Kloc[i] = 0
      Kloc[i, i] = 1
      r_loc[i] = d_loc[i + 3]

  return Kloc, r_loc, Bb


def dc(a, propertires, ne, elem, nodes):

  for i in range(ne):

    H_loc_1 = a[elem[i][0]]
    H_loc_2 = a[elem[i][1]]
    H_loc_3 = a[elem[i][2]]

    H_loc = np.array([H_loc_1, H_loc_2, H_loc_3])

    yloc1 = nodes[elem[i][0]][2]
    yloc2 = nodes[elem[i][1]][2]
    yloc3 = nodes[elem[i][2]][2]

    yloc = np.array([yloc1, yloc2, yloc3])

    Hc = np.sum(H_loc) / 3
    yc = np.sum(yloc) / 3

    if Hc < yc:
      propertires[i][0] = 0.0001
      propertires[i][1] = 0.0001

  return propertires


def velocities_gradients(a, elem, ne, Bb, propertires, nodes, nn):

  v = np.zeros((ne, 3))
  I = np.zeros((ne, 3))
  pw = np.zeros(nn)
  yw = 10

  for i in range(ne):

    a1 = a[elem[i][0]]
    a2 = a[elem[i][1]]
    a3 = a[elem[i][2]]

    a_loc = np.array([a1, a2, a3])
    ixiy = Bb[i] @ a_loc

    v[i][0] = ixiy[0] * propertires[i][0]
    v[i][1] = ixiy[1] * propertires[i][1]
    v[i][2] = (v[i][0]**2 + v[i][1]**2)**0.5

    I[i][0] = ixiy[0]
    I[i][1] = ixiy[1]
    I[i][2] = (ixiy[0]**2 + ixiy[1]**2)**0.5

  for i in range(nn):
    pw[i] = (a[i] - nodes[i][2]) * yw

  return v, I, pw


def create_data_filtration(nodes, elem, a, pw, v, I, nodes_s):

  x = nodes[:, 1]
  y = nodes[:, 2]
  elem = elem
  H_water = a
  pw = pw
  vx = v[:, 0]
  vy = v[:, 1]
  vu = v[:, 2]
  ix = I[:, 0]
  iy = I[:, 1]
  iu = I[:, 2]
  xc = nodes_s[:, 0]
  yc = nodes_s[:, 1]

  results_data = {
      'x,m': x,
      'y,m': y,
      'elements_3': elem,
      'H_water, m': H_water,
      'Water pressure,kPa': pw,
      'Velocities X, m/day': vx,
      'Velocities Y, m/day': vy,
      'Velocities |U|, m/day': vu,
      'Hydralic gradient X': ix,
      'Hydralic gradient Y': iy,
      'Hydralic gradient |U|': iu,
      'xc,m': xc,
      'yc,m': yc
  }

  return results_data


def isofields_filtration(results_data, v):

  x = results_data.get('x,m')
  y = results_data.get('y,m')
  xc = results_data.get('xc,m')
  yc = results_data.get('yc,m')

  elem = results_data.get('elements_3')

  data = [results_data.get('H_water, m'), results_data.get('Water pressure,kPa'), results_data.get('Velocities X, m/day'), results_data.get('Velocities Y, m/day'),
          results_data.get('Velocities |U|, m/day'), results_data.get('Hydralic gradient X'), results_data.get('Hydralic gradient Y'), results_data.get('Hydralic gradient |U|')]

  units = ['м', 'кПа', 'м/сут', 'м/сут', 'м/сут', '', '', '']

  names = list(results_data.keys())
  min_max_values = {}

  for i in range(len(data)):

    if i <= 1:

      fig, ax = plt.subplots()

      triang = tri.Triangulation(x, y, elem.astype(int), mask=None)

      "Создаем графическое отображение результатов."

      print(data[i])
      pc = ax.tricontourf(triang, data[i], cmap='jet', levels=20)
      pc1 = ax.scatter(x, y, c=data[i], s=0, cmap='jet', alpha=1)
      fig.colorbar(pc1, ax=ax)
      ax.set(title=names[i + 3], xlabel='X Axis', ylabel='Y Axis')
      ax.set_aspect('equal', 'box')
      print(f'Максимальное {names[i+3]}:', max(data[i]))
      print(f'Минимальное {names[i+3]}:', min(data[i]))

      min_max_values[f"filtration_{i + 1}"] = {
        "min": round(min(data[i]), 3),
        "max": round(max(data[i]), 3),
      }

      df = pd.DataFrame(index=range(len(x)))

      df['x'] = x
      df['y'] = y
      df['Значение'] = data[i]

      labels = []
      for j in range(len(x)):
        label = round(df.iloc[[j], 2:3].T, 3)
        # label.columns = ['№{0}'.format(i)]
        # print(str(label.to_html()))
        # print(label)
        labels.append(str(label.to_html()))

      points = ax.plot(df.x, df.y, 'o', color='b',
                       mec='k', ms=15, mew=1, alpha=0)

      tooltip = plugins.PointHTMLTooltip(points[0], labels,
                                         voffset=10, hoffset=10)
      plugins.connect(fig, tooltip)

      mpld3.save_json(
        fig, f'static/src/dist/results/filtration/isofields_{i + 1}.json')

    if i >= 2:

      fig, ax = plt.subplots()

      triang = tri.Triangulation(x, y, elem.astype(int), mask=None)

      "Создаем графическое отображение результатов."

      pc = ax.tripcolor(triang, data[i], cmap='jet')
      pc1 = ax.scatter(xc, yc, c=data[i], s=0, cmap='jet', alpha=1)
      fig.colorbar(pc1, ax=ax)
      ax.set(title=names[i + 3], xlabel='X Axis', ylabel='Y Axis')
      ax.set_aspect('equal', 'box')
      print(f'Максимальное {names[i+3]}:', max(data[i]))
      print(f'Минимальное {names[i+3]}:', min(data[i]))

      min_max_values[f"filtration_{i + 1}"] = {
        "min": round(min(data[i]), 3),
        "max": round(max(data[i]), 3),
      }

      df = pd.DataFrame(index=range(len(xc)))

      df['xc'] = xc
      df['yc'] = yc
      df['Значение'] = data[i]

      labels = []
      for j in range(len(xc)):
        label = round(df.iloc[[j], 2:3].T, 3)
        # label.columns = ['№{0}'.format(i)]
        # print(str(label.to_html()))
        # print(label)
        labels.append(str(label.to_html()))

      points = ax.plot(df.xc, df.yc, 'o', color='b',
                       mec='k', ms=15, mew=1, alpha=0)

      tooltip = plugins.PointHTMLTooltip(points[0], labels,
                                         voffset=10, hoffset=10)
      plugins.connect(fig, tooltip)

      mpld3.save_json(
        fig, f'static/src/dist/results/filtration/isofields_{i + 1}.json')

  fig, ax = plt.subplots()

  vx = data[2]
  vy = data[3]
  vu = data[4]

  pc = ax.quiver(xc, yc, -vx, -vy, vu, scale=5, cmap='jet',
                 norm=colors.Normalize(np.min(v[:, 2]), np.max(v[:, 2])))
  ax.set_aspect('equal', 'box')
  fig.colorbar(pc, ax=ax)
  mpld3.save_json(fig, f'static/src/dist/results/filtration/isofields_9.json')

  return min_max_values, units


def bc(elem, ne, list_node_line, data_2):
  boundary_lines = []
  bcwater = []
  bc_water_nodes = []
  H_water_lines_value2 = []
  d_ind = np.zeros((ne, 6))

  for i in range(len(data_2.get('lines'))):
    try:
      data_2.get('lines')[
          i]['propertyParams']['nodalPressure']
    except KeyError:
      continue
    else:
      boundary_lines.append(data_2.get('lines')[i]['name'])
      boundary_lines.append(data_2.get('lines')[
          i]['propertyParams']['nodalPressure'])

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
