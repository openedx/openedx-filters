"""
Package where filters related to management command execution are implemented.
"""

from contextlib import AbstractContextManager

from openedx_filters.tooling import OpenEdxPublicFilter


class ManagementCommandContextmanagerRequested(OpenEdxPublicFilter):
    """
    Filter used to wrap Django management command execution in a context manager.

    Purpose:
        Unlike web requests, Django management commands do not go through the
        platform's usual request/response middleware, so they are normally a
        blind spot for cross-cutting concerns such as logging, performance
        monitoring, error tracking, or APM tracing. Rather than adding that
        instrumentation to each command individually, this filter gives
        pipeline steps a single place to wrap the execution of *every*
        management command in shared setup and teardown logic.

        This filter is triggered in ``manage.py`` before a management command
        is executed. It receives a no-op context manager (``command_name`` and
        ``service_variant``, such as ``lms`` or ``cms``, are provided for
        context) and returns a context manager that ``manage.py`` uses to wrap
        the command's execution. A pipeline step can, for example, return a
        context manager that opens a Datadog span for the duration of the
        command and tags it with the command name and status.

    Usage:
        Configure a pipeline step for this filter the same way as any other
        Open edX filter, for example in Django settings::

            OPEN_EDX_FILTERS_CONFIG = {
                "org.openedx.management.command.contextmanager.requested.v1": {
                    "fail_silently": True,
                    "pipeline": [
                        "my_plugin.pipeline.MonitorManagementCommand",
                    ],
                },
            }

        Where the pipeline step's ``run_filter`` accepts and returns
        ``command_contextmanager``, ``command_name``, and ``service_variant``,
        typically replacing ``command_contextmanager`` with one that wraps the
        incoming value.

    Filter Type:
        org.openedx.management.command.contextmanager.requested.v1

    Trigger:
        - Repository: openedx/openedx-platform
        - Path: manage.py
        - Function or Method: __main__
    """

    filter_type = "org.openedx.management.command.contextmanager.requested.v1"

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
