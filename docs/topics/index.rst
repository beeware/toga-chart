.. _topics:

======
Topics
======

Topic guides explain the concepts and design decisions behind Toga Chart.

Matplotlib and Toga Chart
=========================

Toga Chart provides a bridge between `Matplotlib <https://matplotlib.org/>`__ and
Toga's native widget system. A :class:`toga_chart.Chart` owns a Matplotlib
:class:`~matplotlib.figure.Figure`; when the widget needs to be drawn, Toga Chart
passes that figure to your ``on_draw`` handler, then renders the Matplotlib
output onto a Toga ``Canvas``.

Toga Chart doesn't replace Matplotlib's plotting API. You still create subplots,
plot data, set labels, configure titles, and adjust layouts with Matplotlib. If
you need details on plotting commands, consult the `Matplotlib documentation
<https://matplotlib.org/stable/index.html>`__.

The Toga-specific part of a chart is the widget lifecycle: create a
:class:`~toga_chart.Chart`, provide an ``on_draw`` handler, put the chart in your
Toga layout, and call :meth:`~toga_chart.Chart.redraw` when data changes.
