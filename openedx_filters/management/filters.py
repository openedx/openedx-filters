"""
Package where filters related to management command execution are implemented.
"""

from collections.abc import Callable
from typing import Any

from openedx_filters.tooling import OpenEdxPublicFilter


class ManagementCommandExecutionRequested(OpenEdxPublicFilter):
    """
    Filter used to modify the execution of Django management commands.

    Purpose:
        This filter is triggered in ``manage.py`` before a management command is
        executed, allowing pipeline steps to wrap or replace the command runner.

    Filter Type:
        org.openedx.platform.management.command.execute.requested.v1

    Trigger:
        - Repository: openedx/edx-platform
        - Path: manage.py
        - Function or Method: __main__
    """

    filter_type = "org.openedx.platform.management.command.execute.requested.v1"

    @classmethod
    def run_filter(
        cls,
        command_name: str,
        service_variant: str,
        command_runner: Callable[..., Any],
    ) -> dict[str, Any]:
        """
        Process management command execution arguments through the pipeline.

        Arguments:
            command_name (str): name of the management command being executed.
            service_variant (str): service variant, such as lms or cms.
            command_runner (Callable): callable that executes the command.

        Returns:
            dict[str, Any]: accumulated pipeline output, including possibly
                modified command metadata and command runner.
        """
        return super().run_pipeline(
            command_name=command_name,
            service_variant=service_variant,
            command_runner=command_runner,
        )
