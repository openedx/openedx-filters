How-to Create a new Filter
##########################

.. How-tos should have a short introduction sentence that captures the user's goal and introduces the steps.

The mechanisms implemented by the Open edX Filters library are supported and maintained by the Open edX community. The
library is designed to be extensible, and we welcome contributions of new filters.

Therefore, we've put together this guide that will walk you through the process of adding a new filter to the library,
and will provide you with a template to follow when adding new filters.

Assumptions
***********

.. This section should contain a bulleted list of assumptions you have of the
   person who is following the How-to.  The assumptions may link to other
   how-tos if possible.

* You have a development environment set up.
* You have a basic understanding of Python and Django.
* You understand the concept of filters or have reviewed the relevant
  :doc:`/concepts/index` docs.
* You are familiar with the terminology used in the project, such as
  :term:`filter type<Filter Type>`, :term:`filter signature<Filter Signature>`, etc. If not, you can review the :doc:`/reference/glossary` docs.

Steps
*****

.. A task should have 3 - 7 steps.  Tasks with more should be broken down into digestible chunks.

#. Propose a new filter to the Open edX community

    When creating a new filter, you must justify its implementation. For example, you could create a post in Discuss,
    send a message through slack or open a new issue in the library repository listing your use cases for it. Or even,
    if you have time, you could accompany your proposal with the implementation of the filter to illustrate its behavior.

#. Place your filter in an architecture subdomain

    As specified in the Architectural Decisions Record (ADR) filter naming and versioning, the :term:`filter definition<Filter Definition>` needs an Open edX Architecture
    Subdomain for:

    - The :term:`type of the filter<Filter Type>`: ``{Reverse DNS}.{Architecture Subdomain}.{Subject}.{Action}.{Major Version}``
    - The package name where the definition will live, eg. ``learning/``.

    For those reasons, after studying your new filter purpose, you must place it in one of the subdomains already in use, or introduce a new subdomain:

    +-------------------+----------------------------------------------------------------------------------------------------+
    | Subdomain name    | Description                                                                                        |
    +===================+====================================================================================================+
    | Learning          | Allows learners to consume content and perform actions in a learning activity on the platform.     |
    +-------------------+----------------------------------------------------------------------------------------------------+

    New subdomains may require some discussion, because there does not yet exist and agreed upon set of subdomains. So we encourage you to start the conversation
    as soon as possible through any of the communication channels available.

    Refer to `edX DDD Bounded Contexts <https://openedx.atlassian.net/l/cp/vf8XjRiX>`_ confluence page for more documentation on domain-driven design in the Open edX project.

#. Define the filter's behavior

    Defining the filter's behavior includes:

    - Defining the :term:`filter type<Filter Type>` for identification
    - Defining the :term:`filter signature<Filter Signature>`
    - Defining the filter's behavior for stopping the process in which it is being used

    The :term:`filter type<Filter Type>` is the name that will be used to identify the filter's and it'd help others identifying its purpose. For example, if you're creating a filter that will be used during the student registration process in the LMS,
    according to the documentation, the :term:`filter type<Filter Type>` is defined as follows:

    ``{Reverse DNS}.{Architecture Subdomain}.student.registration.requested.{Major Version}``

    Where ``student`` is the subject and ``registration.requested`` the action being performed. The major version is the version of the filter, which will be incremented
    when a change is made to the filter that is not backwards compatible, as explained in the ADR.

    Now that you have the :term:`filter type<Filter Type>`, you'll need to define the :term:`filter signature<Filter Signature>` and overall behavior. The :term:`filter signature<Filter Signature>`, which is the set of parameters that the filter will manipulate, depends on where the filter is located. For example,
    if you're creating a filter that will be used during the student registration process in the LMS, the :term:`filter signature<Filter Signature>` will be the set of parameters available for that time for the user. In this case, the :term:`filter signature<Filter Signature>` will be the set of parameters that the registration form sends to the LMS.

    You can ask yourself the following questions to help you figure out your filter's parameters:

    - What is the filter's purpose? (e.g. to validate the student's email address)
    - What parameters will the filter need to to that? (e.g. the email address)
    - Where in the registration process will the filter be used? (e.g. after the student submits the registration form but before anything else)

    With that information, you can define the :term:`filter signature<Filter Signature>`:

    - Arguments: ``email``. Since we want this filter to be broadly used, we'll add as much relevant information as possible for the user at that point. As we mentioned above, we can send more information stored in the registration form like ``name`` or ``username``.
    - Returns: since filters take in a set of parameters and return a set of parameters, we'll return the same set of parameters that we received.

    Since filters also can act according to the result of the filter's execution, we'll need to define the filter's behavior for when the filter stops the process in which it is being used. For example, if you're using the filter in the LMS, you'll need to define
    what happens when the filter stops the registration process. So, for this filter we'll define the following behavior:

    - When stopping the registration process, we'll raise a ``PreventRegistration`` exception.

