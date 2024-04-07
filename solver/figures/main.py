import numpy as np
import mpld3
import matplotlib.tri as tri
import matplotlib.pyplot as plt


def create_figure_1(list_node_coor, list_node_line, list_node_polygon):
  "############################################################################################"
  "ЭТОТ РАЗДЕЛ ДЛЯ РАБОТЫ С ЛИНИЯМИ:"

  "Получаем число линий из расчетной схемы:"
  number_of_lines = len(list_node_line)
  "Получаем название линий из расчетной схемы:"
  line_names = list(list_node_line.keys())
  "Создаем список, который содержит номер элемента линий и номера узлов, которые их описывают:"
  line_data = list(list_node_line.values())
  "Создаем пустые списки координат линий, по которым будем строить линии:"
  x = []
  y = []
  "Проходимся по БОЛЬШИМ линиям и вытаскиваем первую координату маленькой линии и последнюю:"
  for i in range(number_of_lines):
    "Списки заполняются по принципу: в общий список идет вложенный с координатов по оси х и у -начала и конца линии:"
    x.append([list_node_coor[line_data[i][0][1]][1],
             list_node_coor[line_data[i][-1][3]][1]])
    y.append([list_node_coor[line_data[i][0][1]][2],
             list_node_coor[line_data[i][-1][3]][2]])

  "############################################################################################"
  "ЭТОТ РАЗДЕЛ ДЛЯ РАБОТЫ С ПОЛИГОНАМИ:"
  poly_names = list(list_node_polygon.keys())
  poly_atribute = []
  for i in range(0, len(poly_names)):
    poly_atribute.append(i)
  surface_data = list(list_node_polygon.values())

  data_elem = []

  for i in range(0, len(poly_names)):
    for j in range(0, len(surface_data[i])):
      n1 = surface_data[i][j][1]
      n2 = surface_data[i][j][2]
      n3 = surface_data[i][j][3]
      n4 = surface_data[i][j][4]
      n5 = surface_data[i][j][5]
      n6 = surface_data[i][j][6]
      data_elem.append([poly_atribute[i], n1, n4, n6])
      data_elem.append([poly_atribute[i], n4, n2, n5])
      data_elem.append([poly_atribute[i], n5, n3, n6])
      data_elem.append([poly_atribute[i], n4, n5, n6])

  return x, y, line_names, data_elem, list_node_coor, poly_atribute, poly_names


"Фукнция строит линии по данным расчтной схемы"


def create_figure_2(x, y, line_names, vert, elem_0, list_node_coor, poly_names, data_elem):

  fig, ax = plt.subplots()

  for i in range(len(x)):
    plt.plot([x[i][0], x[i][1]], [y[i][0], y[i][1]])
    "Находим середину каждой линии, чтобы вставить туда подпись ее имени"
    xc = (x[i][1] - x[i][0]) / 2 + x[i][0]
    yc = (y[i][1] - y[i][0]) / 2 + y[i][0]
    ax.annotate(str(line_names[i]), xy=(xc, yc), xytext=(
      xc, yc), fontsize=10, font='Arial', color='k', label='Line_objects')

  nv = len(list_node_coor)

  nt = len(data_elem)
  nodes = np.zeros((nv, 2))
  elements = np.zeros((nt, 3))

  atrr = np.zeros(nt)

  for i in range(nv):
    nodes[i, 0] = vert[i][1]
    nodes[i, 1] = vert[i][2]

  for i in range(nt):
    elements[i, 0] = elem_0[i][1]
    elements[i, 1] = elem_0[i][2]
    elements[i, 2] = elem_0[i][3]
    atrr[i] = elem_0[i][0]

  xx = nodes[:, 0]
  yy = nodes[:, 1]

  triang = tri.Triangulation(xx, yy, elements.astype(int), mask=None)

  "Создаем графическое отображение результатов."

  pc = ax.tripcolor(triang, atrr, cmap='jet', alpha=1, antialiased=False)
  # fig.colorbar(pc, ax = ax)
  ax.set(xlabel='X Axis', ylabel='Y Axis')
  ax.set_aspect('equal', 'box')
  # ax.legend([poly_names])

  coord = np.zeros((nt, 3))
  for i in range(nt):
    coord[i, 0] = 1 / 3 * (vert[elem_0[i][1]][1] +
                           vert[elem_0[i][2]][1] + vert[elem_0[i][3]][1])
    coord[i, 1] = 1 / 3 * (vert[elem_0[i][1]][2] +
                           vert[elem_0[i][2]][2] + vert[elem_0[i][3]][2])
    coord[i, 2] = atrr[i]

  colors = []
  for i in range(len(poly_names)):
    colors.append(i)

  ploty = ax.scatter(coord[:, 0], coord[:, 1],
                     c=coord[:, 2], s=0, cmap='jet', alpha=1)
  handles = ploty.legend_elements(num=colors)[0]

  ax.legend(bbox_to_anchor=(1.02, 1), handles=handles,
            loc='upper left', labels=poly_names)

  fig.set_size_inches(12, 4.8, forward=True)

  response_json = mpld3.fig_to_dict(fig)

  # f = open('data/schemes/scheme.json', 'r', -1, 'ascii')
  # response_json = f.read()
  return response_json


