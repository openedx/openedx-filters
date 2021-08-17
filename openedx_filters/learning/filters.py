"""
Package where filters related to the learning subdomain are implemented.

The learning subdomain corresponds to {Architecture Subdomain} defined in
the OEP-41.
"""

from openedx_filters.learning.data import UserData, CourseEnrollmentData, CertificateData
from openedx_filters.tooling import OpenEdxPublicFilter

# .. filter_name: org.openedx.learning.student.registration.started.v1
# .. filter_name: STUDENT_REGISTRATION_COMPLETED
# .. filter_description: emitted when the user registration process in the LMS starts.
# .. filter_data: UserData
# .. filter_status: provisional
STUDENT_REGISTRATION_STARTED = OpenEdxPublicFilter(
    filter_name="org.openedx.learning.student.registration.started.v1",
    data={
        "user": UserData,
    }
)


# .. filter_name: org.openedx.learning.auth.session.login.started.v1
# .. filter_name: SESSION_LOGIN_STARTED
# .. filter_description: eemitted when the user's login process in the LMS starts.
# .. filter_data: UserData
# .. filter_status: provisional
SESSION_LOGIN_STARTED = OpenEdxPublicFilter(
    filter_name="org.openedx.learning.auth.session.login.started.v1",
    data={
        "user": UserData,
    }
)


# .. filter_name: org.openedx.learning.course.enrollment.started.v1
# .. filter_name: COURSE_ENROLLMENT_CREATED
# .. filter_description: emitted when the user's enrollment process starts.
# .. filter_data: CourseEnrollmentData
# .. filter_status: provisional
COURSE_ENROLLMENT_STARTED = OpenEdxPublicFilter(
    filter_name="org.openedx.learning.course.enrollment.started.v1",
    data={
        "enrollment": CourseEnrollmentData,
    }
)


# .. filter_name: org.openedx.learning.course.unenrollment.started.v1
# .. filter_name: COURSE_ENROLLMENT_CHANGED
# .. filter_description: emitted when the user's unenrollment process starts.
# .. filter_data: CourseEnrollmentData
# .. filter_status: provisional
COURSE_UNENROLLMENT_STARTED= OpenEdxPublicFilter(
    filter_name="org.openedx.learning.course.unenrollment.completed.v1",
    data={
        "enrollment": CourseEnrollmentData,
    }
)


# .. filter_name: org.openedx.learning.certificate.creation.started.v1
# .. filter_name: CERTIFICATE_CREATED
# .. filter_description: emitted when the user's certificate creation process starts.
# .. filter_data: CertificateData
# .. filter_status: provisional
CERTIFICATE_CREATION_STARTED = OpenEdxPublicFilter(
    filter_name="org.openedx.learning.certificate.created.v1",
    data={
        "certificate": CertificateData,
    }
)

# .. filter_name: org.openedx.learning.certificate.change.started.v1
# .. filter_name: CERTIFICATE_CREATED
# .. filter_description: emitted when the user's certificate modification process starts.
# .. filter_data: CertificateData
# .. filter_status: provisional
CERTIFICATE_CHANGE_STARTED = OpenEdxPublicFilter(
    filter_name="org.openedx.learning.certificate.created.v1",
    data={
        "certificate": CertificateData,
    }
)



# .. filter_name: org.openedx.learning.certificate.revoke.started.v1
# .. filter_name: CERTIFICATE_REVOKED
# .. filter_description: emitted when the user's certificate annulation process starts.
# .. filter_data: CertificateData
# .. filter_status: provisional
CERTIFICATE_REVOKE_STARTED = OpenEdxPublicFilter(
    filter_name="org.openedx.learning.certificate.revoked.v1",
    data={
        "certificate": CertificateData,
    }
)
