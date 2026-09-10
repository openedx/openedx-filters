"""
Tests for filters step definition.
"""
from unittest.mock import Mock

from django.test import TestCase

from openedx_filters.filters import PipelineStep


class TestPipelineStepDefinition(TestCase):
    """
    Test pipeline step definition for the hooks execution mechanism.
    """

    def test_pipeline_step_definition(self):
        """
        Test pipeline step definition with class PipelineStep.

        Expected behavior:
            Can't create a pipeline step without overriding the run_filter
            method.
        """
        pipeline_step = PipelineStep(
            "org.openedx.learning.student.registration.requested.v1",
            [Mock(), Mock()],
            extra_config={
                "extra_config": "something_meaningful",
            }
        )
        kwargs = {
            "user": Mock(),
        }

        with self.assertLogs(level="WARNING"):
            pipeline_step.run_filter(**kwargs)
