"""
Data attributes for filters within the architecture subdomain `learning`.

These attributes follow the form of attr objects specified in OEP-49 data
pattern.
"""
import socket
from datetime import datetime
from uuid import UUID, uuid1

import attr
from django.conf import settings

import openedx_filters


@attr.s(frozen=True)
class FiltersMetadata:
    """
    Attributes defined for Open edX Filters metadata object.

    The attributes defined in this class are a subset of the
    OEP-41: Asynchronous Server filter Message Format.

    Arguments:
        id (UUID): filter identifier.
        filter_name (str): name of the filter.
        minorversion (int): version of the filter type.
        source (str): logical source of an filter.
        sourcehost (str): physical source of the filter.
        time (datetime): timestamp when the filter was sent.
        sourcelib (str): Open edX Filters library version.
    """

    id = attr.ib(type=UUID, init=False)
    filter_name = attr.ib(type=str)
    minorversion = attr.ib(type=int, converter=attr.converters.default_if_none(0))
    source = attr.ib(type=str, init=False)
    sourcehost = attr.ib(type=str, init=False)
    time = attr.ib(type=datetime, init=False)
    sourcelib = attr.ib(type=tuple, init=False)

    def __attrs_post_init__(self):
        """
        Post-init hook that generates metadata for the Open edX filter.
        """
        # Have to use this to get around the fact that the class is frozen
        # (which we almost always want, but not while we're initializing it).
        # Taken from edX Learning Sequences data file.
        object.__setattr__(self, "id", uuid1())
        object.__setattr__(
            self,
            "source",
            "openedx/{service}/web".format(
                service=getattr(settings, "SERVICE_VARIANT", "")
            ),
        )
        object.__setattr__(self, "sourcehost", socket.gethostname())
        object.__setattr__(self, "time", datetime.utcnow())
        object.__setattr__(
            self, "sourcelib", tuple(map(int, openedx_filters.__version__.split(".")))
        )
