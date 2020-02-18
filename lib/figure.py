import cv2
import numpy

from PIL import Image, ImageDraw


class Figure:
    width = 0
    height = 0
    xmin = -1
    ymin = -1
    xmax = 1
    ymax = 1

    base_image = None
    frames = []
    current_frame = None
    current_draw = None

    bgcolor = (100, 100, 100)

    def __init__(self, xmin=-1, xmax=1, ymin=-1, ymax=1,
                 width=800, height=800):

        if height == 0 or width == 0 or xmin >= xmax or ymin >= ymax:
            raise ValueError("Figure dimensions are inconsistant")

        self.width = width
        self.height = height
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax

        self.base_image = Image.new("RGB", (width, height), self.bgcolor)

    def new_frame(self):
        self.current_frame = self.base_image.copy()
        self.frames.append(self.current_frame)
        self.current_draw = ImageDraw.Draw(self.current_frame)

    def save(self, name, duration=100):

        if len(self.frames) == 1:
            self.frames[0].save(name)
        elif len(self.frames) > 1:
            self.frames[0].save(name,
                                save_all=True,
                                append_images=self.frames[1:],
                                duration=duration,
                                loop=0)

    def save_movie(self, name, fps=20):

        if not name.endswith(".avi"):
            raise ValueError("Movie name must end in .avi")

        out = cv2.VideoWriter(name, cv2.VideoWriter_fourcc(*'XVID'), fps, (self.width, self.height))

        for frame in self.frames:
            out.write(numpy.asarray(frame)[:, :, ::-1].copy())

        out.release()

    def _pt2px(self, x, y):
        px = int(x * self.width / (self.xmax - self.xmin) + self.width / 2)
        py = int(self.height / 2 - y * self.height / (self.ymax - self.ymin))

        return px, py

    def draw_circle(self, xpos, ypos, radius, color):
        # The first point has to be the upper-left of the bounding box
        self.current_draw.ellipse([self._pt2px(xpos - radius, ypos + radius),
                                   self._pt2px(xpos + radius, ypos - radius)],
                                  fill=color, outline=color)

    def draw_line(self, x0, y0, x1, y1, color, width):
        self.current_draw.line([self._pt2px(x0, y0),
                                self._pt2px(x1, y1)],
                               fill=color, width=width)
