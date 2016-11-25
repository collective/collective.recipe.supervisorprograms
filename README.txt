.. image:: https://travis-ci.org/collective/collective.recipe.supervisorprograms.svg?branch=master
   :target: https://travis-ci.org/collective/collective.recipe.supervisorprograms
   :alt: Build status

Overview
========

This recipe helps to configure the ``programs`` option of the `collective.recipe.supervisor`_
recipe.

Instead of doing this::

    [supervisor]
    recipe = collective.recipe.supervisor
    # (...)
    programs =
          10 process1 ${buildout:bin-directory}/process1
          20 process2 ${buildout:bin-directory}/process2

You'll do this::

    [supervisor]
    recipe = collective.recipe.supervisor
    programs = ${supervisor-programs:programs}

    [supervisor-programs]
    recipe = collective.recipe.supervisorprograms

    [process1-program]
    priority = 10
    command = {buildout:bin-directory}/process1

    [process2-program]
    priority = 20
    command = {buildout:bin-directory}/process2

All options accepted by ``collective.recipe.supervisor`` are supported.


Configuring programs
====================

The recipe will scan the buildout configuration looking for all sections with names ending in
``-program``. Each section will specify one program to be controlled by supervisor. The
``programs`` option of this recipe then will contain the value to be passed to the ``programs``
option of the ``collective.recipe.supervisor`` part.

The ``*-program`` sections accepts the following options:

- ``priority``
- ``command``
- ``args``
- ``directory``
- ``redirect-stderr``
- ``user``

Only ``priority`` and ``command`` are required. The value of the ``args`` option should not be
between ``[]``. Any other options will be inserted into the ``process_opts`` field of
``collective.recipe.supervisor``.

The ``process_name`` will be extracted from the section name.


Example usage
=============

We'll start by creating a buildout that uses the recipe::

    >>> write('buildout.cfg',
    ... """
    ... [buildout]
    ... parts = fake-supervisor
    ...
    ... [fake-supervisor]
    ... recipe = collective.recipe.supervisorprograms:printer
    ... programs = ${supervisor-programs:programs}
    ...
    ... [supervisor-programs]
    ... recipe = collective.recipe.supervisorprograms
    ...
    ... [program-base]
    ... redirect-stderr = true
    ...
    ... [first-program]
    ... <= program-base
    ... priority = 10
    ... command = bin/first
    ... directory = /tmp/first
    ...
    ... [second-program]
    ... <= program-base
    ... priority = 20
    ... command = bin/second
    ... directory = /tmp/second
    ... user = www-data
    ... args = -a -b --verbose=1
    ... startsecs = 10
    ...
    ... """)

The ``:printer`` recipe is used to print out the generated ``programs`` option. We don't want
to install supervisor just to test. In real life you would replace the ``fake-supervisor`` section
by::

    [supervisor]
    recipe = collective.recipe.supervisor
    # (...)
    programs = ${supervisor-programs:programs}

Also, we're using the inheritance feature of buildout (``<= program-base``) to show how to define
default parameters for all programs. It's use is optional.

Running the buildout gives us::

    >>> print 'start', system(buildout)
    start...
    programs = 10 first bin/first /tmp/first true
    20 second (startsecs=10) bin/second [-a -b --verbose=1] /tmp/second true www-data
    <BLANKLINE>

.. References

.. _`collective.recipe.supervisor`: http://pypi.python.org/pypi/collective.recipe.supervisor







