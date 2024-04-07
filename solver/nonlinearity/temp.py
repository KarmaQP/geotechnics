import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import mpld3
from mpld3 import plugins
import pandas as pd


def output(result, geometry_points, geometry_nodes, phase_name):
  # Выбор фазы для визуализации
  result = result[phase_name]
  geometry_points = geometry_points[phase_name]
  geometry_nodes = geometry_nodes[phase_name]

  # Словарь для максимальных и минимальных значений
  min_max_values = {}

  # Получение исходных данных
  coor_x = geometry_points['x']
  coor_y = geometry_points['y']
  map = geometry_points['map']
  map_6 = geometry_nodes['map']
  colors = geometry_nodes['mat_colors']

  elastic, plastic, tension = result['stress_points']
  names = ['u_x', 'u_y', 'eps_XX', 'eps_YY', 'eps_XY',
           'sigma_XX', 'sigma_YY', 'sigma_XY', 'stress_points']
  # Настройка пропорций картинки
  width = np.max(coor_x) - np.min(coor_x)
  height = np.max(coor_y) - np.min(coor_y)
  if height <= width:
    scale = height / width
  else:
    scale = 1

  # Получение сетки триангуляции
  mesh = mpl.tri.Triangulation(coor_x, coor_y, map)
  mesh_large = mpl.tri.Triangulation(coor_x, coor_y, map_6)

  # Получение картинок для перемещений
  for num, i in enumerate(result.keys()):
    fig, ax = plt.subplots()
    if i == 'u_x' or i == 'u_y':
      pic = ax.tricontourf(mesh, result[i], levels=20, cmap="jet")
      pic_1 = ax.scatter(coor_x, coor_y, c=result[i], s=0, cmap='jet', alpha=1)
    #   ax.triplot(mesh_large, '-', linewidth=0.3, color='gray')
      ax.set(title=names[num], xlabel='ось X', ylabel='ось Y')
      ax.set_aspect('equal')
      fig.colorbar(pic_1, fraction=0.046, pad=0.04)
      print(f'Максимальное {names[num]}:', max(result[i]))
      print(f'Минимальное {names[num]}:', min(result[i]))

      print(num + 1)
      min_max_values[f"nonlinearity_{num + 1}"] = {
        "min": round(min(result[i]), 3),
        "max": round(max(result[i]), 3),
      }

      df = pd.DataFrame(index=range(len(coor_x)))

      df['coor_x'] = coor_x
      df['coor_y'] = coor_y
      df['Значение'] = result[i]

      labels = []
      for j in range(len(coor_x)):
        label = round(df.iloc[[j], 2:3].T, 3)
        # label.columns = ['№{0}'.format(i)]
        # print(str(label.to_html()))
        # print(label)
        labels.append(str(label.to_html()))

      points = ax.plot(df.coor_x, df.coor_y, 'o', color='b',
                       mec='k', ms=15, mew=1, alpha=0)

      tooltip = plugins.PointHTMLTooltip(points[0], labels,
                                         voffset=10, hoffset=10)
      plugins.connect(fig, tooltip)

    if i in ['eps_XX', 'eps_YY', 'eps_XY', 'sigma_XX', 'sigma_YY', 'sigma_XY']:
      pic = ax.tricontourf(mesh, result[i], levels=20, cmap="jet")
      pic_1 = ax.scatter(coor_x, coor_y, c=result[i], s=0, cmap='jet', alpha=1)
    #   ax.triplot(mesh_large, '-', linewidth=0.3, color='gray')
      ax.set(title=names[num], xlabel='ось X', ylabel='ось Y')
      ax.set_aspect('equal')
      fig.colorbar(pic_1, fraction=0.046, pad=0.04)
      print(f'Максимальное {names[num]}:', max(result[i]))
      print(f'Минимальное {names[num]}:', min(result[i]))

      print(num + 1)
      min_max_values[f"nonlinearity_{num + 1}"] = {
        "min": round(min(result[i]), 3),
        "max": round(max(result[i]), 3),
      }

      df = pd.DataFrame(index=range(len(coor_x)))

      df['coor_x'] = coor_x
      df['coor_y'] = coor_y
      df['Значение'] = result[i]

      labels = []
      for j in range(len(coor_x)):
        label = round(df.iloc[[j], 2:3].T, 3)
        # label.columns = ['№{0}'.format(i)]
        # print(str(label.to_html()))
        # print(label)
        labels.append(str(label.to_html()))

      points = ax.plot(df.coor_x, df.coor_y, 'o', color='b',
                       mec='k', ms=15, mew=1, alpha=0)

      tooltip = plugins.PointHTMLTooltip(points[0], labels,
                                         voffset=10, hoffset=10)
      plugins.connect(fig, tooltip)

    if i == 'stress_points':
      pic = ax.tripcolor(mesh_large, facecolors=colors, cmap='Set3')
      if elastic.shape[0] != 0:
        el = ax.scatter(elastic[:, 0], elastic[:, 1],
                        c='indigo', s=10, marker='.')
      else:
        el = None
      if plastic.shape[0] != 0:
        pl = ax.scatter(plastic[:, 0], plastic[:, 1],
                        c='red', s=10, marker='s')
      else:
        pl = None
      if tension.shape[0] != 0:
        ten = ax.scatter(tension[:, 0], tension[:, 1],
                         c='snow', s=10, marker='s')
      else:
        ten = None
    #   ax.triplot(mesh_large, '-', linewidth=0.3, color='gray')
      ax.legend((el, pl, ten), ('elastic', 'plastic',
                'tension cut-off'), loc='lower left')
      ax.set(title=names[num], xlabel='ось X', ylabel='ось Y')
      ax.set_aspect('equal')

    # plt.show()
    mpld3.save_json(
      fig, f'static/src/dist/results/nonlinearity/isofields_{num + 1}.json')
  return min_max_values
