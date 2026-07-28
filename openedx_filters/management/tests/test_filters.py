"""
Tests for management subdomain filters.
"""
from contextlib import nullcontext

from django.test import TestCase

from openedx_filters.management.filters import ManagementCommandContextmanagerRequested


class TestManagementFilters(TestCase):
    """
    Test class to verify standard behavior of management filters.
    """

    def test_management_command_contextmanager_requested(self):
        """
        Test ManagementCommandContextmanagerRequested filter behavior.

        Expected behavior:
            - The filter should return context manager and command metadata.
        """
        command_contextmanager = nullcontext()
        command_name = "migrate"
        service_variant = "lms"

        (
            filtered_command_contextmanager,
            filtered_command_name,
            filtered_service_variant,
        ) = ManagementCommandContextmanagerRequested.run_filter(
            command_contextmanager=command_contextmanager,
            command_name=command_name,
            service_variant=service_variant,
        )

        self.assertEqual(command_contextmanager, filtered_command_contextmanager)
        self.assertEqual(command_name, filtered_command_name)
        self.assertEqual(service_variant, filtered_service_variant)
