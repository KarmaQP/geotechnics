import os
from pathlib import Path
from rest_framework.response import Response
from rest_framework.decorators import api_view
from main.models import FilesManagement
import numpy as np
import mpld3
import matplotlib.pyplot as plt
import matplotlib.tri as tri
import json
from solver.Head import solver
from solver.output_results import create_data, isofields
import matplotlib.colors as colors
from mpld3 import plugins
import pandas as pd
import scipy.sparse.linalg
from scipy.sparse import csr_matrix


BASE_DIR = Path(__file__).resolve().parent.parent


@api_view(['POST'])
def getSolverData(request):
  try:
    data = request.data
    task_type = data['task_type']
    input_data = data['input_data']
    coor_data = data['coor_data']
    polygons_data = data['polygons_data']
    lines_data = data['lines_data']
  except Exception as err:
    response = {
        'msg': f"Ошибка в сборе исходных данных! Пожалуйста, проверьте правильность заполнения исходных данных или сборки gmsh-файла. {type(err).__name__}: {err}.", 'status': 400,
      }

    return Response(response)

  print(task_type)
  if task_type == 'elasticity-nonlinearity':
    # list_coor = create_list_coor(coor_data)
    # polygons_node_list = create_polygons_node_list(polygons_data)
    # lines_node_list = create_lines_node_list(lines_data)
    # num_nodes = len(list_coor)
    try:
      geometry_points, geometry_nodes, result = solver(
        input_data, coor_data, polygons_data, lines_data)

      results_data = create_data(result, geometry_points, geometry_nodes)
      min_max_values = isofields(results_data)

      return Response({'msg': 'Получены данные для решателя.', 'status': 200, 'min_max_values': min_max_values})
    except Exception as err:
      response = {
          'msg': f"Ошибка в расчете! Пожалуйста, проверьте правильность заполнения исходных данных или сборки gmsh-файла. {type(err).__name__}: {err}.", 'status': 400,
      }

      return Response(response)
  elif task_type == 'filtration':
    try:
      coord, list_node_polygon, list_node_line = generate_data(
          coor_data, polygons_data, lines_data)

      nn, ne, nodes, elem, propertires, nodes_s = create_data_wtf(
          coord, list_node_line, list_node_polygon, input_data)

      d_ind = bc(elem, ne, list_node_line, input_data)

      for i in range(0, 5):
        "Нижние две строчки запускают генерацию матрицы и ее расчет:"
        K, r, Bb = gKr(elem, nodes, ne, nn, d_ind, propertires)
        K_sp = csr_matrix(K)
        a = scipy.sparse.linalg.spsolve(K_sp, r)
        # a = np.linalg.solve(K, r)
        propertires = dc(a, propertires, ne, elem, nodes)

      v, I, pw = velocities_gradients(a, elem, ne, Bb, propertires, nodes, nn)
      results_data = create_data_filtration(nodes, elem, a, pw, v, I, nodes_s)
      min_max_values = isofields_filtration(results_data, v)

      return Response({'msg': 'Получены данные для решателя.', 'status': 200, 'min_max_values': min_max_values})
    except Exception as err:
      response = {
          'msg': f"Ошибка в расчете! Пожалуйста, проверьте правильность заполнения исходных данных или сборки gmsh-файла. {type(err).__name__}: {err}.", 'status': 400,
      }

      return Response(response)
  elif task_type == 'temperature':
    try:
      step_num = data['step_num']

      coord, list_node_polygon, list_node_line = generate_data(
        coor_data, polygons_data, lines_data)

      nn, ne, nodes, elem, propertires, nodes_s = create_data_temp(
          coord, list_node_line, list_node_polygon, input_data)

      d_ind = bc_temp(elem, ne, list_node_line, input_data)
      d_ind_T0 = bc_T0(elem, ne, list_node_line, input_data)

      t = int(input_data['timeSteps']['calcTime'])
      N = int(input_data['timeSteps']['numSteps'])

      K, r = gKr_T0(elem, nodes, ne, nn, d_ind_T0, propertires)
      K_sp = csr_matrix(K)
      T0 = scipy.sparse.linalg.spsolve(K_sp, r)
      # T0 = np.linalg.solve(K, r)

      N, dt, Tstep, data_fig, T = inithial_param(N, t, T0)

      for i in range(N):
        "Нижние две строчки запускают генерацию матрицы и ее расчет:"
        K, r = gKr_temp(elem, nodes, ne, nn, d_ind, propertires, T, dt)
        K_sp = csr_matrix(K)
        T = scipy.sparse.linalg.spsolve(K_sp, r)
        # T = np.linalg.solve(K, r)
        Tstep.append(T)
        data_fig[f"Время расчета t={t*(i+1)/N}, с:"] = Tstep[i + 1]

      # step = 2
      step = int(step_num)
      min_max_values = isofields_temp(nodes, data_fig, elem, step)
      data_keys = data_fig.keys()

      return Response({'msg': 'Получены данные для решателя.', 'status': 200, 'min_max_values': min_max_values, 'select_values': data_keys})
    except Exception as err:
      response = {
          'msg': f"Ошибка в расчете! Пожалуйста, проверьте правильность заполнения исходных данных или сборки gmsh-файла. {type(err).__name__}: {err}.", 'status': 400,
      }

      return Response(response)


