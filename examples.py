import math
import cmath
import numpy

from graph import Graph


def main():

#    name = "trivial"
    name = "rotation"
#    name = "unitary"
#    name = "permutation"

    transfer = numpy.array([[1, 0, 0],
                            [0, 1, 0],
                            [0, 0, 1]])

    transfer_matrices = [transfer, transfer, transfer, transfer]

    if name == "rotation":
        transfer = numpy.array([[cmath.exp(cmath.pi*1j/2), 0, 0],
                                [0, cmath.exp(cmath.pi * 1j / 2), 0],
                                [0, 0, cmath.exp(cmath.pi * 1j / 2)]])

        transfer_matrices = [transfer, transfer, transfer, transfer]

    elif name == "permutation":
        transfer0 = numpy.array([[0, 0, 1],
                                 [1, 0, 0],
                                 [0, 1, 0]])

        transfer1 = numpy.array([[0, 1, 0],
                                 [0, 0, 1],
                                 [1, 0, 0]])

        transfer_matrices = [transfer0, transfer1, transfer0, transfer1]

    elif name == "unitary":
        transfer = numpy.array([[1 / 2, (1 + 1j) / 2, -1 / 2],
                                [-1j/cmath.sqrt(3), 1j/cmath.sqrt(3), 1/cmath.sqrt(3)],
                                [5j/(2*cmath.sqrt(15)), (3+1j)/(2*cmath.sqrt(15)), (4+3j)/(2*cmath.sqrt(15))]])

        transfer_matrices = [transfer, transfer, transfer, transfer]

    positions = [numpy.array([0, 1]),
                 numpy.array([math.sqrt(3)/2, -1/2]),
                 numpy.array([-math.sqrt(3) / 2, -1 / 2]),
                 numpy.array([0, 0])]



    res = Graph.get_edge_resolution()

    funct_zero = numpy.zeros(res, dtype=complex)

    funct_sin = numpy.zeros(res, dtype=complex)

    funct_const = numpy.zeros(res, dtype=complex)

    for i in range(res):
        funct_sin[i] = cmath.rect(math.sin(2 * cmath.pi * i / res), 2 * cmath.pi * i / res)
        funct_const[i] = cmath.rect(.85, cmath.pi / 4)

    functions = [[None,        funct_sin,   funct_const,   funct_zero],
                 [funct_const, None,        funct_sin,   funct_zero],
                 [funct_sin, funct_const, None,        funct_zero],
                 [funct_zero,  funct_zero,  funct_zero,  None]]

    warp = [[False, True,  False, False],
            [False, False, False, False],
            [False, False, False, False],
            [False, False, False, False]]

    graph = Graph(positions, transfer_matrices, functions,warp)

    graph.movie(name="{}.avi".format(name),
                  xmin=-2, xmax=2, ymin=-2, ymax=2,
                  n_frames=200, fps=10)


if __name__ == "__main__":
    main()
