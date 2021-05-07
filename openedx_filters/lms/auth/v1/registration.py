"""
Filters related to the registration process.

Each filter function must follow this naming rule:
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
from openedx_filters.names import PRE_USER_REGISTRATION
from openedx_filters.pipeline import run_pipeline


def before_creation(data, *args, **kwargs):
    """
    Filter that executes just after the registration process starts.

    This filter can alter the registration flow, either by modifying the
    incoming user's data or raising an error. It's placed before the
    user and account creation, so it's garanteed that the user has not
    been registered yet.

    Example usage:

    Arguments:
        - data (querydict): data from the registration form filled by the
        user.

    Raises:
        - HookFilterException: re-raised by the pipeline runner
        when one of its functions raises it (due to an error,
        unfulfilled premisses, unmet business rule...).
    """
    kwargs.update({
        "data": data,
    })
    out = run_pipeline(
        PRE_USER_REGISTRATION,
        *args,
        **kwargs
    )
    return out.get("data")
