"""
Package where filters related to management command execution are implemented.
"""

from contextlib import AbstractContextManager

from openedx_filters.tooling import OpenEdxPublicFilter


class ManagementCommandContextmanagerRequested(OpenEdxPublicFilter):
    """
    Filter used to wrap Django management command execution in a context manager.

    Purpose:
        This filter is triggered in ``manage.py`` before a management command is
        executed, allowing pipeline steps to provide a context manager wrapper.

    Filter Type:
        org.openedx.platform.management.command.contextmanager.requested.v1

    Trigger:
        - Repository: edx/edx-platform
        - Path: manage.py
        - Function or Method: __main__
    """

    filter_type = "org.openedx.platform.management.command.contextmanager.requested.v1"

    @classmethod
    def run_filter(
        cls,
        command_contextmanager: AbstractContextManager[None],
        command_name: str,
        service_variant: str,
    ) -> tuple[AbstractContextManager[None], str, str]:
        """
        Process management command context manager arguments through the pipeline.

        Arguments:
            command_contextmanager (AbstractContextManager[None]): context manager used to wrap command execution.
            command_name (str): name of the management command being executed.
            service_variant (str): service variant, such as lms or cms.

        Returns:
            tuple[AbstractContextManager[None], str, str]:
                - context manager used to wrap command execution.
                - name of the management command.
                - service variant, such as lms or cms.
        """
        data = super().run_pipeline(
            command_contextmanager=command_contextmanager,
            command_name=command_name,
            service_variant=service_variant,
        )
        return (
            data.get("command_contextmanager", command_contextmanager),
            data.get("command_name", command_name),
            data.get("service_variant", service_variant),
        )
