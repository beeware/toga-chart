import numpy as np
import toga
from toga.constants import COLUMN
from toga.style import Pack

import toga_chart


class ExampleChartApp(toga.App):
    MU = 100  # mean of distribution
    SIGMA = 15  # standard deviation of distribution

    def set_data(self):
        # Generate some example data
        self.x = self.MU + self.SIGMA * np.random.randn(437)

    def draw_chart(self, chart, figure, *args, **kwargs):
        num_bins = 50

        # Add a subplot that is a histogram of the data,
        # using the normal matplotlib API
        ax = figure.add_subplot(1, 1, 1)
        n, bins, patches = ax.hist(self.x, num_bins, density=1)

        # add a 'best fit' line
        y = (1 / (np.sqrt(2 * np.pi) * self.SIGMA)) * np.exp(
            -0.5 * (1 / self.SIGMA * (bins - self.MU)) ** 2
        )
        ax.plot(bins, y, "--")

        ax.set_xlabel("Value")
        ax.set_ylabel("Probability density")
        ax.set_title(r"Histogram: $\mu=100$, $\sigma=15$")

        figure.tight_layout()

    def recreate_data(self, widget):
        self.set_data()
        self.chart.redraw()

    def startup(self):
        np.random.seed(19680801)
        self.set_data()

        # Set up main window
        self.main_window = toga.MainWindow()

        self.chart = toga_chart.Chart(style=Pack(flex=1), on_draw=self.draw_chart)

        self.main_window.content = toga.Box(
            children=[
                self.chart,
                toga.Button("Recreate data", on_press=self.recreate_data),
            ],
            style=Pack(direction=COLUMN),
        )

        self.main_window.show()


def main():
    return ExampleChartApp("Chart", "org.beeware.widgets.chart")


if __name__ == "__main__":
    main().main_loop()
