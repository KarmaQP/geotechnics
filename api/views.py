from pathlib import Path
from rest_framework.response import Response
from rest_framework.decorators import api_view
from main.models import FilesManagement
import json
from solver.elasticity.Head import solver_elasticity
from solver.elasticity.output_results import create_data, isofields
from solver.nonlinearity.Head import solver_nonlinearity
from solver.nonlinearity.temp import output
from solver.temperature.main import generate_data, create_data_temp, bc_temp, bc_T0, gKr_temp, isofields_temp, inithial_param, gKr_T0
from solver.filtration.main import create_data_wtf, gKr, dc, velocities_gradients, create_data_filtration, isofields_filtration, bc
from solver.parsers.main import msh_prs, msh_prs_3_nodes
from solver.figures.main import create_figure_1, create_figure_2, create_figure_1_3nodes, create_figure_2_3nodes
import scipy.sparse.linalg
from scipy.sparse import csr_matrix


BASE_DIR = Path(__file__).resolve().parent.parent


@api_view(['POST'])
def getSolverData(request):
  try:
    data = request.data
    task_type = data['task_type']
    phase_name = data['phase_name']
    input_data = data['input_data']
    coor_data = data['coor_data']
    polygons_data = data['polygons_data']
    lines_data = data['lines_data']
    materials_data = data['materials_data']
  except Exception as err:
    response = {
        'msg': f"Ошибка в сборе исходных данных! Пожалуйста, проверьте правильность заполнения исходных данных или сборки gmsh-файла. {type(err).__name__}: {err}.", 'status': 400,
      }

    return Response(response)

  print(task_type)
  if task_type == 'elasticity':
    try:
      geometry_points, geometry_nodes, result = solver_elasticity(
        input_data, coor_data, polygons_data, lines_data)

      results_data = create_data(result, geometry_points, geometry_nodes)
      min_max_values = isofields(results_data)

      return Response({'msg': 'Получены данные для решателя.', 'status': 200, 'min_max_values': min_max_values})
    except Exception as err:
      response = {
          'msg': f"Ошибка в расчете! Пожалуйста, проверьте правильность заполнения исходных данных или сборки gmsh-файла. {type(err).__name__}: {err}.", 'status': 400,
      }

      return Response(response)
  elif task_type == 'nonlinearity':
    try:
      geometry_points, geometry_nodes, result = solver_nonlinearity(input_data, materials_data,
                                                                    coor_data, lines_data, polygons_data)

      min_max_values = output(result, geometry_points,
                              geometry_nodes, phase_name)

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
        propertires = dc(a, propertires, ne, elem, nodes)

      v, I, pw = velocities_gradients(a, elem, ne, Bb, propertires, nodes, nn)
      results_data = create_data_filtration(nodes, elem, a, pw, v, I, nodes_s)
      min_max_values, units = isofields_filtration(results_data, v)

      return Response({'msg': 'Получены данные для решателя.', 'status': 200, 'min_max_values': min_max_values, 'units': units})
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

      N, dt, Tstep, data_fig, T = inithial_param(N, t, T0)

      for i in range(N):
        "Нижние две строчки запускают генерацию матрицы и ее расчет:"
        K, r = gKr_temp(elem, nodes, ne, nn, d_ind, propertires, T, dt)
        K_sp = csr_matrix(K)
        T = scipy.sparse.linalg.spsolve(K_sp, r)
        Tstep.append(T)
        data_fig[f"Время расчета t={t*(i+1)/N}, с:"] = Tstep[i + 1]

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

  if task_type == 'elasticity' or task_type == 'nonlinearity':
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
        'msg': 'Данные загружены успешно! Тип задачи: упругость/нелинейность.', 'status': 200, 'json': gmsh_json_content, 'calculatedSchemeData': {
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


# ??????????????????????????????????
# def create_list_coor(coor_data):
#   list_coor = []

#   for i in range(len(coor_data)):
#     list_coor.append(coor_data[i][1])
#     list_coor[i].pop(0)

#   list_coor = np.array(list_coor)
#   return list_coor


# def create_polygons_node_list(polygons_data):
#   polygons_node_list = {}
#   for i in range(len(polygons_data)):
#     for j in range(len(polygons_data[i])):
#       polygons_node_list[polygons_data[i][0]] = polygons_data[i][1]

#   for i in polygons_node_list.keys():
#     for j in polygons_node_list[i]:
#       j.pop(0)
#   return polygons_node_list


# def create_lines_node_list(lines_data):
#   lines_node_list = {}

#   for i in range(len(lines_data)):
#     for j in range(len(lines_data[i])):
#       lines_node_list[lines_data[i][0]] = lines_data[i][1]

#   return lines_node_list
# ????????????????????????????????????????
