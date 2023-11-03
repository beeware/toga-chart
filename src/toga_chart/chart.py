import math
import sys

from matplotlib.backend_bases import RendererBase
from matplotlib.figure import Figure
from matplotlib.path import Path
from matplotlib.transforms import Affine2D
from toga import Canvas, Widget
from toga.colors import color as parse_color, rgba
from toga.fonts import CURSIVE, FANTASY, MONOSPACE, SANS_SERIF, SERIF, Font
from toga.handlers import wrapped_handler


class Chart(Widget):
    def __init__(
        self,
        id: str = None,
        style=None,
        on_resize: callable = None,
        on_draw: callable = None,
    ):
        """Create a new matplotlib chart.

        :param id: An identifier for this widget.
        :param style: An optional style object. If no style is provided then a new one
            will be created for the widget.
        :param on_resize: Handler to invoke when the chart is resized. The default
            resize handler will draw the chart on every resize; generally, you won't
            need to override this default behavior.
        :param on_draw: Handler to invoke when the chart needs to be drawn. This
            performs the matplotlib drawing operations that will be displayed on the
            chart.
        """
        self.on_draw = on_draw
        if on_resize is None:
            on_resize = self._on_resize

        # The Chart widget that the user interacts with is a subclass of Widget, not
        # Canvas; this subclass acts as a facade over the underlying Canvas
        # implementation (mostly so that the redraw() method of the Chart is independent
        # of the Canvas redraw() method). The _impl of the Chart is set to the Canvas
        # _impl so that functionally, the widget behaves as a Canvas.
        self.canvas = Canvas(style=style, on_resize=on_resize)

        super().__init__(id=id, style=style)

        self._impl = self.canvas._impl

    @Widget.app.setter
    def app(self, app):
        # Invoke the superclass property setter
        Widget.app.fset(self, app)
        # Point the canvas to the same app
        self.canvas.app = app

    @Widget.window.setter
    def window(self, window):
        # Invoke the superclass property setter
        Widget.window.fset(self, window)
        # Point the canvas to the same window
        self.canvas.window = window

    @property
    def layout(self):
        return self.canvas.layout

    @layout.setter
    def layout(self, value):
        self.canvas.layout = value

    def _draw(self, figure: Figure):
        """Draw the matplotlib figure onto the canvas.

        :param figure: The matplotlib figure to draw
        """
        l, b, w, h = figure.bbox.bounds
        renderer = ChartRenderer(self.canvas, w, h)

        # Invoke the on_draw handler.
        # This is where the user adds the matplotlib draw instructions
        # to construct the chart, so it needs to happen before the
        # figure is rendered onto the canvas.
        self.on_draw(figure=figure)

        figure.draw(renderer)

    def _on_resize(self, widget, **kwargs):
        self.redraw()

    def redraw(self):
        """Redraw the chart."""
        # 100 is the default DPI for figure at time of writing.
        dpi = 100
        figure = Figure(
            figsize=(
                self.layout.content_width / dpi,
                self.layout.content_height / dpi,
            ),
        )
        self._draw(figure)

    @property
    def on_draw(self) -> callable:
        """The handler to invoke when the canvas needs to be drawn."""
        return self._on_draw

    @on_draw.setter
    def on_draw(self, handler: callable):
        self._on_draw = wrapped_handler(self, handler)


class ChartRenderer(RendererBase):
    def __init__(self, canvas: Canvas, width: int, height: int):
        """
        The matplotlib handler for drawing/rendering operations.

        :param canvas: The canvas to render onto
        :param width: Width of canvas
        :param height: height of canvas
        """
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

        color = parse_color(rgba(r * 255, g * 255, b * 255, a))

        if rgbFace is not None:
            stroke_fill_context = self._canvas.context.Fill(color=color)
        else:
            offset, sequence = gc.get_dashes()
            stroke_fill_context = self._canvas.context.Stroke(
                color=color,
                line_width=gc.get_linewidth(),
                line_dash=sequence,
            )

        transform = transform + Affine2D().scale(1.0, -1.0).translate(0.0, self.height)

        with stroke_fill_context as context:
            with context.Context() as path_segments:
                for points, code in path.iter_segments(transform):
                    if code == Path.MOVETO:
                        path_segments.move_to(points[0], points[1])
                    elif code == Path.LINETO:
                        path_segments.line_to(points[0], points[1])
                    elif code == Path.CURVE3:
                        path_segments.quadratic_curve_to(
                            points[0],
                            points[1],
                            points[2],
                            points[3],
                        )
                    elif code == Path.CURVE4:
                        path_segments.bezier_curve_to(
                            points[0],
                            points[1],
                            points[2],
                            points[3],
                            points[4],
                            points[5],
                        )
                    elif code == Path.CLOSEPOLY:
                        path_segments.ClosedPath(points[0], points[1])

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
        if sys.platform == "win32":
            ismath = False
            s = s.replace("$", "")

        # Math mode text must be rendered using paths.
        # Otherwise, we can use canvas-level text markup.
        if ismath:
            path, transform = self._get_text_path_transform(
                x, y, s, prop, angle, ismath
            )
            color = gc.get_rgb()

            gc.set_linewidth(0.75)
            self.draw_path(gc, path, transform, rgbFace=color)
        else:
            self._canvas.context.translate(x, y)
            self._canvas.context.rotate(-math.radians(angle))
            with self._canvas.context.Fill(
                color=self.to_toga_color(*gc.get_rgb())
            ) as fill:
                font = self.get_font(prop)
                fill.write_text(s, x=0, y=0, font=font)
            self._canvas.context.reset_transform()

    def flipy(self):
        return True

    def get_canvas_width_height(self):
        return self.width, self.height

    def get_text_width_height_descent(self, s, prop, ismath):
        """Get the width and height in display coords of the string s
        with FontProperty prop
        """
        font = self.get_font(prop)
        w, h = self._canvas.measure_text(s, font)
        return w, h, 1

    def get_font(self, prop):
        if prop.get_family()[0] in {SANS_SERIF, CURSIVE, FANTASY, MONOSPACE}:
            font_family = prop.get_family()[0]
        else:
            font_family = SERIF

        size = int(prop.get_size_in_points())
        return Font(family=font_family, size=size)

    def to_toga_color(self, r, g, b, a):
        return parse_color(rgba(r * 255, g * 255, b * 255, a))