@api_view(['POST'])
def getData(request):
  task_type = request.POST['taskType']

  gmsh_file = request.FILES['gmshFile']
  file_obj = FilesManagement.objects.create(gmsh_file=gmsh_file)
  gmsh_file = FilesManagement.objects.all()[0]

  gmsh_file_path = BASE_DIR / f'{gmsh_file.gmsh_file.name}'

  if task_type == 'elasticity-nonlinearity':
    try:
      list_node_coor, list_node_line, list_node_polygon = msh_prs(
        gmsh_file_path)
      x, y, line_names, data_elem, list_node_coor, poly_atribute, poly_names = create_figure_1(
        list_node_coor, list_node_line, list_node_polygon)

      response_data = create_figure_2(x, y, line_names, list_node_coor,
                                      data_elem, list_node_coor, poly_names, data_elem)

      gmsh_json_content = json.dumps(response_data)

      file_obj.delete()
      response = {
        'msg': 'Данные загружены успешно! Тип задачи: упругость.', 'status': 200, 'json': gmsh_json_content, 'calculatedSchemeData': {
          'list_node_coor': list_node_coor,
          'list_node_line': list_node_line,
          'list_node_polygon': list_node_polygon,
        }
      }
      return Response(response)
    except Exception as err:
      file_obj.delete()

      response = {
          'msg': f"Ошибка при чтении файла! Пожалуйста, проверьте правильность сборки gmsh-файла и типа выбранной задачи. {type(err).__name__}: {err}.", 'status': 400,
      }
      return Response(response)
  else:
    try:
      list_node_coor, list_node_line, list_node_polygon = msh_prs_3_nodes(
        gmsh_file_path)
      x, y, line_names, data_elem, list_node_coor, poly_atribute, poly_names = create_figure_1_3nodes(
        list_node_coor, list_node_line, list_node_polygon)

      response_data = create_figure_2_3nodes(
        x, y, line_names, list_node_coor, data_elem, list_node_coor, poly_names)

      file_obj.delete()
      response = {
        'msg': 'Данные загружены успешно! Тип задачи: фильтрация/температуры.', 'status': 200, 'json': json.dumps(response_data), 'calculatedSchemeData': {
          'list_node_coor': list_node_coor,
          'list_node_line': list_node_line,
          'list_node_polygon': list_node_polygon,
        }
      }
      return Response(response)
    except Exception as err:
      file_obj.delete()

      response = {
          'msg': f"Ошибка при чтении файла! Пожалуйста, проверьте правильность сборки gmsh-файла и типа выбранной задачи. {type(err).__name__}: {err}.", 'status': 400,
      }
      return Response(response)


def inithial_param(N, t, T0):

  dt = t / N
  Tstep = []

  Tstep.append(T0)
  data_fig = {"Время расчета t=0, с": Tstep[0]}
  T = T0

  return N, dt, Tstep, data_fig, T


def create_list_coor(coor_data):
  list_coor = []

  for i in range(len(coor_data)):
    list_coor.append(coor_data[i][1])
    list_coor[i].pop(0)

  list_coor = np.array(list_coor)
  return list_coor


def create_polygons_node_list(polygons_data):
  polygons_node_list = {}
  for i in range(len(polygons_data)):
    for j in range(len(polygons_data[i])):
      polygons_node_list[polygons_data[i][0]] = polygons_data[i][1]

  for i in polygons_node_list.keys():
    for j in polygons_node_list[i]:
      j.pop(0)
  return polygons_node_list


