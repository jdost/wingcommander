import cmd
import logging
from . import util
import sys


class WingCommander(cmd.Cmd):
    END_CMDS = ['back', 'exit', 'EOF']

    def __init__(self, name="", parent=None):
        cmd.Cmd.__init__(self)
        self.parent = parent
        self.name = name
        self.prompt = util.gen_prompt(self)
        self.handler = logging.StreamHandler(sys.stdout)

    @classmethod
    def command(cls, cmd=None, completions=None):
        if not cmd:
            if isinstance(completions, list):
                completions = completions

                def tmp(s, arg, text, *_args):
                    if len(arg) == 0:
                        return completions

                    return [o for o in completions if o.startswith(arg)]
                return lambda f: cls.command(cmd=f, completions=tmp)
            elif isinstance(completions, dict):
                completions = completions

                def tmp(s, arg, text, *_args):
                    args = text.split(' ')

                    if len(args) == 1:
                        return completions.keys()

                    if len(args) <= 2:
                        completion_set = completions.keys()
                    else:
                        lookup = args[len(args) - 2]
                        completion_set = completions.get(lookup, [])

                    if not len(arg):
                        return completion_set

                    return [o for o in completion_set if o.startswith(arg)]
                return lambda f: cls.command(cmd=f, completions=tmp)

            return lambda f: cls.command(
                cmd=f, completions=completions)

        def cmd_help():
            print(cmd.__doc__)

        name = cmd.__name__
        setattr(cls, "do_" + name, cmd)
        setattr(cls, "help_" + name, cmd_help)
        if completions:
            setattr(cls, "complete_" + name, completions)

    def default(self, command):
        if command in self.END_CMDS:
            return True

        return cmd.Cmd.default(self, command)
