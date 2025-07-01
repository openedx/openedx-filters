.. _Filter Configuration:

Filter Configurations
#####################

The :term:`filter configuration` is a dictionary used to configure the pipeline steps for a particular filter. The configuration settings are specific for each :term:`filter type`. The following table shows the three valid configuration formats:

Configuration Formats
*********************

+-----------------------------------+-------------------------------+-----------------------------------+------------------------+
| **Option**                        | **Format**                    | **fail_silently**                 | **Additional Options** |
+===================================+===============================+===================================+========================+
| **Full Dictionary Configuration** | Dictionary with pipeline list | Configurable (``True``/``False``) | Allowed                |
+-----------------------------------+-------------------------------+-----------------------------------+------------------------+
| **Pipeline List Configuration**   | List of pipeline steps        | Always ``True``                   | Not allowed            |
+-----------------------------------+-------------------------------+-----------------------------------+------------------------+
| **Single Step Configuration**     | Single pipeline step string   | Always ``True``                   | Not allowed            |
+-----------------------------------+-------------------------------+-----------------------------------+------------------------+

Detailed Examples
*****************

Full Dictionary Configuration
=============================

This is the most detailed option and from it, the others can be derived. This configuration is very explicit. It contains the list of functions for the pipeline and any other optional setting for a filter.

.. code-block:: python

    OPEN_EDX_FILTERS_CONFIG = {
        "<filter_type>": {  # Replace with the specific filter type
            "fail_silently": True,  # Set to True to ignore exceptions and continue the pipeline
            "pipeline": [
                "module.path.PipelineStep0",  # Replace with the actual module path and class name
                "module.path.PipelineStep1",
                # Add more steps as needed
                "module.path.PipelineStepN",
            ],
            "other_option": "value1",
            "another_option": "value2",
            # Add other options as needed
        },
    }

**Configuration Elements:**

- ``<filter_type>`` is the :term:`filter type`.
- ``fail_silently`` is a boolean flag indicating whether the pipeline should continue executing the next steps when a runtime exception is raised by a pipeline step.

  - If ``True``, when a pipeline step raises a runtime exception (e.g., ``ImportError`` or ``AttributeError``) that the developer does not intentionally raise during the filter's execution, the exception will not be propagated, and the execution will resume, i.e., the next steps will be executed.
  - If ``False``, the exception will be propagated, and the execution will stop returning control to the caller.

- ``pipeline`` is a list of paths for each pipeline step. Each path is a string with the following format: ``module.path.PipelineStepClassName``. The module path is the path to the module where the pipeline step class was implemented and the class name is the name of the class that implements the ``run_filter`` method to be executed when the filter is triggered.
- ``other_option`` and ``another_option`` are placeholders for any other options that may be required by the pipeline steps.

**Exception Handling Example:**

.. code-block:: python

    OPEN_EDX_FILTERS_CONFIG = {
        "<filter_type>": {
            "fail_silently": True,
            "pipeline": [
                "non_existing_module.PipelineStep",
                "existing_module.NonExistingPipelineStep",
                "module.path.PipelineStep",
            ]
        },
    }

**Behavior:**

- The pipeline tooling will catch the ``ImportError`` exception raised by the first step and continue executing the next steps.
- The pipeline tooling will catch the ``AttributeError`` exception raised by the second step and continue executing the next steps.
- The pipeline tooling will execute the third step successfully and then return the result.

Pipeline List Configuration
===========================

This option only considers the configuration of the list of functions to be run by the pipeline. The ``fail_silently`` option is always set to ``True`` and no other additional options are allowed.

.. code-block:: python

    OPEN_EDX_FILTERS_CONFIG = {
        "<filter_type>": [
            "module.path.PipelineStep0",  # Replace with the actual module path and class name
            "module.path.PipelineStep1",
            # Add more steps as needed
            "module.path.PipelineStepN",
        ],
    }

**Configuration Elements:**

- ``<filter_type>`` is the :term:`filter type` and the value of this key is a list of paths for each pipeline step.

**Exception Handling Example:**

.. code-block:: python

    OPEN_EDX_FILTERS_CONFIG = {
        "<filter_type>": [
            "non_existing_module.PipelineStep",
            "existing_module.NonExistingPipelineStep",
            "module.path.PipelineStep",
        ],
    }

**Behavior:** The same behavior as for non-existent pipeline methods in **Full Dictionary Configuration** will be applied.

Single Step Configuration
=========================

This option considers that there's just one function to be run. The ``fail_silently`` option is always set to ``True`` and no other additional options are allowed.

.. code-block:: python

    OPEN_EDX_FILTERS_CONFIG = {
        "<filter_type>": "module.path.PipelineStep",
    }

**Configuration Elements:**

- ``<filter_type>`` is the :term:`filter type` and the value of this key is a path for the unique pipeline step.

**Exception Handling Examples:**

.. code-block:: python

    OPEN_EDX_FILTERS_CONFIG = {
        "<filter_type>": "non_existing_module.PipelineStep",
        # or
        "<filter_type>": "existing_module.NonExistingPipelineStep",
        # or
        "<filter_type>": "existing_module.PipelineStep",
    }

**Behavior:**

- The pipeline tooling will catch the ``ImportError`` exception raised by the first step and return control to the caller.
- The pipeline tooling will catch the ``AttributeError`` exception raised by the second step and return control to the caller.
- The pipeline tooling will execute the step successfully and return the result.

For more details on the configuration, see :ref:`ADR-2`.

**Maintenance chart**

+--------------+-------------------------------+----------------+--------------------------------+
| Review Date  | Reviewer                      |   Release      |Test situation                  |
+--------------+-------------------------------+----------------+--------------------------------+
|2025-02-13    | Maria Grimaldi                |  Sumac         |Pass.                           |
+--------------+-------------------------------+----------------+--------------------------------+
