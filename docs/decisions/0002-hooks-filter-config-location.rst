2. Configuration for filters in the Hooks Extension Framework
=============================================================

Status
------

Accepted


Context
-------

Context taken from the Discuss thread `Configuration for the Hooks Extension Framework <https://discuss.openedx.org/t/configuration-for-the-hooks-extension-framework/4527>`_

We need a way to configure a list of functions (filters) that will be called at
different places (hooks) in the code of edx-platform.

So, for a string like:

"org.openedx.lms.auth_user.filter.before_creation.v1"

We need to define a list of functions:

.. code-block:: python

    [
        "from_a_plugin.filters.filter_1",
        "from_a_plugin.filters.filter_n",
        "from_some_other_package.filters.filter_1",
        # ... and so.
    ]


We have considered two alternatives:

* A dict in the Django settings.
    * Advantages:
        * It is very standard, everyone should know how to change it by now.
        * Can be altered without installing plugins.
    * Disadvantages:
        * It is hard to document a large dict.
        * Could grow into something difficult to manage.

* In a view of the AppConfig of your plugin.
    * Advantages:
        * Each plugin can extend the config to add its own filters without
          collisions.
    * Disadvantages:
        * It’s not possible to control the ordering of different filters being
          connected to the same trigger by different plugins.
        * For updates, an operator must install a new version of the dependency
          which usually is longer and more difficult than changing vars and
          restart.
        * Not easy to configure by tenant if you use site configs.
        * Requires a plugin.

Decision
--------

We decided to use a dictionary in Django settings using one of these three
formats:

**Option 1**: this is the more detailed option and from it, the others can be
derived. This configuration is very explicit. It contains the list of functions
for the pipeline and any other optional setting for a filter.


.. code-block:: python

    OPEN_EDX_FILTERS_CONFIG = {
        "org.openedx.lms.auth_user.filter.before_creation.v1": {
            "pipeline": [
                "from_a_plugin.filters.filter_1",
                "from_a_plugin.filters.filter_n",
                "from_some_other_package.filters.filter_1",
            ],
            "other_options": "go here",
        }
    }

**Option 2**: this option only considers the configuration of the list of
functions to be run by the pipeline.

.. code-block:: python

    OPEN_EDX_FILTERS_CONFIG = {
        "org.openedx.lms.auth_user.filter.before_creation.v1": {
            [
                "from_a_plugin.filters.filter_1",
                "from_a_plugin.filters.filter_n",
                "from_some_other_package.filters.filter_1",
            ],
        }
    }

**Option 3**: this option considers that there's just one function to be run.

.. code-block:: python

    OPEN_EDX_FILTERS_CONFIG = {
        "org.openedx.lms.auth_user.filter.before_creation.v1": "from_a_plugin.filters.filter_1",
    }


Consequences
------------

1. Open edX plugins will need to use the settings entry point to add a function
to a filter hook.

2. Given that Site Configurations is not available in this repository, it can't
be used to configure hooks.
