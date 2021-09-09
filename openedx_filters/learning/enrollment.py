"""
Package where filters related to the enrollment process are implemented.
"""
from openedx_filters.exceptions import OpenEdxFilterException
from openedx_filters.tooling import OpenEdxPublicFilter


class PreEnrollmentFilter(OpenEdxPublicFilter):
    """
    Custom class used to create PreEnrollment filters.
    """

    class PreventEnrollment(OpenEdxFilterException):
        """
        Custom class used to stop the enrollment process.
        """

    def run(self, course_key, user, mode):
        """
        Executes a filter with the signature specified.

        Arguments:
            course_key (CourseKey): name of the filter.
            user (User):
            mode (str):
        """
        data = super().execute_filter(
            course_key=course_key, user=user, mode=mode,
        )

        return data.get("course_key"), data.get("user"), data.get("mode")
