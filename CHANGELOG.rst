Change Log
==========

..
   All enhancements and patches to openedx_filters will be documented
   in this file.  It adheres to the structure of https://keepachangelog.com/ ,
   but in reStructuredText instead of Markdown (for ease of incorporation into
   Sphinx documentation and the PyPI description).

   This project adheres to Semantic Versioning (https://semver.org/).

.. There should always be an "Unreleased" section for changes pending release.

Unreleased
----------

[1.9.0] - 2024-06-14
--------------------

Added
~~~~~~~

* RenderXBlockStarted filter added which allows reading / modifying of XBlock context prior to render.

[1.8.1] - 2024-04-12
--------------------

Changed
~~~~~~~

* Updated Python classifiers to include Python 3.11.

[1.8.0] - 2024-04-11
--------------------

Added
~~~~~

* ORASubmissionViewRenderStarted filter added which can be used to modify the ORA submission view.

[1.7.0] - 2024-04-11
--------------------

Added
~~~~~

* Add Python 3.11 support.

[1.6.0] - 2023-08-18
--------------------

Added
~~~~~

* CourseRunAPIRenderStarted filter added which can be used to modify the courserun data for B2C dashboard rendering process.


[1.5.0] - 2023-07-19
--------------------

Added
~~~~~

* CourseEnrollmentAPIRenderStarted filter added which can be used to modify the isStarted B2C dashboard rendering process.


[1.4.0] - 2023-07-18
--------------------

Added
~~~~~

* InstructorDashboardRenderStarted filter added which can be used to modify the instructor dashboard rendering process.


[1.3.0] - 2023-05-25
--------------------

Added
~~~~~

* CourseHomeUrlCreationStarted filter added which can be used to modify the course_home_url for externally hosted courses.

[1.2.0] - 2023-03-01
--------------------

Added
~~~~~

* AccountSettingsRenderStarted filter added which can be used to modify the rendered output of the account settings page.

[1.1.0] - 2023-02-16
--------------------

Added
~~~~~

* VerticalBlockRenderCompleted filter added which can be used to modify the rendered output of a VerticalBlock.

Changed
~~~~~~~

* Introduced PreventChildBlockRender exception to the VerticalBlockChildRenderStarted filter.

[1.0.0] - 2023-01-18
--------------------

Added
~~~~~

* Bump version to 1.x to acknowledge that this is in use in production.
* CourseEnrollmentQuerysetRequested filter added that is called when returning course enrollments queryset object.


[0.8.0] - 2022-08-18
--------------------

Added
~~~~~

* VerticalBlockChildRenderStarted filter added that is called when every child block of a VericalBlock is about to be rendered.

[0.7.0] - 2022-05-26
--------------------

Added
~~~~~

* Cohort assignment filter to be used with every cohort assignment.

[0.6.2] - 2022-04-07
--------------------

Changed
~~~~~~~

* Change dashboard/course about render exceptions naming for clarity

[0.6.1] - 2022-04-07
--------------------

Changed
~~~~~~~

* Remove CourseHomeRenderStarted since it's not going to be used.
* Change RenderAlternativeCertificate to RenderAlternativeInvalidCertificate.

[0.6.0] - 2022-04-01
--------------------

Added
~~~~~

* More significant exceptions for template interaction.

[0.5.1] - 2022-03-29
--------------------

Added
~~~~~

* More significant arguments to the certificate creation filter.

[0.5.0] - 2022-02-23
--------------------

Added
~~~~~

* Unenrollment filter definition.
* Certificate creation/rendering filters.
* Dashboard render filter definition.
* Course home/about render filters.
* Cohort change filter.

[0.4.3] - 2022-01-24
--------------------

Changed
~~~~~~~

* Add fail_silently when importing filter steps.

[0.4.2] - 2021-12-16
--------------------

Changed
~~~~~~~

* Fix dictionary mishandling in OpenEdxPublicFilter tooling.

[0.4.1] - 2021-12-16
--------------------

Changed
~~~~~~~

* Use `run_filter` instead of `run` in OpenEdxPublicFilter tooling.

[0.4.0] - 2021-12-15
--------------------

Added
~~~~~

* Filter definitions for registration and login.
* Sensitive data mixin for filters.

Changed
~~~~~~~

* Pipeline runner from `run` to `run_filter`.
* Moved filters definitions to filters file inside their domain.

[0.3.0] - 2021-11-24
--------------------

Added
~~~~~

* ADRs for naming, payload and debugging tools.
* OpenEdxPublicFilter class with the necessary tooling for filters execution
* PreEnrollmentFilter class definition

Changed
~~~~~~~

* Update doc-max-length following community recommendations.

[0.2.0] - 2021-09-02
--------------------

Added
~~~~~

* First version of Open edX Filters tooling.

Changed
~~~~~~~

* Update setup.cfg with complete bumpversion configuration.


[0.1.0] - 2021-04-07
--------------------

Added
~~~~~

* First release on PyPI.
