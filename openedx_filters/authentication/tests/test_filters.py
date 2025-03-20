"""
Tests for ``authentication`` subdomain filters.
"""
from unittest.mock import Mock

from django.test import TestCase

from openedx_filters.authentication.filters import SessionJWTCreationRequested


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
        payload = Mock()
        user = Mock()

        payload_result, user_result = SessionJWTCreationRequested.run_filter(payload, user)

        self.assertEqual(payload, payload_result)
        self.assertEqual(user, user_result)
