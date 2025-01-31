Documenting Open edX Filters Classes
====================================

When creating a new filter, you should document the purpose of the filter in the docstring of the filter class. This will help other developers understand the purpose of the filter and how to use it.

The docstring should comply with the following guidelines:

- The docstring should be a triple-quoted string.
- The docstring should be placed at the beginning of the class definition.
- The docstring should include a brief description of what's supposed to do.
- The docstring should describe the purpose of the filter.
- The docstring should include the filter type ``filter_type``, which is the unique identifier for the filter.
- The docstring should include the trigger information, which includes the repository, path, and function or method that triggers the filter. If for some reason the filter is triggered by multiple functions or methods, you should list them all. If it's not triggered by any function or method, you should use NA (Not Applicable).
- The docstring should include any other relevant information about the filter (e.g., it works only for legacy views not MFEs).

Consider the following example:

.. code-block:: python

    class AccountSettingsRenderStarted(OpenEdxPublicFilter):
    """
    Filter used to modify the rendering of the account settings page in the LMS.

    Purpose:
        This filter is triggered when a user visits the account settings page, just before the page is rendered allowing
        the filter to modify the context and the template used to render the page.

    Filter Type:
        org.openedx.learning.student.settings.render.started.v1

    Trigger:
        - Repository: openedx/edx-platform
        - Path: openedx/core/djangoapps/user_api/accounts/settings_views.py
        - Function or Method: account_settings

    Additional Information:
        This filter doesn't work alongside the account MFE, only with the legacy account settings page.
    """
