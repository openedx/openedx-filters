"""
Filters related to the login process.

Each filter must follow this naming rule:
...

def {Placement}.{Action}(...):
...

Where Placement can be:
    - after
    - during
    - before

And Action can be:
    - update
    - creation
    - activation
    - deactivation
    - deletion
    ...
"""
from openedx_filters.names import PRE_USER_LOGIN
from openedx_filters.pipeline import run_pipeline


def before_creation(user, *args, **kwargs):
    """
    Filter that executes just after the login process starts.

    This filter can alter the login flow, either by modifying the
    incoming user or raising an error. It's placed before the
    auth session is created, so it's garanteed that the user
    has not been logged in yet.

    Example usage:
        To be provided.

    Arguments:
        - user (User): Django User object associated with the
        email used in the login form.

    Raises:
        - HookFilterException: re-raised by the pipeline runner
        when one of its functions raises it (due to an error,
        unfulfilled premisses, unmet business rule...).
    """
    kwargs.update({
        "user": user,
    })
    out = run_pipeline(
        PRE_USER_LOGIN,
        *args,
        **kwargs
    )
    return out.get("user")
