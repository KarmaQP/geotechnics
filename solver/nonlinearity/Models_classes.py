import numpy as np


class ModelLE:
  # Linear Elastic
  def __init__(self, weight=None, e_ur=None, v_ur=None):
    self.weight = weight
    self.e_ur = e_ur
    self.v_ur = v_ur

  def d_matrix(self, sigma=None, index=None):
    d_e = self.e_ur / ((1 - 2 * self.v_ur) * (1 + self.v_ur)) * np.array([[1 - self.v_ur, self.v_ur, 0],
                                                                          [self.v_ur, 1 -
                                                                           self.v_ur, 0],
                                                                          [0, 0, (1 - 2 * self.v_ur) / 2]])
    return d_e

  def sigma_check(self, sig, eps, index):
    # Операция опредения новых "упругих" напряжений при получении расчетных дефомраций
    sig_new = sig + self.d_matrix() @ eps
    sig1 = - 1 / 2 * ((sig_new[0] + sig_new[1]) -
                      ((sig_new[0] - sig_new[1]) ** 2 + 4 * sig_new[2] ** 2) ** 0.5)
    sig3 = - 1 / 2 * ((sig_new[0] + sig_new[1]) +
                      ((sig_new[0] - sig_new[1]) ** 2 + 4 * sig_new[2] ** 2) ** 0.5)
    tau = (sig1 - sig3) / 2
    return sig_new, index, tau, sig_new


