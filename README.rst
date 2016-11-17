=======
lifelog
=======

Generate an HTML version of a Markdown logbook. Content is enriched with
images/photographs of that day, Sleep as Android sleep stats, Google Fit steps
and the weather.

|PyPI version| |PyPI downloads| |PyPI license| |Code health|

`lifelog` outputs a [paragoo](https://github.com/aquatix/paragoo) project, which
can be rendered to HTML. Use the [paragoo-theme-lifelog](https://github.com/aquatix/paragoo-theme-material)
for the best results.


Installation
------------


Configuration
-------------

`lifelog` uses a small Yaml file for describing what to do.

Use
---

python lifelog.py build_logbook --path=/home/myuser/captainslog -d /home/myuser/workspace/html/captainslog


Plugins
-------

- Photos (by imagine)
- Sleep as Android sleep stats
- Google Fit steps (Google Checkout or maybe API)
- Pocket read stats (by pocketstats)
- Weather (which provider?)


.. |PyPI version| image:: https://img.shields.io/pypi/v/lifelog.svg
   :target: https://pypi.python.org/pypi/lifelog/
.. |PyPI downloads| image:: https://img.shields.io/pypi/dm/lifelog.svg
   :target: https://pypi.python.org/pypi/lifelog/
.. |PyPI license| image:: https://img.shields.io/github/license/aquatix/lifelog.svg
   :target: https://pypi.python.org/pypi/lifelog/
.. |Code health| image:: https://landscape.io/github/aquatix/lifelog/master/landscape.svg?style=flat
   :target: https://landscape.io/github/aquatix/ns-api/master
   :alt: Code Health
