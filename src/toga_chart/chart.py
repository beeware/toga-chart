import math
import sys

from matplotlib.backend_bases import FigureCanvasBase, RendererBase
from matplotlib.path import Path
from matplotlib.transforms import Affine2D

from toga.colors import color as parse_color
from toga.colors import rgba
from toga.fonts import CURSIVE, FANTASY, MONOSPACE, SANS_SERIF, SERIF, Font
from toga.widgets.canvas import Canvas


class Chart(Canvas, FigureCanvasBase):
    """Create new chart.

    Args:
        id (str):  An identifier for this widget.
        style (:obj:`Style`): An optional style object. If no
            style is provided then a new one will be created for the widget.
        factory (:obj:`module`): A python module that is capable to return a
            implementation of this class with the same name. (optional &
            normally not needed)
    """
    def __init__(self, id=None, style=None, factory=None):
        Canvas.__init__(self, id=id, style=style, factory=factory)

    def draw(self, figure):
        """Draws the matplotlib figure onto the canvas

        Args:
            figure (figure):  matplotlib figure to draw
        """
        self.figure = figure
        FigureCanvasBase.__init__(self, self.figure)
        l, b, w, h = self.figure.bbox.bounds
        renderer = ChartRenderer(self, w, h)
        self.figure.draw(renderer)


class ChartRenderer(RendererBase):
    """
    The renderer handles drawing/rendering operations.

    Args:
        renderer (:obj:`Canvas`):  canvas to render onto
        width (int): width of canvas
        height (int): height of canvas
    """
    def __init__(self, renderer, width, height):
        self.width = width
        self.height = height
        self._renderer = renderer
        RendererBase.__init__(self)

    def draw_path(self, gc, path, transform, rgbFace=None):
        """
        TODO alpha
        TODO Hatch
        """
        if rgbFace is not None:
            r, g, b, a = rgbFace
        else:
            r, g, b, a = gc.get_rgb()

        color = parse_color(rgba(r*255, g*255, b*255, a))

        if rgbFace is not None:
            stroke_fill_context = self._renderer.fill(color=color)
        else:
            offset, sequence = gc.get_dashes()
            stroke_fill_context = self._renderer.stroke(color=color, line_width=gc.get_linewidth(), line_dash=sequence)

        transform = transform + \
            Affine2D().scale(1.0, -1.0).translate(0.0, self.height)

        with stroke_fill_context as context:
            with context.context() as path_segments:
                for points, code in path.iter_segments(transform):
                    if code == Path.MOVETO:
                        path_segments.move_to(points[0], points[1])
                    elif code == Path.LINETO:
                        path_segments.line_to(points[0], points[1])
                    elif code == Path.CURVE3:
                        path_segments.quadratic_curve_to(points[0], points[1], points[2], points[3])
                    elif code == Path.CURVE4:
                        path_segments.bezier_curve_to(points[0], points[1], points[2], points[3], points[4], points[5])
                    elif code == Path.CLOSEPOLY:
                        path_segments.closed_path(points[0], points[1])

    def draw_image(self, gc, x, y, im):
        pass

    def draw_text(self, gc, x, y, s, prop, angle, ismath=False, mtext=None):
        """
        Draw text on the chart.

        Math-formatted text is drawn using paths; normal text is written using
        native Canvas methods.
        """
        # TODO: Winforms canvas doesn't support math mode text (yet!)
        # Do a minimalist attempt at stripping the math markup and turn the
        # string into a non-math string.
        if sys.platform == 'win32':
            ismath = False
            s = s.replace('$', '')

        # Math mode text must be rendered using paths.
        # Otherwise, we can use canvas-level text markup.
        if ismath:
            path, transform = self._get_text_path_transform(x, y, s, prop, angle, ismath)
            color = gc.get_rgb()

            gc.set_linewidth(.75)
            self.draw_path(gc, path, transform, rgbFace=color)
        else:
            self._renderer.translate(x, y)
            self._renderer.rotate(-math.radians(angle))
            with self._renderer.fill(color=self.to_toga_color(*gc.get_rgb())) as fill:
                font = self.get_font(prop)
                fill.write_text(s, x=0, y=0, font=font)
            self._renderer.reset_transform()

    def flipy(self):
        return True

    def get_canvas_width_height(self):
        return self.width, self.height

    def get_text_width_height_descent(self, s, prop, ismath):
        """
        get the width and height in display coords of the string s
        with FontPropertry prop
        """
        font = self.get_font(prop)
        w, h = self._renderer.measure_text(s, font)
        return w, h, 1

    def get_font(self, prop):
        if prop.get_family()[0] == SANS_SERIF:
            font_family = SANS_SERIF
        elif prop.get_family()[0] == CURSIVE:
            font_family = CURSIVE
        elif prop.get_family()[0] == FANTASY:
            font_family = FANTASY
        elif prop.get_family()[0] == MONOSPACE:
            font_family = MONOSPACE
        else:
            font_family = SERIF

        size = int(prop.get_size_in_points())
        return Font(family=font_family, size=size)

    def to_toga_color(self, r, g, b, a):
        return parse_color(rgba(r * 255, g * 255, b * 255, a))
