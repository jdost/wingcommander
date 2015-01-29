.. Wing Commander documentation master file, created by
   sphinx-quickstart on Sun Jan 25 22:24:25 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Wing Commmander
===============

Wing Commander is a Python Library to ease the creation of command line interface
(CLI) applications.  It extends the built in cmd_ library to make the setup more
pythonic by using decorators and leveraging things like docstrings and providing
helpers for other things.

.. _cmd: https://docs.python.org/2/library/cmd.html

::

   from wingcommander import WingCommander


   class MyShellApplication(WingCommander):
      pass

   @MyShellApplication.command
   def hello(shell, *args):
      ''' Greets whatever you tell it to.
      '''
      return ' '.join(["hello"] + args)


Contents:

.. toctree::
   :maxdepth: 2

   user/introduction
   user/quickstart
   user/completions
   api
