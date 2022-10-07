from pathlib import Path

import numpy as np
import trimesh

from abspy import CellComplex

dir_tests = Path(__file__).parent


def example_cell_complex():
    """
    Simple CellComplex construction from specified planes and bounds.
    """
    # start from two planes
    planes = np.array([[0, 1, 0, -50], [0, 0, 1, -50]])

    # specify the bounds
    bounds = np.array([[[0, 50, 0], [100, 50, 100]], [[0, 0, 50], [100, 50, 50]]])

    # specify the initial bound
    initial_bound = [[0, 0, 0], [100, 100, 100]]

    # initialise the cell complex
    cell_complex = CellComplex(planes, bounds, initial_bound=initial_bound, build_graph=True)

    # prioritise certain (vertical by default) planes
    cell_complex.prioritise_planes()

    # construct the complex
    cell_complex.construct()

    # print out info
    cell_complex.print_info()

    # cell representatives
    num_representatives = 100
    representatives = cell_complex.cell_representatives(location='random', num=num_representatives)
    representatives = np.concatenate(representatives, axis=0)
    colours = np.zeros([num_representatives * cell_complex.num_cells, 4])
    for i in range(cell_complex.num_cells):
        colours[num_representatives * i: num_representatives * (i + 1)] = trimesh.visual.color.random_color()
    representatives_vis = trimesh.PointCloud(representatives, colours)
    representatives_vis.show()

    # cells inside reference mesh
    cells_in_mesh = cell_complex.cells_in_mesh(dir_tests / 'test_data' / 'test_mesh_manifold.obj')

    # visualise the inside cells (only if pyglet installation is found and valid indices are provided)
    if len(cells_in_mesh):
        cell_complex.visualise(indices_cells=cells_in_mesh, temp_dir='./test_output/')

    # save cell complex to OBJ and PLM files
    cell_complex.save_obj(dir_tests / 'test_output' / 'cells.obj', use_mtl=True)
    cell_complex.save_plm(dir_tests / 'test_output' / 'cells.plm')


if __name__ == '__main__':
    example_cell_complex()