def create_lines_node_list(lines_data):
  lines_node_list = {}

  for i in range(len(lines_data)):
    for j in range(len(lines_data[i])):
      lines_node_list[lines_data[i][0]] = lines_data[i][1]

  return lines_node_list


def msh_prs(file_path):
  # Импорт данных сетки из GMesh формата Abaqus INP

  # Чтение файла
  # script_dir = os.path.dirname(__file__)
  # file_path = os.path.join(script_dir, name)  # <---- название файла
  try:
    f = open(file_path, "r")
    data = f.read()
    data = data.split('\n')

    # Поиск границ групп по ключевым словам
    node_start = 0
    node_end = 0
    for i, line in enumerate(data):
      if line == '*NODE':
        node_start = i + 1
      if line == '******* E L E M E N T S *************':
        node_end = i
      if line == data[-1]:
        el_end = i
    el_start = node_end + 1

    # Вычленение списка координат в формате списка Пайтон: номер строки - номер узла, далее координаты Х и У.
    list_node_coor = []
    for i, line in enumerate(data[node_start:node_end]):
      "Я ПЕРЕПИСАЛ СТРОЧКУ 31!!! Т.к. в парсере элементы шли не по порядку и номера узлов путались. Теперь массив узлов в начале содержит конкретный номер узла из расчетной схемы."
      list_node_coor.append([np.int64(line.split(
        ', ')[0]) - 1, np.float64(line.split(', ')[1]), np.float64(line.split(', ')[2])])

    # Вычленение номеров строк геометрических примитивов и их наименований
    line_index = []  # номера строк, где находится начало группы линий
    line_id = []  # индентификаторы групп линий
    polygon_index = []  # номера строк, где находится начало группы полигонов
    polygon_id = []  # индентификаторы групп полигонов

    for i, line in enumerate(data[el_start:el_end]):
      if '*ELEMENT, type=T3D3, ELSET=' in line:
        line_index.append(i + el_start)
        line_id.append(line[len('*ELEMENT, type=T3D3, ELSET='):len(line)])
      if '*ELEMENT, type=CPS6, ELSET=' in line:
        polygon_index.append(i + el_start)
        polygon_id.append(line[len('*ELEMENT, type=CPS6, ELSET='):len(line)])

    def dict_map_create(text, index, name):
      # Функция заполняет словари карт связности геометрических примитивов
      dict_map = {}
      element = []
      for j, string in enumerate(text[index[0]: index[-1]]):
        for s in range(len(index)):
          if j + index[0] == index[s]:
            element.append(text[index[s] + 1: index[s + 1]])

      element_el = []
      for j in range(len(element)):
        for s in range(len(element[j])):
          element_el.append(element[j][s].split(', '))
          element_el[s] = list(filter(None, element_el[s]))
          element_el[s] = list(map(int, element_el[s]))
        dict_map[name[j]] = element_el[0:len(element_el)]
        element_el.clear()

      for j in range(len(dict_map)):
        dict_map[name[j]] = np.asarray(dict_map[name[j]], dtype=np.int_)

      return dict_map

    line_index.append(polygon_index[0])
    polygon_index.append(el_end)
    list_node_line = dict_map_create(data, line_index, line_id)
    list_node_polygon = dict_map_create(data, polygon_index, polygon_id)

    # Принимаем нумерацию узлов и элементов с 0
    subtract_one = np.vectorize(lambda k: k - 1)
    for t in list_node_line.keys():
      list_node_line[t] = subtract_one(list_node_line[t])
    for t in list_node_polygon.keys():
      list_node_polygon[t] = subtract_one(list_node_polygon[t])

    # ДОПОЛНИТЕЛЬНО: преобразуем элементы словарей карт связности в списки Пайтон
    for t in list_node_line.keys():
      list_node_line[t] = list_node_line[t].tolist()
    for t in list_node_polygon.keys():
      list_node_polygon[t] = list_node_polygon[t].tolist()

    # ЗАКЛЮЧЕНИЕ. Из этого файла выводим:
    # list_node_coor - координаты узлов в виде списка пайтон
    # list_node_line - словарь карт связности линий. Внутри списки пайтон
    # list_node_polygon - словарь карт связности полигонов. Внутри списки пайтон
    "Я ПЕРЕПИСАЛ СТРОЧКУ 98!!! Поскольку узлы были перемешаны, мне нужно было их отсортировать."
    list_node_coor.sort()

    return list_node_coor, list_node_line, list_node_polygon
  except:
    f.close()
    return [], [], []


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


