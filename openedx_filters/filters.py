"""
Necessary classes used to define pipeline steps used by OpenEdxPublicFilter's pipeline runner.
"""
from abc import abstractmethod
from logging import getLogger

log = getLogger(__name__)


class PipelineStep:
    """
    Defines each step of the pipeline to be executed by the pipeline runner.

    Example usage:

        Let's say we want a filter step that changes enrollment modes:

        1. If the enrollment mode is honor, then changes it to no-id-professional.
        2. If it's other mode, then stop pipeline execution.

        This pipeline step can be used in conjunction with PreEnrollmentFilter, that's
        why the runner method accepts user, course_key and mode as arguments.

        class MyFilterStep(PipelineStep):

            def run_filter(self, user, course_key, mode):
                if mode != "honor":
                    return

                return {
                    "user": user,
                    "course_key": course_key,
                    "mode": "no-id-professional",
                }
        Another version would be:

        class MyFilterStep(PipelineStep):

            def run_filter(self, user, course_key, mode):
                if mode != "honor":
                    return

                return {"mode": "no-id-professional"}
    """

    def __init__(self, filter_type, running_pipeline, **extra_config):
        """
        Init method for PipelineStep base class.

        Arguments:
            filter_type (str): name of the filter.
            running_pipeline ([type]): list of steps currently running.
            extra_config (dict): extra configuration defined in OPEN_EDX_FILTERS_CONFIG.
        """
        self.filter_type = filter_type
        self.running_pipeline = running_pipeline
        self.extra_config = extra_config

    @abstractmethod
    def run_filter(self, **kwargs):
        """
        Abstract pipeline step runner.

        Used to implement custom code that'll be executed by OpenEdxPublicFilter's pipeline runner.
        It must be implemented by child classes.
        """
        log.warning(
            "PipelineStep run method not implemented.\n"
            "Child classes must implement this method with their custom code.\n"
            "By design, the pipeline expects either of three (3) types of returns:\n"
            "1. A dictionary with the arguments the method received. They can be modified in the process.\n"
            "2. None. Returning this will stop the pipeline execution. The accumulated output until "
            "this moment will be returned.\n"
            "3. An object different from a dict. Returning this will stop the pipeline execution. "
            "The accumulated output until this moment will be returned.\n"
        )
