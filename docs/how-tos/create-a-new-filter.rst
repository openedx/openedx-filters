Create a New Open edX Filter with Long-Term Support
####################################################

Open edX Filters are supported and maintained by the Open edX community. This mechanism is designed to be extensible and flexible to allow developers to create new filters to implement custom behavior in the application. This guide describes how to create a new Open edX filter with long-term support by following the practices outlined in the :doc:`../decisions/0007-filter-design-practices` ADR.

Filters design with long-support follow closely the practices described in the ADR to minimize breaking changes, maximize compatibility and support for future versions of Open edX.

.. note:: Before starting, ensure you've reviewed the documentation on :doc:`docs.openedx.org:developers/concepts/hooks_extension_framework`, this documentation helps you decide if creating a new filter is necessary. You should also review the documentation on :doc:`../decisions/0007-filter-design-practices` to understand the practices that should be followed when creating a new filter.

Throughout this guide, we will use an example of creating a new filter that will be triggered when a user enrolls in a course from the course about page to better illustrate the steps involved in creating a new filter.

Key Outlines from Filter Design Practices
-----------------------------------------

- Clearly describe the behavior the filter modifies.
- Use concise names that reflect the filter's purpose.
- Ensure consistent and narrow triggering logic.
- Provide sufficient context in arguments to modify intended behavior.
- Avoid runtime dependencies by including relevant context in arguments.
- Keep arguments closely tied to the filter's responsibility.
- Allow flexibility for developers to customize behavior.
- Handle exceptions properly to halt the application behavior when needed without breaking the application.
- Align exceptions with filter behavior and specify when halting is needed.
- Annotate the argument types for clarity and safety.

Assumptions
-----------

- You have a development environment set up using `Tutor`_.
- You have a basic understanding of Python and Django.
- You understand the concept of filters or have reviewed the relevant :doc:`/concepts/index` docs.
- You are familiar with the terminology used in the project, such as the terms :term:`Filter Type`. If not, you can review the :doc:`../reference/glossary` docs.
- You have reviewed the :doc:`../decisions/0007-filter-design-practices` ADR.
- You have identified that you need to create a new filter and have a use case for the filter.

Steps
-----

To create a new Open edX Filter with long-term support, follow these steps:

Step 1: Propose the Use Case to the Community
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Before contributing a new filter, it is important to propose the filter to the community to get feedback on the filter's design and use case. For instance, you could create a post in Open edX Discuss Forum or create a new issue in the repository's issue tracker describing your use case for the new filter. Here is an example of community members that have taken this step:

- `Add Extensibility Mechanism to IDV to Enable Integration of New IDV Vendor Persona`_

.. note:: If your use case is too specific to your organization, you can implement them in your own library and use it within your services by adopting an organization-scoped approach. However, if you think that your use case could be beneficial to the community, you should propose it to the community for feedback and collaboration.

In our example our use case proposal could be:

   I want to add a filter that will be triggered when a user enrolls in a course from the course about page. This filter will be used to prfilter users from enrolling in a course if they do not meet the eligibility criteria. The filter will be triggered when the user clicks the enroll button on the course about page and will check if the user meets the eligibility criteria. If the user does not meet the criteria, the filter will raise an exception to prfilter the user from enrolling in the course.

If you are confident that the filter is beneficial to the community, you can proceed to the next steps and implement the filter.

Step 2: Place Your Filter in an Architecture Subdomain
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To implement the new filter in the library, you should understand the purpose of the filter and where it fits in the Open edX main architecture subdomains. This will help you place the filter in the right architecture subdomain and ensure that the filter is consistent with the framework's definitions. Fore more details on the Open edX Architectural Subdomains, refer to the :doc:`../reference/architecture-subdomains`.

In our example, the filter is related to the enrollment process, which is part of the ``learning`` subdomain. Therefore, the filter should be placed in the ``/learning`` module in the library. The subdomain is also used as part of the :term:`filter type <Filter Type>`, which is used to identify the filter. The filter type should be unique and follow the naming convention for filter types specified in the :doc:`../decisions/0004-filters-naming-and-versioning` ADR.

