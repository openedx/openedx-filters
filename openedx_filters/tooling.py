"""
Tooling necessary to use Open edX Filters.
"""
from logging import getLogger

from openedx_filters.exceptions import OpenEdxFilterException
from openedx_filters.utils import get_functions_for_pipeline, get_pipeline_configuration

log = getLogger(__name__)


class OpenEdxPublicFilter:
    """
    Custom class used to create Open edX Filters.
    """

    filter_type = ""

    def __repr__(self):
        """
        Represent OpenEdxPublicFilter as a string.
        """
        return "<OpenEdxPublicFilter: {filter_type}>".format(filter_type=self.filter_type)

    @classmethod
    def run_pipeline(cls, *args, **kwargs):
        """
        Execute filters in order.

        Given a list of functions paths, this function will execute
        them using the Accumulative Pipeline pattern defined in
        docs/decisions/0003-hooks-filter-tooling-pipeline.rst

        Example usage:
            filter_result = OpenEdxPublicFilter.run(
                user=user,
            )
            >>> filter_result
            {
                'result_test_1st_function': 1st_object,
                'result_test_2nd_function': 2nd_object,
            }

        Arguments:
            filter_name (str): determines which trigger we are listening to.
            It also specifies which filter configuration to use.

        Returns:
            accumulated_output (dict): accumulated outputs of the functions defined in pipeline.
            filter_result (obj): return object of one of the pipeline functions. This will
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
        pipeline, raise_exception = get_pipeline_configuration(cls.filter_type)

        if not pipeline:
            return kwargs

        functions = get_functions_for_pipeline(pipeline)

        accumulated_output = kwargs.copy()
        for function in functions:
            try:
                step_result = function(*args, **accumulated_output) or {}

                if not isinstance(step_result, dict):
                    log.info(
                        "Pipeline stopped by '%s' for returning an object.",
                        function.__name__,
                    )
                    return step_result
                accumulated_output.update(step_result)
            except OpenEdxFilterException as exception:
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
                continue

        return accumulated_output
