"""
Package where filters related to the Course Authoring architectural subdomain are implemented.
"""

from openedx_filters.tooling import OpenEdxPublicFilter


class LMSPageURLRequested(OpenEdxPublicFilter):
    """
    Custom class used to get lms page url filters and its custom methods.
    """

    filter_type = "org.openedx.course_authoring.lms.page.url.requested.v1"

    @classmethod
    def run_filter(cls, url, org):
        """
        Execute a filter with the signature specified.

        Arguments:
            url (str): the URL of the page to be modified.
            org (str): Course org filter used as context data to get LMS configurations.
        """
        data = super().run_pipeline(url=url, org=org)
        return data.get("url"), data.get("org")
