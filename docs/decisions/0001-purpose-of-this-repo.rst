1. Purpose of this Repo
=======================

Status
------

Accepted


Context
-------

OEP-50 (Hooks Extension Framework) was written with the intention of defining a
common pattern to extend the platform in a number of locations in a very stable
way. After receiving feedback from different community members and edx arch
team, it was decided that the best path forward would be to create a repository
that holds the signature of the public promise made by the framework.


Decision
--------

In this repository will reside the functions that define the filter used by the
edx-platform repo. The same applies to the necessary tooling used by the Hooks
Extension Framework to manage the filter pipelines and extra tools.


Consequences
------------

All tools needed to manage filters will be implemented in this repository and
imported into Open edX platform.
Developers that want to extend to use filters on the defined hooks should also
import this repository as a dependency in their Open edX plugins and use the
same function definitions.
