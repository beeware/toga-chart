.. _reference:

=========
Reference
=========

This is the technical reference for public APIs provided by Toga Chart.

.. module:: toga_chart

Chart
=====

.. py:class:: Chart(id=None, style=None, on_resize=None, on_draw=None)

   A Toga widget that displays a Matplotlib figure.

   ``Chart`` is a standalone Toga widget. It can be used anywhere a normal Toga
   widget can be used: assign it as the content of a window, add it to a
   :class:`toga.Box`, or style it with :class:`toga.style.Pack`.

   When the chart is drawn, Toga Chart creates a Matplotlib
   :class:`matplotlib.figure.Figure`, passes that figure to the ``on_draw``
   handler, and renders the resulting Matplotlib drawing operations onto a Toga
   ``Canvas``.

   :param str id: An optional identifier for the widget.
   :param style: An optional Toga style object. If no style is provided, a new
       style object will be created for the widget.
   :param callable on_resize: A handler to invoke when the chart is resized. If
       this is not provided, the chart redraws itself whenever its size changes.
   :param callable on_draw: A handler to invoke when the chart needs to be drawn.
       This handler is where you define the Matplotlib plot.

   .. py:attribute:: on_draw

      The handler invoked when the chart needs to be drawn.

      The handler receives the chart widget as its first positional argument, and
      the Matplotlib figure as a keyword argument named ``figure``:

      .. code-block:: python

         def draw_chart(widget, figure, **kwargs):
             axes = figure.add_subplot(1, 1, 1)
             axes.plot([1, 2, 3], [1, 4, 9])

      The handler should use the standard Matplotlib API to populate the figure.
      It does not need to return a value.

   .. py:method:: redraw()

      Redraw the chart.

      Calling this method creates a new Matplotlib figure sized to match the
      widget's current layout, invokes the ``on_draw`` handler, and renders the
      updated figure onto the widget.

      Call this method when the data behind a chart changes:

      .. code-block:: python

         self.chart.redraw()

Example
=======

A minimal chart widget can be created with an ``on_draw`` handler:

.. code-block:: python

   import toga_chart


   def draw_chart(widget, figure, **kwargs):
       axes = figure.add_subplot(1, 1, 1)
       axes.plot([1, 2, 3, 4], [1, 4, 9, 16])
       figure.tight_layout()


   chart = toga_chart.Chart(on_draw=draw_chart)

See the :ref:`tutorial` for a complete Toga application using this widget.
