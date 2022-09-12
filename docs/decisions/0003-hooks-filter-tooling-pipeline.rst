Filter tooling: pipeline behaviour
==================================

Status
------

Accepted


Context
-------

Taking into account the design considerations outlined in OEP-50 Hooks extension
framework about

1. The order of execution for multiple functions in a filter must be respected
2. The result of a previous function must be available to the current one in the
   form of a pipeline


See https://github.com/openedx/open-edx-proposals/pull/184 for more information.

To do this, we considered three similar approaches for the pipeline implementation:

1. Unix-like (how unix pipe operator works): the output of the previous function
   is the input of the next one. For the first function, includes the initial
   arguments.
2. Unix-like modified: the output of the previous function is the input of the
   next one including the initial arguments for all functions.
3. Accumulative: the output of every (i, …, i-n) function is accumulated using a
   data structure and fed into the next function i-n+1, including the initial
   arguments. We draw inspiration from python-social-auth/social-core.
   See: https://github.com/python-social-auth/social-core

These approaches follow the pipeline pattern and have as main difference what
each function receive as input.

It is important to emphasize that the main objectives with this implementation
are: to have function interchangeability and to maintain the function signature
of a filter defined by the Hooks Extension Framework.


Decision
--------

We decided to use the accumulative approach as the only pipeline for filters.


Consequences
------------

1. The order of execution is maintained.
2. Given that all pipeline functions will expect the same input arguments,
   i.e accumulated output plus initial arguments, their signature will stay the
   same. And for this reason, these functions are interchangeable.
3. To avoid any mismatch filters must have \*args and \*\*kwargs in their
   function definition.
