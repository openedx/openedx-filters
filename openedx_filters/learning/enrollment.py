"""
Package where filters related to the enrollment process are implemented.
"""
from openedx_filters.exceptions import OpenEdxFilterException
from openedx_filters.tooling import OpenEdxPublicFilter


class PreEnrollmentFilter(OpenEdxPublicFilter):
    """
    Custom class used to create PreEnrollment filters.
    """

    filter_type = "org.openedx.learning.course.enrollment.started.v1"

    class PreventEnrollment(OpenEdxFilterException):
        """
        Custom class used to stop the enrollment process.
        """

    @classmethod
    def run(cls, course_key, user, mode):
        """
        Executes a filter with the signature specified.

        Arguments:
            user (User):
            course_key (CourseKey): name of the filter.
            mode (str):
        """
        data = super().run_pipeline(
            user=user, course_key=course_key, mode=mode,
        )
        return data.get("user"), data.get("course_key"), data.get("mode")
