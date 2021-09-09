"""
Package where filters related to the learning subdomain are implemented.

The learning subdomain corresponds to {Architecture Subdomain} defined in
the OEP-41.
"""
from openedx_filters.learning.enrollment import PreEnrollmentFilter

# .. filter_type: org.openedx.learning.course.enrollment.started.v1
# .. filter_name: COURSE_ENROLLMENT_CREATED
# .. filter_description: emitted when the user's enrollment process starts.
COURSE_ENROLLMENT_STARTED = PreEnrollmentFilter(
    filter_type="org.openedx.learning.course.enrollment.started.v1",
)
