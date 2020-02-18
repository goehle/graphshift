import math

from lib.edge import Edge

class Warp_Edge(Edge):

    shrink_factor = .75

    def __init__(self, small_vertex, large_vertex, up_function, down_function):

        Edge.__init__(self, small_vertex, large_vertex, up_function, down_function)

    def draw(self, fig):

        res = self.get_edge_resolution()
        half_res = int( res / 2 )

        width = self._edge_width

        xdiff = self.large_vertex.position[0] - self.small_vertex.position[0]
        ydiff = self.large_vertex.position[1] - self.small_vertex.position[1]

        xdiff *= self.shrink_factor
        ydiff *= self.shrink_factor

        length = math.sqrt(xdiff * xdiff + ydiff * ydiff)

        xoffset = ydiff * self._edge_offset / length
        yoffset = -xdiff * self._edge_offset / length

        xstep = xdiff / res
        ystep = ydiff / res

        xoverlap = self._edge_resolution_overlap * xstep
        yoverlap = self._edge_resolution_overlap * ystep

        # down function
        x = self.large_vertex.position[0] + xoffset
        y = self.large_vertex.position[1] + yoffset

        for i in range(half_res):
            fig.draw_line(x, y, x + xstep + xoverlap, y + ystep + yoverlap,
                          width=width,
                          color=self.color(self.down_function[i])
                          )
            x += xstep
            y += ystep

        x = self.small_vertex.position[0] + xoffset
        y = self.small_vertex.position[1] + yoffset

        for i in range(half_res):
            fig.draw_line(x, y, x - xstep - xoverlap, y - ystep - yoverlap,
                          width=width,
                          color=self.color(self.down_function[res-i-1])
                          )
            x -= xstep
            y -= ystep

        # up function
        x = self.small_vertex.position[0] - xoffset
        y = self.small_vertex.position[1] - yoffset

        for i in range(half_res):
            fig.draw_line(x, y, x - xstep - xoverlap, y - ystep - yoverlap,
                          color=self.color(self.up_function[i]),
                          width=width,
                          )
            x -= xstep
            y -= ystep

        x = self.large_vertex.position[0] - xoffset
        y = self.large_vertex.position[1] - yoffset

        for i in range(half_res):
            fig.draw_line(x, y, x + xstep + xoverlap, y + ystep + yoverlap,
                          color=self.color(self.up_function[res-i-1]),
                          width=width,
                          )
            x += xstep
            y += ystep