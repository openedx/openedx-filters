.. _ADR-4:

4. Open edX filters naming and versioning
=========================================

Status
------

Draft


Context
-------

Filter-type hooks are an important public promise. They are a strong foundation
of a healthy ecosystem of extensions for the Open edX world and have been
recognized as such by the arch team of the Open edX core and also by the community.

This ADR has the purpose of defining the rules to be followed when naming an
Open edX Filter with the intent of covering the use cases of:

* Open edX core developers wanting to add new filters.
* Open edX core developers wanting to deprecate and eventually remove filters.
* Open edX core developers wanting to add additional information to an existing
  filters in a mostly backward compatible way.
* Open edX extension developers wanting to have as few restrictions as reasonable
  on the extension capabilities at the filter location.
* Open edX extension developers wanting to create and maintain stable
  applications, even when the filters framework evolves and changes over time.

Evolving stably and creating few restrictions on the filters are two use cases
at odds with each other, and this ADR and overall framework tries to
find a good balance between them.


Decisions
---------

1. The name of a filter will be a ``string`` that follows the `type format`_
defined in the `OEP-41`_:

``{Reverse DNS}.{Architecture Subdomain}.{Subject}.{Action}.{Major Version}``

Rationale: Although filters are geared more towards edx-platform and will not
be sent via a message bus, we still find that having a consistent naming scheme
is very important.

Examples:

* org.openedx.learning.course.enrollment.creation.requested.v1
* org.openedx.learning.student.registration.requested.v2
* org.openedx.learning.session.login.requested.v1
* org.openedx.learning.certificate.render.started.v1


2. This name will be used as part of the configuration of every filter,
for example:

.. code-block:: python

    OPEN_EDX_FILTERS_CONFIG = {
        "org.openedx.learning.course.enrollment.creation.requested.v1": {
            "pipeline": [
                "first_plugin.module.check_enrollment_if_enterprise",
                "second_plugin.module.check_crm_data_for_enrollment",
            ],
        }
    }


3. The filter definitions will be placed written in code in a way that is more
practical and familiar for python developers with an emphasis on Django experience.
The definition will be grouped by subdomain along with other data structures in a
way that favors reuse.
Only the `Architecture Subdomain`_ part of the filter name will be used in the
package name of the filter definition.
What constitutes a filter is that is a class that inherits from the main
OpenEdxPublicFilter, which implements all the inner workings of the framework.


4. The filters library will use SemVer 2. The major version will not be tied to
Open edX releases for the time being. We still recognize that Open edX releases
are the logical boundary to remove filters and make breaking changes
such as eliminating filter definitions.


5. Each filter will have a major and minor version only. The major version will
be part of the `filter name` and be written to the classname defining
the filter. However, version 1 (V1) of a filter will remove the _V1 suffix for
readability. We also expect to have relatively few breaking changes to the
filter definitions. The minor version of a filter will be written in the payload
passed to the implementing function so that extension developers can react to it
if they so desire.


6. The filters library will be a single library containing the filter
definitions, the necessary classes, and the tools to support the filters
framework. These definitions will be written with a logical boundary such that if
the project ever decides to separate them in a split library, there is no
necessary large refactor.

.. _type format: https://open-edx-proposals.readthedocs.io/en/latest/oep-0041-arch-async-server-event-messaging.html#id5
.. _Architecture Subdomain: https://openedx.atlassian.net/wiki/spaces/AC/pages/663224968/edX+DDD+Bounded+Contexts
.. _OEP-41: https://open-edx-proposals.readthedocs.io/en/latest/oep-0041-arch-async-server-event-messaging.html#specification

Consequences
------------

1. There will not be a necessary correspondence between Open edX releases and
major versions of this library. Also, there will not be a need to make a major
release if there is no breaking for consecutive Open edX releases.

2. Open edX core, and in particular, edx-platform must run the filters meant for
public consumption as they are written in this library, changes in edx-platform
that require changes in the public filter will require a backward compatible
addition to this library or an altogether new filter with support for the old
filter until deprecated and removed.

3. Changing the arguments passed to a filter must always be done in a backward
compatible way since making it incompatible warrants the use of a new major
version.
