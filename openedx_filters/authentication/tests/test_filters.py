"""
Tests for ``authentication`` subdomain filters.
"""
from unittest.mock import Mock, patch

from django.test import TestCase

from openedx_filters.authentication.filters import SessionJWTCreationRequested
from openedx_filters.tooling import OpenEdxPublicFilter


class TestSessionJWTCreationRequested(TestCase):
    """
    Test class to verify standard behavior of the filters located in rendering views.
    You'll find test suites for:

    - SessionJWTCreationRequested
    """

    def test_session_jwt_creation_requested(self):
        """
        Test SessionJWTCreationRequested filter behavior under normal conditions.

        Expected behavior:
            - The filter should return the payload and the user.
        """
        payload = {'key': 'value'}
        modified_payload = {'key': 'modified_value'}
        user = Mock()

        with patch.object(
            OpenEdxPublicFilter,
            'run_pipeline',
            return_value={"payload": modified_payload, "user": user},
        ) as mock_run_pipeline:
            payload_result, user_result = SessionJWTCreationRequested.run_filter(payload, user)

            mock_run_pipeline.assert_called_once_with(payload=payload, user=user)
            self.assertEqual(modified_payload, payload_result)
            self.assertEqual(user, user_result)
