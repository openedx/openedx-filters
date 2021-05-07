"""
Tests for pipeline runner used by filters.
"""
from unittest.mock import Mock, patch

from django.test import TestCase

from ..exceptions import HookFilterException
from ..pipeline import run_pipeline


class TestRunningPipeline(TestCase):
    """
    Test class to verify standard behavior of the Pipeline runner.
    """

    def setUp(self):
        """
        Setup common conditions for every test case.
        """
        super().setUp()
        self.kwargs = {
            "request": Mock(),
        }
        self.pipeline = Mock()
        self.hook_name = "openedx.service.context.location.type.vi"

    @patch("openedx_filters.pipeline.get_pipeline_configuration")
    @patch("openedx_filters.pipeline.get_functions_for_pipeline")
    def test_run_empty_pipeline(self, get_functions_mock, get_configuration_mock):
        """
        This method runs an empty pipeline, i.e, a pipeline without
        defined functions.

        Expected behavior:
            Returns the same input arguments.
        """
        get_configuration_mock.return_value = (
            [],
            True,
        )
        get_functions_mock.return_value = []

        result = run_pipeline(self.hook_name, **self.kwargs)

        get_configuration_mock.assert_called_once_with(
            "openedx.service.context.location.type.vi",
        )
        get_functions_mock.assert_not_called()
        self.assertDictEqual(result, self.kwargs)

    @patch("openedx_filters.pipeline.get_pipeline_configuration")
    @patch("openedx_filters.pipeline.get_functions_for_pipeline")
    def test_raise_hook_exception(self, get_functions_mock, get_configuration_mock):
        """
        This method runs a pipeline with a function that raises
        HookFilterException. This means that fail_silently must be set to
        False.

        Expected behavior:
            The pipeline re-raises the exception caught.
        """
        get_configuration_mock.return_value = {
            "pipeline": self.pipeline,
            "fail_silently": False,
        }
        exception_message = "There was an error executing filter X."
        function = Mock(side_effect=HookFilterException(message=exception_message))
        function.__name__ = "function_name"
        get_functions_mock.return_value = [function]
        log_message = "Exception raised while running '{func_name}':\n HookFilterException: {exc_msg}".format(
            func_name="function_name", exc_msg=exception_message,
        )

        with self.assertRaises(HookFilterException), self.assertLogs() as captured:
            run_pipeline(self.hook_name, **self.kwargs)
        self.assertEqual(
            captured.records[0].getMessage(), log_message,
        )

    @patch("openedx_filters.pipeline.get_pipeline_configuration")
    @patch("openedx_filters.pipeline.get_functions_for_pipeline")
    def test_not_raise_hook_exception(self, get_functions_mock, get_hook_config_mock):
        """
        This method runs a pipeline with a function that raises
        HookFilterException but raise_exception is set to False. This means
        fail_silently must be set to True or not defined.

        Expected behavior:
            The pipeline does not re-raise the exception caught.
        """
        get_hook_config_mock.return_value = (
            Mock(),
            False,
        )
        return_value = {
            "request": Mock(),
        }
        function_with_exception = Mock(side_effect=HookFilterException)
        function_without_exception = Mock(return_value=return_value)
        get_functions_mock.return_value = [
            function_with_exception,
            function_without_exception,
        ]

        result = run_pipeline(self.hook_name, **self.kwargs)

        self.assertDictEqual(result, return_value)
        function_without_exception.assert_called_once_with(**self.kwargs)

    @patch("openedx_filters.pipeline.get_pipeline_configuration")
    @patch("openedx_filters.pipeline.get_functions_for_pipeline")
    def test_not_raise_common_exception(self, get_functions_mock, get_hook_config_mock):
        """
        This method runs a pipeline with a function that raises a
        common Exception.

        Expected behavior:
            The pipeline continues execution after caughting Exception.
        """
        get_hook_config_mock.return_value = (
            self.pipeline,
            True,
        )
        return_value = {
            "request": Mock(),
        }
        function_with_exception = Mock(side_effect=ValueError("Value error exception"))
        function_with_exception.__name__ = "function_with_exception"
        function_without_exception = Mock(return_value=return_value)
        get_functions_mock.return_value = [
            function_with_exception,
            function_without_exception,
        ]
        log_message = (
            "Exception raised while running 'function_with_exception': "
            "Value error exception\nContinuing execution."
        )

        with self.assertLogs() as captured:
            result = run_pipeline(self.hook_name, **self.kwargs)

        self.assertEqual(
            captured.records[0].getMessage(), log_message,
        )
        self.assertDictEqual(result, return_value)
        function_without_exception.assert_called_once_with(**self.kwargs)

    @patch("openedx_filters.pipeline.get_pipeline_configuration")
    @patch("openedx_filters.pipeline.get_functions_for_pipeline")
    def test_getting_pipeline_result(self, get_functions_mock, get_hook_config_mock):
        """
        This method runs a pipeline with functions defined via configuration.

        Expected behavior:
            Returns the processed dictionary.
        """
        get_hook_config_mock.return_value = (
            self.pipeline,
            True,
        )
        return_value_1st = {
            "request": Mock(),
        }
        return_value_2nd = {
            "user": Mock(),
        }
        return_overall_value = {**return_value_1st, **return_value_2nd}
        first_function = Mock(return_value=return_value_1st)
        second_function = Mock(return_value=return_value_2nd)
        get_functions_mock.return_value = [
            first_function,
            second_function,
        ]

        result = run_pipeline(self.hook_name, **self.kwargs)

        first_function.assert_called_once_with(**self.kwargs)
        second_function.assert_called_once_with(**return_value_1st)
        self.assertDictEqual(result, return_overall_value)

    @patch("openedx_filters.pipeline.get_pipeline_configuration")
    @patch("openedx_filters.pipeline.get_functions_for_pipeline")
    def test_partial_pipeline(self, get_functions_mock, get_hook_config_mock):
        """
        This method runs a pipeline with functions defined via configuration.
        At some point, returns an object to stop execution.

        Expected behavior:
            Returns the object used to stop execution.
        """
        get_hook_config_mock.return_value = (
            self.pipeline,
            True,
        )
        return_value_1st = Mock()
        first_function = Mock(return_value=return_value_1st)
        first_function.__name__ = "first_function"
        second_function = Mock()
        get_functions_mock.return_value = [
            first_function,
            second_function,
        ]
        log_message = "Pipeline stopped by 'first_function' for returning an object."

        with self.assertLogs() as captured:
            result = run_pipeline(self.hook_name, **self.kwargs)

        self.assertEqual(
            captured.records[0].getMessage(), log_message,
        )
        first_function.assert_called_once_with(**self.kwargs)
        second_function.assert_not_called()
        self.assertEqual(result, return_value_1st)
