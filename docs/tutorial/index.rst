.. _tutorial:

========
Tutorial
========

This tutorial builds a minimal Toga app that displays a Matplotlib chart as its
only widget.

Create an app
=============

Start with a regular Toga application module:

.. code-block:: python

   import toga
   from toga.style import Pack

   import toga_chart


   class ChartApp(toga.App):
       def startup(self):
           self.main_window = toga.MainWindow()

           self.chart = toga_chart.Chart(
               style=Pack(flex=1),
               on_draw=self.draw_chart,
           )

           self.main_window.content = self.chart
           self.main_window.show()

       def draw_chart(self, widget, figure, **kwargs):
           axes = figure.add_subplot(1, 1, 1)
           axes.plot([1, 2, 3, 4], [1, 4, 9, 16])
           axes.set_xlabel("x")
           axes.set_ylabel("x squared")
           axes.set_title("A Toga Chart")
           figure.tight_layout()


   def main():
       return ChartApp("Chart", "org.example.chart")


   if __name__ == "__main__":
       main().main_loop()

Walkthrough
===========

The app imports Toga, :class:`toga.style.Pack`, and ``toga_chart``. The
``ChartApp`` class is a normal :class:`toga.App`; Toga calls its ``startup()``
method when the application starts.

``startup()`` creates a main window, then creates a :class:`toga_chart.Chart`.
The ``flex=1`` style tells the chart to expand to fill the available space. The
``on_draw`` handler identifies the method that will populate the Matplotlib
figure whenever the chart needs to be rendered.

The chart is assigned directly to ``main_window.content``, making it the only
widget in the window. Finally, ``show()`` displays the window.

``draw_chart()`` receives a Matplotlib ``figure``. The method uses the normal
Matplotlib API to add a subplot, plot some data, label the axes, set a title, and
tighten the layout. Toga Chart takes care of rendering that figure into the Toga
widget.

Updating a chart
================

If the data behind a chart changes, call :meth:`toga_chart.Chart.redraw` on the
chart widget. This causes Toga Chart to create a new Matplotlib figure, invoke
your ``on_draw`` handler, and render the updated figure.

The ``examples`` directory in the Toga Chart repository contains a larger app
that uses sliders and a button to update chart data interactively.
