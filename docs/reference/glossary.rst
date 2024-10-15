Open edX Filters Glossary
##########################

This glossary provides definitions for some of the terms to ease the adoption of the Open edX Filters library.

Pipelines
---------

A pipeline is a list of functions that are executed in order. Each function receives the output of the previous function as input. The output of the last function is the output of the pipeline.

Pipeline steps
--------------

A pipeline step is a function that receives data, manipulates it and returns it. It can be used to transform data, to validate it, to filter it, to enrich it, etc.

Open edX Filter
---------------

An Open edX Filter is a Python class that inherits from `OpenEdXPublicFilter`, which is used for executing pipelines or list of functions in specific order. It implements a `run_filter` method that receives the data to be processed and returns the output of the pipeline.

Filter definition
-----------------

It's the class that implements the `run_filter` method, usually implemented in this repository for community use. It's invoked by services to execute configured pipeline steps.

Open edX Filter signature
-------------------------

It's the signature of the `run_filter` method of each filter. It defines the input and output of the filter. The input is a dictionary with the data to be processed and the output is a dictionary with the processed data.

Open edX Filters' pipeline steps
--------------------------------

In the context of Open edX Filters, a pipeline step is a class that inherits from ``PipelineStep`` that implements the `run_filter` method which must match the Open edX Filter signature.

Filter type
-----------

It's the filter identifier. It's used to identify the filter in the configuration settings. When configuring the pipeline for a filter, the type is as an index for the filter configuration.

Filter exceptions
-----------------

Besides acting as a filter, an Open edX Filter can also raise exceptions. These exceptions are used to control the execution of the pipeline. If an exception is raised, the pipeline execution is stopped and the exception is raised again as the output of the pipeline. These exceptions are intentionally raised by the developer during the filter's execution when a condition is met.

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
- ``fail_silently`` is a boolean value.

If ``fail_silently`` is ``True``: when a pipeline step raises a runtime exception -- like ``ImportError`` or ``AttributeError`` exceptions which are not intentionally raised by the developer during the filter's execution; the exception won't be propagated and the pipeline execution will resume, i.e the next steps will be executed
If ``fail_silently`` is ``False``: the exception will be propagated and the pipeline execution will stop.

For example, with this configuration:

.. code-block:: python

    OPEN_EDX_FILTERS_CONFIG = {
        "<FILTER EVENT TYPE>": {
            "fail_silently": True,
            "pipeline": [
                "non_existing_module.non_existing_function",
                "existing_module.function_raising_attribute_error",
                "existing_module.existing_function",
            ]
        },
    }

The pipeline tooling will catch the ``ImportError`` exception raised by the first step and the ``AttributeError`` exception raised by the second step, then continue and execute the third step. Now, if ``fail_silently`` is ``False``, the pipeline tooling will catch the ``ImportError`` exception raised by the first step and propagate it, i.e the pipeline execution will stop.

- ``pipeline`` is list of paths for each pipeline step. Each path is a string with the following format: ``<MODULE PATH>.<CLASS NAME>``. The module path is the path to the module where the pipeline step class is defined and the class name is the name of the class that implements the ``run_filter`` method to be executed.
