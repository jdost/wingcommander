import cmd
import logging
from . import util
import sys


class WingCommander(cmd.Cmd):
    END_CMDS = ['back', 'exit', 'EOF']

    def __init__(self, name="", parent=None, *args, **kwargs):
        cmd.Cmd.__init__(self, *args, **kwargs)
        self.parent = parent
        self.name = name
        self.prompt = util.gen_prompt(self)
        self.handler = logging.StreamHandler(sys.stdout)

    @classmethod
    def command(cls, cmd=None, completions=None):
        if not cmd:
            return lambda f: cls.command(
                cmd=f, completions=util.gen_completion(completions))

        def cmd_help():
            print(cmd.__doc__)

        name = cmd.__name__

        def cmd_(cmdr, args):
            return cmd(cmdr, *args.split(' '))

        setattr(cls, "do_" + name, cmd_)
        setattr(cls, "help_" + name, cmd_help)
        if completions:
            setattr(cls, "complete_" + name, completions)

    def default(self, command):
        if command in self.END_CMDS:
            return True

        return cmd.Cmd.default(self, command)

    def preloop(self):
        self.old_completer_fix = None
        try:
            import readline
            self.old_completer_fix = readline.get_completer()
            readline.set_completer(self.complete)
            if 'libedit' in readline.__doc__:
                completekey = "^I" if self.completekey == "tab" \
                    else self.completekey
                readline.parse_and_bind("bind " + completekey
                                        + " rl_complete")
        except ImportError:
            pass

    def postloop(self):
        if self.old_completer_fix:
            self.old_completer = self.old_completer_fix
