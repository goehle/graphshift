import numpy

from lib.edge import Edge
from lib.warpedge import Warp_Edge
from lib.vertex import Vertex
from lib.figure import Figure


class Graph:

    @staticmethod
    def get_edge_resolution():
        return Edge.get_edge_resolution()

    @staticmethod
    def set_edge_resolution(edge_resolution):
        Edge.set_edge_resolution(edge_resolution)

    # Constructor
    # Verticies of the graph are numbered 0 - (N-1)
    # number_edges: number of edges out of/into each vertex
    # functions: matrix of functions for edges.  The i,j entry is the function from vertex i to j.
    #           also serves as the adjacency matrix
    # positions contains the position of each vertex
    # transfer_matricies: is a transfer matrix for each vertex
    #      each transfer matrix indicates how the values coming in from the edges (in increasing vertex order)
    #      are translated into values coming out of the edges (in increasing vertex order)

    def __init__(self, positions, transfer_matrices, functions, warp=None):

        self.n_verts = len(positions)

        if numpy.shape(functions) != (self.n_verts, self.n_verts):
            raise ValueError("Adjacency matrix is not square")

        if len(transfer_matrices) != self.n_verts:
            raise ValueError("Number of transfer matricies does not match number of verticies")

        number_edges = 0

        for i in range(self.n_verts):
            if not functions[0][i] is None:
                number_edges += 1

        Vertex.set_number_edges(number_edges)

        self.verts = []

        for i in range(self.n_verts):
            self.verts.append(Vertex(i, positions[i], transfer_matrices[i]))

        self.res = -1
        self.edges = []

        self.fig = None

        if warp is None:
            warp = []
            for i in range(len(functions)):
                warp.append([])
                for j in range(len(functions[i])):
                        warp[i].append(False)

        for i in range(self.n_verts):
            for j in range(i+1, self.n_verts):

                if not functions[i][j] is None:

                    if functions[j][i] is None:
                        raise ValueError("Adjacency matrix is not symmetricly nonzero")

                    if self.res == -1:
                        self.res = numpy.size(functions[i][j])
                        Edge.set_edge_resolution(self.res)

                    if warp[i][j]:
                        self.edges.append(Warp_Edge(self.verts[i], self.verts[j], functions[i][j], functions[j][i]))
                    else:
                        self.edges.append(Edge(self.verts[i], self.verts[j], functions[i][j], functions[j][i]))

    def draw(self, name, xmin, xmax, ymin, ymax, width=800, height=800):

        self.fig = Figure(xmin, xmax, ymin, ymax, width, height)

        # need one frame for static image
        self.fig.new_frame()

        for edge in self.edges:
            edge.draw(self.fig)

        for vert in self.verts:
            vert.draw(self.fig)

        self.fig.save(name)

    def movie(self, name, xmin, xmax, ymin, ymax, width=800, height=800, n_frames=30, fps=20):

        self.fig = Figure(xmin, xmax, ymin, ymax, width, height)

        for i in range(n_frames):
            self.fig.new_frame()

            for edge in self.edges:
                edge.draw(self.fig)

            for vert in self.verts:
                vert.draw(self.fig)

            for edge in self.edges:
                edge.shift()

        self.fig.save_movie(name, fps)
