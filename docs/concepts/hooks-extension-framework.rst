Extending Open edX with the Hooks Extensions Framework
######################################################

To sustain the growth of the Open edX ecosystem, the business rules of the
platform must be open for extension following the open-closed principle. This
framework allows developers to do just that without needing to fork and modify
the main edx-platform repository.

Context
*******

Hooks are predefined places in the edx-platform core where externally defined
functions can take place. In some cases, those functions can alter what the user
sees or experiences in the platform. Other cases are informative only. All cases
are meant to be extended using Open edX plugins and configuration.

Hooks can be of two types, events and filters. Events are in essence Django signals, in
that they are sent in specific application places and whose listeners can extend
functionality. On the other hand Filters are passed data and can act on it
before this data is put back in the original application flow. In order to allow
extension developers to use the Events and Filters definitions on their plugins,
both kinds of hooks are defined in lightweight external libraries.

* `openedx-filters`_
* `openedx-events`_

Hooks are designed with stability in mind. The main goal is that developers can
use them to change the functionality of the platform as needed and still be able
to migrate to newer open releases with very little to no development effort. In
the case of filters, this is detailed in the `naming and versioning ADR`_.

A longer description of the framework and it's history can be found in `OEP 50`_.

.. _OEP 50: https://open-edx-proposals.readthedocs.io/en/latest/oep-0050-hooks-extension-framework.html
.. _naming and versioning ADR: https://github.com/openedx/openedx-filters/blob/main/docs/decisions/0004-filters-naming-and-versioning.rst
.. _openedx-filters: https://github.com/openedx/openedx-filters
.. _openedx-events: https://github.com/openedx/openedx-events

On the technical side, filters are implemented using a pipeline mechanism, that executes
a list of functions called ``steps`` configured through Django settings. Each
pipeline step receives a dictionary with data, processes it and returns an output. During
this process, they can alter the application execution flow by halting the process
or modifying their input arguments.
