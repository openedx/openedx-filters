"""
Tooling necessary to use Open edX Filters.
"""
from logging import getLogger
from pprint import pformat

from openedx_filters.exceptions import OpenEdxFilterException
from openedx_filters.utils import get_filter_config, get_functions_for_pipeline, get_pipeline_configuration

log = getLogger(__name__)


class FiltersLoggingStrategy:
    """
    Custom class used to create Open edX Filters.
    """

    FILTERS_LOGGING_NAMESPACE = "Open"

    def __init__(self):
        self._steps_context = {}
        self._pipeline_context = {}

    def info_logging(self, pipeline_result):
        """
        Log relevant information for tracing purposes.
        """
        log.info(
            "Pipeline results for Open edX filter <%s>\n", pformat(pipeline_result, depth=2),
        )

    def debug_logging(self, filter_type, current_configuration):
        """
        Log relevant information for debugging purposes.
        """
        message = (
            "Pipeline execution for Open edX filter <%s>\n"
            "Pipeline contexts during execution:\n%s\n"
            "Steps contexts during pipeline execution:\n%s\n"
            "Current filter configuration:%s"
        )
        log.debug(
            message,
            filter_type,
            pformat(self._pipeline_context, depth=2),
            pformat(self._steps_context, depth=2),
            pformat(current_configuration, depth=2),
        )

    def performance_logging(self, filter_type, current_configuration):
        """
        Log relevant information for performance monitoring purposes.
        """
        message = (
            "Pipeline execution for Open edX filter <%s>\n"
            "Steps contexts during pipeline execution:\n%s"
            "Pipeline contexts during execution:%s\n"
            "Current filter configuration:%s"
        )
        log.info(
            message,
            filter_type,
            pformat(self._pipeline_context, depth=2),
            pformat(self._steps_context, depth=2),
            pformat(current_configuration, depth=2),
        )

    def log_filter_execution(self, accumulated_output, filter_type, current_configuration):
        """
        Log relevant information for the filter execution.

        This function decides which type of logging is required by the filters
        configuration.
        """
        if current_configuration.get("debug_mode"):
            self.debug_logging(filter_type, current_configuration)
        elif current_configuration.get("performance_mode"):
            self.performance_logging(filter_type, current_configuration)
        else:
            self.info_logging(accumulated_output)

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


class OpenEdxPublicFilter(FiltersLoggingStrategy):
    """
    Custom class used to create Open edX Filters.
    """

    def __init__(self, filter_type):
        """
        Init method for OpenEdxPublicFilter definition class.

        Arguments:
            filter_type (str): name of the filter.
        """
        self.filter_type = filter_type
        self.current_configuration = get_filter_config(self.filter_type)
        super().__init__()

    def __repr__(self):
        """
        Represent OpenEdxPublicFilter as a string.
        """
        return "<OpenEdxPublicFilter: {filter_type}>".format(filter_type=self.filter_type)

    def run_pipeline(self, filter_name, *args, **kwargs):
        """
        Execute filters in order.

        Given a list of functions paths, this function will execute
        them using the Accumulative Pipeline pattern defined in
        docs/decisions/0003-hooks-filter-tooling-pipeline.rst

        Example usage:
            step_result = run_pipeline(
                'org.openedx.service.subject.filter.action.major_version',
                raise_exception=True,
                request=request,
                user=user,
            )
            >>> step_result
        {
            'result_test_1st_function': 1st_object,
            'result_test_2nd_function': 2nd_object,
        }

        Arguments:
            filter_name (str): determines which trigger we are listening to.
            It also specifies which filter configuration to use.

        Returns:
            accumulated_output (dict): accumulated outputs of the functions defined in pipeline.
            step_result (obj): return object of one of the pipeline functions. This will
            be the returned by the pipeline if one of the functions returns
            an object different than Dict or None.

        Exceptions raised:
            OpenEdxFilterException: custom exception re-raised when a function raises
            an exception of this type and raise_exception is set to True. This
            behavior is common when using filters.

        This pipeline implementation was inspired by: Social auth core. For more
        information check their Github repository:
        https://github.com/python-social-auth/social-core
        """
        pipeline, raise_exception = get_pipeline_configuration(filter_name)

        if not pipeline:
            return kwargs

        functions = get_functions_for_pipeline(pipeline)

        self.collect_pipeline_context(
            pipeline_steps=pipeline,
            raise_exception=raise_exception,
            initial_input=kwargs,
        )

        accumulated_output = kwargs.copy()
        for function in functions:
            try:
                step_result = function(*args, **accumulated_output) or {}

                self.collect_step_context(
                    function.__name__,
                    accumulated_output=accumulated_output,
                    step_result=step_result,
                )

                if not isinstance(step_result, dict):
                    log.info(
                        "Pipeline stopped by '%s' for returning an object.",
                        function.__name__,
                    )
                    return step_result
                accumulated_output.update(step_result)
            except OpenEdxFilterException as exception:
                self.collect_step_context(
                    function.__name__,
                    accumulated_output=accumulated_output,
                    step_exception=exception,
                )
                if raise_exception:
                    log.exception(
                        "Exception raised while running '%s':\n %s", function.__name__, exception,
                    )
                    raise
            except Exception as exception:  # pylint: disable=broad-except
                # We're catching this because we don't want the core to blow up
                # when a filter is broken. This exception will probably need some
                # sort of monitoring hooked up to it to make sure that these
                # errors don't go unseen.
                log.exception(
                    "Exception raised while running '%s': %s\n%s",
                    function.__name__,
                    exception,
                    "Continuing execution.",
                )
                self.collect_step_context(
                    function.__name__,
                    accumulated_output=accumulated_output,
                    step_exception=exception,
                )
                continue

        self.log_filter_execution(
            accumulated_output, self.filter_type, self.current_configuration,
        )
        return accumulated_output

    def execute_filter(self, **kwargs):
        """
        Send filters to all connected receivers.

        Used to send filters just like Django filters are sent. In addition,
        some validations are run on the arguments, and then relevant metadata
        that can be used for logging or debugging purposes is generated.
        Besides this behavior, send_filter behaves just like the send method.

        Example usage:

        >>> data = STUDENT_REGISTRATION_STARTED.execute_filter(
        ...         user=UserData(
        ...             pii=UserPersonalData(
        ...                 username=data.get('username'),
        ...                 email=data.get('email'),
        ...                 name=data.get('name'),
        ...             )
        ...         )
        ...     )

        Returns:
            dict: Open edX filter pipeline step_result. For a detailed explanation
            checkout docs/decisions/0003-hooks-filter-tooling-pipeline.rst

        Exceptions raised:
            ExecutionValidationError: raised when there's a mismatch between
            arguments passed to this method and arguments used to initialize
            the filter.
        """
        return self.run_pipeline(self.filter_type, **kwargs)
