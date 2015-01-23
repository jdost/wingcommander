from wingcommander.util import gen_completion


class Command(object):
    def __init__(self, command):
        self.__name__ = command.__name__
        self.help_text = command.__doc__
        self.complete = None
        self.__command__ = command

    def update_help(self, txt):
        self.help_text = txt

    def update_completion(self, completions):
        self.complete = gen_completion(completions)

    def __doc__(self):
        return self.__help__()

    def __help__(self):
        print self.help_text

    def __complete__(self, *args, **kwargs):
        return self.complete(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        self.__command__(*args, **kwargs)

    def __call_split__(self, cmdr, args):
        self.__call__(self, cmdr, *args.split(' '))

    def __attach__(self, cmdr):
        setattr(cmdr, "do_" + self.__name__, self.__call_split__)
        setattr(cmdr, "help_" + self.__name__, self.__help__)
        if self.complete:
            setattr(cmdr, "complete_" + self.__name__, self.__complete__)