#. Implement the new filter

.. Following the steps, you should add the result and any follow-up tasks needed.

    Up to this point, you should have the following:

.. code-block:: python

  class StudentRegistrationRequested(OpenEdxPublicFilter):
      """
      Custom class used to create registration filters and its custom methods.
      """

      filter_type = "org.openedx.learning.student.registration.requested.v1"

      class PreventRegistration(OpenEdxFilterException):
          """
          Custom class used to stop the registration process.
          """

      @classmethod
      def run_filter(cls, form_data):
          """
          Execute a filter with the signature specified.

          Arguments:
              form_data (QueryDict): contains the request.data submitted by the registration
              form.
          """
          sensitive_data = cls.extract_sensitive_data(form_data)
          data = super().run_pipeline(form_data=form_data)
          return data.get("form_data")

.. note::
  This is not exactly what the registration filter looks like, but it's a good starting point. You can find the full implementation of the registration filter in the library's repository.

    Some things to note:

    - The filter's type is defined in the ``filter_type`` class attribute. In this case, the :term:`filter type<Filter Type>` is ``org.openedx.learning.student.registration.requested.v1``.
    - The :term:`filter signature<Filter Signature>` is defined in the ``run_filter`` method. In this case, the signature is the ``form_data`` parameter.
    - The ``run_filter`` is a class method that returns the same set of parameters that it receives.
    - The ``run_filter`` class method calls the ``run_pipeline`` method, which is the method that executes the filter's logic. This method is defined in the ``OpenEdxPublicFilter`` class, which is the base class for all the filters in the library. This method returns a dictionary with the following structure:

    .. code-block:: python

      {
        "<INPUT ARGUMENT 1>": <INPUT ARGUMENT OBJECT 1>,
        "<INPUT ARGUMENT 2>": <INPUT ARGUMENT OBJECT 2>,
        ...
        "<OUTPUT ARGUMENT N>": <OUTPUT ARGUMENT OBJECT N>,
      }

    Where in this specific example would be:

    .. code-block:: python

      {
        "form_data": form_data,
      }

    Where ``form_data`` is the same set of parameters that the filter receives, which is the accumulated output for the :term:`filter pipeline<Filter Pipeline>`. That is how ``run_filter`` should always look like.
    - The filter's behavior for stopping the process is defined in the ``PreventRegistration`` exception which inherits from the ``OpenEdxFilterException`` base exception. In this case, the exception is raised when the filter stops the registration process. This is done in the service where the filter is being used, which in this case is the LMS.
    - The class name is the filter's type ``{Subject}.{Action}`` part in a camel case format. In this case, the filter's name is ``StudentRegistrationRequested``.

#. Add tests for the new filter

    Each filter has its own set of tests. The tests for the filter you're creating should be located in the ``tests`` directory in the library's repository. The tests should be located in the ``test_filters.py`` file, which is where all the tests for the filters are located. Each set of tests is related to a specific type of filter, so you should add your tests to the set of tests that are related to the filter you're creating.
    For example, if you're creating a filter that will be used during the student registration process in the LMS, you should add your tests to the ``TestAuthFilters`` set of tests. This is how the tests for the registration filter look like:


.. code-block:: python

    def test_student_registration_requested(self):
        """
        Test StudentRegistrationRequested filter behavior under normal conditions.

        Expected behavior:
            - The filter must have the signature specified.
            - The filter should return form data.
        """
        expected_form_data = {
            "password": "password",
            "newpassword": "password",
            "username": "username",
        }

        form_data = StudentRegistrationRequested.run_filter(expected_form_data)

        self.assertEqual(expected_form_data, form_data)

    @data(
        (
            StudentRegistrationRequested.PreventRegistration, {"message": "Can't register in this site."}
        ),
    )
    @unpack
    def test_halt_student_auth_process(self, auth_exception, attributes):
        """
        Test for student auth exceptions attributes.

        Expected behavior:
            - The exception must have the attributes specified.
        """
        exception = auth_exception(**attributes)

        self.assertDictContainsSubset(attributes, exception.__dict__)

.. note::
    Basically, we're testing the :term:`filter signature<Filter Signature>` and the filter's behavior for stopping the process. The first test is testing the :term:`filter signature<Filter Signature>`, which is the set of parameters that the filter receives and returns. The second test is testing the filter's behavior for stopping the process, which is the exception that is raised when the filter stops the process.

.. .. seealso::

  :ref:`title to link to`
