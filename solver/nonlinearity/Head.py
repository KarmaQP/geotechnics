from solver.nonlinearity.Solve_classes import StageConstruction
# from Input import coor_data, lines_data, polygons_data, input_data, materials_data
# from temp import output


def solver_nonlinearity(input_data, materials_data, coor_data, lines_data, polygons_data):
  geometry_points, geometry_nodes, result = StageConstruction(phases=input_data,
                                                              list_coor=coor_data,
                                                              list_line=lines_data,
                                                              list_polygon=polygons_data,
                                                              lib_material=materials_data).result_print()
  return geometry_points, geometry_nodes, result


# geometry_points, geometry_nodes, result = solver()

# output(result, geometry_points, geometry_nodes)
