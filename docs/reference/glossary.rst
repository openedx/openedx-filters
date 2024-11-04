Open edX Filters Glossary
##########################

A filter has multiple components that are used to define, execute and handle filters, such as pipeline, pipeline steps, filter definition, filter signature, filter type, filter exceptions, filter configuration, etc.  This glossary provides definitions for some of the terms to ease the adoption of the Open edX Filters library.

.. glossary::

   Pipeline
     A pipeline is a list of functions executed in a specific order; these functions are known as pipeline steps. Each function in the pipeline takes the output of the previous function as its input, with the final function's output serving as the overall output of the filter. These pipelines are configured in the filter configuration and are executed in sequence.

   Pipeline Step
     A pipeline step is a function within a pipeline that receives, processes, and returns data. Each step may perform operations like transforming, validating, filtering, or enriching data. Pipeline steps are implemented as classes that inherit from a base step class and define specific logic within their ``run_filter`` method, which conforms to the filter's signature.

   Filter Definition
     A filter definition is the class that defines the ``run_filter`` method for a filter, specifying the input and output behavior. This class, which inherits from a standard filter base, executes the configured pipeline steps, enabling custom processing within the defined filter.

   Filter Signature
     The filter signature consists of the specific parameters required by a filter's ``run_filter`` method. It defines the expected input and output structure for the filter, detailing the data the filter will process.

   Filter Type
     The filter type is a unique identifier for the filter, following a standardized format (e.g., reverse DNS style). This type is used as an index for configuring the filter pipeline and specifies which configuration settings apply to a given filter.

   Filter Exceptions
     Filters can raise exceptions to control the flow of the pipeline. If a filter raises an exception, the pipeline halts, and the exception becomes the pipeline's output. Exceptions are typically raised when certain conditions specified in the filter's logic are met, signaling an event or state change.

   Filter Configuration
     Filter configuration is a dictionary that defines the pipeline settings for a filter. Each filter type has its own configuration, which includes settings like whether errors should fail silently or propagate, and the sequence of pipeline steps. Configurations specify the filter type, error-handling preferences, and a list of module paths for each pipeline step to be executed.

.. note::
    In practice, "filter" is used to refer to the whole mechanism, including the pipeline steps, filter definition and so on.
