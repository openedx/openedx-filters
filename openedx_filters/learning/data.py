"""
Definitions that representing the Open edX platform filters.

All signals defined in this module must follow the name and versioning
conventions specified in docs/decisions/0002-events-naming-and-versioning.rst

They also must comply with the payload definition specified in
docs/decisions/0003-events-payload.rst
"""

"""
Data attributes for events within the architecture subdomain `learning`.
These attributes follow the form of attr objects specified in OEP-49 data
pattern.
"""
from datetime import datetime

import attr
from opaque_keys.edx.keys import CourseKey

@attr.s(frozen=True)
class UserNonPersonalData:
    """
    Attributes defined for Open edX user object based on non-PII data.

    Arguments:
        id (int): unique identifier for the Django User object.
        is_active (bool): indicates whether the user is active.
    """

    id = attr.ib(type=int)
    is_active = attr.ib(type=bool)


@attr.s(frozen=True)
class UserPersonalData(UserNonPersonalData):  # TODO: fix inheritance error
    """
    Attributes defined for Open edX user object based on PII data.

    Arguments:
        username (str): username associated with the Open edX user.
        email (str): email associated with the Open edX user.
        name (str): email associated with the Open edX user's profile.
    """

    username = attr.ib(type=str)
    email = attr.ib(type=str)
    name = attr.ib(type=str, factory=str)


@attr.s(frozen=True)
class UserData:
    """
    Attributes defined for Open edX user object.

    Arguments:
        pii (UserPersonalData): user's Personal Identifiable Information.
    """

    pii = attr.ib(type=UserPersonalData)


@attr.s(frozen=True)
class RegistrationData:
    """
    Attributes defined for Open edX user object.

    Arguments:
        pii (UserPersonalData): user's Personal Identifiable Information.
    """

    country = attr.ib(type=str)
    gender = attr.ib(type=str)
    year_of_birth = attr.ib(type=str)
    level_of_education = attr.ib(type=str)
    goals = attr.ib(type=str)


@attr.s(frozen=True)
class CourseData:
    """
    Attributes defined for Open edX Course Overview object.
    Arguments:
        course_key (str): identifier of the Course object.
        display_name (str): display name associated with the course.
        start (datetime): start date for the course.
        end (datetime): end date for the course.
    """

    course_key = attr.ib(type=CourseKey)
    display_name = attr.ib(type=str, factory=str)
    start = attr.ib(type=datetime, default=None)
    end = attr.ib(type=datetime, default=None)


@attr.s(frozen=True)
class CourseEnrollmentData:
    """
    Attributes defined for Open edX Course Enrollment object.

    Arguments:
        user (UserData): user associated with the Course Enrollment.
        course (CourseData): course where the user is enrolled in.
        mode (str): course mode associated with the course.
        is_active (bool): whether the enrollment is active.
        creation_date (datetime): creation date of the enrollment.
        created_by (UserData): if available, who created the enrollment.
    """

    user = attr.ib(type=UserData)
    course = attr.ib(type=CourseData)
    mode = attr.ib(type=str)
    is_active = attr.ib(type=bool, default=False)
    creation_date = attr.ib(type=datetime, default=None)
    created_by = attr.ib(type=UserData, default=None)


@attr.s(frozen=True)
class CertificateData:
    """
    Attributes defined for Open edX Certificate data object.

    Arguments:
        user (UserData): user associated with the Certificate.
        course (CourseData): course where the user obtained the certificate.
        mode (str): course mode associated with the course.
        grade (str): user's grade in this course run.
        current_status (str): current certificate status.
        previous_status (str): if available, pre-event certificate status.
        download_url (str): URL where the PDF version of the certificate.
        name (str): user's name.
    """

    user = attr.ib(type=UserData)
    course = attr.ib(type=CourseData)
    mode = attr.ib(type=str)
    grade = attr.ib(type=str)
    download_url = attr.ib(type=str)
    name = attr.ib(type=str)
    current_status = attr.ib(type=str)
    previous_status = attr.ib(type=str, factory=str)
