"""
Tests for authentication subdomain filters.
"""
from unittest.mock import Mock

from django.test import TestCase

from openedx_filters.authentication.filters import (
    AuthnMFEContextGenerated,
    LoginAltRedirectURLRequested,
    LoginFormGenerated,
    LogistrationViewContextGenerated,
    LogistrationViewRenderCompleted,
    RegistrationFormGenerated,
)
from openedx_filters.authentication.types import RunningPipeline


class TestLogistrationViewContextGeneratedFilter(TestCase):
    """
    Tests for the LogistrationViewContextGenerated filter.
    """

    def test_filter_type(self):
        assert LogistrationViewContextGenerated.filter_type == \
            "org.openedx.authentication.logistration_view.context.generated.v1"

    def test_run_filter_passes_through_context(self):
        context = {"data": {}}

        returned_context = LogistrationViewContextGenerated.run_filter(context)

        assert returned_context is context


class TestAuthnMFEContextGeneratedFilter(TestCase):
    """
    Tests for the AuthnMFEContextGenerated filter.
    """

    def test_filter_type(self):
        assert AuthnMFEContextGenerated.filter_type == "org.openedx.authentication.mfe.context.generated.v1"

    def test_run_filter_passes_through_all_arguments(self):
        context = {"countryCode": "US"}
        extra_context = {}

        returned_context, returned_extra_context = AuthnMFEContextGenerated.run_filter(context, extra_context)

        assert returned_context is context
        assert returned_extra_context is extra_context


class TestLoginAltRedirectURLRequestedFilter(TestCase):
    """
    Tests for the LoginAltRedirectURLRequested filter.
    """

    def test_filter_type(self):
        assert LoginAltRedirectURLRequested.filter_type == \
            "org.openedx.authentication.login.alt_redirect_url.requested.v1"

    def test_run_filter_passes_through_all_arguments(self):
        user = Mock()

        returned_url, returned_user = LoginAltRedirectURLRequested.run_filter("/dashboard", user)

        assert returned_url == "/dashboard"
        assert returned_user is user


class TestLoginFormGeneratedFilter(TestCase):
    """
    Tests for the LoginFormGenerated filter.
    """

    def test_filter_type(self):
        assert LoginFormGenerated.filter_type == \
            "org.openedx.authentication.login.form.generated.v1"

    def test_run_filter_passes_through_all_arguments(self) -> None:
        form_desc = Mock()
        running_pipeline: RunningPipeline = {
            "kwargs": {"details": {}, "response": {}},
            "backend": "tpa-saml",
        }
        current_provider = Mock()

        returned_form_desc, returned_pipeline, returned_provider = LoginFormGenerated.run_filter(
            form_desc, running_pipeline, current_provider,
        )

        assert returned_form_desc is form_desc
        assert returned_pipeline is running_pipeline
        assert returned_provider is current_provider

    def test_run_filter_passes_through_absent_third_party_auth_state(self):
        form_desc = Mock()

        returned_form_desc, returned_pipeline, returned_provider = LoginFormGenerated.run_filter(
            form_desc, None, None,
        )

        assert returned_form_desc is form_desc
        assert returned_pipeline is None
        assert returned_provider is None


class TestRegistrationFormGeneratedFilter(TestCase):
    """
    Tests for the RegistrationFormGenerated filter.
    """

    def test_filter_type(self):
        assert RegistrationFormGenerated.filter_type == \
            "org.openedx.authentication.registration.form.generated.v1"

    def test_run_filter_passes_through_all_arguments(self) -> None:
        form_desc = Mock()
        running_pipeline: RunningPipeline = {
            "kwargs": {"details": {}, "response": {}},
            "backend": "tpa-saml",
        }
        current_provider = Mock()

        returned_form_desc, returned_pipeline, returned_provider = RegistrationFormGenerated.run_filter(
            form_desc, running_pipeline, current_provider,
        )

        assert returned_form_desc is form_desc
        assert returned_pipeline is running_pipeline
        assert returned_provider is current_provider

    def test_run_filter_passes_through_absent_third_party_auth_state(self):
        form_desc = Mock()

        returned_form_desc, returned_pipeline, returned_provider = RegistrationFormGenerated.run_filter(
            form_desc, None, None,
        )

        assert returned_form_desc is form_desc
        assert returned_pipeline is None
        assert returned_provider is None


class TestLogistrationViewRenderCompletedFilter(TestCase):
    """
    Tests for the LogistrationViewRenderCompleted filter.
    """

    def test_filter_type(self):
        assert LogistrationViewRenderCompleted.filter_type == \
            "org.openedx.authentication.logistration_view.render.completed.v1"

    def test_run_filter_passes_through_all_arguments(self):
        response = Mock()
        context = {"enable_sidebar": False}

        returned_response, returned_context = LogistrationViewRenderCompleted.run_filter(response, context)

        assert returned_response is response
        assert returned_context is context
