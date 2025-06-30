.. _Naming Suggestions:

Naming Suggestions for Open edX Filters
#######################################

When naming a new filter and contributing it back to this repository, consider the following suggestions:

- Use a name that is descriptive of the filter's purpose. For example, the filter associated with the course enrollment process is named ``CourseEnrollmentStarted`` because it is triggered when a course enrollment starts.
- Use a name that is unique within the framework.
- Match the name of the filter to its ``filter_type``. For example, if the ``filter_type`` is a ``org.openedx.learning.course.enrollment.started.v1`` filter, the name of the filter should be ``CourseEnrollmentStarted``. You can use the ``filter_type`` to determine the name of the filter. See :ref:`ADR-4` for more information.
- Avoid using ``Filter`` in the name of the filter. It is implied that the class is a filter, so there is no need to include it in the name.
- Try reviewing the names of :ref:`existing filters <Existing Filters>` to get an idea of how to name your filter.
