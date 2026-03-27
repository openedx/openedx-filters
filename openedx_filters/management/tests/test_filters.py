"""
Tests for management subdomain filters.
"""
from unittest.mock import Mock

from django.test import TestCase

from openedx_filters.management.filters import ManagementCommandExecutionRequested


class TestManagementFilters(TestCase):
    """
    Test class to verify standard behavior of management filters.
    """

    def test_management_command_execution_requested(self):
        """
        Test ManagementCommandExecutionRequested filter behavior.

        Expected behavior:
            - The filter should return management command metadata and runner.
        """
        command_name = "migrate"
        service_variant = "lms"
        command_runner = Mock()

        result = ManagementCommandExecutionRequested.run_filter(
            command_name=command_name,
            service_variant=service_variant,
            command_runner=command_runner,
        )

        self.assertEqual(command_name, result.get("command_name"))
        self.assertEqual(service_variant, result.get("service_variant"))
        self.assertEqual(command_runner, result.get("command_runner"))
