"""
Package where filters related to the Course Authoring architectural subdomain are implemented.
"""

from openedx_filters.tooling import OpenEdxPublicFilter


class LMSPageURLRequested(OpenEdxPublicFilter):
    """
    Filter used to modify the URL of the page requested by the user.

    Purpose:
        This filter is triggered when a user loads a page in Studio that references an LMS page, allowing the filter to
        modify the URL of the page requested by the user.

    Filter Type:
        org.openedx.content_authoring.lms.page.url.requested.v1

    Trigger:
        - Repository: openedx/edx-platform
        - Path: cms/djangoapps/contentstore/asset_storage_handler.py
        - Function or Method: get_asset_json
    """

    filter_type = "org.openedx.content_authoring.lms.page.url.requested.v1"

    @classmethod
    def run_filter(cls, url: str, org: str) -> tuple[str | None, str | None]:
        """
        Process the inputs using the configured pipeline steps to modify the URL of the page requested by the user.

        Arguments:
            url (str): the URL of the page to be modified.
            org (str): Course org filter used as context data to get LMS configurations.

        Returns:
            tuple[str, str]:
                - str: the modified URL of the page requested by the user.
                - str: the course org.
        """
        data = super().run_pipeline(url=url, org=org)
        return data.get("url"), data.get("org")
