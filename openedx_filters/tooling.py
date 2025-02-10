"""
Tooling necessary to use Open edX Filters.
"""
from logging import getLogger
from typing import Any

from django.conf import settings
from django.utils.module_loading import import_string

from openedx_filters.exceptions import OpenEdxFilterException

log = getLogger(__name__)


class OpenEdxPublicFilter:
    """
    Custom class used to create Open edX Filters.
    """

    filter_type = ""

    def __repr__(self) -> str:
        """
        Represent OpenEdxPublicFilter as a string.
        """
        return "<OpenEdxPublicFilter: {filter_type}>".format(filter_type=self.filter_type)

    @classmethod
    def get_steps_for_pipeline(cls, pipeline: list, fail_silently: bool = True) -> list[type]:
        """
        Get pipeline objects from paths.

        Helper function that given a pipeline with step paths gets
        the objects related to each path.

        Arguments:
            pipeline (list): paths where steps are defined.
            fail_silently (bool): True meaning it won't raise exceptions and False the opposite.

        Returns:
            list: objects related to each path in the pipeline.

        Example usage:
            >>> steps = get_steps_for_pipeline(
                [
                    '1st_path_to_step',
                    ...
                ]
            )
            >>> steps
            [
                <class 1st_class at 0x00000000000>,
                <class 2nd_class at 0x00000000001>,
                ...
            ]

        """
        step_list = []
        for step_path in pipeline:
            try:
                function = import_string(step_path)
                step_list.append(function)
            except ImportError:
                log.exception("Failed to import: '%s'", step_path)
                if fail_silently:
                    continue
                raise

        return step_list

    @classmethod
    def get_pipeline_configuration(cls) -> tuple[list[str], bool, dict[str, Any]]:
        """
        Get pipeline configuration from filter settings.

        Helper function used to get the configuration needed to execute
        the Pipeline Runner. It will take from the hooks configuration
        the list of functions to execute and how to execute them.

        Returns:
            tuple: pipeline configuration with the following structure:
                - list: Paths where functions for the pipeline are defined.
                - bool: Indicates whether exceptions are raised while executing the pipeline associated with a filter.
                  Determined by the `fail_silently` configuration: `True` means it won't raise exceptions, and `False`
                  means the opposite.
                - dict: Extra configuration defined in the filter configuration.


        Example usage:
            >>> pipeline_config = cls.get_pipeline_configuration()
            >>> pipeline_config
                (
                    [
                        'my_plugin.hooks.filters.PipelineStepV1',
                        'my_plugin.hooks.filters.PipelineStepV2',
                    ],
                    False,
                    {
                        'log_level': 'debug'
                    }
                )
        """
        filter_config = cls.get_filter_config()

        pipeline: list = []
        fail_silently: bool = True
        extra_config: dict = {}

        if not filter_config:
            return pipeline, fail_silently, extra_config

        if isinstance(filter_config, dict):
            filter_config_copy = filter_config.copy()
            pipeline, fail_silently, extra_config = (
                filter_config_copy.pop("pipeline", []),
                filter_config_copy.pop("fail_silently", True),
                filter_config_copy,
            )

        elif isinstance(filter_config, list):
            pipeline = filter_config

        elif isinstance(filter_config, str):
            pipeline.append(filter_config)

        return pipeline, fail_silently, extra_config

    @classmethod
    def get_filter_config(cls) -> dict[str, Any]:
        """
        Get filters configuration from Django settings.

        Helper function used to get configuration needed for using a filter.

        Where:
            - pipeline (list): paths where the functions to be executed by the pipeline are defined.
            - fail_silently (bool): determines whether the pipeline can raise exceptions while executing.
               If its value is True then common exceptions (TypeError, ImportError...) are caught and
               the execution continues, if False then exceptions are re-raised and the execution fails.
            - The rest of the keys are extra configuration that can be used to customize the filter.

        Returns:
            dict: configuration for the filter type defined in the class.

        Example usage:
            >>> configuration = get_filter_config('trigger')
            >>> configuration
            {
                'pipeline':
                    [
                        'my_plugin.hooks.filters.PipelineStepV1',
                        'my_plugin.hooks.filters.PipelineStepV2',
                    ],
                'fail_silently': False,
                'log_level': 'debug'
            }
        """
        filters_config = getattr(settings, "OPEN_EDX_FILTERS_CONFIG", {})

        return filters_config.get(cls.filter_type, {})

    @classmethod
    def run_pipeline(cls, **kwargs: Any) -> dict[str, Any] | Any:
        """
        Execute filters in order based on the pipeline configuration.

        Given a list of pipeline steps, this function will execute them using the Accumulative Pipeline pattern
        as specified in :doc:`../decisions/0003-hooks-filter-tooling-pipeline`.

        Arguments:
            **kwargs: arguments to be passed to the pipeline steps.

        Returns:
            dict | Any: accumulated outputs of the pipelines that were executed or the return value of a pipeline step
                if it's not a dictionary.

        Raises:
            OpenEdxFilterException: exception re-raised when a pipeline step raises
                an exception of this type. This behavior is common when using filters
                to alter the application execution.

        This pipeline implementation was inspired by: Social auth core. For more
        information check their Github repository: https://github.com/python-social-auth/social-core

        Example usage:
            >>> result = OpenEdxPublicFilter.run_filter(user=user, course=course)
            >>> result
            {
                'result_1st_function': 1st_object,
                'result_2nd_function': 2nd_object,
            }
        """
        pipeline, fail_silently, extra_config = cls.get_pipeline_configuration()

        if not pipeline:
            return kwargs

        steps = cls.get_steps_for_pipeline(pipeline, fail_silently)
        filter_metadata = {
            "filter_type": cls.filter_type,
            "running_pipeline": pipeline,
            **extra_config,
        }

        accumulated_output = kwargs.copy()
        for step in steps:
            try:
                step_runner = step(**filter_metadata)
                result = step_runner.run_filter(**accumulated_output)

                if not isinstance(result, dict):
                    log.info(
                        "Pipeline stopped by '%s' for returning an object different from a dictionary.",
                        step.__name__,
                    )
                    return accumulated_output
                accumulated_output.update(result)
            except OpenEdxFilterException as exc:
                log.exception(
                    "Exception raised while running '%s':\n %s", step.__name__, exc,
                )
                raise
            except Exception as exc:
                # We're catching this because we don't want the core to blow up
                # when a filter is broken and fail_silently is False. Otherwise,
                # the pipeline resumes its execution.
                log.exception(
                    "Exception raised while running '%s': %s\n",
                    step.__name__,
                    exc,
                )
                if fail_silently:
                    continue
                raise

        return accumulated_output