def msh_prs_3_nodes(file_path):
  try:
    # Чтение файла
    f = open(file_path, "r")
    data = f.read()
    data = data.split('\n')

    # Поиск границ групп по ключевым словам
    node_start = 0
    node_end = 0
    for i, line in enumerate(data):
      if line == '*NODE':
        node_start = i + 1
      if line == '******* E L E M E N T S *************':
        node_end = i
      if line == data[-1]:
        el_end = i
    el_start = node_end + 1

    # Вычленение списка координат в формате списка Пайтон: номер строки - номер узла, далее координаты Х и У.
    list_node_coor = []
    for i, line in enumerate(data[node_start:node_end]):
      "Я ПЕРЕПИСАЛ СТРОЧКУ 31!!! Т.к. в парсере элементы шли не по порядку и номера узлов путались. Теперь массив узлов в начале содержит конкретный номер узла из расчетной схемы."
      list_node_coor.append([np.int64(line.split(
        ', ')[0]) - 1, np.float64(line.split(', ')[1]), np.float64(line.split(', ')[2])])

    # Вычленение номеров строк геометрических примитивов и их наименований
    line_index = []  # номера строк, где находится начало группы линий
    line_id = []  # индентификаторы групп линий
    polygon_index = []  # номера строк, где находится начало группы полигонов
    polygon_id = []  # индентификаторы групп полигонов

    for i, line in enumerate(data[el_start:el_end]):
      if '*ELEMENT, type=T3D2, ELSET=' in line:
        line_index.append(i + el_start)
        line_id.append(line[len('*ELEMENT, type=T3D2, ELSET='):len(line)])
      if '*ELEMENT, type=CPS3, ELSET=' in line:
        polygon_index.append(i + el_start)
        polygon_id.append(line[len('*ELEMENT, type=CPS3, ELSET='):len(line)])

    def dict_map_create(text, index, name):
      # Функция заполняет словари карт связности геометрических примитивов
      dict_map = {}
      element = []
      for j, string in enumerate(text[index[0]: index[-1]]):
        for s in range(len(index)):
          if j + index[0] == index[s]:
            element.append(text[index[s] + 1: index[s + 1]])

      element_el = []
      for j in range(len(element)):
        for s in range(len(element[j])):
          element_el.append(element[j][s].split(', '))
          element_el[s] = list(filter(None, element_el[s]))
          element_el[s] = list(map(int, element_el[s]))
        dict_map[name[j]] = element_el[0:len(element_el)]
        element_el.clear()

      for j in range(len(dict_map)):
        dict_map[name[j]] = np.asarray(dict_map[name[j]], dtype=np.int_)

      return dict_map

    line_index.append(polygon_index[0])
    polygon_index.append(el_end)
    list_node_line = dict_map_create(data, line_index, line_id)
    list_node_polygon = dict_map_create(data, polygon_index, polygon_id)

    # Принимаем нумерацию узлов и элементов с 0
    subtract_one = np.vectorize(lambda k: k - 1)
    for t in list_node_line.keys():
      list_node_line[t] = subtract_one(list_node_line[t])
    for t in list_node_polygon.keys():
      list_node_polygon[t] = subtract_one(list_node_polygon[t])

    # ДОПОЛНИТЕЛЬНО: преобразуем элементы словарей карт связности в списки Пайтон
    for t in list_node_line.keys():
      list_node_line[t] = list_node_line[t].tolist()
    for t in list_node_polygon.keys():
      list_node_polygon[t] = list_node_polygon[t].tolist()

    # ЗАКЛЮЧЕНИЕ. Из этого файла выводим:
    # list_node_coor - координаты узлов в виде списка пайтон
    # list_node_line - словарь карт связности линий. Внутри списки пайтон
    # list_node_polygon - словарь карт связности полигонов. Внутри списки пайтон
    "Я ПЕРЕПИСАЛ СТРОЧКУ 98!!! Поскольку узлы были перемешаны, мне нужно было их отсортировать."
    list_node_coor.sort()

    return list_node_coor, list_node_line, list_node_polygon
  except:
    f.close()
    return [], [], []


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

  return min_max_values


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
