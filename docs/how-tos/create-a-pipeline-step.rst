.. include:: ../common_refs.rst

Create a Pipeline Step
######################

When a filter is triggered in the Open edX platform, the pipeline tooling executes a series of pipeline steps in a specific order. Each pipeline step processes data and returns the output to the next step in the pipeline which can be used to modify the application's behavior. This guide explains how to create a pipeline step for a filter in the Open edX platform.

Throughout this guide, we will implement the use case of allowing users to enroll in a course only if they have a valid email address. We will create a pipeline step that checks if the user's email address is valid and raise an exception if it is not.

Assumptions
-----------

- You have a development environment set up using `Tutor`_.
- You have a basic understanding of Python and Django.
- You understand the concept of filters or have reviewed the relevant :doc:`/concepts/index` docs.
- You are familiar with the terminology used in the project, such as the terms :term:`Filter Type`. If not, you can review the :doc:`../reference/glossary` docs.
- You have reviewed the :doc:`../decisions/0007-filter-design-practices` ADR.
- You understand the use case for the filter and the specific logic you want to implement in the pipeline step.

Steps
-----

To create a pipeline step for a filter in the Open edX platform, follow these steps:

Step 1: Understand your Use Case and Identify the Filter to Use
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Before creating a pipeline step, you should understand your use case for the filter and the specific logic you want to implement in the pipeline step. In our example, we want to prevent users from enrolling in a course if they do not have a valid email address. We will create a pipeline step that checks if the user's email address is valid and raise an exception if it is not.

You should review the :doc:`list of filters <../reference/filters>` available in the Open edX platform and identify the filter that best fits your use case. In our example, we will use the |CourseEnrollmentStarted| filter to implement the logic for our use case. You should review the filter's arguments to understand the data that will be passed to the pipeline step and the expected output. This will help you define the pipeline step's logic and signature.

Step 2: Install Open edX Filters
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

First, add the ``openedx-filters`` library into your dependencies so the environment recognizes the filter you want to use. You can install ``openedx-filters`` by running:

.. code-block:: bash

   pip install openedx-filters

This will mainly make the filters available for your CI/CD pipeline and local development environment. If you are using the Open edX platform, the library should be already be installed in the environment so no need to install it.

Step 3: Create a Pipeline Step
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A :term:`pipeline step` is a class that inherits from the base class |PipelineStep| and defines specific logic within its |PipelineStep.run_filter| method. The ``run_filter`` method is executed by the pipeline tooling when the filter is triggered. To create a pipeline step, you should:

1. Create a new Python module for the pipeline step called ``pipeline.py``. Pipeline steps are usually implemented in a `Open edX Django plugins`_, so you should create the module in the plugin's directory.
2. Create a new class for the pipeline step that inherits from the base class |PipelineStep|.
3. Implement the logic for the pipeline step within the |PipelineStep.run_filter| method. The method signature should match the filter's signature to ensure compatibility with the pipeline tooling. In our example, the method should accept the user, course key, and enrollment mode as arguments and return the same arguments if the email address is valid. If the email address is not valid, the method should raise an exception.
4. You can take an iterative approach to developing the pipeline step by testing it locally and making changes as needed.

In our example, the pipeline step could look like this:

.. code-block:: python

   from openedx_filters.filters import PipelineStep

   # Location my_plugin/pipeline.py
   class CheckValidEmailPipelineStep(PipelineStep):
       def run_filter(self, user, course_key, mode):
           if self.not is_user_email_allowed(user.email):
               log.debug("User %s does not have a valid email address, stopping enrollment", user.email)
               raise CourseEnrollmentStarted.PreventEnrollment("User does not have a valid email address")
           log.debug("User has a valid email address, allowing enrollment")
           return {
               "user": user,
               "course_key": course_key,
               "mode": mode,
            }

- In this example, we create a new class called ``CheckValidEmailPipelineStep`` that inherits from the base class |PipelineStep|.
- We implement the logic for the pipeline step within the |PipelineStep.run_filter| method. The method checks if the user's email address is valid using the ``is_user_email_allowed`` method and raises an exception if it is not. If the email address is valid, the method returns the user, course key, and enrollment mode in a dictionary.
- The method signature matches the filter's signature, accepting the user, course key, and enrollment mode as arguments and returning the same arguments if the email address is valid. You can also return an empty dictionary if you don't need to modify the data.

Consider the following when creating a pipeline step:

- Limit each step to a single responsibility to make the code easier to maintain and test.
- Keep the pipeline step logic simple and focused on the specific task it needs to perform.
- Consider the performance implications of the pipeline step and avoid adding unnecessary complexity or overhead, considering the pipeline will be executed each time the filter is triggered.
- Implement error handling and logging in the pipeline step to handle exceptions and provide useful information for debugging, considering both development and production environments. E.g., when the email is not valid, we raise an exception to prevent the user from enrolling in the course. Logging relevant information when an exception is raised can help identify the root cause of a problem.

Step 4: Configure the Pipeline for the Filter
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

After creating the pipeline step, you need to configure the pipeline for the filter in the :term:`filter configuration`. The configuration settings are specific for each :term:`filter type` and define the pipeline steps to be executed when the filter is triggered. You should add the path to the pipeline step class in the filter's pipeline configuration.

In our example, we will configure the pipeline for the |CourseEnrollmentStarted| filter to include the pipeline step we created. The configuration should look like this:

.. code-block:: python

   OPEN_EDX_FILTERS_CONFIG = {
       "org.openedx.learning.course.enrollment.started.v1": {
           "fail_silently": False,
           "pipeline": [
               "my_plugin.pipeline.CheckValidEmailPipelineStep",
           ]
       },
   }

Step 5: Test the Pipeline Step
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

After creating the pipeline step and configuring the pipeline for the filter, you should test the pipeline step to ensure it works as expected. You can trigger the filter in your development environment and verify that the pipeline step is executed correctly. You should test different scenarios, including valid and invalid email addresses, to ensure the pipeline step behaves as expected.

You should also implement unit tests for the pipeline step to verify its functionality and handle edge cases. Unit tests can help you identify issues early in the development process and ensure the pipeline step works as intended. To implement the unit test you can directly call the ``run_filter`` method of the filter definition and assert that the pipeline step behaves as expected. Or you can directly call the pipeline step class and assert that the method returns the expected output.

In our example, you could write a unit test for the pipeline step like this:

.. code-block:: python

    # Location my_plugin/tests/test_pipeline.py
    @override_settings(
        OPEN_EDX_FILTERS_CONFIG={
            "org.openedx.learning.course.enrollment.started.v1": {
                "fail_silently": False,
                "pipeline": [
                    "my_plugin.pipeline.CheckValidEmailPipelineStep",
                ]
            }
        }
    )
    def test_stop_enrollment_invalid_email(self):
        user = UserFactory(email="invalid_email")
        with self.assertRaises(CourseEnrollmentStarted.PreventEnrollment):
            CourseEnrollmentStarted.run_filter(
                user=user, course_key=self.course_key, mode="audit",
            )

Step 6: Debug and Iterate
~~~~~~~~~~~~~~~~~~~~~~~~~

After testing the pipeline step, you should debug and iterate on the implementation as needed. Consider the following when debugging and iterating on the pipeline step:

- Review the logs and error messages to identify the root cause of any issues and determine the appropriate action to resolve them.
- Use the development environment to test the pipeline step in different scenarios and verify that it behaves as expected. Try using ``fail_silently: False`` in the filter configuration to see the error messages in the logs.
- Implement a fallback mechanism in the pipeline step to handle unexpected scenarios and prevent the filter from failing silently. You can log debug messages to provide useful information for debugging.
- Implement unit tests for the pipeline step to verify its functionality and handle edge cases. Make incremental changes to the pipeline step and test each change to ensure it works as intended.
- In unit tests, mock external dependencies as closely as possible to the real environment to ensure the pipeline step behaves as expected in different scenarios, since sometimes using real data can lead to unexpected results.
- In production environments, monitor the pipeline step's performance and behavior to identify any issues and optimize the implementation as needed.

.. note:: The default behavior of the pipeline tooling is to fail silently if a runtime exception is raised in a pipeline step. You can configure the filter to raise an exception when the pipeline step fails by setting ``fail_silently: False`` in the filter configuration. This will help you identify issues early and take appropriate action to resolve them. :term:`Filter Exceptions` will always be raised in the pipeline and will halt the execution of the pipeline. You can use exceptions to control the flow of the pipeline and handle specific scenarios in the pipeline step. In our example, we raise an exception when the user's email address is not valid to prevent them from enrolling in the course. The exceptions considered by the ``fail_silently`` flag are runtime exceptions that are not intentionally raised by the developer during the filter's execution, use the configuration as you see fit.

.. _Open edX Django plugins: https://docs.openedx.org/en/latest/developers/concepts/platform_overview.html#new-plugin
