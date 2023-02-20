How to use
----------

Using openedx-filters in your code is very straight forward. We can consider the
two possible cases:

Configuring a filter
^^^^^^^^^^^^^^^^^^^^

Implement pipeline steps
************************

Let's say you want to consult student's information with a third party service
before generating the students certificate. This is a common use case for filters,
where the functions part of the filter's pipeline will perform the consulting tasks and
decide the execution flow for the application. These functions are the pipeline steps,
and can be implemented in an installable Python library:

.. code-block:: python

    # Step implementation taken from openedx-filters-samples plugin
    from openedx_filters import PipelineStep
    from openedx_filters.learning.filters import CertificateCreationRequested

    class StopCertificateCreation(PipelineStep):

        def run_filter(self, user, course_id, mode, status):
            # Consult third party service and check if continue
            # ...
            # User not in third party service, denied certificate generation
            raise CertificateCreationRequested.PreventCertificateCreation(
                "You can't generate a certificate from this site."
            )

There's two key components to the implementation:

1. The filter step must be a subclass of ``PipelineStep``.

2. The ``run_filter`` signature must match the filters definition, eg.,
the previous step matches the method's definition in CertificateCreationRequested.

Attach/hook pipeline to filter
******************************

After implementing the pipeline steps, we have to tell the certificate creation
filter to execute our pipeline.

.. code-block:: python

    OPEN_EDX_FILTERS_CONFIG = {
        "org.openedx.learning.certificate.creation.requested.v1": {
            "fail_silently": False,
            "pipeline": [
                "openedx_filters_samples.samples.pipeline.StopCertificateCreation"
            ]
        },
    }

Triggering a filter
^^^^^^^^^^^^^^^^^^^

In order to execute a filter in your own plugin/library, you must install the
plugin where the steps are implemented and also, ``openedx-filters``.

.. code-block:: python

    # Code taken from lms/djangoapps/certificates/generation_handler.py
    from openedx_filters.learning.filters import CertificateCreationRequested

    try:
        self.user, self.course_id, self.mode, self.status = CertificateCreationRequested.run_filter(
            user=self.user, course_id=self.course_id, mode=self.mode, status=self.status,
        )
    except CertificateCreationRequested.PreventCertificateCreation as exc:
        raise CertificateGenerationNotAllowed(str(exc)) from exc

Testing filters' steps
^^^^^^^^^^^^^^^^^^^^^^

It's pretty straightforward to test your pipeline steps, you'll need to include the
``openedx-filters`` library in your testing dependencies and configure them in your test case.

.. code-block:: python

   from openedx_filters.learning.filters import CertificateCreationRequested

    @override_settings(
        OPEN_EDX_FILTERS_CONFIG={
            "org.openedx.learning.certificate.creation.requested.v1": {
                "fail_silently": False,
                "pipeline": [
                    "openedx_filters_samples.samples.pipeline.StopCertificateCreation"
                ]
            }
        }
    )
    def test_certificate_creation_requested_filter(self):
        """
        Test filter triggered before the certificate creation process starts.

        Expected results:
          - The pipeline step configured for the filter raises PreventCertificateCreation
          when the conditions are met.
        """
        with self.assertRaises(CertificateCreationRequested.PreventCertificateCreation):
            CertificateCreationRequested.run_filter(
                user=self.user, course_key=self.course_key, mode="audit",
            )

        # run your assertions

Changes in the ``openedx-filters`` library that are not compatible with your code
should break this kind of test in CI and let you know you need to upgrade your code.
The main limitation while testing filters' steps it's their arguments, as they are edxapp
memory objects, but that can be solved in CI using Python mocks.
