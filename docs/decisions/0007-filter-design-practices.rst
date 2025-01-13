7. Filters Design Practices
###########################

Status
------

Draft

Context
-------

It is important to follow standards to ensure that the filters are designed in a way that is easy to understand and maintain. This ADR aims to provide guidelines for designing Open edX Filters with long term maintainability in mind.

Decision
--------

These are the practices that we recommend reviewing and following when designing Open edX Filters and contributing them to the library. Consider this example of a filter that is triggered when a user requests a certificate, we will use this example to illustrate the practices:

.. code-block:: python

    class CertificateCreationRequested(OpenEdxPublicFilter):

        class PreventCertificateCreation(OpenEdxFilterException):
            """
            Custom class used to stop the certificate creation process.
            """

        @classmethod
        def run_filter(cls, user, course_key, mode, status, grade, generation_mode):

Design Clarity and Understanding
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- A filter should describe as accurately as possible what behavior intends to modify.
- A filter should have a clear and concise name that describes its purpose.
- Ensure that the triggering logic of the filter is consistent and narrow. It should only trigger when the conditions are met and cover all the cases that the filter should be applied with the minimum number of modifications.

Consider the example above, the filter name is ``CertificateCreationRequested`` which indicates that it is a filter that is triggered when the certificate creation is requested, providing a clear understanding of the filter behavior. Avoid using generic names such as ``Filter`` or ``Process`` that do not provide any context about the filter behavior.

The ``CertificateCreationRequested`` is triggered by `_generate_certificate_task`_ which handles all the cases that the filter should be applied avoiding unnecessary modifications.

Contextual Information
~~~~~~~~~~~~~~~~~~~~~~

- A filter should provide enough context in its arguments about the process that is modifying to be able to modify the intended behavior.
- A filter should provide enough context in its arguments to avoid runtime dependencies with the application.
- The arguments of the filter should be directly related to the responsibility of the filter.

Consider the filter example above, the filter provides the necessary context to understand the behavior that is being modified such as the user, course key, mode, status, grade, and generation mode. The arguments are directly related to the responsibility of the filter.

Flexibility and Customization
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- A filter should be flexible enough to allow the developer to customize the behavior of the application.

Error Handling
~~~~~~~~~~~~~~

- Ensure that the exceptions when using the filter are handled properly and that the filter does not break the application.
- The filter exceptions should correspond with the filter behavior. If the filter is not supposed to halt the application behavior in any case, then do not specify exceptions. If the filter is supposed to halt the application behavior in some cases, then specify the exceptions that the filter can raise with enough reason to understand why the filter is halting the application behavior.

Consider the example above, the filter specifies an exception that is raised when the certificate creation process is stopped, providing a clear understanding of the filter behavior when the exception is raised. This exception should be handled properly in the application to avoid runtime errors.

.. note:: The application should catch the exception and handle it properly by returning an error message to the user through API responses, UI messages, or logs depending on the application context and where the filter is being used. For reference, see how the exception is handled in the `Pull Request edx-platform#35407`_.

Type Safety
~~~~~~~~~~~

- A filter should annotate the type of the arguments that it receives, only when it doesn't create unnecessary dependencies with the application.

Consequences
------------

Following these practices will ensure that the filters are designed in a way that is easy to understand and maintain. Having these standards in place will also make the decision process easier when designing new filters.

.. _`_generate_certificate_task`: https://github.com/openedx/edx-platform/blob/master/lms/djangoapps/certificates/generation_handler.py#L116-L128
.. _`Pull Request edx-platform#35407`: https://github.com/openedx/edx-platform/pull/35407
