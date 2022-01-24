"""
Tooling necessary to use Open edX Filters.
"""
from logging import getLogger

from django.conf import settings
from django.utils.module_loading import import_string

from openedx_filters.exceptions import OpenEdxFilterException

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
    def get_steps_for_pipeline(cls, pipeline, fail_silently):
        """
        Get pipeline objects from paths.

        Helper function that given a pipeline with step paths gets
        the objects related to each path.

        Example usage:
            steps = get_steps_for_pipeline(
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

        Arguments:
            pipeline (list): paths where steps are defined.
            fail_silently (bool): True meaning it won't raise exceptions and
            False the opposite.

        Returns:
            step_list (list): class objects defined in pipeline.
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
    def get_pipeline_configuration(cls):
        """
        Get pipeline configuration from filter settings.

        Helper function used to get the configuration needed to execute
        the Pipeline Runner. It will take from the hooks configuration
        the list of functions to execute and how to execute them.

        Example usage:
            pipeline_config = cls.get_pipeline_configuration()
            >>> pipeline_config
                (
                    [
                        'my_plugin.hooks.filters.PipelineStepV1',
                        'my_plugin.hooks.filters.PipelineStepV2',
                    ],
                )

        Returns:
            pipeline (list): paths where functions for the pipeline are
            defined.
            fail_silently (bool): defines whether exceptions are raised while
            executing the pipeline associated with a filter. It's determined by
            fail_silently configuration, True meaning it won't raise exceptions and
            False the opposite.
            extra_config: anything else defined in the dictionary.
        """
        filter_config = cls.get_filter_config()

        pipeline, fail_silently, extra_config = [], True, {}

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
    def get_filter_config(cls):
        """
        Get filters configuration from settings.

        Helper function used to get configuration needed for using
        Hooks Extension Framework.

        Example usage:
                configuration = get_filter_config('trigger')
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

                Where:
                    - pipeline (list): paths where the functions to be executed by
                    the pipeline are defined.
                    - fail_silently (bool): determines whether the pipeline can
                    raise exceptions while executing. If its value is True then
                    common exceptions (TypeError, ImportError...) are caught and
                    the execution continues, if False then exceptions are re-raised and the
                    execution fails.
                    - The rest: anything else defined in the dictionary.

        Arguments:
            filter_name (str): determines which configuration to use.

        Returns:
            filters configuration (dict): taken from Django settings
            containing filters configuration.
        """
        filters_config = getattr(settings, "OPEN_EDX_FILTERS_CONFIG", {})

        return filters_config.get(cls.filter_type, {})

    @classmethod
    def run_pipeline(cls, **kwargs):
        """
        Execute filters in order.

        Given a list of functions paths, this function will execute
        them using the Accumulative Pipeline pattern defined in
        docs/decisions/0003-hooks-filter-tooling-pipeline.rst

        Example usage:
            filter_result = OpenEdxPublicFilter.run_filter(
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
            result (obj): return object of one of the pipeline functions. This will
            be the returned by the pipeline if one of the functions returns
            an object different than Dict or None.

        Exceptions raised:
            OpenEdxFilterException: custom exception re-raised when a function raises
            an exception of this type. This behavior is common when using filters
            to halt application execution.

        This pipeline implementation was inspired by: Social auth core. For more
        information check their Github repository:
        https://github.com/python-social-auth/social-core
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
