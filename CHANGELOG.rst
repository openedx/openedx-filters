Change Log
----------

..
   All enhancements and patches to openedx_filters will be documented
   in this file.  It adheres to the structure of https://keepachangelog.com/ ,
   but in reStructuredText instead of Markdown (for ease of incorporation into
   Sphinx documentation and the PyPI description).
   
   This project adheres to Semantic Versioning (https://semver.org/).

.. There should always be an "Unreleased" section for changes pending release.

Unreleased
~~~~~~~~~~

[0.5.0] - 2022-02-23
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Added
_____

* Unenrollment filter definition.
* Certificate creation/rendering filters.
* Dashboard render filter definition.
* Course home/about render filters.
* Cohort change filter.

[0.4.3] - 2022-01-24
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Changed
_______

* Add fail_silently when importing filter steps.

[0.4.2] - 2021-12-16
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Changed
_______

* Fix dictionary mishandling in OpenEdxPublicFilter tooling.

[0.4.1] - 2021-12-16
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Changed
_______

* Use `run_filter` instead of `run` in OpenEdxPublicFilter tooling.

[0.4.0] - 2021-12-15
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Added
_____

* Filter definitions for registration and login.
* Sensitive data mixin for filters.

Changed
_______

* Pipeline runner from `run` to `run_filter`.
* Moved filters definitions to filters file inside their domain.

[0.3.0] - 2021-11-24
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Added
_____

* ADRs for naming, payload and debugging tools.
* OpenEdxPublicFilter class with the necessary tooling for filters execution
* PreEnrollmentFilter class definition

Changed
_______

* Update doc-max-length following community recommendations.

[0.2.0] - 2021-09-02
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Added
_____

* First version of Open edX Filters tooling.

Changed
_______

* Update setup.cfg with complete bumpversion configuration.


[0.1.0] - 2021-04-07
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Added
_____

* First release on PyPI.
