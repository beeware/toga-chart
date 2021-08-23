import toga
import toga_chart
from toga.style import Pack
from matplotlib.figure import Figure
import numpy as np
from toga.constants import COLUMN


class ExampleChartApp(toga.App):

    def draw_chart(self):
        # example data
        mu = 100  # mean of distribution
        sigma = 15  # standard deviation of distribution
        x = mu + sigma * np.random.randn(437)

        num_bins = 50

        dpi = 100  # as of writing, 100 is also the default DPI for matplotlib.figure.Figure
        f = Figure(figsize=(self.chart.layout.content_width / dpi, self.chart.layout.content_height / dpi), dpi=dpi)
        ax = f.add_subplot(1, 1, 1)

        # the histogram of the data
        n, bins, patches = ax.hist(x, num_bins, density=1)

        # add a 'best fit' line
        y = ((1 / (np.sqrt(2 * np.pi) * sigma)) * np.exp(-0.5 * (1 / sigma * (bins - mu))**2))
        ax.plot(bins, y, '--')
        ax.set_xlabel('Value')
        ax.set_ylabel('Probability density')
        ax.set_title(r'Histogram: $\mu=100$, $\sigma=15$')

        f.tight_layout()
        return f


    def on_resize(self, *args, **kwargs):
        self.chart.draw(self.draw_chart())


    def startup(self):
        np.random.seed(19680801)

        # Set up main window
        self.main_window = toga.MainWindow(title=self.name)

        self.chart = toga_chart.Chart(style=Pack(flex=1), on_resize=self.on_resize)

        self.main_window.content = toga.Box(
            children=[
                self.chart,
            ],
            style=Pack(direction=COLUMN)
        )

        self.chart.draw(self.draw_chart())

        self.main_window.show()


def main():
    return ExampleChartApp('Chart', 'org.pybee.widgets.chart')


if __name__ == '__main__':
    main().main_loop()
