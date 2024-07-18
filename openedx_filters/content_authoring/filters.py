"""
Package where filters related to the content authoring architectural subdomain are implemented.
"""

from openedx_filters.exceptions import OpenEdxFilterException
from openedx_filters.tooling import OpenEdxPublicFilter


class LmsUrlCreationStarted(OpenEdxPublicFilter):
    """
    Custom class used to create lms url creation link render filters and its custom methods.
    """

    filter_type = "org.openedx.course_authoring.lms.url.creation.started.v1"

    class PreventLmsUrlCreationRender(OpenEdxFilterException):
        """
        Custom class used to stop lms url creation link render process.
        """

    @classmethod
    def run_filter(cls, context, org, val_name, default):
        """
        Execute a filter with the signature specified.

        Arguments:
        context (str): rendering context value
        org (str): Course org filter, this value will be used to filter out the correct lms url configuration.
        val_name (str): Name of the key for which to return configuration value.
        default: default value to return if key is not present in the configuration
        """
        data = super().run_pipeline(context=context, org=org, val_name=val_name, default=default)
        return data.get("context")
