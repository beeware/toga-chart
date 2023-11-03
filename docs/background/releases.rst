===============
Release History
===============

.. towncrier release notes start

0.2.0 (2023-11-03)
==================

Features
--------

* Chart is a now standalone widget, rather than an extension of a Toga Canvas. (#22)

Bugfixes
--------

* The requirements of ``toga-chart`` were modified so that toga-chart is only dependent on ``toga-core``, rather than the ``toga`` meta-package. This makes it possible to install ``toga-chart`` on Android, as the meta-package no longer attempts to install the ``toga-gtk`` backend on Android; but it requires that end-users explicitly specify ``toga`` or an explicit backend in their own app requirements. (#24)

Misc
----

* #25, #26, #27, #28, #29, #30, #31, #32, #36, #37, #38, #39, #40, #41, #42, #43, #44, #45, #46, #47, #48, #49, #50, #51, #52, #53, #55, #56, #58, #63


0.1.1 (2022-08-19)
==================

Features
--------

* Chart now has an ``on_draw()`` handler to ensure the chart auto-resizes. (#14)


Bugfixes
--------

* Added a `None` check before calling `on_draw` (#17)


Misc
----

* #18


0.1.0 (2020-08-09)
------------------

Initial public release.
