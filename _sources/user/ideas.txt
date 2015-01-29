.. _ideas

Ideas
=====

This is a page used to list various features and ideas for additional functionality
to be added, it includes notes/thoughts on how to implement the feature both in
terms of functionality and in terms of the language interface.

Piping
------

Being able to pipe commands into each other, this would also mean providing a set of
common replacements for commands that can be used to consume these piped in values
such as ``grep`` or ``cut`` among others.  This should ideally be used with a
command that produces a generator rather than dump out the result when all of the
data has been gathered.  Then the generated output could be tied as input for the
consuming functions.  A pipe consumer should produce a function based on the
arguments given that then takes a generator and returns a generator, which creates
data based on the output.

If the root function does not return a generator, the piping should still work (this
is how it works for things like ``uniq`` and ``sort`` in the shell).

.. History

.. Configuration
