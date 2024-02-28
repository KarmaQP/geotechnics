import matplotlib.pyplot as plt
import matplotlib.tri as tri
import mpld3


def create_data(result, geometry_points, geometry_nodes):
  x = geometry_points.get('x')
  y = geometry_points.get('y')
  elem = geometry_points.get('map')
  xstr = geometry_nodes.get('x_mid')
  ystr = geometry_nodes.get('y_mid')
  elem_str = geometry_nodes.get('map_mid')
  ux = result.get('u_x')
  uy = result.get('u_y')
  u = (ux**2 + uy**2)**0.5
  eps_XX = result.get('eps_XX')
  eps_YY = result.get('eps_YY')
  eps_XY = result.get('eps_XY')
  sigma_XX = result.get('sigma_XX')
  sigma_YY = result.get('sigma_YY')
  sigma_XY = result.get('sigma_XY')

  results_data = {
      'x,m': x,
      'y,m': y,
      'elements_3': elem,
      'x_str,m': xstr,
      'y_str,m': ystr,
      'elements_3_str': elem_str,
      'ux,m': ux,
      'uy,m': uy,
      'u,m': u,
      'sigma_xx, kPa': sigma_XX,
      'sigma_yy, kPa': sigma_YY,
      'tay_xy, kPa': sigma_XY,
      'epsilon_xx': eps_XX,
      'epsilon_yy': eps_YY,
      'gamma_xy': eps_XY,
      'sigma_1, kPa': 0.5 * (sigma_XX + sigma_YY + ((sigma_XX - sigma_YY)**2 + 4 * sigma_XY)**0.5),
      'sigma_3, kPa': 0.5 * (sigma_XX + sigma_YY - ((sigma_XX - sigma_YY)**2 + 4 * sigma_XY)**0.5),
      'epsilon_1': 0.5 * ((eps_XX + eps_YY) + ((eps_XX - eps_YY)**2 + eps_XY**2)**0.5),
      'epsilon_3': 0.5 * ((eps_XX + eps_YY) - ((eps_XX - eps_YY)**2 + eps_XY**2)**0.5)
  }

  return results_data

# print(results_data)


"Модуль отвечает за визуализацию результатов расчета"


def isofields(results_data):
  x = results_data.get('x,m')
  y = results_data.get('y,m')
  xstr = results_data.get('x_str,m')
  ystr = results_data.get('y_str,m')

  elem = results_data.get('elements_3')
  elem_str = results_data.get('elements_3_str')

  data = [results_data.get('ux,m'), results_data.get('uy,m'), results_data.get('u,m'), results_data.get('sigma_xx, kPa'), results_data.get('sigma_yy, kPa'), results_data.get('tay_xy, kPa'), results_data.get(
    'epsilon_xx'), results_data.get('epsilon_yy'), results_data.get('gamma_xy'), results_data.get('sigma_1, kPa'), results_data.get('sigma_3, kPa'), results_data.get('epsilon_1'), results_data.get('epsilon_3')]

  names = list(results_data.keys())
  min_max_values = {}

  for i in range(len(data)):

    if i <= 2:

      fig, ax = plt.subplots()

      triang = tri.Triangulation(x, y, elem.astype(int), mask=None)

      "Создаем графическое отображение результатов."

      pc = ax.tricontourf(triang, data[i], cmap='jet', levels=20)
      pc1 = ax.scatter(x, y, c=data[i], s=0, cmap='jet', alpha=1)
      fig.colorbar(pc1, ax=ax)
      ax.set(title=names[i + 6], xlabel='X Axis', ylabel='Y Axis')
      print(f'Максимальное {names[i+6]}:', max(data[i]))
      print(f'Минимальное {names[i+6]}:', min(data[i]))

      min_max_values[f"filtration_{i + 1}"] = {
        "min": round(min(data[i]), 3),
        "max": round(max(data[i]), 3),
      }

      mpld3.save_json(fig, f'static/src/dist/results/isofields_{i + 1}.json')

    if i >= 3:

      fig, ax = plt.subplots()

      triang = tri.Triangulation(xstr, ystr, elem_str.astype(int), mask=None)

      "Создаем графическое отображение результатов."

      pc = ax.tricontourf(triang, data[i], cmap='jet', levels=20)
      pc1 = ax.scatter(xstr, ystr, c=data[i], cmap='jet', alpha=0)
      fig.colorbar(pc1, ax=ax)
      ax.set(title=names[i + 6], xlabel='X Axis', ylabel='Y Axis')

      print(f'Максимальное {names[i+6]}:', max(data[i]))
      print(f'Минимальное {names[i+6]}:', min(data[i]))

      min_max_values[f"filtration_{i + 1}"] = {
        "min": round(min(data[i]), 3),
        "max": round(max(data[i]), 3),
      }

      mpld3.save_json(fig, f'static/src/dist/results/isofields_{i + 1}.json')

  return min_max_values
