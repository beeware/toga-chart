import math
import sys

from matplotlib.backend_bases import FigureCanvasBase, RendererBase
from matplotlib.figure import Figure
from matplotlib.path import Path
from matplotlib.transforms import Affine2D
from toga import Widget

from toga.colors import color as parse_color
from toga.colors import rgba
from toga.fonts import CURSIVE, FANTASY, MONOSPACE, SANS_SERIF, SERIF, Font
from toga.handlers import wrapped_handler
from toga.widgets.canvas import Canvas


class Chart(Widget):
    """Create new chart.

    Args:
        id (str):  An identifier for this widget.
        style (:obj:`Style`): An optional style object. If no
            style is provided then a new one will be created for the widget.
        on_resize (:obj:`callable`): Handler to invoke when the chart is resized.
            The default resize handler will draw the chart on every resize;
            generally, you won't need to override this default behavior.
        on_draw (:obj:`callable`): Handler to invoke when the chart needs to be
            drawn.
        factory (:obj:`module`): A python module that is capable to return a
            implementation of this class with the same name. (optional &
            normally not needed)
    """
    def __init__(self, style=None, on_resize=None, on_draw=None, factory=None):
        if on_resize is None:
            on_resize = self._resize
        super().__init__(style=style, factory=factory)
        self.canvas = Canvas(style=style, on_resize=on_resize, factory=factory)
        self._impl = self.canvas._impl
        self.on_draw = on_draw

    def draw(self, figure):
        """Draws the matplotlib figure onto the canvas

        Args:
            figure (figure):  matplotlib figure to draw
        """
        l, b, w, h = figure.bbox.bounds
        matplotlib_canvas = MatplotlibCanvasProxy(figure=figure, canvas=self.canvas)
        renderer = ChartRenderer(matplotlib_canvas, w, h)

        # Invoke the on_draw handler (if present).
        # This is where the user adds the matplotlib draw instructions
        # to construct the chart, so it needs to happen before the
        # figure is rendered onto the canvas.
        if self.on_draw:
            self.on_draw(self, figure=figure)

        figure.draw(renderer)

    def _resize(self, *args, **kwargs):
        ""
        # 100 is the default DPI for figure at time of writing.
        dpi = 100
        figure = Figure(
            figsize=(
                self.layout.content_width / dpi,
                self.layout.content_height / dpi
            )
        )
        self.draw(figure)

    @property
    def on_draw(self):
        """The handler to invoke when the canvas needs to be drawn.

        Returns:
            The handler that is invoked on canvas draw.
        """
        return self._on_draw

    @on_draw.setter
    def on_draw(self, handler):
        """Set the handler to invoke when the canvas is drawn.

        Args:
            handler (:obj:`callable`): The handler to invoke when the canvas is drawn.
        """
        self._on_draw = wrapped_handler(self, handler)


class MatplotlibCanvasProxy(FigureCanvasBase):
    def __init__(self, figure, canvas: Canvas):
        super().__init__(figure)
        self.canvas = canvas

    def fill(self, color):
        return self.canvas.fill(color=color)

    def stroke(self, color, line_width, line_dash):
        return self.canvas.stroke(color=color, line_width=line_width, line_dash=line_dash)

    def measure_text(self, text, font):
        return self.canvas.measure_text(text=text, font=font)

    def translate(self, tx, ty):
        return self.canvas.translate(tx, ty)

    def rotate(self, radians):
        return self.canvas.rotate(radians)

    def reset_transform(self):
        return self.canvas.reset_transform()


class ChartRenderer(RendererBase):
    """
    The renderer handles drawing/rendering operations.

    Args:
        canvas (:obj:`Canvas`):  canvas to render onto
        width (int): width of canvas
        height (int): height of canvas
    """
    def __init__(self, canvas, width, height):
        self.width = width
        self.height = height
        self._canvas = canvas
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
            stroke_fill_context = self._canvas.fill(color=color)
        else:
            offset, sequence = gc.get_dashes()
            stroke_fill_context = self._canvas.stroke(color=color, line_width=gc.get_linewidth(), line_dash=sequence)

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
            self._canvas.translate(x, y)
            self._canvas.rotate(-math.radians(angle))
            with self._canvas.fill(color=self.to_toga_color(*gc.get_rgb())) as fill:
                font = self.get_font(prop)
                fill.write_text(s, x=0, y=0, font=font)
            self._canvas.reset_transform()

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
        w, h = self._canvas.measure_text(s, font)
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