For the enrollment filter, the filter type could be ``org.openedx.learning.course.enrollment.v1``, where ``learning`` is the subdomain.

.. note:: If you don't find a suitable subdomain for your filter, you can propose a new subdomain to the community. However, new subdomains may require some discussion with the community. So we encourage you to start the conversation as soon as possible through any of the communication channels available.

Step 3: Identify the Triggering Logic
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The triggering logic for the filter should be identified to ensure that the filter is triggered in the right places and that the filter is triggered consistently. We should identify the triggering logic to ensure that maximum coverage is achieved with minimal modifications. The goal is to focus on core, critical areas where the logic we want to modify executes, ensuring the filter is triggered consistently.

In our example, the triggering logic could be a place where all enrollment logic goes through. This could be the ``enroll`` method in the enrollment model in the LMS, which is called when a user enrolls in a course in all cases.

.. note:: When designing an filter take into account the support over time of the service and triggering logic. If the service is likely to change or be deprecated, consider the implications of implementing the filter in that service.

.. note:: It is helpful to inspect the triggering logic to review the data that is available at the time the filter is triggered. This will help you determine the arguments of the filter and how the filter can modify the behavior.

Step 4: Determine the Arguments of the Filter
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Filter arguments are in-memory objects that can be manipulated and returned to the calling process to change a component's behavior. This is why they depend heavily on the specific behavior you want to modify and the information available at that point in the application flow. It's helpful to ask yourself:

- How can this be modified?
- What can I add or change to adjust the behavior?
- Think about the use cases you aim to address.

Our goal is to provide developers with enough control to implement new features while reducing dependencies on the service where the filter is being implemented. However, in some cases, dependencies might be unavoidable, depending on the use case.

As a rule of thumb, start by passing the most relevant context data from the application flow, and then gradually add more details as you analyze the behavior of the triggering logic.

.. note:: Consider the criticality of the arguments, could they be removed in the near future? This would mean introducing breaking changes to the filter.

In our example, the filter arguments could include the user, course key, and enrollment mode. These arguments are essential for the filter to determine if the user meets the eligibility criteria for enrollment and it is the minimum information required to make the decision (user to check the eligibility, course key to identify the course, and mode to determine the type of enrollment).

Step 5: Implement the Filter Definition
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Implement the :term:`filter definition` by creating a new class that inherits from the `OpenEdxPublicFilter`_ class. The filter definition should implement the ``run_filter`` method, which defines the input and output behavior of the filter. The ``run_filter`` method should call the method `run_pipeline`_, passing down the input arguments and returning the final output of the filter. This class should be placed in the appropriate subdomain module in the library, in the ``filters.py`` file.

.. note:: The input arguments of the ``run_filter`` method should match the arguments that the triggering logic provides. The output of the filter should be consistent with the behavior that the filter intends to modify. Usually, the output is the modified data or the original data if no modifications are needed.

.. note:: Try using type hints to annotate the arguments and return types of the ``run_filter`` method to provide clarity and safety.

You can add custom exceptions to the filter to handle specific cases where the filter should halt the application behavior. This will help developers understand when the filter is supposed to halt the application behavior and why. Try not to raise exceptions that are not related to the filter behavior, as this could lead to confusion and unexpected behavior. Only add exceptions if you can justify why the filter should halt the application behavior in that case.

In our example, the filter definition could be implemented as follows:

.. code-block:: python

    class CourseEnrollmentStarted(OpenEdxPublicFilter):
        """
        Custom class used to create enrollment filters and its custom methods.
        """

        filter_type = "org.openedx.learning.course.enrollment.started.v1"

        class PreventEnrollment(OpenEdxFilterException):
            """
            Custom class used to stop the enrollment process.
            """

        @classmethod
        def run_filter(cls, user, course_key, mode):
            """
            Execute a filter with the signature specified.

            Arguments:
                user (User): is a Django User object.
                course_key (CourseKey): course key associated with the enrollment.
                mode (str): is a string specifying what kind of enrollment.
            """
            data = super().run_pipeline(
                user=user, course_key=course_key, mode=mode,
            )
            return data.get("user"), data.get("course_key"), data.get("mode")

