Real-Life Use Cases for Open edX Filters
##########################################

Overview
**********

As mentioned in the :doc:`docs.openedx.org:developers/concepts/hooks_extension_framework`, Open edX Filters filters can be used when implementing features meant to modify the application's behavior, navigation, or user interaction.

To illustrate the different solutions that can be implemented with this approach, we have compiled a list of implementations built using Open edX Filters to address various challenges. The goal of this list is to serve as a reference for extension developers to implement their own solutions based on the community's experience.

Use Cases
***********

The following list of real-life use cases showcases the different ways Open edX Filters can be used to facilitate the modification of the Open edX platform behavior without modifying the codebase, only through configurations and feature implementation in plugins.

Reusable LTI Configuration
===========================

When a course creator adds an LTI tool, a filter is executed to fetch reusable and pluggable LTI configurations from external plugins and display them to course creators as configuration options in Studio. This use case simplifies the setup of LTI tools by allowing reusable options to be used instead of manually setting them for each tool.

More details on:

* `Reusable LTI Configuration`_.

Verification of Skills by Users
=================================

When a user enters a unit, a filter is executed to inject verification forms where users can vote on the skills they have learned. This use case helps gather feedback from users about their learning experience in the course, helping to ensure the course objectives match what learners experience.

More details on:

* `Verification of Skills by Users`_.

IDV Integration with New Vendors
==================================

A filter is executed to return the URL for the configured Identity Verification (IDV) vendor. When student verify their identity from their account settings, they are redirected to the IDV vendor's configured to complete the verification process. This use case can be used to integrate new IDV vendors with the Open edX platform.

More details on:

* `IDV Integration with new Vendors`_.

Show Consent Warning to Users
===============================

When a student loads an Open Response Assessment (ORA) problem, a filter is executed to display a consent warning to the student. This use case can be used to inform students about the data collection and processing that will occur when they submit their responses. This is especially useful when the data is being processed by third-party services.

More details on:

* `Show Consent Warning to Users`_.

Adding Custom Tabs to the Instructor Dashboard
=================================================

When an instructor enters the instructor dashboard, a filter is executed to modify the section tabs. This allows adding new features implemented in plugins to the instructor dashboard, such as custom reports, analytics, or other tools that help instructors manage their courses.

More details on:

* `Aspects Reports`_.
* `Feedback Xblock Aggregated Data`_
* `Forum Digest Instructor Configurations`_.

Prevent Enrollment From Unauthorized Users
============================================

When a student enrolls in a course, before the enrollment is completed, a filter is executed to check if the student is authorized to enroll in that course. If the student doesn't meet the conditions for enrollment, they will not be able to enroll. For instance, when the student is not part of a partner institution or doesn't have the required prerequisites. This use case can also be extended to cover login, registration, and other actions.

More details on:

* `Prevent Enrollment From Non-Partner Users`_.
* `Prevent Enrollment for Non-Authorized Email Domains`_.
* `Prevent Registration of Users with Specific Email Domains`_.
* `Prevent Login of Users with Specific Email Domains`_.

Webfilters Integration
========================

Webfilters, as mentioned in `openedx-webhooks`_, are a type of webhook that allows you to make HTTP requests to external services and modify the application behavior depending on the response. This use case can be used to validate data with external services, such as verifying the user's subscription with a third-party service before allowing them to enroll in a course. This is a more generalized implementation of the previous use case.

More details on `Open edX Webhooks - Webfilters`_.

Schedules Filtering
=====================

When an automatic email message is scheduled to be sent to students, a filter is executed to modify the schedule. This functionality allows you to define specific criteria to determine which students will receive the email. For example, filters can check whether students have opted to receive newsletters, assess their progress in the course, evaluate their activity, or consider other relevant conditions.

More details on `Schedule Filtering`_.

Other Use Cases
***************

Here are some additional use cases that can be implemented using Open edX Filters:

