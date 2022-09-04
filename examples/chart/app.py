import toga
import toga_chart
from toga.style import Pack
import numpy as np
from toga.constants import COLUMN


class ExampleChartApp(toga.App):
    mu = 100  # mean of distribution
    sigma = 15  # standard deviation of distribution

    def draw_chart(self, chart, figure, *args, **kwargs):

        num_bins = 50

        # Add a subplot that is a histogram of the data,
        # using the normal matplotlib API
        ax = figure.add_subplot(1, 1, 1)
        n, bins, patches = ax.hist(self.x, num_bins, density=1)

        # add a 'best fit' line
        y = ((1 / (np.sqrt(2 * np.pi) * self.sigma)) * np.exp(-0.5 * (1 / self.sigma * (bins - self.mu))**2))
        ax.plot(bins, y, '--')

        ax.set_xlabel('Value')
        ax.set_ylabel('Probability density')
        ax.set_title(r'Histogram: $\mu=100$, $\sigma=15$')

        figure.tight_layout()

    def startup(self):
        np.random.seed(19680801)
        self.recreate_data()

        # Set up main window
        self.main_window = toga.MainWindow(title=self.name)

        self.chart = toga_chart.Chart(style=Pack(flex=1), on_draw=self.draw_chart)

        self.main_window.content = toga.Box(
            children=[
                self.chart,
                toga.Button(
                    "Recreate Data",
                    on_press=self.on_recreate_press,
                    style=Pack(padding_bottom=10, padding_top=10)
                )
            ],
            style=Pack(direction=COLUMN)
        )

        self.main_window.show()

    def recreate_data(self):
        # Generate some example data
        self.x = self.mu + self.sigma * np.random.normal(size=500)

    def on_recreate_press(self, widget):
        self.recreate_data()
        self.chart.draw(self.chart.build_figure())


def main():
    return ExampleChartApp('Chart', 'org.beeware.widgets.chart')


if __name__ == '__main__':
    main().main_loop()