class ModelMC:
  # Mohr-Coulomb
  def __init__(self, weight, e_ur, v_ur, c, fi, T, psi):
    self.weight = weight
    self.e_ur = e_ur
    self.v_ur = v_ur
    self.c = c
    self.fi = np.radians(fi)
    self.T = T
    self.psi = np.radians(psi)

  def d_e_matrix(self):
    d_e = self.e_ur / ((1 - 2 * self.v_ur) * (1 + self.v_ur)) * np.array([[1 - self.v_ur, self.v_ur, 0],
                                                                          [self.v_ur, 1 -
                                                                           self.v_ur, 0],
                                                                          [0, 0, 0.5 - self.v_ur]])
    return d_e

  # Вычитаемая часть из упругой матрицы в УПМ для критерия Кулона - Мора
  def f1_ep(self, x, y, t):
    # x = - x
    # y = - y
    t = t

    # A, B и C - замены в формулах для сокращения записи формул
    # Условие прописано для того, что-бы избежать деления на 0 в формате 0/0, т.е. не вредит результатам
    if np.sqrt((y - x) ** 2 + 4 * t ** 2) != 0:
      A = np.sqrt((y - x) ** 2 + 4 * t ** 2)
    if np.sqrt((y - x) ** 2 + 4 * t ** 2) == 0:
      A = 1
    B = (y - x) / A
    C = 4 * t / A

    # Упругий модуль деформации в соответсвии с Фадеевым
    E_el = self.e_ur / ((1 + self.v_ur) * (1 - 2 * self.v_ur))

    # Одноименный компонент из формулы УПМ
    d = (2 * (1 - self.v_ur) * (np.sin(self.fi) * np.sin(self.psi) + B ** 2) +
         2 * self.v_ur * (np.sin(self.fi) * np.sin(self.psi) - B ** 2) + (0.5 - self.v_ur) * C ** 2)

    # Частные производные от функции текучести (если ставим fi) и от пластического потенциала (если ставим ksi)
    def el(num, a):
      if num == 1:
        e = (1 - self.v_ur) * (-B + np.sin(a)) + self.v_ur * (B + np.sin(a))
      if num == 2:
        e = (1 - self.v_ur) * (B + np.sin(a)) + self.v_ur * (-B + np.sin(a))
      if num == 3:
        e = (0.5 - self.v_ur) * C
      return e

    f1 = E_el / d * np.array([[el(1, self.psi) * el(1, self.fi),
                               el(1, self.psi) * el(2, self.fi),
                               el(1, self.psi) * el(3, self.fi)],
                              [el(2, self.psi) * el(1, self.fi),
                               el(2, self.psi) * el(2, self.fi),
                               el(2, self.psi) * el(3, self.fi)],
                              [el(3, self.psi) * el(1, self.fi),
                               el(3, self.psi) * el(2, self.fi),
                               el(3, self.psi) * el(3, self.fi)]])
    return f1

  # Вычитаемая часть из упругой матрицы в УПМ для разрыва по сигма 3
  def f2_ep(self, x, y, t):
    # A, B и C - замены в формулах для сокращения записи формул
    # Условие прописано для того, что-бы избежать деления на 0 в формате 0/0, т.е. не вредит результатам
    if np.sqrt((y - x) ** 2 + 4 * (t ** 2)) != 0:
      A = np.sqrt((y - x) ** 2 + 4 * (t ** 2))
    if np.sqrt((y - x) ** 2 + 4 * t ** 2) == 0:
      A = 1
    B = (y - x) / A
    C = 4 * t / A

    # Упругий модуль деформации в соответсвии с Фадеевым
    E_ur = self.e_ur / ((1 + self.v_ur) * (1 - 2 * self.v_ur))

    # Одноименный компонент из формулы УПМ
    d = ((1 - self.v_ur) * (np.square(1 - B) + np.square(1 + B)) +
         2 * self.v_ur * (1 - np.square(B)) + (0.5 - self.v_ur) * np.square(C))
    # print(d * E_ur / 4)

    # Частные производные от функции текучести (если ставим fi) и от пластического потонциала (если ставим ksi)
    def el(num):
      if num == 1:
        e = (1 - self.v_ur) * (1 - B) + self.v_ur * (1 + B)
      if num == 2:
        e = (1 - self.v_ur) * (1 + B) + self.v_ur * (1 - B)
      if num == 3:
        e = (0.5 - self.v_ur) * C
      return e

    f2 = E_ur / d * np.array([[np.square(el(1)), el(1) * el(2), el(1) * el(3)],
                              [el(2) * el(1), np.square(el(2)), el(2) * el(3)],
                              [el(3) * el(1), el(3) * el(2), np.square(el(3))]
                              ])
    return f2

  def f3_ep(self, x, y, t):
    D = self.d_e_matrix() - self.f1_ep(x, y, t)
    # print(D)
    # A, B и C - замены в формулах для сокращения записи формул
    # Условие прописано для того, что-бы избежать деления на 0 в формате 0/0, т.е. не вредит результатам
    if np.sqrt((y - x) ** 2 + 4 * t ** 2) != 0:
      A = np.sqrt((y - x) ** 2 + 4 * t ** 2)
    if np.sqrt((y - x) ** 2 + 4 * t ** 2) == 0:
      A = 1
    B = (y - x) / A
    C = 4 * t / A

    dfT = np.array([[1 - B, 1 + B, C]])
    dg = np.array([[1 - B], [1 + B], [C]])

    d = dfT @ D @ dg

    f3 = 1 / d * D @ dg @ dfT @ D

    return f3

  def f4_ep(self, x, y, t):
    D = self.d_e_matrix() - self.f2_ep(x, y, t)
    # print(D)
    # A, B и C - замены в формулах для сокращения записи формул
    # Условие прописано для того, что-бы избежать деления на 0 в формате 0/0, т.е. не вредит результатам
    if np.sqrt((y - x) ** 2 + 4 * t ** 2) != 0:
      A = np.sqrt((y - x) ** 2 + 4 * t ** 2)
    if np.sqrt((y - x) ** 2 + 4 * t ** 2) == 0:
      A = 1
    B = -(y - x) / A
    C = 4 * t / A

    dfT = np.array([[1 - B, 1 + B, C]])
    dg = np.array([[1 - B], [1 + B], [C]])

    d = dfT @ D @ dg

    f4 = 1 / d * D @ dg @ dfT @ D

    return f4

  # Вызов актуальной матрицы жесткости элемента в зависимости от напряжений и пластики в точке
  def d_matrix(self, sigma, index):
    # Упругость
    if index == 0:
      D = self.d_e_matrix()

    # Критерий Кулона-Мора
    if index == 1:
      D = self.d_e_matrix() - self.f1_ep(sigma[0], sigma[1], sigma[2])

    # Разрыв в одном направлении
    if index == 2:
      D = self.d_e_matrix() - self.f2_ep(sigma[0], sigma[1], sigma[2])

    # Разрыв в одном направлении + критерий Кулона-Мора
    if index == 3:
      D = self.d_e_matrix() - self.f1_ep(sigma[0], sigma[1], sigma[2]) - self.f3_ep(sigma[0], sigma[1],
                                                                                    sigma[2])

    # Разрыв в двух направлениях
    if index == 4:
      D = (self.d_e_matrix() - self.f2_ep(sigma[0], sigma[1], sigma[2])) - self.f4_ep(sigma[0], sigma[1],
                                                                                      sigma[2])
    return D

  def characteristics(self):
    s = 2 * self.c / (np.tan(np.pi / 4 - self.fi / 2))
    ctg_psi = (1 + np.sin(self.fi)) / (1 - np.sin(self.fi))
    ctg_betta = 1 / np.tan(np.pi / 4)
    # ctg_betta = ctg_psi
    return s, ctg_psi, ctg_betta

  def sigma_check(self, sig, eps, index):
    # Операция опредения новых "упругих" напряжений при получении расчетных дефомраций
    sig_new = sig + self.d_matrix(sig, index) @ eps

    # Определение главных "упругих" напряжений
    sig_1 = - 1 / 2 * ((sig_new[0] + sig_new[1]) -
                       ((sig_new[0] - sig_new[1]) ** 2 + 4 * sig_new[2] ** 2) ** 0.5)
    sig_3 = - 1 / 2 * ((sig_new[0] + sig_new[1]) +
                       ((sig_new[0] - sig_new[1]) ** 2 + 4 * sig_new[2] ** 2) ** 0.5)

    # Угол между основными и главными осями для пересчета
    if sig_new[2] == 0:
      if sig_new[1] <= sig_new[0]:
        alpha = np.pi / 2
      else:
        alpha = 0
    elif sig_1 + sig_new[1] != 0:
      alpha = np.arctan(- sig_new[2] / (sig_1 + sig_new[1]))
    else:
      alpha = np.pi / 2

    # Различные переменные, учавствующие в расчетах
    Ss = 2 * self.c / np.tan(np.pi / 4 - self.fi / 2)
    L1 = (sig_1 - Ss) * (1 - np.sin(self.fi)) / (1 + np.sin(self.fi))
    L2 = 0
    L3 = (Ss - sig_1) * (1 + np.sin(self.psi)) / (1 - np.sin(self.psi))
    L4 = Ss

    # Перерасчет корректных напряжений из "упругих"

    ind = index

    # Случай, когда изначально была упругость
    if ind == 0:
      if (sig_1 < L2) & (sig_3 < L2):
        S1 = 0
        S3 = 0
        ind = 4
      elif sig_1 < L4:
        if sig_3 < L2:
          S1 = sig_1 - sig_3 * self.v_ur / (1 - self.v_ur)
          S3 = 0
          ind = 2
          if S1 > Ss:
            S1 = Ss
            S3 = 0
            ind = 3
        else:
          S1 = sig_1
          S3 = sig_3
          ind = 0
      elif sig_3 < L3:
        S1 = Ss
        S3 = 0
        ind = 3
      elif sig_3 > L1:
        S1 = sig_1
        S3 = sig_3
        ind = 0
      else:
        S3 = (sig_1 + sig_3 * (1 - np.sin(self.psi)) / (1 + np.sin(self.psi)) - Ss) / (
            (1 - np.sin(self.psi)) / (1 + np.sin(self.psi)) + (1 + np.sin(self.fi)) / (1 - np.sin(self.fi)))
        S1 = Ss + S3 * ((1 + np.sin(self.fi)) / (1 - np.sin(self.fi)))
        ind = 1

    # Случай, когда уже идет разрыв + Кулон-Мор
    if ind == 3:
      S1 = Ss
      S3 = 0

    # Случай, когда уже идет разрыв в 2-х направлениях
    if ind == 4:
      S1 = 0
      S3 = 0

    # Случай, когда уже находимся на линии Кулона-Мора
    if ind == 1:
      if sig_3 < L3:
        S1 = Ss
        S3 = 0
        ind = 3

      else:
        S3 = (sig_1 + sig_3 * (1 - np.sin(self.psi)) / (1 + np.sin(self.psi)) - Ss) / (
            (1 - np.sin(self.psi)) / (1 + np.sin(self.psi)) + (1 + np.sin(self.fi)) / (1 - np.sin(self.fi)))
        S1 = Ss + S3 * ((1 + np.sin(self.fi)) / (1 - np.sin(self.fi)))
        ind = 1

    # Случай, когда уже находимся в зоне разрыва в 1-м направлении
    if ind == 2:
      if sig_1 < L2:
        S1 = 0
        S3 = 0
        ind = 4

      elif sig_1 > L4:
        S1 = Ss
        S3 = 0
        ind = 3

      else:
        S1 = sig_1 - sig_3 * self.v_ur / (1 - self.v_ur)
        S3 = 0
        ind = 2
        if S1 > Ss:
          S1 = Ss
          S3 = 0
          ind = 3

    sigma1 = S1
    sigma3 = S3
    index = ind

    if (sigma1 is None) or (sigma3 is None) or (index is None):
      print('Error in sigma_calc calculation')
      exit()
    tau = max((sigma1 - sigma3) / 2, self.c * np.cos(self.fi))

    sigma_internal = np.zeros(3, dtype=np.float64)
    sigma_internal[0] = - sigma1 * \
        (np.cos(alpha) ** 2) - sigma3 * (np.sin(alpha) ** 2)
    sigma_internal[1] = - sigma1 * \
        (np.sin(alpha) ** 2) - sigma3 * (np.cos(alpha) ** 2)
    sigma_internal[2] = - 0.5 * (sigma1 - sigma3) * np.sin(2 * alpha)
    return sigma_internal, index, tau, sig_new
