"""
Utilities for Open edX Filters usage.
"""
import logging
import traceback
from pprint import PrettyPrinter, pformat

LOG = logging.getLogger(__name__)


class StepsContextPrettyPrinter(PrettyPrinter):
    """
    Custom printer for Open edX Filter Strategy.

    This class pretty-prints the exceptions raised while executing filter functions.
    """

    def _format(self, obj, stream, indent, allowance, context, level):  # pylint: disable=arguments-differ
        """
        Override format method exposing more information about exceptions.

        When formatting an exception this method will return the stack trace of the
        exception.
        With other objects has the same behavior.
        """
        if isinstance(obj, Exception):
            exc_type, exc_value, exc_traceback = type(obj), obj, obj.__traceback__
            exc_traceback_formatted = traceback.format_exception(
                exc_type, exc_value, exc_traceback
            )
            obj = "".join(exc_traceback_formatted)
        return super()._format(obj, stream, indent, allowance, context, level)


def format_steps_context(obj, indent=1, width=80, depth=None, *, compact=False, sort_dicts=True):
    """
    Format Steps context dictionary into a pretty-printed representation.

    Example usage:

        log_strategy.collect_step_context(
            function.__name__,
            accumulated_output=accumulated_output,
            step_exception=exception,
        )
        Will result in:

    Arguments:
        obj (tuple): response object to be formatted.
        indent (int): specifies the amount of indentation added to each recursive level.
        width (int): desired output width.
        depth (int): number of levels to represent.
        compact (bool): when true, will format as many items as will fit within the width
        on each output line.
        sort_dicts (bool): dictionaries will be formatted with their keys sorted.

    Same as in https://docs.python.org/3/library/pprint.html#pprint.PrettyPrinter

    Returns:
        (str) string representation of Open edX events responses.
    """
    return StepsContextPrettyPrinter(
        indent=indent,
        width=width,
        depth=depth,
        compact=compact,
        sort_dicts=sort_dicts,
    ).pformat(obj)


class FiltersLogStrategy:
    """
    Class that implements each log level for Open edX Filters.
    """

    DEBUG = "debug"
    PERFORMANCE = "performance"
    INFO = "info"
    DEFAULT_LOG_LEVEL = INFO
    DEBUG_MESSAGE = (
        "Pipeline execution for Open edX filter <%s>\n"
        "Pipeline contexts during execution:\n%s\n"
        "Steps contexts during pipeline execution:\n%s\n"
        "Current filter functions:%s"
    )
    INFO_MESSAGE = (
        "Pipeline results for Open edX filter <%s>:\n"
        "%s\n"
    )
    LOG_MESSAGES = {
        DEBUG: DEBUG_MESSAGE,
        INFO: INFO_MESSAGE,
    }

    def __init__(self, log_level):
        """
        Init method for FiltersLogStrategy.

        Arguments:
            log_level (str): specifies which and how much information is logged.

        The available log levels are:
            - DEBUG
            - INFO
        """
        self.log_level = log_level
        self._steps_context = {}
        self._pipeline_context = {}

    def log(self, **kwargs):
        """
        Call log method specified by log_level.
        """
        log_message = self.LOG_MESSAGES.get(self.log_level)
        log_args = (
            log_message, kwargs.get("filter_type"), pformat(kwargs.get("accumulated_output", {}))
        )
        if self.log_level == self.DEBUG:
            log_args = (
                log_message,
                kwargs.get("filter_type"),
                pformat(self._pipeline_context),
                format_steps_context(self._steps_context),
                pformat(kwargs.get("current_configuration")),
            )
        getattr(LOG, self.log_level, self.DEFAULT_LOG_LEVEL)(*log_args)

    def collect_step_context(self, current_step, **step_context):
        """
        Collect context during the pipeline execution for logging purposes.
        """
        self._steps_context[current_step] = step_context

    def collect_pipeline_context(self, **pipeline_context):
        """
        Collect context during the pipeline execution for logging purposes.
        """
        self._pipeline_context = pipeline_context
