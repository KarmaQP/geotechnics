import numpy as np
import scipy as sc
from solver.nonlinearity.Phases_classes import PhasePlastic
from solver.nonlinearity.Models_classes import ModelLE, ModelMC


class StageConstruction:
  def __init__(self, phases, list_coor, list_line, list_polygon, lib_material):
    self.phases = phases
    self.list_coor = list_coor
    self.list_line = list_line
    self.list_polygon = list_polygon
    self.lib_material = lib_material

  @staticmethod
  def key_remove(d, key):
    r = dict(d)
    del r[key]
    return r

  def list_coor_create(self):
    input = self.list_coor
    # Метод создания списка координат определенного вида
    coor = []
    for i in range(len(input)):
      coor.append(input[i][1])
      coor[i].pop(0)
    coor = np.asarray(coor)
    return coor

  def list_line_create(self):
    input = self.list_line
    # Метод создания словаря карт связностей линий определенного вида
    list_line = {}
    for i in range(len(input)):
      for j in range(len(input[i])):
        list_line[input[i][0]] = input[i][1]
    for i in list_line.keys():
      for j in list_line[i]:
        j.pop(0)
    return list_line

  def list_polygon_create(self):
    input = self.list_polygon
    # Метод создания словаря карт связностей полигонов определенного вида
    list_polygon = {}
    for i in range(len(input)):
      for j in range(len(input[i])):
        list_polygon[input[i][0]] = input[i][1]
    for i in list_polygon.keys():
      for j in list_polygon[i]:
        j.pop(0)
    for i in list_polygon.keys():
      list_polygon[i] = np.asarray(list_polygon[i])
    return list_polygon

  def material_create(self):
    # Метод создания словаря материалов определенного вида
    materials_soils = {}
    for i in self.lib_material.keys():
      if i == 'twoDimData':
        for j in self.lib_material[i]:
          if list(j.values())[0]['mechParameter'] == 'linear-elastic':
            materials_soils[list(j.keys())[0]] = ModelLE(weight=list(j.values())[0]['weight'],
                                                         e_ur=list(j.values())[
                0]['elasticModulus'],
                v_ur=list(j.values())[0]['poisson'])
          if list(j.values())[0]['mechParameter'] == 'mohr-coloumb':
            materials_soils[list(j.keys())[0]] = ModelMC(weight=list(j.values())[0]['weight'],
                                                         e_ur=list(j.values())[
                0]['elasticModulus'],
                v_ur=list(j.values())[
                0]['poisson'],
                c=list(j.values())[
                0]['adhesion'],
                fi=list(j.values())[
                0]['internalFrictionAngle'],
                T=list(j.values())[
                0]['tensileStrength'],
                psi=list(j.values())[0]['dilatancyAngle'])
    return materials_soils

  def material_in_phase(self):
    # Метод переопределяет название материала в фазе в объект с назначенными свойствами
    lib = self.material_create()
    for i in self.phases:
      for j in i['data']['soils']:
        j['material'] = lib[j['material']]

  def redefenition(self):
    # Метод переопределяет исходные данные в нужный вид для расчета (вызывать не более 1 раза)
    self.list_polygon = self.list_polygon_create()
    self.list_line = self.list_line_create()
    self.list_coor = self.list_coor_create()
    self.material_in_phase()

  def sequence(self):
    result = {}
    sigma = {}
    for i, string in enumerate(self.phases[0]['data']['soils']):
      num_el = len(self.list_polygon[string['name']][:, 0])
      sigma[string['name']] = np.zeros((3 * num_el, 3), dtype=np.float64)
    for i, string in enumerate(self.phases):
      # Если фаза Initial_phase
      if string['startFromPhase'] is None:
        print('Solve Initial_phase')
        result[string['id']] = PhasePlastic(phase=self.phases[i]['data'],
                                            list_coor=self.list_coor,
                                            list_line=self.list_line,
                                            list_polygon=self.list_polygon,
                                            sigma=sigma,
                                            tolerated_error=self.phases[i]['numericalControlParameters']['toleratedError'],
                                            min_num_iter=self.phases[i]['numericalControlParameters'][
                                                'desiredMinNumberOfIterations'],
                                            max_num_iter=self.phases[i]['numericalControlParameters'][
                                                'desiredMaxNumberOfIterations'],
                                            max_steps=self.phases[i]['numericalControlParameters'][
                                                'maxSteps'],
                                            max_unloading_steps=self.phases[i]['numericalControlParameters'][
                                                'maxUnloadingSteps'],
                                            max_load_fraction_per_step=self.phases[i]['numericalControlParameters'][
                                                'maxLoadFractionPerStep'],
                                            max_number_of_iterations=self.phases[i]['numericalControlParameters'][
                                                'maxNumberOfIterations']).plastic_solve()
      # Если фаза последующая
      if string['startFromPhase'] == self.phases[i - 1]['id']:
        print('\n')
        print('Solve ', string['id'])
        result[string['id']] = PhasePlastic(phase=self.phases[i]['data'],
                                            list_coor=self.list_coor,
                                            list_line=self.list_line,
                                            list_polygon=self.list_polygon,
                                            sigma=result[self.phases[i - 1]
                                                         ['id']]['sigma'],
                                            tolerated_error=self.phases[i]['numericalControlParameters']['toleratedError'],
                                            min_num_iter=self.phases[i]['numericalControlParameters'][
                                                'desiredMinNumberOfIterations'],
                                            max_num_iter=self.phases[i]['numericalControlParameters'][
                                                'desiredMaxNumberOfIterations'],
                                            max_steps=self.phases[i]['numericalControlParameters'][
                                                'maxSteps'],
                                            max_unloading_steps=self.phases[i]['numericalControlParameters'][
                                                'maxUnloadingSteps'],
                                            max_load_fraction_per_step=self.phases[i]['numericalControlParameters'][
                                                'maxLoadFractionPerStep'],
                                            max_number_of_iterations=self.phases[i]['numericalControlParameters'][
                                                'maxNumberOfIterations']).plastic_solve()
    print()
    print('Solve completed')
    return result

  def deactive_nodes(self, phase_num):
    # Метод получения списка деактивируемых узлов
    list_deactive_nodes = []
    list_active_nodes = []
    for i in self.phases[phase_num]['data']['soils']:
      if not i["phaseActivity"]:
        list_deactive_nodes.extend(self.list_polygon[i['name']].tolist())
      else:
        list_active_nodes.extend(self.list_polygon[i['name']].tolist())
    list_deactive_nodes = np.unique(np.asarray(list_deactive_nodes))
    list_active_nodes = np.unique(np.asarray(list_active_nodes))
    list_deactive = sorted(
      list(set(list_deactive_nodes) - set(list_active_nodes)))
    return list_deactive

  def list_coor_print(self, phase_num):
    list_coor = self.list_coor
    if len(self.deactive_nodes(phase_num)) != 0:
      for i, val in enumerate(self.deactive_nodes(phase_num)):
        num = val - i
        list_coor = np.delete(list_coor, num, axis=0)
    return list_coor

  def list_active_nodes(self, phase_num):
    # Метод формирования карты связности включенных полигонов в виде массива из словаря
    list_active_nodes = []
    # Удаляем выключенные полигоны
    for i in self.phases[phase_num]['data']['soils']:
      if i["phaseActivity"]:
        list_active_nodes.extend(self.list_polygon[i['name']].tolist())
    list_nodes = np.asarray(list_active_nodes)
    # Изменяем номера узлов из-за выключенных полигонов
    list_deactive_nodes = self.deactive_nodes(phase_num)
    sup = np.zeros_like(list_nodes)
    if len(list_deactive_nodes) != 0:
      for i in list_deactive_nodes:
        if (i > list_nodes).any():
          sup += np.array((i < list_nodes), dtype=np.int_)
    list_nodes -= sup
    return list_nodes

  def list_nodes_print(self, phase_num):
    list_nodes = self.list_active_nodes(phase_num)
    # Переформировываем карту связности
    r, c = list_nodes.shape
    list_nodes_tri = np.zeros((r * 4, 3))
    for i in range(r):
      list_nodes_tri[4 * i, 0] = list_nodes[i, 0]
      list_nodes_tri[4 * i, 1] = list_nodes[i, 3]
      list_nodes_tri[4 * i, 2] = list_nodes[i, 5]

      list_nodes_tri[4 * i + 1, 0] = list_nodes[i, 3]
      list_nodes_tri[4 * i + 1, 1] = list_nodes[i, 1]
      list_nodes_tri[4 * i + 1, 2] = list_nodes[i, 4]

      list_nodes_tri[4 * i + 2, 0] = list_nodes[i, 5]
      list_nodes_tri[4 * i + 2, 1] = list_nodes[i, 4]
      list_nodes_tri[4 * i + 2, 2] = list_nodes[i, 2]

      list_nodes_tri[4 * i + 3, 0] = list_nodes[i, 4]
      list_nodes_tri[4 * i + 3, 1] = list_nodes[i, 5]
      list_nodes_tri[4 * i + 3, 2] = list_nodes[i, 3]
    return list_nodes_tri

  def displacement_print(self, x, phase_num):
    num_nodes = len(self.list_coor[:, 0])
    disp_x = np.zeros(num_nodes, dtype=np.float64)
    disp_y = np.zeros(num_nodes, dtype=np.float64)
    for j in range(num_nodes):
      disp_x[j] = x[2 * j]
      disp_y[j] = x[2 * j + 1]
    list_deactive_nodes = self.deactive_nodes(phase_num)
    for i, val in enumerate(list_deactive_nodes):
      num = val - i
      disp_x = np.delete(disp_x, num, axis=0)
      disp_y = np.delete(disp_y, num, axis=0)
    return disp_x, disp_y

  def sigma_print(self, sigma, phase_num):
    # Удаляем выключенные полигоны
    for i in self.phases[phase_num]['data']['soils']:
      if not i["phaseActivity"]:
        sigma = self.key_remove(sigma, i['name'])
    # Объединяем значения словаря в массив
    a = np.array([[0, 0, 0]])
    for i in sigma.values():
      a = np.concatenate((a, i), axis=0)
    a = np.delete(a, 0, axis=0)
    return a

  def epsilon_print(self, epsilon, phase_num):
    # Объединяем значения словаря в массив
    a = np.array([[0, 0, 0]])
    for i in epsilon.values():
      a = np.concatenate((a, i), axis=0)
    a = np.delete(a, 0, axis=0)
    return a

  def mid_coor_calc(self, phase_num):
    nodes = self.list_active_nodes(phase_num)
    coor = self.list_coor_print(phase_num)
    num_el = nodes.shape[0]
    # Вычисление координат точек интегрирования и карт связности промежуточных треугольников
    list_coor_mid = np.zeros((num_el * 3, 2), dtype=np.float64)
    for i in range(num_el):
      # 0 точка интегрирования
      list_coor_mid[3 * i, 0] = (coor[nodes[i, 0], 0] +
                                 coor[nodes[i, 3], 0] + coor[nodes[i, 5], 0]) / 3
      list_coor_mid[3 * i, 1] = (coor[nodes[i, 0], 1] +
                                 coor[nodes[i, 3], 1] + coor[nodes[i, 5], 1]) / 3
      # 1 точка интегрирования
      list_coor_mid[3 * i + 1, 0] = (coor[nodes[i, 3], 0] +
                                     coor[nodes[i, 1], 0] + coor[nodes[i, 4], 0]) / 3
      list_coor_mid[3 * i + 1, 1] = (coor[nodes[i, 3], 1] +
                                     coor[nodes[i, 1], 1] + coor[nodes[i, 4], 1]) / 3
      # 2 точка интегрирования
      list_coor_mid[3 * i + 2, 0] = (coor[nodes[i, 2], 0] +
                                     coor[nodes[i, 5], 0] + coor[nodes[i, 4], 0]) / 3
      list_coor_mid[3 * i + 2, 1] = (coor[nodes[i, 2], 1] +
                                     coor[nodes[i, 5], 1] + coor[nodes[i, 4], 1]) / 3
    return list_coor_mid

  def map_large(self, phase_num):
    list_nodes = self.list_active_nodes(phase_num)
    # Возвращаем словарь без промежуточных узлов
    return list_nodes[:, 0:3]

  def index_print(self, index, phase_num):
    # Удаляем выключенные полигоны
    for i in self.phases[phase_num]['data']['soils']:
      if not i["phaseActivity"]:
        index = self.key_remove(index, i['name'])
    a = np.array([[0]])
    for i in index.values():
      if len(i.shape) == 2:
        a = np.concatenate((a, i), axis=0)
    a = np.delete(a, 0, axis=0)

    elastic = []
    plastic = []
    tension = []
    coor = self.mid_coor_calc(phase_num)

    for i, string in enumerate(a):
      if string == 0:
        elastic.append([coor[i, 0], coor[i, 1]])
      if string == 1 or string == 3:
        plastic.append([coor[i, 0], coor[i, 1]])
      if string == 2 or string == 4:
        tension.append([coor[i, 0], coor[i, 1]])
    elastic = np.asarray(elastic)
    plastic = np.asarray(plastic)
    tension = np.asarray(tension)
    return elastic, plastic, tension

  def materials_color(self):
    lib = self.material_create()
    for i, color in enumerate(lib.keys()):
      lib[color] = i
    color_lib = {}
    for i in self.phases:
      for polygon in i['data']['soils']:
        color_lib[polygon['name']] = lib[polygon['material']]
    return color_lib

  def element_color(self, color_lib, phase_num):
    list_polygon = self.list_polygon
    for i in self.phases[phase_num]['data']['soils']:
      if not i["phaseActivity"]:
        list_polygon = self.key_remove(list_polygon, i['name'])
    colors = []
    for i in list_polygon.keys():
      if i in list(color_lib.keys()):
        colors += ((np.ones_like(list_polygon[i]
                   [:, 0]) * color_lib[i]).tolist())
    return colors

  def interpolate(self, values, phase_num):
    x = self.mid_coor_calc(phase_num)[:, 0]
    y = self.mid_coor_calc(phase_num)[:, 1]
    xnew = self.list_coor_print(phase_num)[:, 0]
    ynew = self.list_coor_print(phase_num)[:, 1]

    inter = sc.interpolate.Rbf(x, y, values, function='linear')
    value_new = inter(xnew, ynew)
    return value_new

  def result_print(self):
    color_lib = self.materials_color()
    self.redefenition()
    res = self.sequence()
    print('Archive results to Output')
    geometry_points = {}
    geometry_nodes = {}
    result = {}
    for i, name in enumerate(res.keys()):
      geometry_points[name] = {'x': self.list_coor_print(i)[:, 0],
                               'y': self.list_coor_print(i)[:, 1],
                               'map': self.list_nodes_print(i)}
      geometry_nodes[name] = {'map': self.map_large(i),
                              'mat_colors': self.element_color(color_lib, i)}
      result[name] = {'u_x': self.displacement_print(res[name]['x'], i)[0],
                      'u_y': self.displacement_print(res[name]['x'], i)[1],
                      'eps_XX': self.interpolate(self.epsilon_print(res[name]['epsilon'], i)[:, 0], i),
                      'eps_YY': self.interpolate(self.epsilon_print(res[name]['epsilon'], i)[:, 1], i),
                      'eps_XY': self.interpolate(self.epsilon_print(res[name]['epsilon'], i)[:, 2], i),
                      'sigma_XX': self.interpolate(self.sigma_print(res[name]['sigma'], i)[:, 0], i),
                      'sigma_YY': self.interpolate(self.sigma_print(res[name]['sigma'], i)[:, 1], i),
                      'sigma_XY': self.interpolate(self.sigma_print(res[name]['sigma'], i)[:, 2], i),
                      'stress_points': self.index_print(res[name]['index'], i)}
    return geometry_points, geometry_nodes, result
