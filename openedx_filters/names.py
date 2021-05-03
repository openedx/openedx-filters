"""
Name of the filters used to index HOOKS_FILTER_CONFIG setting.

The naming convention is described in ADR #4 Filters naming convention
(docs/decisions/0004-filters-naming.rst).
"""
PRE_ENROLLMENT_CREATION = "org.openedx.lms.course_enrollment.creation.started.v1"
PRE_ENROLLMENT_DEACTIVATION = "org.openedx.lms.course_enrollment.deactivation.started.v1"
PRE_USER_REGISTRATION = "org.openedx.lms.auth.user.registration.started.v1"
PRE_USER_LOGIN = "org.openedx.lms.auth.session.login.started.v1"
