Open edX Filters Glossary
##########################

A filter has multiple components that are used to define, execute and handle filters, such as pipeline, pipeline steps, filter definition, filter signature, filter type, filter exceptions, filter configuration, etc.  This glossary provides definitions for some of the terms to ease the adoption of the Open edX Filters library.

.. glossary::

   Pipeline
     A pipeline is a list of functions executed in a specific order; these functions are known as pipeline steps. Each function in the pipeline takes the output of the previous function as its input, with the final function's output serving as the overall output of the filter. The pipeline behavior was inspired by the `Python Social Auth accumulative pipeline`_, which is described in detail in the :doc:`/decisions/0003-hooks-filter-tooling-pipeline` ADR. These pipelines are configured in the filter configuration and are executed in sequence.

   Pipeline Step
     A pipeline step is a function within a pipeline that receives, processes, and returns data. Each step may perform operations like transforming, validating, filtering, or enriching data. Pipeline steps are implemented as classes that inherit from the base class `PipelineStep`_ and define specific logic within their `run_filter`_ method, which is executed by the pipeline tooling when the filter is triggered.

   Filter Definition
     A filter definition is a class that inherits from `OpenEdxPublicFilter`_ that implements the ``run_filter`` method which defines the input and output behavior of the filter. This class executes the configured pipeline steps by calling the method `run_pipeline`_, passing down the input arguments, handling exceptions and returning the final output of the filter. Since the ``run_filter`` method is the entry point for the filter, the pipeline steps must have the same signature as the filter definition.

   Filter Signature
     The filter signature consists of the specific parameters required by a filter's ``run_filter`` method. It defines the expected input and output structure for the filter, specifying the data the filter will process. The filter signature is used to ensure that all pipeline steps have the same input and output structure, enabling interchangeability between steps.

   Filter Type
     The filter type is a unique identifier for the filter, following a standardized format following the :doc:`/decisions/0004-filters-naming-and-versioning`. This type is used as an index for configuring the filter pipeline and specifies which configuration settings apply to a given filter.

   Filter Exceptions
     Filters can raise exceptions to control the flow of the pipeline. If a filter raises an exception, the pipeline halts, and the exception becomes the pipeline's output. Exceptions are typically raised when certain conditions specified in the filter's logic are met, allowing the filter to control the application flow.

   Filter Configuration
     Filter configuration is a dictionary that defines the pipeline settings for a filter. Each filter type has its own configuration, which includes settings like whether errors should fail silently or propagate, and the sequence of pipeline steps. Configurations specify the filter type, error-handling preferences, and a list of module paths for each pipeline step to be executed.

This glossary provides a high-level overview of the key concepts and components of the Open edX Filters library. Understanding these terms will help you implement filters in your application and leverage the filter tooling to control the flow of your application based on specific conditions. For a better illustration of these concepts, refer to the :doc:`/how-tos/using-filters` guide.

.. _Python Social Auth accumulative pipeline: https://python-social-auth.readthedocs.io/en/latest/pipeline.html
.. _PipelineStep: https://github.com/openedx/openedx-filters/blob/main/openedx_filters/filters.py#L10
.. _run_filter: https://github.com/openedx/openedx-filters/blob/main/openedx_filters/filters.py#L60
.. _OpenEdxPublicFilter: https://github.com/openedx/openedx-filters/blob/main/openedx_filters/tooling.py#L14
.. _run_pipeline: https://github.com/openedx/openedx-filters/blob/main/openedx_filters/tooling.py#L164
