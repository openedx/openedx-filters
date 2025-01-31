Filter Configurations
#####################

The :term:`filter configuration` is a dictionary used to configure the pipeline steps for a particular filter. The configuration settings are specific for each :term:`filter type`. The dictionary looks like this:

.. code-block:: python

    OPEN_EDX_FILTERS_CONFIG = {
        "FILTER_TYPE": {  # Replace with the specific filter type
            "fail_silently": True,  # Set to True to ignore exceptions and continue the pipeline
            "pipeline": [
                "module.path.PipelineStep0",  # Replace with the actual module path and class name
                "module.path.PipelineStep1",
                # Add more steps as needed
                "module.path.PipelineStepN",
            ]
        },
    }

Where:

- ``FILTER_TYPE`` is the :term:`filter type`.
- ``fail_silently`` is a boolean flag indicating whether the pipeline should continue executing the next steps when a runtime exception is raised by a pipeline step.
   - If ``True``, when a pipeline step raises a runtime exception (e.g., ``ImportError`` or ``AttributeError``) which are not intentionally raised by the developer during the filter's execution; the exception won't be propagated and the execution will resume, i.e the next steps will be executed.
   - If ``False``, the exception will be propagated and the execution will stop returning control to the caller.
- ``pipeline`` is list of paths for each pipeline step. Each path is a string with the following format: ``module.path.PipelineStepClassName``. The module path is the path to the module where the pipeline step class was implemented and the class name is the name of the class that implements the ``run_filter`` method to be executed when the filter is triggered.

With this configuration:

.. code-block:: python

    OPEN_EDX_FILTERS_CONFIG = {
        "FILTER_TYPE": {
            "fail_silently": True,
            "pipeline": [
                "non_existing_module.PipelineStep",
                "existing_module.NonExistingPipelineStep",
                "module.path.PipelineStep",
            ]
        },
    }

Triggering the filter will behave as follows:

- The pipeline tooling will catch the ``ImportError`` exception raised by the first step and continue executing the next steps.
- The pipeline tooling will catch the ``AttributeError`` exception raised by the second step and continue executing the next steps.
- The pipeline tooling will execute the third step successfully and then return the result.

For more details on the configuration see :doc:`../decisions/0002-hooks-filter-config-location`.
