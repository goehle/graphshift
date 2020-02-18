import numpy
import lib.edge


class Vertex:

    _radius = .02

    _number_edges = 3

    @staticmethod
    def set_number_edges(number_edges):
        Vertex._number_edges = number_edges

    @staticmethod
    def get_number_edges():
        return Vertex._number_edges

    # Constructor
    # We assume the following picture
    #   ( Small Vertex   ) -----up function---> ( Large Vertex    )
    #   ( i.e. low index ) <-- down function -- ( i.e. high index )
    # where the small vertex has the smaller index, the large vertex has the larger index
    # and the up function goes from small to large and the down function vice versa
    def __init__(self, index, position, transfer_matrix):

        self.index = index

        n = Vertex.get_number_edges()

        if position.size != 2:
            raise ValueError("Position is not a point (size 2 array)")

        self.position = numpy.copy(position)

        if transfer_matrix.shape != (n, n):
            raise ValueError("Transfer matrix is not {}x{}".format(n, n))

        self.transfer_matrix = numpy.copy(transfer_matrix)

        self.edges = []
        self.last_vals = numpy.zeros(n, dtype=complex)
        self.upd_lasts = []

# Edges are stored in order according to the index of the vertex they attach to
    def add_edge(self, new_edge):

        if not isinstance(new_edge, lib.edge.Edge):
            raise ValueError("edge is not an Edge")

        new_edge_vindex = new_edge.other_vertex_index(self.index)

        index = 0

        for i in range(len(self.edges)):
            if new_edge_vindex > self.edges[i].other_vertex_index(self.index):
                index = i+1

        self.edges.insert(index, new_edge)

        if self == new_edge.small_vertex:
            self.last_vals[index] = new_edge.down_function[-1]
        else:
            self.last_vals[index] = new_edge.up_function[-1]

        self.upd_lasts.insert(index, False)

    # Get a value on an edge shifted through vertex from other edges
    def get_shifted_value(self, desired_edge):

        n = Vertex.get_number_edges()

        desired_index = -1

        for i in range(n):
            if self.edges[i] == desired_edge:
                desired_index = i
                self.upd_lasts[i] = True

        output_vector = numpy.matmul(self.transfer_matrix, self.last_vals)

        # Important that this happens after we compute the output vector
        self._update_lasts()

        return output_vector[desired_index]

    def _update_lasts(self):
        n = Vertex.get_number_edges()

        do_upd = True
        for i in range(n):
            if not self.upd_lasts:
                do_upd = False
                break

        if do_upd:
            for i in range(n):
                self.upd_lasts[i] = False
                if self == self.edges[i].small_vertex:
                    self.last_vals[i] = self.edges[i].down_function[-1]
                else:
                    self.last_vals[i] = self.edges[i].up_function[-1]

    # color of point
    @staticmethod
    def color():

        return (50, 50, 50)

    def draw(self, fig):

        fig.draw_circle(self.position[0],
                        self.position[1],
                        self._radius,
                        self.color())
