===============
Release History
===============

.. towncrier release notes start

0.2.1 (2025-04-22)
==================

Features
--------

* The example app was modified to be more illustrative of potential usage. (#66)
* Support for Python 3.13 was added. (#183)

Bugfixes
--------

* Widget construction was made compatible with Toga 0.5. (#194)

Backward Incompatible Changes
-----------------------------

* Support for Python 3.8 was dropped. (#183)
* toga-chart now requires matplotlib 3.9.0 or newer. (#194)

Documentation
-------------

* The README badges were updated to display correctly on GitHub. (#122)
* Building toga-chart's documentation now requires the use of Python 3.12. (#153)

Misc
----

* #65, #67, #68, #69, #70, #71, #74, #75, #76, #77, #78, #81, #82, #83, #84, #85, #86, #87, #88, #89, #90, #91, #92, #93, #94, #95, #96, #97, #98, #99, #100, #101, #102, #103, #104, #105, #106, #107, #108, #109, #110, #111, #112, #113, #114, #115, #116, #117, #118, #119, #120, #121, #123, #124, #125, #126, #127, #128, #129, #130, #131, #132, #133, #134, #135, #136, #137, #138, #139, #140, #141, #142, #143, #144, #145, #146, #147, #148, #149, #150, #152, #155, #156, #157, #158, #160, #161, #162, #163, #164, #165, #166, #167, #168, #169, #170, #171, #172, #173, #174, #175, #176, #177, #178, #179, #180, #181, #182, #184, #185, #186, #187, #188, #189, #190, #192, #194, #195, #196, #197, #198, #199, #200, #201, #202, #203, #204, #205, #206, #207, #208, #209, #210, #211, #212, #213, #214, #215, #216, #217, #218, #219, #220, #221, #222, #223, #224, #225, #226, #227


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
