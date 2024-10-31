Django Plugins and Filters
##########################

Django plugins is one of the most valuable extension mechanisms for the Open edX platform. In this section, we will
guide you through the process of using filters inside your own plugin.


Use filters inside your plugin
******************************

Imagine you have your own registration plugin and you want to add a filter to it. The first thing you need to do is
adding ``openedx-filters`` to your requirements file. Then, you can import the registration filter and use it inside
your registration flow as it's used in the LMS registration flow. You can even add your own filters to your registration,
after implementing their definitions in your plugin.

Configure filters
*****************

Filters are configured in the ``OPEN_EDX_FILTERS_CONFIG`` dictionary which can be specified in your plugin's settings
file. The dictionary has the following structure:

.. code-block:: python

    OPEN_EDX_FILTERS_CONFIG = {
        "<FILTER EVENT TYPE>": {
            "fail_silently": <BOOLEAN>,
            "pipeline": [
                "<STEP NAME 0>",
                "<STEP NAME 1>",
                ...
                "<STEP NAME N-1>",
            ]
        },
    }


Create pipeline steps
*********************

In your own plugin, you can create your own `:term: pipeline steps<Pipeline Steps>` by inheriting from ``PipelineStep`` and implementing the
``run_filter`` method. You can find examples of `:term: pipeline steps<Pipeline Steps>` in the ``openedx-filters-samples`` repository. See :doc:`/quickstarts/index` for more details.
