"""
Tooling necessary to use Open edX Filters.
"""
from openedx_filters.data import FiltersMetadata
from openedx_filters.exceptions import ExecutionValidationError
from openedx_filters.pipeline import run_pipeline


class OpenEdxPublicFilter:
    """
    Custom class used to create Open edX Filters.
    """

    def __init__(self, filter_name, data, minor_version=0):
        """
        Init method for OpenEdxPublicFilter definition class.

        Arguments:
            filter_name (str): name of the filter.
            data (dict): attributes passed to the filter.
            minor_version (int): version of the filter type.
        """
        self.init_data = data
        self.filter_name = filter_name
        self.minor_version = minor_version
        super().__init__()

    def __repr__(self):
        """
        Represent OpenEdxPublicFilter as a string.
        """
        return "<OpenEdxPublicFilter: {filter_name}>".format(filter_name=self.filter_name)

    def generate_filter_metadata(self):
        """
        Generate filter metadata when a filter is executed.

        These fields are generated on the fly and are a subset of the filter
        Message defined in the OEP-41.

        Example usage:
            >>> metadata = \
                STUDENT_REGISTRATION_COMPLETED.generate_filter_metadata()
                attr.asdict(metadata)
            {
                'filter_name': '...learning.student.registration.started.v1',
                'minorversion': 0,
                'time': '2021-06-09T14:12:45.320819Z',
                'sourcelib: (0,1,0,),
            }
        """
        return FiltersMetadata(
            filter_name=self.filter_name,
            minorversion=self.minor_version,
        )

    def execute_filter(self, **kwargs):
        """
        Send filters to all connected receivers.

        Used to send filters just like Django filters are sent. In addition,
        some validations are run on the arguments, and then relevant metadata
        that can be used for logging or debugging purposes is generated.
        Besides this behavior, send_filter behaves just like the send method.

        Example usage:

        >>> data = STUDENT_REGISTRATION_STARTED.execute_filter(
        ...         user=UserData(
        ...             pii=UserPersonalData(
        ...                 username=data.get('username'),
        ...                 email=data.get('email'),
        ...                 name=data.get('name'),
        ...             )
        ...         )
        ...     )

        Returns:
            dict: Open edX filter pipeline result. For a detailed explanation
            checkout docs/decisions/0003-hooks-filter-tooling-pipeline.rst

        Exceptions raised:
            ExecutionValidationError: raised when there's a mismatch between
            arguments passed to this method and arguments used to initialize
            the filter.
        """

        def validate_execution():
            """
            Run validations over the send arguments.

            The validation checks whether the send arguments match the
            arguments used when instantiating the filter. If they don't a
            validation error is raised.
            """
            if len(kwargs) != len(self.init_data):
                raise ExecutionValidationError(
                    filter_name=self.filter_name,
                    message="There's a mismatch between initialization data and send_filter arguments",
                )

            for key, value in self.init_data.items():
                argument = kwargs.get(key)
                if not argument:
                    raise ExecutionValidationError(
                        filter_name=self.filter_name,
                        message="Missing required argument '{key}'".format(key=key),
                    )
                if not isinstance(argument, value):
                    raise ExecutionValidationError(
                        filter_name=self.filter_name,
                        message="The argument '{key}' is not instance of the Class Attribute '{attr}'".format(
                            key=key, attr=value.__class__.__name__
                        ),
                    )

        validate_execution()

        return run_pipeline(self.filter_name, **kwargs)
