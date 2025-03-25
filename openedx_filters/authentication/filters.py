"""
Package where filters related to the ``authentication`` architectural subdomain are implemented.
"""
from typing import Any, Dict, Tuple

from openedx_filters.tooling import OpenEdxPublicFilter


class SessionJWTCreationRequested(OpenEdxPublicFilter):
    """
    Filter used to update the JWT token's payload by adding extra data when its creation is requested.

    Purpose:
        This filter is triggered when the JWT token's creation is requested, and grants the possibility to add new
        additional data to it.

    Filter Type:
        org.openedx.authentication.session.jwt.creation.requested.v1

    Trigger:
        - Repository: openedx/edx-platform
        - Path: openedx/core/djangoapps/oauth_dispatch/jwt.py
        - Function or Method: _create_jwt
    """

    filter_type = "org.openedx.authentication.session.jwt.creation.requested.v1"

    @classmethod
    def run_filter(cls, payload: Dict[str, Any], user: Any) -> Tuple[Dict[str, Any], Any]:
        """
        Process the inputs using the configured pipeline steps to modify the payload of the JWT token.

        Arguments:
            payload (str): the payload of JWT token to be modified.
            user (User): Django User related to the JWT token.

        Returns:
            tuple[dict, User]:
                - dict: the modified payload of the JWT token.
                - User: the user of the JWT token.
        """
        data = super().run_pipeline(payload=payload, user=user)
        return data.get("payload", {}), data.get("user")
