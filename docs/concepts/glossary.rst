Open edX filters glossary
##########################

This glossary provides definitions for some of the concepts needed to use the Open edX Filters library.


Pipelines
---------

A pipeline is a list of functions that are executed in order. Each function receives the output of the previous function as input. The output of the last function is the output of the pipeline.

Pipeline steps
--------------

A pipeline step is a function that receives data, manipulates it and returns it. It can be used to transform data, to validate it, to filter it, to enrich it, etc.

Open edX Filter
---------------

An Open edX Filter is a Python class used for executing pipelines or list of functions in specific order. It implements a `run_filter` method that receives the data to be processed and returns the output of the pipeline.

Filter signature
----------------

It's the signature of the `run_filter` method. It defines the input and output of the filter. The input is a dictionary with the data to be processed. The output is a dictionary with the processed data.

Filter type
-----------

It's the filter identifier. It's used to identify the filter in the configuration settings. When configuring the pipeline for a filter, the type is as an index for the filter configuration.

Filter exceptions
-----------------

Besides acting as a filter, an Open edX Filter can also raise exceptions. These exceptions are used to control the execution of the pipeline. If an exception is raised, the pipeline execution is stopped and the exception is raised again as the output of the pipeline.

Filter configuration
--------------------

The filter configuration is a dictionary with the configuration settings for the filter. It's used to configure the pipeline for a filter. The configuration settings are specific for each filter type. The dictionary looks like this:

.. code-block:: python

    OPEN_EDX_FILTERS_CONFIG = {
        "<FILTER EVENT TYPE>": {
            "fail_silently": <BOOLEAN>,
            "pipeline": [
                "<STEP MODULE PATH 0>",
                "<STEP MODULE PATH 1>",
                ...
                "<STEP MODULE PATH N-1>",
            ]
        },
    }

Where:

- ``<FILTER EVENT TYPE>`` is the filter type.
- ``fail_silently`` is a boolean value. If ``True``, the method ``run_pipeline`` won't raise runtime exceptions, and the pipeline execution will resume if one is raised. If ``False``, it will raise runtime exceptions and the pipeline execution will stop. By runtime exceptions we mean exceptions like ``ImportError`` or ``AttributeError``, which are not raised by the filter itself.
- ``pipeline`` is list of paths for each pipeline step.
