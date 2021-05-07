"""
Pipeline runner used to execute list of functions (actions or filters).
"""
from logging import getLogger

from .exceptions import HookFilterException
from .utils import get_functions_for_pipeline, get_pipeline_configuration

log = getLogger(__name__)


def run_pipeline(hook_name, *args, **kwargs):
    """
    Execute filters in order.

    Given a list of functions paths, this function will execute
    them using the Accumulative Pipeline pattern defined in
    docs/decisions/0003-hooks-filter-tooling-pipeline.rst

    Example usage:
        result = run_pipeline(
            'org.openedx.service.subject.filter.action.major_version',
            raise_exception=True,
            request=request,
            user=user,
        )
        >>> result
       {
           'result_test_1st_function': 1st_object,
           'result_test_2nd_function': 2nd_object,
       }

    Arguments:
        hook_name (str): determines which trigger we are listening to.
        It also specifies which hook configuration defined through settings.

    Returns:
        out (dict): accumulated outputs of the functions defined in pipeline.
        result (obj): return object of one of the pipeline functions. This will
        be the returned by the pipeline if one of the functions returns
        an object different than Dict or None.

    Exceptions raised:
        HookFilterException: custom exception re-raised when a function raises
        an exception of this type and raise_exception is set to True. This
        behavior is common when using filters.

    This pipeline implementation was inspired by: Social auth core. For more
    information check their Github repository:
    https://github.com/python-social-auth/social-core
    """
    pipeline, raise_exception = get_pipeline_configuration(hook_name)

    if not pipeline:
        return kwargs

    functions = get_functions_for_pipeline(pipeline)

    out = kwargs.copy()
    for function in functions:
        try:
            result = function(*args, **out) or {}
            if not isinstance(result, dict):
                log.info(
                    "Pipeline stopped by '%s' for returning an object.",
                    function.__name__,
                )
                return result
            out.update(result)
        except HookFilterException as exc:
            if raise_exception:
                log.exception(
                    "Exception raised while running '%s':\n %s", function.__name__, exc,
                )
                raise
        except Exception as exc:  # pylint: disable=broad-except
            # We're catching this because we don't want the core to blow up
            # when a hook is broken. This exception will probably need some
            # sort of monitoring hooked up to it to make sure that these
            # errors don't go unseen.
            log.exception(
                "Exception raised while running '%s': %s\n%s",
                function.__name__,
                exc,
                "Continuing execution.",
            )
            continue

    return out
