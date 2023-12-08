import os
from pathlib import Path
from rest_framework.response import Response
from rest_framework.decorators import api_view
from main.models import FilesManagement
import numpy as np
import mpld3
import matplotlib.pyplot as plt
import matplotlib as mpl


BASE_DIR = Path(__file__).resolve().parent.parent


@api_view(['POST'])
def getData(request):
  gmsh_file = request.FILES['gmshFile']
  file_obj = FilesManagement.objects.create(gmsh_file=gmsh_file)

  gmsh_file = FilesManagement.objects.all()[0]
  gmsh_file_path = BASE_DIR / f'{gmsh_file}'

  list_node_coor, list_node_line, list_node_polygon = msh_prs(gmsh_file_path)
  x, y, line_names = create_figure_1(list_node_coor, list_node_line)

  response_data = create_figure_2(x, y, line_names)

  file_obj.delete()
  response = {
    'msg': 'Принял файл, считал, загрузил расчетную сетку', 'status': 200, 'json': response_data, 'calculatedSchemeData': {
      'list_node_coor': list_node_coor,
      'list_node_line': list_node_line,
      'list_node_polygon': list_node_polygon,
     }}

  return Response(response)


def msh_prs(name):
  # Импорт данных сетки из GMesh формата Abaqus INP

  # Чтение файла
  # script_dir = os.path.dirname(__file__)
  # file_path = os.path.join(script_dir, name)  # <---- название файла
  f = open(name, "r")
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


def create_figure_1(list_node_coor, list_node_line):
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
    "Списки заполняются по принципу: в общий список идет вложенный с координатов по оси х и у -начала и конца линии: "
    x.append([list_node_coor[line_data[i][0][1]][1],
             list_node_coor[line_data[i][-1][3]][1]])
    y.append([list_node_coor[line_data[i][0][1]][2],
             list_node_coor[line_data[i][-1][3]][2]])

  return x, y, line_names


def create_figure_2(x, y, line_names):

  fig, ax = plt.subplots()

  for i in range(len(x)):
    plt.plot([x[i][0], x[i][1]], [y[i][0], y[i][1]])
    "Находим середину каждой линии, чтобы вставить туда подпись ее имени"
    xc = (x[i][1] - x[i][0]) / 2 + x[i][0]
    yc = (y[i][1] - y[i][0]) / 2 + y[i][0]
    ax.annotate(str(line_names[i]), xy=(xc, yc), xytext=(
      xc, yc), fontsize=12, font='Arial', color='k', label='Line_objects')

  ax.set_aspect('equal', 'box')
  mpld3.save_json(fig, 'data/schemes/scheme.json')

  f = open('data/schemes/scheme.json', 'r')
  response_json = f.read()
  return response_json
