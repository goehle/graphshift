import math
import cmath
import numpy
import lib.vertex


class Edge:
    # Constants
    _edge_resolution = 50
    _edge_resolution_overlap = 0.1
    _edge_offset = 0.01
    _edge_width = 5

    @staticmethod
    def get_edge_resolution():
        return Edge._edge_resolution

    @staticmethod
    def set_edge_resolution(edge_resolution):
        Edge._edge_resolution = edge_resolution

    # Constructor
    # We assume the following picture
    #   ( Small Vertex   ) -----up function---> ( Large Vertex    )
    #   ( i.e. low index ) <-- down function -- ( i.e. high index )
    # where the small vertex has the smaller index, the large vertex has the larger index
    # and the up function goes from small to large and the down function vice versa
    def __init__(self, small_vertex, large_vertex, up_function, down_function):

        if small_vertex.index >= large_vertex.index:
            raise ValueError("small vertex doesn't have smaller index than large vertex")

        if not isinstance(small_vertex, lib.vertex.Vertex):
            raise ValueError("down vertex is not of type Vertex")

        # Have to set up functions before adding edge to vertex
        if down_function.size != Edge.get_edge_resolution():
            raise ValueError("down function doesn't have correct length")

        self.down_function = numpy.copy(down_function)

        if up_function.size != Edge.get_edge_resolution():
            raise ValueError("Right function doesn't have correct length")

        self.up_function = numpy.copy(up_function)

        self.small_vertex = small_vertex

        if not isinstance(large_vertex, lib.vertex.Vertex):
            raise ValueError("Right vertex is not of type Vertex")

        self.large_vertex = large_vertex

        small_vertex.add_edge(self)
        large_vertex.add_edge(self)

    def other_vertex_index(self, index):
        if self.large_vertex.index == index:
            return self.small_vertex.index
        elif self.small_vertex.index == index:
            return self.large_vertex.index
        else:
            raise ValueError("index does not match either vertex index")

    # Shift functions one timestep forward
    def shift(self):

        res = Edge.get_edge_resolution()

        for i in reversed(range(1, res)):
            self.up_function[i] = self.up_function[i - 1]

        self.up_function[0] = self.small_vertex.get_shifted_value(self)

        for i in reversed(range(1, res)):
            self.down_function[i] = self.down_function[i - 1]

        self.down_function[0] = self.large_vertex.get_shifted_value(self)

    @staticmethod
    def color(value):

        mag = abs(value)

        if mag > 1:
            mag = 1

        mag *= 255

        phase = numpy.degrees(cmath.phase(value))

        if phase < 0:
            phase = 360 + phase

        red = 0

        if phase < 120:
            red = mag * phase / 120
        elif phase > 240:
            red = mag * (360 - phase) / 60

        green = 0

        if phase < 120:
            green = mag * abs(120 - phase) / 120

        blue = 0

        if phase > 120:
            blue = mag * abs(240 - phase) / 120

        return "rgb({},{},{})".format(int(red), int(blue), int(green))

    def draw(self, fig):

        res = self.get_edge_resolution()

        width = self._edge_width

        xdiff = self.large_vertex.position[0] - self.small_vertex.position[0]
        ydiff = self.large_vertex.position[1] - self.small_vertex.position[1]

        length = math.sqrt(xdiff*xdiff + ydiff*ydiff)

        xoffset = ydiff * self._edge_offset / length
        yoffset = -xdiff * self._edge_offset / length

        xstep = xdiff / res
        ystep = ydiff / res

        xoverlap = self._edge_resolution_overlap * xstep
        yoverlap = self._edge_resolution_overlap * ystep

        # down function starts up and goes down
        x = self.large_vertex.position[0] + xoffset
        y = self.large_vertex.position[1] + yoffset

        for i in range(res):
            fig.draw_line(x, y, x - xstep - xoverlap, y - ystep - yoverlap,
                          width=width,
                          color=self.color(self.down_function[i])
                          )
            x -= xstep
            y -= ystep

        # up function starts down and goes up,
        # and is offset in other direction
        x = self.small_vertex.position[0] - xoffset
        y = self.small_vertex.position[1] - yoffset

        for i in range(res):
            fig.draw_line(x, y, x + xstep + xoverlap, y + ystep + yoverlap,
                          color=self.color(self.up_function[i]),
                          width=width,
                          )
            x += xstep
            y += ystep