def create_figure_1_3nodes(list_node_coor, list_node_line, list_node_polygon):
  "############################################################################################"
  "ЭТОТ РАЗДЕЛ ДЛЯ РАБОТЫ С ЛИНИЯМИ:"

  "Получаем число линий из расчетной схемы:"
  number_of_lines = len(list_node_line)
  "Получаем название линий из расчетной схемы:"
  line_names = list(list_node_line.keys())

  "Создаем список, который содержит номер элемента линий и номера узлов, которые их описывают:"
  line_data = list(list_node_line.values())

  "Создаем пустые списки координат линий, по которым будем строить линии:"
  x = []
  y = []

  "Проходимся по БОЛЬШИМ линиям и вытаскиваем первую координату маленькой линии и последнюю:"
  for i in range(number_of_lines):

    "Списки заполняются по принципу: в общий список идет вложенный с координатов по оси х и у -начала и конца линии:"
    x.append([list_node_coor[line_data[i][0][1]][1],
             list_node_coor[line_data[i][-1][1]][1]])
    y.append([list_node_coor[line_data[i][0][1]][2],
             list_node_coor[line_data[i][-1][1]][2]])

  "############################################################################################"
  "ЭТОТ РАЗДЕЛ ДЛЯ РАБОТЫ С ПОЛИГОНАМИ:"

  poly_names = list(list_node_polygon.keys())
  poly_atribute = []

  for i in range(0, len(poly_names)):
    poly_atribute.append(i)

  surface_data = list(list_node_polygon.values())

  data_elem = []

  for i in range(0, len(poly_names)):
    for j in range(0, len(surface_data[i])):
      n1 = surface_data[i][j][1]
      n2 = surface_data[i][j][2]
      n3 = surface_data[i][j][3]
      data_elem.append([poly_atribute[i], n1, n2, n3])

  return x, y, line_names, data_elem, list_node_coor, poly_atribute, poly_names


def create_figure_2_3nodes(x, y, line_names, vert, elem_0, list_node_coor, poly_names):

  fig, ax = plt.subplots()

  for i in range(len(x)):
    plt.plot([x[i][0], x[i][1]], [y[i][0], y[i][1]])
    "Находим середину каждой линии, чтобы вставить туда подпись ее имени"
    xc = (x[i][1] - x[i][0]) / 2 + x[i][0]
    yc = (y[i][1] - y[i][0]) / 2 + y[i][0]
    ax.annotate(str(line_names[i]), xy=(xc, yc), xytext=(
      xc, yc), fontsize=10, font='Arial', color='k', label='Line_objects')

  nv = len(list_node_coor)

  nt = len(elem_0)
  nodes = np.zeros((nv, 2))
  elements = np.zeros((nt, 3))

  atrr = np.zeros(nt)

  for i in range(nv):
    nodes[i, 0] = vert[i][1]
    nodes[i, 1] = vert[i][2]

  for i in range(nt):
    elements[i, 0] = elem_0[i][1]
    elements[i, 1] = elem_0[i][2]
    elements[i, 2] = elem_0[i][3]
    atrr[i] = elem_0[i][0]

  xx = nodes[:, 0]
  yy = nodes[:, 1]

  triang = tri.Triangulation(xx, yy, elements.astype(int), mask=None)

  "Создаем графическое отображение результатов."

  pc = ax.tripcolor(triang, atrr, cmap='jet', alpha=1, antialiased=False)
  ax.set(xlabel='X Axis', ylabel='Y Axis')
  ax.set_aspect('equal', 'box')

  coord = np.zeros((nt, 3))
  for i in range(nt):
    coord[i, 0] = 1 / 3 * (vert[elem_0[i][1]][1] +
                           vert[elem_0[i][2]][1] + vert[elem_0[i][3]][1])
    coord[i, 1] = 1 / 3 * (vert[elem_0[i][1]][2] +
                           vert[elem_0[i][2]][2] + vert[elem_0[i][3]][2])
    coord[i, 2] = atrr[i]

  colors = []
  for i in range(len(poly_names)):
    colors.append(i)

  ploty = ax.scatter(coord[:, 0], coord[:, 1],
                     c=coord[:, 2], s=0, cmap='jet', alpha=1)
  handles = ploty.legend_elements(num=colors)[0]

  ax.legend(bbox_to_anchor=(1.02, 1), handles=handles,
            loc='upper left', labels=poly_names)
  fig.set_size_inches(12, 4.8, forward=True)

  response_json = mpld3.fig_to_dict(fig)

  # f = open('data/schemes/scheme.json', 'r')
  # response_json = f.read()
  return response_json
