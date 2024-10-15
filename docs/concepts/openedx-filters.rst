Open edX Filters
================

Overview
--------

In the context of Open edX, filters provide a mechanism for modifying the platform's behavior by altering runtime data or halting execution based on specific conditions. Filters allow developers to implement application flow control based on their business logic or requirements without directly modifying the application code.

What are Open edX Filters?
--------------------------

An Open edX Filter is a pipeline mechanism that executes a series of functions specified in a configuration setting. Each function can modify the input data or halt execution, altering the application's behavior during runtime. Filters are defined using the ``OpenEdxFilter`` class, which provides a structured way to define the filter function and the parameters it should receive.

Why are Open edX Filters important?
-----------------------------------

Open edX Filters are a key component of the Hooks Extension Framework. Filters allow developers to implement their own functions to alter the platform's functionality without directly modifying the core codebase, saving time, effort, and decreasing maintainability costs. This enables a wide range of use cases, from modifying the behavior of existing components to dynamically adding new functionality to the platform.

How are Open edX Filters used?
------------------------------

Developers can implement pipeline functions that take a set of arguments and return a modified set to the caller or raise exceptions during processing. In these functions, developers can implement business logic or requirements that modify the application's behavior based on specific conditions. These pipeline functions are configured by using the ``OPEN_EDX_FILTERS_CONFIG`` setting in the Django settings file. This setting allows developers to specify the functions that should run when invoking a specific filter.

For more information on how to use Open edX Filters, refer to the `Using Open edX Filters`_ how-to guide.

How do Open edX Filters work?
-----------------------------

Open edX Filters are implemented using an accumulative pipeline mechanism, which executes a series of functions in a specific order. Each function in the pipeline receives the output of the previous function as input, allowing developers to build complex processing logic by chaining multiple functions together. The pipeline ensures that the order of execution is maintained and that the result of a previous function is available to the current one in the form of a pipeline.

The lifecycle of an Open edX Filter can be summarized as follows:

1. A service invokes calls a filter by invoking ``run_filter()`` method with the initial arguments.
2. The filter's tooling gets the pipeline functions to execute from the filter configuration ``OPEN_EDX_FILTERS_CONFIG``.
3. The tooling executes the functions in a specific order, passing the output of the previous function as input to the next one.
4. Each function in the pipeline can modify the input data or halt execution based on specific conditions.
5. The filter returns the final output of the pipeline to the caller to be used by the rest of the process.
6. The filter is considered complete once all functions in the pipeline have executed.

Here is an example of how that might look like with an existing filter:

1. A user enrolls in a course, `triggering the CourseEnrollmentStarted filter`_. This filter includes information about the user, course, and enrollment details.
2. The filter tooling executes a series of functions in a specific order, such as checking if the user is eligible for enrollment, updating the user's enrollment status, and sending a notification to the user.
3. Each function in the pipeline can modify the input data or halt execution based on specific conditions, such as denying enrollment if the user is not eligible.
4. The filter returns the final output of the pipeline to the caller, which may include updated enrollment details or a raising an exception if the user is not eligible.
5. The filter is considered complete once all functions in the pipeline have executed.

.. _Using Open edX Filters: ../how-tos/using-filters.html
.. _Hooks Extension Framework: https://open-edx-proposals.readthedocs.io/en/latest/oep-0050-hooks-extension-framework.html
.. _Django Signals Documentation: https://docs.djangoproject.com/en/4.2/topics/signals/
.. _triggering the CourseEnrollmentStarted filter: https://github.com/openedx/edx-platform/blob/master/common/djangoapps/student/models/course_enrollment.py#L719-L724
