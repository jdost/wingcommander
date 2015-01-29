.. _completions:

Completions
===========

The completion engine provided by the base python ``cmd`` module is very confusing
and not easily approachable.  There are a few helper methods provided (and used by
default) to generate the completions for a command in the various stages of the
command composition.

Syntax Note
-----------

Throughout this page, there will be sections that show the state of a command being
composed and completions being requested.  The syntax used will include a character
``▯`` in the line where the completion is requested (this is normally done using
``<Tab>``).  So in::

   $ complete this▯

The completion will be for the ``this`` argument in the composition (based on the
``complete`` command).

Completion Function
-------------------

If you want to write your own completion function, you need to have it meet the
argument map compatible with the underlying readline interface used by the include
``cmd`` module.

The basic signature of the function used to generate completions looks like::

   def completion_func(current_argument, command_text, *_args)

- The ``*_args`` is just a collection of the other arguments passed in, they are
  ``begidx`` and ``endidx`` .
- The ``current_argument`` is the active "word" in the overall command composition.
- The ``command_text`` is the full argument string for the command being composed.

For example in the case of ::

   $ set name Mar▯

The values would be ``Mar`` for ``current_argument`` and ``set name Mar`` for
``command_text``.

Generation Helpers
------------------

You can also provide either a ``list`` or ``dict`` to be converted into a completion
function.  The ``list`` just dictates possible values that can be suggested
regardless of the state of the other arguments (the order is arbitrary).  So with a
completion set of ``foo, bar, baz`` the completions would be::

   $ complete foo ba▯
   bar baz
   $ complete ba▯
   bar baz
   $ complete foo bar ba▯
   bar baz

If you provide a ``dict``, the keys make up the first layer of suggestions for the
command.  Then the second layer is made up of the value of the key corresponding to
the first argument, if this value is a ``dict``, it is used the same way, if it is a
``list`` it behaves the same was as above.  If the completion set is::

   { "language": ["spanish", "french", "english"],
     "os": { "bsd": ["freebsd", "openbsd"],
             "linux": ["debian", "arch", "gentoo"] },
     "wm": ["xmonad", "openbox", "gnome"] }

The completions would look like::

   $ complete ▯
   language os wm
   $ complete lang▯
   language
   $ complete language ▯
   spanish french english
   $ complete os ▯
   bsd linux
   $ complete os linux ▯
   debian arch gentoo
   $ compelte os bsd ▯
   freebsd openbsd
