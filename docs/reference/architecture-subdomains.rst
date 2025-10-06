.. _Architecture Subdomains Reference:

Architecture Subdomains
#######################

Currently, these are the `architecture subdomains`_ used by the Open edX Filters library:

+-------------------+----------------------------------------------------------------------------------------------------+
| Subdomain Name    | Description                                                                                        |
+===================+====================================================================================================+
| Content Authoring | Allows educators to create, modify, package, annotate (tag), and share learning content.           |
+-------------------+----------------------------------------------------------------------------------------------------+
| Learning          | Allows learners to consume content and perform actions in a learning activity on the platform.     |
+-------------------+----------------------------------------------------------------------------------------------------+

Here we list useful information about Open edX architecture subdomains and their use in the Hooks Extension framework:

- :ref:`Filters Naming and Versioning <ADR-4>`
- `edX Domain Driven Design documentation`_
- `Subdomains from OEP-41`_
- `Message Content Data Guidelines`_

.. note:: When creating new filters in a new subdomain, please list the subdomain in this document and in :ref:`Existing Filters`.

.. _edX Domain Driven Design documentation: https://openedx.atlassian.net/wiki/spaces/AC/pages/213910332/Domain-Driven+Design
.. _Subdomains from OEP-41: https://docs.openedx.org/projects/openedx-proposals/en/latest/architectural-decisions/oep-0041-arch-async-server-event-messaging.html#subdomain-from-domain-driven-design
.. _Message Content Data Guidelines: https://docs.openedx.org/projects/openedx-proposals/en/latest/architectural-decisions/oep-0041-arch-async-server-event-messaging.html?highlight=subdomain#message-content-data-guidelines
.. _architecture subdomains: https://microservices.io/patterns/decomposition/decompose-by-subdomain.html

**Maintenance chart**

+--------------+-------------------------------+----------------+--------------------------------+
| Review Date  | Reviewer                      |   Release      |Test situation                  |
+--------------+-------------------------------+----------------+--------------------------------+
|2025-02-13    | Maria Grimaldi                |  Sumac         |Pass.                           |
+--------------+-------------------------------+----------------+--------------------------------+
