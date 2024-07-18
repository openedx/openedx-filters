"""
Package where filters related to the authoring architectural subdomain are implemented.
"""

from openedx_filters.exceptions import OpenEdxFilterException
from openedx_filters.tooling import OpenEdxPublicFilter


class LMSPageURLRequested(OpenEdxPublicFilter):
    """
    Custom class used to get lms page url filters and its custom methods.
    """

    filter_type = "org.openedx.authoring.lms.page.url.requested.v1"

    @classmethod
    def run_filter(cls, target_url, org):
        """
        Execute a filter with the signature specified.

        Arguments:
        target_url (str): target url to use.
        org (str): Course org filter, this value will be used to filter out the correct lms url configuration.
        """
        data = super().run_pipeline(target_url=target_url, org=org)
        return data.get("target_url"), data.get("org")
