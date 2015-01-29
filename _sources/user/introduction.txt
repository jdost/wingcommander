.. _introduction:

Introduction
============

When trying to create Python applications that provide a convenient and easy to use
and write command line interface (CLI), there is no real option.  One can either
create a simple conditional chain and read using the ``input`` function, but lose
most of the strengths of a "rich" CLI such as a unix shell like Bash or Zsh.  Or
you can try and implement an application using the include ``cmd_`` module which
provides a well set up readline interface, but adding in commands, help text for
those commands, and enabling tab completion is confusing and unintuitive.

.. _cmd: https://docs.python.org/2/library/cmd.html

The goal of ``WingCommander`` is to provide a "pythonic" interface for writing
reusable functions that can be added into a common CLI application class that can
be easily executed and interacted with from the commandline.  The main goals are:

- *pythonic:* meaning the interface for adding and configuring commands for the
  application should use common python concepts and leverage built in features of
  the language
- *extensible:* adding commands to an application, replacing built in functionality,
  or adding in additional functionality should all be intuitive and easily achieved.
- *intuitive:* it should not be frustrating to switch from using a common unix shell
  like Zsh_ or Bash_ into a ``WingCommander`` based application, meaning things like
  tab completion and other common helper commands all carry through

.. _Zsh: http://zsh.sourceforge.net/
.. _Bash: http://www.gnu.org/software/bash/

How is this Pythonic?
---------------------

The interface makes heavy use of decorators to add additional functionality and
definition to a simple python function.  The decorators are meant to do the heavy
lifting and interfacing with the internal interface for the CLI application.  This
includes generating completions for a command based on any state of the command
line, using the docstring of the function to provide the helper text for the
command, and adding "smart" parsing rules for flags passed into a command (having
``-d`` and ``--debug`` mean the same thing).

If there is any point where how to implement some included functionality is
confusing or jarring, file and issue and it should be addressed.  This module is
meant to make writing CLI applications easy, not confusing.

Extending
---------

All of the included functionality uses simple interfaces that are also exposed by
the module.  So anything that is currently being done should also be possible to
quickly reimplement with your own changes.  None of those nested private attributes
and methods that you can't easily call or override.

Intuitive
---------

Being a *big* shell user, it is paramount for a CLI application to work in the same
sorts of ways as other commands in a shell.  Things such as piping, redirecting
input and output, tab completion, history searching, among others are all either
implemented, being implemented, or on the roadmap.  If there is some common shell
feature that is missing, file a feature request for it if it is not already on the
:doc:`ideas` page.
