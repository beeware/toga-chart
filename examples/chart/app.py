import toga
import toga_chart
from toga.style import Pack
import numpy as np
from toga.constants import COLUMN


class ExampleChartApp(toga.App):
    def draw_chart(self, chart, figure, *args, **kwargs):
        # Generate some example data
        mu = 100  # mean of distribution
        sigma = 15  # standard deviation of distribution
        x = mu + sigma * np.random.randn(437)

        num_bins = 50

        # Add a subplot that is a histogram of the data,
        # using the normal matplotlib API
        ax = figure.add_subplot(1, 1, 1)
        n, bins, patches = ax.hist(x, num_bins, density=1)

        # add a 'best fit' line
        y = ((1 / (np.sqrt(2 * np.pi) * sigma)) * np.exp(-0.5 * (1 / sigma * (bins - mu))**2))
        ax.plot(bins, y, '--')

        ax.set_xlabel('Value')
        ax.set_ylabel('Probability density')
        ax.set_title(r'Histogram: $\mu=100$, $\sigma=15$')

        figure.tight_layout()

    def startup(self):
        np.random.seed(19680801)

        # Set up main window
        self.main_window = toga.MainWindow(title=self.name)

        self.chart = toga_chart.Chart(style=Pack(flex=1), on_draw=self.draw_chart)

        self.main_window.content = toga.Box(
            children=[
                self.chart,
            ],
            style=Pack(direction=COLUMN)
        )

        self.main_window.show()


def main():
    return ExampleChartApp('Chart', 'org.beeware.widgets.chart')


if __name__ == '__main__':
    main().main_loop()
