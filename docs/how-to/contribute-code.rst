Contributing code to Toga-Chart
===============================

If you experience problems with Toga-Chart, `log them on GitHub`_. If you want
to contribute code, please `fork the code`_ and `submit a pull request`_.

.. _log them on Github: https://github.com/beeware/toga-chart/issues
.. _fork the code: https://github.com/beeware/toga-chart
.. _submit a pull request: https://github.com/beeware/toga-chart/pulls

.. _setup-dev-environment:

Setting up your development environment
---------------------------------------

The recommended way of setting up your development environment for Toga-Chart is
to use a `virtual environment <https://docs.python.org/3/library/venv.html>`__,
install the required dependencies and start coding:

.. tabs::

  .. group-tab:: macOS

    .. code-block:: bash

      $ git clone https://github.com/beeware/toga-chart.git
      $ cd toga-chart
      $ python3 -m venv venv
      $ . venv/bin/activate

  .. group-tab:: Linux

    .. code-block:: bash

      $ git clone https://github.com/beeware/toga-chart.git
      $ cd toga-chart
      $ python3 -m venv venv
      $ . venv/bin/activate

  .. group-tab:: Windows

    .. code-block:: doscon

      C:\...>git clone https://github.com/beeware/toga-chart.git
      C:\...>cd toga-chart
      C:\...>py -m venv venv
      C:\...>venv\Scripts\activate

To install all the development version of Toga-Chart, along with all it's
requirements, run the following commands within your virtual environment:

.. tabs::

  .. group-tab:: macOS

    .. code-block:: bash

      $ (venv) pip install -e .

  .. group-tab:: Linux

    .. code-block:: bash

      $ (venv) pip install -e .

  .. group-tab:: Windows

    .. code-block:: doscon

      C:\...>pip install -e .

Now you are ready to start hacking! Have fun!

Toga-Chart uses `PyTest <https://pytest.org>`__ for its own test suite. It uses
`tox <https://tox.readthedocs.io/en/latest/>`__ to manage the testing process.
To set up a testing environment and run the full test suite:

.. tabs::

  .. group-tab:: macOS

    .. code-block:: bash

      $ (venv) pip install tox
      $ (venv) tox

  .. group-tab:: Linux

    .. code-block:: bash

      $ (venv) pip install tox
      $ (venv) tox

  .. group-tab:: Windows

    .. code-block:: doscon

      C:\...>pip install tox
      C:\...>tox

By default this will run the test suite multiple times, once on each Python
version supported by Toga-Chart, as well as running some pre-commit checks of
code style and validity. This can take a while, so if you want to speed up
the process while developing, you can run the tests on one Python version only:

.. tabs::

  .. group-tab:: macOS

    .. code-block:: bash

      (venv) $ tox -e py

  .. group-tab:: Linux

    .. code-block:: bash

      (venv) $ tox -e py

  .. group-tab:: Windows

    .. code-block:: bash

      C:\...>tox -e py

Or, to run using a specific version of Python:

.. tabs::

  .. group-tab:: macOS

    .. code-block:: bash

      (venv) $ tox -e py

  .. group-tab:: Linux

    .. code-block:: bash

      (venv) $ tox -e py

  .. group-tab:: Windows

    .. code-block:: bash

      C:\...>tox -e py

substituting the version number that you want to target. You can also specify
one of the pre-commit checks `flake8`, `docs` or `package` to check code
formatting, documentation syntax and packaging metadata, respectively.
