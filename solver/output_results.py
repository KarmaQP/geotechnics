import matplotlib.pyplot as plt
import matplotlib.tri as tri
import pandas as pd
import mpld3
from mpld3 import plugins
import math


def create_data(result, geometry_points, geometry_nodes):
  x = geometry_points.get('x')
  y = geometry_points.get('y')
  elem = geometry_points.get('map')
  xstr = geometry_nodes.get('x_mid')
  ystr = geometry_nodes.get('y_mid')
  ux = result['Initial_phase'].get('u_x')
  uy = result['Initial_phase'].get('u_y')
  u = (ux**2 + uy**2)**0.5
  eps_XX = result['Initial_phase'].get('eps_XX')
  eps_YY = result['Initial_phase'].get('eps_YY')
  eps_XY = result['Initial_phase'].get('eps_XY')
  sigma_XX = result['Initial_phase'].get('sigma_XX')
  sigma_YY = result['Initial_phase'].get('sigma_YY')
  sigma_XY = result['Initial_phase'].get('sigma_XY')

  results_data = {
      'x,m': x,
      'y,m': y,
      'elements_3': elem,
      'x_str,m': xstr,
      'y_str,m': ystr,
      'ux,m': ux,
      'uy,m': uy,
      'u,m': u,
      'sigma_xx, kPa': sigma_XX,
      'sigma_yy, kPa': sigma_YY,
      'tay_xy, kPa': sigma_XY,
      'epsilon_xx': eps_XX,
      'epsilon_yy': eps_YY,
      'gamma_xy': eps_XY,
      'sigma_1, kPa': 0.5 * ((sigma_XX + sigma_YY) + ((sigma_XX - sigma_YY)**2 + 4 * sigma_XY)**0.5),
      'sigma_3, kPa': 0.5 * ((sigma_XX + sigma_YY) - ((sigma_XX - sigma_YY)**2 + 4 * sigma_XY)**0.5),
      'epsilon_1': 0.5 * ((eps_XX + eps_YY) + ((eps_XX - eps_YY)**2 + eps_XY**2)**0.5),
      'epsilon_3': 0.5 * ((eps_XX + eps_YY) - ((eps_XX - eps_YY)**2 + eps_XY**2)**0.5)
  }

  return results_data


"Модуль отвечает за визуализацию результатов расчета"


def isofields(results_data):
  x = results_data.get('x,m')
  y = results_data.get('y,m')
  xstr = results_data.get('x_str,m')
  ystr = results_data.get('y_str,m')

  elem = results_data.get('elements_3')

  data = [results_data.get('ux,m'), results_data.get('uy,m'), results_data.get('u,m'), results_data.get('sigma_xx, kPa'), results_data.get('sigma_yy, kPa'), results_data.get('tay_xy, kPa'), results_data.get(
    'epsilon_xx'), results_data.get('epsilon_yy'), results_data.get('gamma_xy'), results_data.get('sigma_1, kPa'), results_data.get('sigma_3, kPa'), results_data.get('epsilon_1'), results_data.get('epsilon_3')]

  names = list(results_data.keys())
  min_max_values = {}
  for i in range(len(results_data.get('sigma_1, kPa'))):
    if math.isnan(results_data.get('sigma_1, kPa')[i]) == True:
      results_data.get('sigma_1, kPa')[i] = 0
    if math.isnan(results_data.get('sigma_3, kPa')[i]) == True:
      results_data.get('sigma_3, kPa')[i] = 0

  for i in range(len(data)):

    if i <= 2:

      fig, ax = plt.subplots()

      triang = tri.Triangulation(x, y, elem.astype(int), mask=None)

      "Создаем графическое отображение результатов."

      pc = ax.tricontourf(triang, data[i], cmap='jet', levels=20)
      pc1 = ax.scatter(x, y, c=data[i], s=0, cmap='jet', alpha=1)
      fig.colorbar(pc1, ax=ax)
      ax.set(title=names[i + 5], xlabel='X Axis', ylabel='Y Axis')
      print(f'Максимальное {names[i+5]}:', max(data[i]))
      print(f'Минимальное {names[i+5]}:', min(data[i]))

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
          fig, f'static/src/dist/results/isofields_{i + 1}.json')

    if i >= 3:

      fig, ax = plt.subplots()

      # triang = tri.Triangulation(
      #     xstr, ystr, elem_str.astype(int), mask=None)

      "Создаем графическое отображение результатов."

      pc = ax.tricontourf(xstr, ystr, data[i], cmap='jet', levels=20)
      pc1 = ax.scatter(xstr, ystr, c=data[i], s=0, cmap='jet', alpha=1)
      fig.colorbar(pc1, ax=ax)
      ax.set(title=names[i + 5], xlabel='X Axis', ylabel='Y Axis')

      print(f'Максимальное {names[i+5]}:', max(data[i]))
      print(f'Минимальное {names[i+5]}:', min(data[i]))

      df = pd.DataFrame(index=range(len(xstr)))

      df['xstr'] = xstr
      df['ystr'] = ystr
      df['Значение'] = data[i]

      labels = []
      for j in range(len(xstr)):
        label = round(df.iloc[[j], 2:3].T, 3)
        # label.columns = ['№{0}'.format(i)]
        # print(str(label.to_html()))
        # print(label)
        labels.append(str(label.to_html()))

      points = ax.plot(df.xstr, df.ystr, 'o', color='b',
                       mec='k', ms=15, mew=1, alpha=0)

      tooltip = plugins.PointHTMLTooltip(points[0], labels,
                                         voffset=10, hoffset=10)
      plugins.connect(fig, tooltip)

      min_max_values[f"filtration_{i + 1}"] = {
        "min": round(min(data[i]), 3),
        "max": round(max(data[i]), 3),
      }

      mpld3.save_json(
          fig, f'static/src/dist/results/isofields_{i + 1}.json')

  return min_max_values
