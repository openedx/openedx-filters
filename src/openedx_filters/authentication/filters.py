"""
Package where filters related to the authentication architectural subdomain are implemented.
"""

from typing import Any

from openedx_filters.authentication.types import FormDescriptionProtocol, ProviderConfigProtocol, RunningPipeline
from openedx_filters.tooling import OpenEdxPublicFilter


class LogistrationViewContextGenerated(OpenEdxPublicFilter):
    """
    Filter used to enrich or modify the combined login-and-registration page context.

    Purpose:
        This filter hooks into the legacy (server-rendered) login/registration flow. It is
        triggered just after the combined login/registration page context has been generated
        and just before the page is rendered, allowing pipeline steps to modify the context
        dict (e.g. alter sidebar content) based on external conditions.

    Filter Type:
        org.openedx.authentication.logistration_view.context.generated.v1

    Trigger:
        - Repository: openedx/edx-platform
        - Path: openedx/core/djangoapps/user_authn/views/login_form.py
        - Function or Method: login_and_registration_form
    """

    filter_type = "org.openedx.authentication.logistration_view.context.generated.v1"

    @classmethod
    def run_filter(cls, context: dict) -> dict:
        """
        Process the context through the configured pipeline steps.

        Arguments:
            context (dict): the template context dict for the login/registration page.

        Returns:
            dict: the (possibly modified) context.
        """
        data = super().run_pipeline(context=context)
        return data["context"]


class AuthnMFEContextGenerated(OpenEdxPublicFilter):
    """
    Filter used to enrich or modify the authentication MFE context.

    Purpose:
        This filter hooks into the modern authentication MFE (frontend-app-authn) flow. It is
        triggered just after the context served to the authentication micro-frontend has been
        generated, allowing pipeline steps to add or modify entries served to the MFE (e.g.
        branding data) based on external conditions. It is the MFE counterpart to
        LogistrationViewContextGenerated, which enriches the legacy server-rendered page's
        nested context.

        The context is split across two arguments because the caller may only know how to
        serve the entries it declares itself: pipeline steps modify entries the caller
        already declares through ``context``, and contribute entries the caller does not
        declare through ``extra_context``.

    Filter Type:
        org.openedx.authentication.mfe.context.generated.v1

    Trigger:
        - Repository: openedx/edx-platform
        - Path: openedx/core/djangoapps/user_authn/views/utils.py
        - Function or Method: get_mfe_context
    """

    filter_type = "org.openedx.authentication.mfe.context.generated.v1"

    @classmethod
    def run_filter(cls, context: dict, extra_context: dict) -> tuple[dict, dict]:
        """
        Process the context through the configured pipeline steps.

        Arguments:
            context (dict): the context dict served to the authentication MFE. Pipeline
                steps modify the entries the caller declares itself.
            extra_context (dict): additional entries to serve to the authentication MFE.
                Pipeline steps add entries the caller does not declare itself. The caller
                decides how these are merged into what it serves.

        Returns:
            tuple[dict, dict]:
                dict: the (possibly modified) context.
                dict: the (possibly populated) extra context.
        """
        data = super().run_pipeline(context=context, extra_context=extra_context)
        return (data["context"], data["extra_context"])


class LoginAltRedirectURLRequested(OpenEdxPublicFilter):
    """
    Filter used to determine an alternative redirect URL after a successful login.

    Purpose:
        This filter is triggered after a user has been authenticated, before the final redirect
        is issued. Any pipeline step may return an alternative redirect URL to send the user
        through additional post-login flows (e.g. an account-selection page).

    Filter Type:
        org.openedx.authentication.login.alt_redirect_url.requested.v1

    Trigger:
        - Repository: openedx/edx-platform
        - Path: openedx/core/djangoapps/user_authn/views/login.py
        - Function or Method: login_user
    """

    filter_type = "org.openedx.authentication.login.alt_redirect_url.requested.v1"

    @classmethod
    def run_filter(cls, redirect_url: str, user: Any) -> tuple[str, Any]:
        """
        Process the redirect URL through the configured pipeline steps.

        Arguments:
            redirect_url (str): the destination the caller intends to send the user to. A
                pipeline step that redirects elsewhere may attempt to preserve this URL by
                nesting it within another ``/?next=`` layer to create a chain of URLs.
            user (User): the authenticated Django user.

        Returns:
            tuple[str, User]: the (possibly modified) redirect URL and the user.
        """
        data = super().run_pipeline(redirect_url=redirect_url, user=user)
        return data["redirect_url"], data["user"]


