.. _quickstart:

Quickstart
==========

The goal of ``WingCommander`` is to be easy to write a command line interface for
an application.  Getting an application up and running takes three simple steps:

#. Defining the application base class
#. Adding commands to the application
#. Constructing the application from the base class and running it

Definition
----------

In order to define the application, you just need to define the class using the
``WingCommander`` class included in the module::

   from wingcommander import WingCommander

   class LunchOrderer(WingCommander):
      ordered = []
      location = []

Once this is done, you can begin adding in commands for the application.

Adding Commands
---------------

Once you have a class defined for your application, you can begin adding in commands
to the interface using the ``.command`` method as a decorator::

   @LunchOrderer.command
   def ordered(lunch):
      ''' ordered -
         Tells you want you have already ordered.
      '''
      return lunch.ordered[-1] if len(lunch.ordered) else None

Now you can see what you last ordered with the ``ordered`` command.  But how can you
see what you last ordered without first being able to order.  Let's add that ability
with some of our favorite lunches::

   @LunchOrderer.command(completions=
      { "chikfila": ["sandwich", "nuggets", "fries"],
        "kfc": ["drumsticks", "wings"],
        "chinese": ["kungpao", "friedrice", "lomein"] })
   def order(lunch, place, food):
      lunch.location.append(place)
      lunch.ordered.append(food)
      return "You ordered {} from {}".format(food, place)

Now you can order some food with the ``order`` command.  It even gives you tab
completion for your favorite places and the foods that they serve!

Running Everything
------------------

Now all you need to do is run this.  There is an included ``run`` function which
takes care of starting the CLI application.  You just need::

   if __name__ == '__main__':
      orderer = LunchOrderer(name="Lunch")
      run(orderer)
