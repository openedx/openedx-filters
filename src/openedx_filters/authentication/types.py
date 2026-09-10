"""
Structural types shared by filters in the authentication subdomain.

These declare the shape of the payloads that filters in this subdomain pass to their pipeline
steps, so that both the caller producing them and the pipeline step consuming them can be
checked against a single shared definition:

* the ``TypedDict`` declarations describe the mappings the filters pass along, and
* the structural (PEP 544) ``Protocol`` declarations describe the minimal surface of the
  objects the filters pass along, without coupling the filters to any concrete platform
  implementation.
"""

from typing import Any, Protocol, Required, TypedDict


class RunningPipelineKwargs(TypedDict, total=False):
    """
    Partial shape of a paused authentication pipeline's accumulated keyword arguments.

    ``details`` and ``response`` are the only two keys that may be accessed
    unconditionally; the rest should be read with ``.get()``, because their values depend
    on how far the pipeline had progressed
    """

    details: Required[dict[str, Any]]
    response: Required[dict[str, Any]]
    username: str | None
    uid: str | None
    is_new: bool
    new_association: bool
    auth_entry: str
    user: Any
    social: Any


class RunningPipeline(TypedDict):
    """
    Shape of the authentication pipeline state for a request.

    This is the payload that the login and registration form filters pass to their pipeline
    steps to describe the authentication attempt in flight, so that steps can tailor the form
    to the provider the user is authenticating with.

    Unlike its ``kwargs`` member, this mapping is built by its caller as a complete literal
    with exactly these two keys, so it is declared with both of them required: adding,
    omitting or misspelling a key is an error on the caller's side.

    ``backend`` names the authentication backend driving the attempt, and ``kwargs`` holds the
    keyword arguments the pipeline has accumulated so far.
    """

    kwargs: RunningPipelineKwargs
    backend: str


class FormDescriptionProtocol(Protocol):
    """
    Structural interface of the FormDescription object passed to the form-override filters.

    Only the minimal surface consumed by pipeline steps is declared here. Pipeline steps
    should not rely on anything beyond this protocol.

    This protocol is deliberately limited to overriding the properties of fields the
    caller already defines. Adding new registration fields is instead the job of the
    ``PROFILE_EXTENSION_FORM`` setting (or the deprecated ``REGISTRATION_EXTENSION_FORM``)
    in platform settings, which covers ingestion, persistence, and ordering. Custom login
    fields, however, cannot be added at the time of this writing.
    """

    def override_field_properties(
        self,
        field_name: str,
        /,
        *,
        default: Any = ...,
        field_type: str = ...,
        label: str = ...,
        instructions: str = ...,
        restrictions: dict = ...,
    ) -> None:
        """Override the given properties of the named form field."""
        ...  # pylint: disable=unnecessary-ellipsis


class ProviderConfigProtocol(Protocol):
    """
    Structural interface of the third-party auth provider configuration.

    Only the minimal surface consumed by pipeline steps is declared here. Pipeline steps
    should not rely on anything beyond this protocol.
    """

    provider_id: str
    skip_registration_form: bool

    def get_register_form_data(self, pipeline_kwargs: RunningPipelineKwargs, /) -> dict:
        """Return the registration form field values prefilled by the provider."""
        ...  # pylint: disable=unnecessary-ellipsis
