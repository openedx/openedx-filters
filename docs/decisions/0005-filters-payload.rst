Open edX filters payload conventions
====================================

Status
------

Draft


Context
-------

Although filters have a public promise status, and thus maintainability is an
important design goal, filters by definition permit that extension developers
manipulate data that will be passed along to the lms or cms processes.

At the same time, using fixed attr classes such as what is used in events is not
convenient when trying to have few restrictions on what developers can do.

That said, things should still be allowed to evolve in a backward compatible
manner. When things inevitably break, we would like them to break in CI.
Which just as in the case of Open edX Events, should not require the code of
edx-platform to test integrations.


Decisions
---------

1. Filters will receive metadata information about the filter, e.g, its minor version.

2. Filter specific data will be passed to the implementing function unpacked as
keyword arguments, so that mismatch errors are caught in CI.

3. The metadata information will be calculated on the fly by the
`OpenEdxPublicFilters` class to keep this information out of the way when writing
the filter definition and calling location.

4. The data sent to a filter will use in-memory objects in a way that is more
practical and familiar for python developers with Django and Open edX specific
experience.

.. _OEP-41 format: https://open-edx-proposals.readthedocs.io/en/latest/oep-0041-arch-async-server-event-messaging.html#message-format


Consequences
------------

1. During testing I can as a developer mock the edx-platform objects passed to
   my filter and run thorough tests without ever requiring the edx-platform code.

2. Extension developer will be able to manipulate Django or otherwise edx-platform
   objects, which increases the risk of extensions breaking when the platform changes.

3. CI testing will not be able to catch all runtime errors.

4. Catching and debugging errors when testing on a runtime environment that does
   use the edx-platform code is critical.

5. Extension developers will be able to react to different versions of a filter
   simultaneously if the read the envelope information.
