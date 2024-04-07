
import numpy as np
import scipy as sp
import sys
from solver.nonlinearity.Geometry_classes import Polygon, Line


class PhasePlastic:
  def __init__(self, phase, list_coor, list_line, list_polygon, sigma, tolerated_error, min_num_iter, max_num_iter,
               max_steps, max_unloading_steps, max_load_fraction_per_step, max_number_of_iterations,
               index=None, x=None, nodes_off=None):
    self.phase = phase
    self.sigma = sigma
    self.x = x
    self.index = index
    self.list_coor = list_coor
    self.list_line = list_line
    self.list_polygon = list_polygon
    self.nodes_off = nodes_off
    self.tolerated_error = tolerated_error
    self.min_num_iter = min_num_iter
    self.max_num_iter = max_num_iter
    self.max_steps = max_steps
    self.max_unloading_steps = max_unloading_steps
    self.max_load_fraction_per_step = max_load_fraction_per_step
    self.max_number_of_iterations = max_number_of_iterations

  def boundary(self):
    bc = {}
    # Цикл по всем линиям
    for i in self.phase['lines']:
      # Проверка активности линии на фазе
      if i['phaseActivity']:
        # Проверка наличия у линии свойства граничного условия
        if ('ux' in list(i["propertyParams"].keys())) or ('uy' in list(i["propertyParams"].keys())):
          bc[i['name']] = Line(list_node_coor=self.list_coor,
                               list_nodes=self.list_line[i['name']],
                               data=i).bound_cond()
    return bc

  def k_glob_clean(self, k_glob):
    if self.nodes_off is not None:
      # Функция удаления нулевых пар строка-столбец
      string = np.zeros_like(k_glob[0])
      self.nodes_off = []
      for i, row in enumerate(k_glob):
        a_bool = np.all(row == string)
        if a_bool and np.all(row == k_glob[:, i]):
          self.nodes_off.append(i)
      for i, num in enumerate(self.nodes_off):
        k_glob = np.delete(k_glob, num - i, axis=0)
        k_glob = np.delete(k_glob, num - i, axis=1)
    return k_glob

  def k_glob_sum(self, sigma_last, index_last):
    num_nodes = len(self.list_coor[:, 0])
    k_glob = sp.sparse.csc_matrix(
      ([0], ([0], [0])), shape=(num_nodes * 2, num_nodes * 2))
    for i in self.phase['soils']:
      if i['phaseActivity']:
        mat = i['material']
        k_glob += Polygon(self.list_coor, self.list_polygon[i['name']], mat,
                          sigma_last[i['name']], index_last[i['name']]).stiff_matrix()
    for i in self.phase['lines']:
      bound = self.boundary()[i['name']]
      for j, row in enumerate(bound):
        if row[0] == 1:  # граничное условие по Х
          k_glob[2 * j] = 0
          k_glob[2 * j, 2 * j] = 1
        if row[1] == 1:  # граничное условие по Y
          k_glob[2 * j + 1] = 0
          k_glob[2 * j + 1, 2 * j + 1] = 1

    return self.k_glob_clean(k_glob)

  def r_glob_sum(self):
    num_nodes = len(self.list_coor[:, 0])
    r_glob = np.zeros(num_nodes * 2, dtype=np.float64)
    for i in self.phase['soils']:
      if i['phaseActivity']:
        mat = i['material']
        r_glob += Polygon(self.list_coor,
                          self.list_polygon[i['name']], mat, 0, 0).r_glob_vector()
    for i in self.phase['lines']:
      bound = self.boundary()[i['name']]
      for j, row in enumerate(bound):
        if row[0] == 1:  # граничное условие по Х
          r_glob[2 * j] = 0
        if row[1] == 1:  # граничное условие по Y
          r_glob[2 * j + 1] = 0
    if self.nodes_off is not None:
      for i, el in enumerate(self.nodes_off):
        r_glob = np.delete(r_glob, el - i)
    return r_glob

  @staticmethod
  def solve(k_glob, r_glob):
    d_x_vector, exit_code = sp.sparse.linalg.bicg(k_glob, r_glob, atol=1e-3)
    print()
    print('Ошибка решения СЛАУ:', exit_code)
    return d_x_vector

  def sigma_calc(self, index_last, d_x):
    delta = {}
    for i in self.phase['soils']:
      if i['phaseActivity']:
        row, col = self.list_polygon[i['name']].shape
        delta[i['name']] = np.zeros((row, 2 * col), dtype=np.float64)
    for i in delta.keys():
      for j, string in enumerate(delta[i]):
        for k in range(6):
          delta[i][j, 2 * k] = d_x[2 * self.list_polygon[i][j, k]]
          delta[i][j, 2 * k + 1] = d_x[2 * self.list_polygon[i][j, k] + 1]
    sig_int = {}
    tau = {}
    sig_elast = {}
    for i in self.phase['soils']:
      if i['phaseActivity']:
        mat = i['material']
        (sig_int[i['name']],
         index_last[i['name']], tau[i['name']],
         sig_elast[i['name']]) = Polygon(list_coor=self.list_coor,
                                         list_nodes=self.list_polygon[i['name']],
                                         material=mat,
                                         sigma=self.sigma[i['name']],
                                         index=index_last[i['name']]).sigma_calc(delta[i['name']])
    return sig_int, index_last, tau, sig_elast

  def epsilon_calc(self, x):
    delta = {}
    for i in self.phase['soils']:
      if i['phaseActivity']:
        row, col = self.list_polygon[i['name']].shape
        delta[i['name']] = np.zeros((row, 2 * col), dtype=np.float64)
    for i in delta.keys():
      for j, string in enumerate(delta[i]):
        for k in range(6):
          delta[i][j, 2 * k] = x[2 * self.list_polygon[i][j, k]]
          delta[i][j, 2 * k + 1] = x[2 * self.list_polygon[i][j, k] + 1]
    eps = {}
    for i in self.phase['soils']:
      if i['phaseActivity']:
        eps[i['name']] = Polygon(list_coor=self.list_coor,
                                 list_nodes=self.list_polygon[i['name']]).epsilon_calc(delta[i['name']])
    return eps

  def r_internal(self, sigma_int):
    num_nodes = len(self.list_coor[:, 0])
    r = np.zeros(num_nodes * 2, dtype=np.float64)
    for i in self.phase['soils']:
      if i['phaseActivity']:
        r += Polygon(self.list_coor,
                     self.list_polygon[i['name']]).r_internal(sigma_int[i['name']])
    for i in self.phase['lines']:
      bound = self.boundary()[i['name']]
      for j, row in enumerate(bound):
        if row[0] == 1:  # граничное условие по Х
          r[2 * j] = 0
        if row[1] == 1:  # граничное условие по Y
          r[2 * j + 1] = 0
    if self.nodes_off is not None:
      for i, el in enumerate(self.nodes_off):
        r = np.delete(r, el - i)
    return r

  def last_force_int(self):
    # Расчет вектора внутренних сил от деактивированных полигонов с прошлой фазы
    num_nodes = len(self.list_coor[:, 0])
    r = np.zeros(num_nodes * 2, dtype=np.float64)
    for i in self.phase['soils']:
      if i['phaseActivity']:
        r += Polygon(self.list_coor,
                     self.list_polygon[i['name']]).r_internal(self.sigma[i['name']])
    for i in self.phase['lines']:
      bound = self.boundary()[i['name']]
      for j, row in enumerate(bound):
        if row[0] == 1:  # граничное условие по Х
          r[2 * j] = 0
        if row[1] == 1:  # граничное условие по Y
          r[2 * j + 1] = 0
    if self.nodes_off is not None:
      for i, el in enumerate(self.nodes_off):
        r = np.delete(r, el - i)
    return r

  def step_size(self, alfa, m_stage, iter, step):
    if step == 0 and alfa is None:  # First step and iteration
      alfa = self.max_load_fraction_per_step
    else:
      if iter <= self.min_num_iter and m_stage + 2 * alfa <= 1:  # increase alfa
        alfa = 2 * alfa
      else:
        if iter <= self.max_num_iter:  # stay alfa
          if m_stage + alfa <= 1:
            alfa = alfa
          else:
            alfa = 1 - m_stage
        else:  # decrease alfa
          if 0.5 * alfa <= 0.001:
            alfa = 0.001
          else:
            alfa = 0.5 * alfa

    return alfa

  def local_error_check(self, sigma_int, sigma_elast, tau):
    local_error = 0
    for i in sigma_int.keys():
      num_el = len(sigma_int[i][:, 0])
      error = np.zeros(num_el, dtype=np.float64)
      d_sigma = sigma_int[i] - sigma_elast[i]
      for j in range(num_el):
        error[j] = np.sqrt(d_sigma[j, 0] ** 2 + d_sigma[j, 1]
                           ** 2 + d_sigma[j, 2] ** 2) / tau[i][j]
        if error[j] > self.tolerated_error:
          local_error += 1
    return local_error

  @staticmethod
  def global_error_check(r, r_ext):
    global_error = np.linalg.norm(r) / np.linalg.norm(r_ext)
    return global_error

  def stress_disp_acc(self, iteration, alpha, sigma, index_last, step, x_s, m_stage, collapse, global_error,
                      local_error, max_inaccurate_point):
    if (global_error > self.tolerated_error) or (local_error > max_inaccurate_point):
      if m_stage != 1:
        step += 1
        m_stage -= alpha
        collapse += 1
        print()
        print('Уменьшаем величину шага')
      if m_stage == 1:
        print('rrr')
        step += 1
        m_stage -= alpha
        collapse = 10
    else:
      if (iteration <= self.min_num_iter) and (step != 0):
        if m_stage + alpha <= 1.00:
          step += 1
          self.sigma.update(sigma)
          self.x += x_s
          self.index.update(index_last)
          collapse = 0
          print()
          print('Увеличиваем величину шага')
        if m_stage + alpha > 1.00:
          step += 1
          self.sigma.update(sigma)
          self.x += x_s
          self.index.update(index_last)
          collapse = 0
      elif iteration <= self.max_num_iter:
        self.sigma.update(sigma)
        self.x += x_s
        self.index.update(index_last)
        step += 1
        collapse = 0
      elif iteration > self.max_num_iter:
        step += 1
        m_stage -= alpha
        collapse += 1
        print()
        print('Уменьшаем величину шага')
    return step, m_stage, collapse

  def terminate_solve(self, collapse, step):
    if collapse == 6:
      print(end='\n')
      print('Soil body seems to collapse')
      sys.exit()
    elif collapse == 10:
      print(end='\n')
      print('Load advisement procedure fails')
      sys.exit()
    elif step >= self.max_steps:
      print(end='\n')
      print('Accuracy condition is not reached in last step')
      sys.exit()
    else:
      pass

  def plastic_solve(self):
    # Обнуление пластических точек на начало фазы
    self.index = {}
    for i in self.list_polygon.keys():
      num_el = len(self.list_polygon[i][:, 0])
      self.index[i] = np.zeros((3 * num_el), dtype=np.int8)
    # Вектор внешних сил на фазе расчета
    f_ext = self.r_glob_sum()
    self.x = np.zeros_like(f_ext)
    # Вектор внутренних сил от начальных напряжений
    f_int = self.last_force_int()
    # Вектор сил для расчета на фазе
    f = f_ext - f_int
    # Сумма долей приложения нагрузки
    m_stage = 0
    # Доля приложения нагрузки для определения шага
    alfa = None
    # Номер итерации
    iter = 0
    # Номер шага
    step = 0
    # Количество точек с ошибками
    max_inaccurate_point = 0
    # Код ошибки
    collapse = 0

    # Начинается цикл по шагам
    while m_stage < 1:

      # Определяем матрицу жесткости на шаге
      k_s = self.k_glob_sum(self.sigma, self.index)
      # Terminate solve if error is existing
      # self.terminate_solve(collapse, step)
      # Define alfa and m_stage
      alfa = self.step_size(alfa, m_stage, iter, step)
      m_stage += alfa
      # Определение вектора сил на шаге расчета
      d_f = alfa * f
      print('\n')
      print('Current step:', step, ' ', 'M_stage:',
            round(m_stage, 5), ' ', 'alfa:', alfa)
      # Sign of beginning of iter at the step
      global_error = 1.00
      local_error = 0
      # reset variables of last step
      iter = 0
      # Обнуляем вектор внутренних сил на итерации и перемещения с прошлого шага
      sigma_int = None
      u_s = np.zeros(2 * len(self.list_coor[:, 0]), dtype=np.float64)
      f_ext_st = f * m_stage + f_int
      r = d_f
      index_last = {}
      index_last.update(self.index)
      GE_counter = 0

      # Начинается цикл по итерациям
      while (global_error >= self.tolerated_error or local_error >= max_inaccurate_point) and (iter < self.max_number_of_iterations):
        # Обновление матрицы жесткости
        if iter % 5 == 0 and iter != 0:
          k_s = self.k_glob_sum(sigma_int, index_last)
        # Определяем перемещение на итерации
        u_i = self.solve(k_s, r)
        # Суммируем перемещения по итерациям для получения шагового перемещения
        u_s += u_i
        # Вычисляем напряжения и пластические точки из модели грунта
        sigma_int, index_last, tau, sigma_elast = self.sigma_calc(
          index_last, u_s)
        # Вычисляем вектор внутренних сил из напряжений
        f_int_i = self.r_internal(sigma_int)
        # Определяем вектор сил на итерации (вычитаем из вектора внешних сил на шаге вектор внутренних сил)
        r = f_ext_st - f_int_i
        # Calculation local error
        local_error = 0
        # Условие прерывания расчета по итерациям при возрастании ошибки расчета
        if global_error - self.global_error_check(r, f_ext_st - f_int) < 0:
          GE_counter += 1
          if GE_counter == 3:
            iter = 20
        # Calculation global error
        global_error = self.global_error_check(r, f_ext_st - f_int)
        # Calculation number of plastic points
        failure_point = 0
        for i in index_last.keys():
          failure_point += np.sum(index_last[i] > 0)
        max_inaccurate_point = 3 + failure_point / 10
        print('\r', '| Iteration:', iter, '| Global error:', round(global_error, 4),
              '| loc_error_points:', local_error, '| MaxInaccuratePoint', max_inaccurate_point,
              '| U_max', max(u_s), '| U_min', min(u_s), end='')

        # Accamulate iterations
        iter += 1

        # END OF ITERATIONS
      # Накопление перемещений, переопределение напряжений и индексов
      step, m_stage, collapse = self.stress_disp_acc(iter, alfa, sigma_int, index_last, step, u_s, m_stage,
                                                     collapse, global_error, local_error, max_inaccurate_point)

    res_phase = {'sigma': self.sigma, 'index': self.index,
                 'x': self.x, 'epsilon': self.epsilon_calc(self.x)}

    return res_phase