class LoginFormGenerated(OpenEdxPublicFilter):
    """
    Filter used to modify the login form description after it has been generated.

    Purpose:
        This filter is triggered for every login form build, before the form fields are
        added. Pipeline steps may override field properties (e.g. defaults, visibility,
        restrictions). Field property overrides take effect when the fields are subsequently
        added, so steps run before field construction.

        Pipeline steps can pass field overrides (enabling dynamic field hiding), but
        cannot add fields of their own. At the time of this writing, there is no supported
        mechanism for adding custom login fields. The registration form, however, does
        support custom fields via the ``PROFILE_EXTENSION_FORM`` setting (or the
        deprecated ``REGISTRATION_EXTENSION_FORM``) in platform.

        The third-party auth state of the request is passed alongside the form description so
        that pipeline steps can tailor the form to the provider the user is authenticating
        with, without having to resolve that state themselves.

    Filter Type:
        org.openedx.authentication.login.form.generated.v1

    Trigger:
        - Repository: openedx/edx-platform
        - Path: openedx/core/djangoapps/user_authn/views/login_form.py
        - Function or Method: get_login_session_form
    """

    filter_type = "org.openedx.authentication.login.form.generated.v1"

    @classmethod
    def run_filter(
        cls,
        form_desc: FormDescriptionProtocol,
        running_pipeline: RunningPipeline | None,
        current_provider: ProviderConfigProtocol | None,
    ) -> tuple[FormDescriptionProtocol, RunningPipeline | None, ProviderConfigProtocol | None]:
        """
        Process the login form description through the configured pipeline steps.

        Arguments:
            form_desc (FormDescriptionProtocol): the login form description.
            running_pipeline (RunningPipeline): the third-party auth pipeline running for the
                request, or None when third-party auth is disabled or no pipeline is running.
            current_provider (ProviderConfigProtocol): the provider associated with the running
                pipeline, or None when there is no running pipeline or the provider could not
                be determined.

        Returns:
            tuple[FormDescriptionProtocol, RunningPipeline | None, ProviderConfigProtocol | None]:
            the (possibly modified) form description, the running pipeline, and the current
            provider.
        """
        data = super().run_pipeline(
            form_desc=form_desc,
            running_pipeline=running_pipeline,
            current_provider=current_provider,
        )
        return data["form_desc"], data["running_pipeline"], data["current_provider"]


class RegistrationFormGenerated(OpenEdxPublicFilter):
    """
    Filter used to modify the registration form description after it has been generated.

    Purpose:
        This filter is triggered for every registration form build, before the form fields
        are added. Pipeline steps may override field properties (e.g. defaults, visibility,
        restrictions). Field property overrides take effect when the fields are subsequently
        added, so steps run before field construction.

        Pipeline steps can pass field overrides (enabling dynamic field hiding), but
        cannot add fields of their own. If you need to add fields instead, use the
        ``PROFILE_EXTENSION_FORM`` setting (or the deprecated
        ``REGISTRATION_EXTENSION_FORM``) in platform.

        The third-party auth state of the request is passed alongside the form description so
        that pipeline steps can tailor the form to the provider the user is registering
        through, without having to resolve that state themselves.

    Filter Type:
        org.openedx.authentication.registration.form.generated.v1

    Trigger:
        - Repository: openedx/edx-platform
        - Path: openedx/core/djangoapps/user_authn/views/registration_form.py
        - Function or Method: RegistrationFormFactory.get_registration_form
    """

    filter_type = "org.openedx.authentication.registration.form.generated.v1"

    @classmethod
    def run_filter(
        cls,
        form_desc: FormDescriptionProtocol,
        running_pipeline: RunningPipeline | None,
        current_provider: ProviderConfigProtocol | None,
    ) -> tuple[FormDescriptionProtocol, RunningPipeline | None, ProviderConfigProtocol | None]:
        """
        Process the registration form description through the configured pipeline steps.

        Arguments:
            form_desc (FormDescriptionProtocol): the registration form description.
            running_pipeline (RunningPipeline): the third-party auth pipeline running for the
                request, or None when third-party auth is disabled or no pipeline is running.
            current_provider (ProviderConfigProtocol): the provider associated with the running
                pipeline, or None when there is no running pipeline or the provider could not
                be determined.

        Returns:
            tuple[FormDescriptionProtocol, RunningPipeline | None, ProviderConfigProtocol | None]:
            the (possibly modified) form description, the running pipeline, and the current
            provider.
        """
        data = super().run_pipeline(
            form_desc=form_desc,
            running_pipeline=running_pipeline,
            current_provider=current_provider,
        )
        return data["form_desc"], data["running_pipeline"], data["current_provider"]


class LogistrationViewRenderCompleted(OpenEdxPublicFilter):
    """
    Filter used to modify the rendered login/registration page response.

    Purpose:
        This filter hooks into the legacy (server-rendered) login/registration flow. It is
        triggered right after the combined login/registration page has been rendered, allowing
        pipeline steps to modify the response (e.g. set or delete cookies, add headers) using
        the final page context.

    Filter Type:
        org.openedx.authentication.logistration_view.render.completed.v1

    Trigger:
        - Repository: openedx/edx-platform
        - Path: openedx/core/djangoapps/user_authn/views/login_form.py
        - Function or Method: login_and_registration_form
    """

    filter_type = "org.openedx.authentication.logistration_view.render.completed.v1"

    @classmethod
    def run_filter(cls, response: Any, context: dict) -> tuple[Any, dict]:
        """
        Process the response and context through the configured pipeline steps.

        Arguments:
            response (HttpResponse): the rendered login/registration page response.
            context (dict): the template context dict used to render the page.

        Returns:
            tuple[HttpResponse, dict]: the (possibly modified) response and the context.
        """
        data = super().run_pipeline(response=response, context=context)
        return data["response"], data["context"]
