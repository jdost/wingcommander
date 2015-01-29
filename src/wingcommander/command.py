from wingcommander.util import gen_completion
import types


class Command(object):
    '''Wrapper class for commands/actions used in a
    :class:`WingCommander <WingCommander>`

    Base wrapper for the commands used in the ``WingCommander`` controller.
    It is meant to provide an accessible and extensible API around the
    functionality added via the CLI behavior of the controller.

    Can be created manually and imported::

        def echo_func(cmd, *args):
            return " ".join(args)

        echo = Command(echo_func)
        echo.update_help("echoes whatever you give it")
        ShellApp.command(cmd=echo)

    '''
    def __init__(self, command):
        self.__name__ = command.__name__
        self.parent = None
        self.help_text = command.__doc__
        self.complete = None
        self.__command__ = command
        self.__doc__ = lambda x: self.help_text

    def update_help(self, txt):
        '''Updates the help text associated with the ``Command`` in the master
        application.

        :param txt: string containing the new help text to be displayed by the
         help command for this command.
        '''
        self.help_text = txt if isinstance(txt, str) \
            and len(txt) > 0 else self.help_text

    def update_completion(self, completions):
        ''' Updates the completion set for the ``Command`` in the command line
        interface. This takes any of the :doc:`user/completions` accepted types
        and generates a new tab completion function.  This can be a ``list`` of
        any possible arguments that can be completed at any position, a
        ``dict`` of arguments based on inherited position, or a function that
        will be used as the entire completion function.

        :param completions: completion set as described above and in the
         :doc:`user/completions` section.
        '''
        self.complete = gen_completion(completions)

    def __help__(self):
        print self.help_text

    def __complete__(self, *args, **kwargs):
        ''' __complete__
        Generates the completion set based on the current state of the command
        being authored.
        '''
        return self.complete(*args, **kwargs) if self.complete else None

    def __call__(self, cmdr, *args, **kwargs):
        pass_generator = kwargs.get("pass_generator", False)
        if "pass_generator" in kwargs:
            del kwargs["pass_generator"]

        output = self.__command__(cmdr, *args, **kwargs)

        if isinstance(output, types.GeneratorType) and not pass_generator:
            output = map(lambda x: x, output)

        if isinstance(output, tuple):
            output = list(output)
        elif isinstance(output, str):
            output = output.split('\n')

        return output

    def __call_split__(self, cmdr, args):
        ''' Wrapper to handle translating the input from the command line
        interface and returning the command's output in conjunction with the
        ``WingCommander`` master class.

        :param cmdr: The ``self`` reference to the ``WingCommander`` parent
        instance calling the command.
        :param args: string that represents the arguments following the
        execution of the command.
        '''
        output = self.__call__(self, cmdr, *args.split(' '),
                               pass_generator=True)
        if isinstance(output, list):
            print '\n'.join(output)
            return len(output) == 0
        elif isinstance(output, types.GeneratorType):
            for line in output:
                print line
            return True

        return output

    def __attach__(self, cmdr):
        ''' Associates/attaches this ``Command`` object with the parent class
        instance that it is passed.

        :param cmdr: The ``WingCommander`` class definition to register this
        command with.
        '''
        setattr(cmdr, "do_" + self.__name__, self.__call_split__)
        setattr(cmdr, "help_" + self.__name__, self.__help__)
        if self.complete:
            setattr(cmdr, "complete_" + self.__name__, self.__complete__)

        self.parent = cmdr
