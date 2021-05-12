Filter tooling: debugging tools
===============================

Status
------

Draft


Context
-------

By accessing in-memory models and other objects, filters have a large
surface area for breaking. To minimize this, it is necessary that the filter
framework allows for good monitoring, logging, and debugging capabilities.

Measuring performance is best accomplished by having persisted data that can be
used for statistical analysis.


Decisions
---------

1. Tooling for debugging must be able to be turned on/off per filter and in
straightforward way in the same way that filters are normally configured.

2. Logging tools for the pipeline execution must allow that a developer logs
both a filter function individually at its step and together with other
functions called before or after in the same pipeline run.

3. It should be possible to send performance data to external services such as
sentry or newrelic.


Consequences
------------

1. The `OpenEdxPublicFilters` class must implement different logging strategies.

2. There will possibly be a dependency on some third-party tools for data
aggregation.