* `LimeSurvey Management View in the Instructor Dashboard`_.
* `OnTask Service Integration`_.
* `Filters for Close Communication`_.
* `Edit On Git in Units`_.
* `Render Alternative Course About`_.
* `Hide Course About from Users Without Memberships`_.

.. note:: If you have implemented a solution using Open edX Filters and would like to share it with the community, please submit a pull request to add it to this list!

.. _Prevent Enrollment From Non-Partner Users: https://github.com/academic-innovation/mogc-partnerships/blob/main/mogc_partnerships/pipeline.py#L35-L50
.. _Prevent Enrollment for Non-Authorized Email Domains: https://github.com/fccn/nau-openedx-extensions/blob/nau/nutmeg.master/nau_openedx_extensions/filters/pipeline.py#L17-L79
.. _Prevent Registration of Users with Specific Email Domains: https://github.com/UAMx/uamx-social-auth/blob/main/uamx_social_auth/pipeline.py#L59-L63
.. _Prevent Login of Users with Specific Email Domains: https://github.com/UAMx/uamx-social-auth/blob/main/uamx_social_auth/pipeline.py#L72-L76
.. _openedx-webhooks: https://github.com/aulasneo/openedx-webhooks
.. _Open edX Webhooks - Webfilters: https://github.com/aulasneo/openedx-webhooks?tab=readme-ov-file#introduction
.. _Verification of Skills by Users: https://github.com/openedx/taxonomy-connector/blob/master/docs/decisions/0001-xblock-skill-tagging-design.rst#verification-of-skills-by-users
.. _Reusable LTI Configuration: https://github.com/openedx/xblock-lti-consumer/blob/master/docs/decisions/0006-pluggable-lti-configuration.rst
.. _Aspects Reports: https://github.com/openedx/platform-plugin-aspects/pull/2
.. _Feedback Xblock Aggregated Data: https://github.com/openedx/FeedbackXBlock/pull/35
.. _Forum Digest Instructor Configurations: https://github.com/eduNEXT/platform-plugin-forum-email-notifier/pull/3
.. _LimeSurvey Management View in the Instructor Dashboard: https://github.com/eduNEXT/xblock-limesurvey?tab=readme-ov-file#as-an-instructor
.. _OnTask Service Integration: https://github.com/eduNEXT/platform-plugin-ontask/?tab=readme-ov-file#view-from-the-learning-management-system-lms
.. _Filters for Close Communication: https://github.com/edx/commerce-coordinator/blob/main/docs/decisions/0004-openedx-filters-for-close-communication.rst#0004-openedx-filters-for-close-communication
.. _Edit On Git in Units: https://github.com/open-craft/openedx-edit-links?tab=readme-ov-file#overview
.. _Show Consent Warning to Users: https://github.com/openedx/edx-ora2/blob/master/docs/decisions/0003-lightweight-extension-points.rst#decisions
.. _IDV Integration with new Vendors: https://openedx.atlassian.net/wiki/spaces/OEPM/pages/4307386369/Proposal+Add+Extensibility+Mechanisms+to+IDV+to+Enable+Integration+of+New+IDV+Vendor+Persona
.. _Render Alternative Course About: https://github.com/lektorium-tutor/lektorium_main/blob/master/lektorium_main/tilda/pipeline.py#L15-L94
.. _Hide Course About from Users Without Memberships: https://github.com/academic-innovation/mogc-partnerships/blob/main/mogc_partnerships/pipeline.py#L53-L66
.. _Schedule Filtering: https://github.com/fccn/nau-openedx-extensions/pull/56


**Maintenance chart**

+--------------+-------------------------------+----------------+--------------------------------+
| Review Date  | Reviewer                      |   Release      |Test situation                  |
+--------------+-------------------------------+----------------+--------------------------------+
|2025-02-13    | Maria Grimaldi                |  Sumac         |Pass.                           |
+--------------+-------------------------------+----------------+--------------------------------+
