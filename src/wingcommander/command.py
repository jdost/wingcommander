from wingcommander.util import gen_completion
import types


class Command(object):
    def __init__(self, command):
        ''' Command
        Base wrapper for the commands used in the WingCommander controller.
        It is meant to provide an accessible and extensible API around the
        functionality added via the CLI behavior of the controller.
        '''
        self.__name__ = command.__name__
        self.help_text = command.__doc__
        self.complete = None
        self.__command__ = command

    def update_help(self, txt):
        ''' update_help
        Takes a string as an argument and updates the help text for the command
        '''
        self.help_text = txt if isinstance(txt, str) \
            and len(txt) > 0 else self.help_text

    def update_completion(self, completions):
        ''' update_completion
        Takes an argument and converts it into the appropriate completion
        function and updates the completion system for the command with the
        new information.
        '''
        self.complete = gen_completion(completions)

    def __doc__(self):
        return self.help_text

    def __help__(self):
        print self.help_text

    def __complete__(self, *args, **kwargs):
        ''' __complete__
        Method call to retrieve the completions for the command based on the
        format of the current state of the command being composed.
        '''
        return self.complete(*args, **kwargs) if self.complete else None

    def __call__(self, cmdr, *args, **kwargs):
        ''' __call__
        Calls the wrapped base command and normalizes the output to be a list
        of the lines of output.
        '''
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
        ''' __call_split__
        Cleans up the arguments of the command coming from the controller and
        prints whatever the command returns if it is a list, otherwise forwards
        the value to controller.
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
        ''' __attach__
        Sets up the various methods on the passed in master controller class
        to attach this command to the overall controller interface.
        '''
        setattr(cmdr, "do_" + self.__name__, self.__call_split__)
        setattr(cmdr, "help_" + self.__name__, self.__help__)
        if self.complete:
            setattr(cmdr, "complete_" + self.__name__, self.__complete__)
