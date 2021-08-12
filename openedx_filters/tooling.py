"""
Tooling necessary to use Open edX Filters.
"""
from openedx_filters.pipeline import run_pipeline


class OpenEdxPublicFilter:
    """
    Custom class used to create Open edX Filters.
    """

    def __init__(self, filter_name, data, minor_version=0):
        """
        Init method for OpenEdxPublicSignal definition class.

        Arguments:
            filter_name (str): name of the event.
            data (dict): attributes passed to the event.
            minor_version (int): version of the event type.
        """
        if not filter_name:
            raise InstantiationError(
                message="Missing required argument 'filter_name'"
            )
        if not data:
            raise InstantiationError(
                filter_name=filter_name, message="Missing required argument 'data'"
            )
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
        Generate filters metadata when an event is sent.

        These fields are generated on the fly and are a subset of the Event
        Message defined in the OEP-41.

        Example usage:
            >>> metadata = \
                STUDENT_REGISTRATION_STARTED.generate_filter_metadata()
                attr.asdict(metadata)
            {
                'filter_name': '...learning.student.registration.completed.v1',
                'minorversion': 0,
                'time': '2021-06-09T14:12:45.320819Z',
                'source': 'openedx/lms/web',
                'sourcehost': 'edx.devstack.lms',
                'specversion': '1.0',
                'sourcelib: (0,1,0,),
            }
        """
        return {}

    def execute_filter(self, **kwargs):
        """
        Send events to all connected receivers.

        Used to send events just like Django signals are sent. In addition,
        some validations are run on the arguments, and then relevant metadata
        that can be used for logging or debugging purposes is generated.
        Besides this behavior, send_event behaves just like the send method.

        Example usage:


        Keyword arguments:
            send_robust (bool): determines whether the Django signal will be
            sent using the method `send` or `send_robust`.

        Returns:
            list: response of each receiver following the format
            [(receiver, response), ... ]

        Exceptions raised:
            SenderValidationError: raised when there's a mismatch between
            arguments passed to this method and arguments used to initialize
            the event.
        """

        def validate_execution():
            """
            Run validations over the send arguments.

            The validation checks whether the send arguments match the
            arguments used when instantiating the event. If they don't a
            validation error is raised.
            """
            if len(kwargs) != len(self.init_data):
                raise SenderValidationError(
                    filter_name=self.filter_name,
                    message="There's a mismatch between initialization data and send_event arguments",
                )

            for key, value in self.init_data.items():
                argument = kwargs.get(key)
                if not argument:
                    raise SenderValidationError(
                        filter_name=self.filter_name,
                        message="Missing required argument '{key}'".format(key=key),
                    )
                if not isinstance(argument, value):
                    raise SenderValidationError(
                        filter_name=self.filter_name,
                        message="The argument '{key}' is not instance of the Class Attribute '{attr}'".format(
                            key=key, attr=value.__class__.__name__
                        ),
                    )

        validate_execution()
        run_pipeline(self.filter_name, self.data)
