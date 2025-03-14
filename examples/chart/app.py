import numpy as np
import toga
from toga.constants import COLUMN
from toga.style import Pack

import toga_chart


class ExampleChartApp(toga.App):
    def set_data(self):
        # Generate some example data
        self.x = self.mu.value + self.sigma.value * np.random.randn(1000)

    def draw_chart(self, chart, figure, *args, **kwargs):
        num_bins = 50

        # Add a subplot that is a histogram of the data,
        # using the normal matplotlib API
        ax = figure.add_subplot(1, 1, 1)
        n, bins, patches = ax.hist(self.x, num_bins, density=1, range=(0, 200))

        # add a 'best fit' line
        y = (1 / (np.sqrt(2 * np.pi) * self.sigma.value)) * np.exp(
            -0.5 * (1 / self.sigma.value * (bins - self.mu.value)) ** 2
        )
        ax.plot(bins, y, "--")

        ax.set_xlabel("Value")
        ax.set_ylabel("Probability density")
        ax.set_title(
            rf"Histogram: $\mu={self.mu.value:.1f}$, "
            rf"$\sigma={self.sigma.value:.1f}$"
        )

        figure.tight_layout()

    def recreate_data(self, widget):
        self.set_data()
        self.chart.redraw()

    def startup(self):
        # Set up main window
        self.main_window = toga.MainWindow()

        self.chart = toga_chart.Chart(style=Pack(flex=1), on_draw=self.draw_chart)

        self.mu = toga.Slider(
            value=100,
            min=0,
            max=200,
            on_change=self.recreate_data,
            style=Pack(flex=1),
        )
        self.sigma = toga.Slider(
            value=15,
            min=1,
            max=30,
            on_change=self.recreate_data,
            style=Pack(flex=1),
        )

        self.set_data()

        self.main_window.content = toga.Box(
            children=[
                self.chart,
                toga.Box(
                    children=[toga.Label("𝜇"), self.mu],
                    style=Pack(margin=(5, 10)),
                ),
                toga.Box(
                    children=[toga.Label("𝜎"), self.sigma],
                    style=Pack(margin=(5, 10)),
                ),
                toga.Button(
                    "Recreate data",
                    on_press=self.recreate_data,
                    style=Pack(margin=(10, 10, 20, 10)),
                ),
            ],
            style=Pack(direction=COLUMN),
        )

        self.main_window.show()


def main():
    return ExampleChartApp("Chart", "org.beeware.widgets.chart")


if __name__ == "__main__":
    main().main_loop()
