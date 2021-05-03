"""
Filters related to the un-enrollment process.

List of filters defined in this file:
    - before_deactivation: affects the application flow just before starting
    the un-enrollment process.

Each filter defined here must follow this naming rule:

...

def {Placement}.{Action}(...):
...

Where Placement can be:
    - after
    - during
    - before
    ...

And Action can be:
    - update
    - creation
    - activation
    - deactivation
    - deletion
    ...
"""
from openedx_filters.names import PRE_ENROLLMENT_DEACTIVATION
from openedx_filters.pipeline import run_pipeline


def before_deactivation(enrollment, *args, **kwargs):
    """
    Filter that executes just before the enrollment is soft-deleted.

    This filter can alter the un-enrollment flow, either by modifying the
    incoming enrollment or raising an error. It's placed before the
    enrollment is deactivated, so it's garanteed that the user has not
    been un-enrolled from the course yet.

    Example usage:

    Arguments:
        - enrollment (CourseEnrollment): user's Enrollment record for
        the Course.

    Raises:
    """
    kwargs.update({
        "enrollment": enrollment,
    })
    out = run_pipeline(
        PRE_ENROLLMENT_DEACTIVATION,
        *args,
        **kwargs
    )
    return out.get("enrollment")