- The ``filter_type`` attribute should be set to the filter type that was identified in the previous steps. This attribute is used to identify the filter in the :term:`filter configuration`.
- The ``PreventEnrollment`` class is a custom exception that is raised when the filter should halt the application behavior.
- The ``run_filter`` method is the main method of the filter that is called when the filter is triggered. The method should call the ``run_pipeline`` method, passing down the input arguments and returning the final output of the filter.

Step 6: Trigger the Filter in the Application
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

After implementing the filter definition, you should trigger the filter in the application where the triggering logic is executed. This will ensure that the filter is triggered when the conditions are met and that the filter is modifying the behavior as intended.

In our example, we identified that the triggering logic is the ``enroll`` method in the enrollment model in the LMS. Therefore, we should trigger the filter in the ``enroll`` method, passing down the user, course key, and mode arguments to the filter. The filter should be placed so that it is triggered before the enrollment process is completed, so can alter the enrollment process if the user does not meet the eligibility criteria.

.. note:: Try placing the filter so it can be triggered before the process is completed, so it can alter the process if needed. In some cases, this would be at the beginning of the process, while in others it would be elsewhere.

Step 7: Implement Your Pipeline Steps
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Filters can be configured with pipeline steps to modify the behavior of the code where the filter is triggered. This allows you to define a sequence of steps that are executed in a specific order to modify the behavior of the application.

.. TODO: Add a link to the pipeline steps documentation.

Step 8: Test the Filter
~~~~~~~~~~~~~~~~~~~~~~~

After triggering the filter in the application, you should test the filter to ensure that it is triggered when the conditions are met and that the filter is modifying the behavior as intended. You should test the filter with different scenarios to ensure that the filter is working as expected and that the filter is not breaking the application by adding tests in the service where the filter is being implemented. Also, test the filter signature by adding unit tests to the library to ensure that the arguments are being passed correctly and that the output is consistent with the behavior that the filter intends to modify.

In the service tests you should include at least the following scenarios:

- The filter is triggered when the triggering logic is executed.
- The filter when executed with the correct arguments returns the expected output.
- When there are pipeline steps configured, the filter executes the pipeline steps.
- When no pipeline steps are configured, the filter acts as a no-op.
- The filter does not break the application when raising exceptions.

You can test the filter by configuring a dummy :term:`Pipeline Step` only for testing purposes. This will allow you to test the filter in isolation and ensure that the filter is working as expected. You can also test the filter in the application by triggering the filter with different scenarios to ensure that the filter is working as expected. In the `test_filters.py`_ you can review how this is done for the enrollment filter.

Step 9: Continue the Contribution Process
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

After implementing the filter, you should continue the contribution process by creating a pull request in the repository. The pull requests should contain the changes you made to implement the filter, including the filter definition, data attrs, and the places where the filter is triggered.

For more details on how the contribution flow works, refer to the :doc:`docs.openedx.org:developers/concepts/hooks_extension_framework` documentation.

.. _Tutor: https://docs.tutor.edly.io/
.. _Add Extensibility Mechanism to IDV to Enable Integration of New IDV Vendor Persona: https://openedx.atlassian.net/wiki/spaces/OEPM/pages/4307386369/Proposal+Add+Extensibility+Mechanisms+to+IDV+to+Enable+Integration+of+New+IDV+Vendor+Persona
.. _OpenEdxPublicFilter: https://github.com/openedx/openedx-filters/blob/main/openedx_filters/tooling.py#L14
.. _run_pipeline: https://github.com/openedx/openedx-filters/blob/main/openedx_filters/tooling.py#L164
.. _test_filters.py: https://github.com/openedx/edx-platform/blob/master/common/djangoapps/student/tests/test_filters.py#L114-L190
