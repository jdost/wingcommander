import cmd
import logging
from wingcommander import util
from wingcommander.command import Command
import sys


class WingCommander(cmd.Cmd):
    """Master class for command line applications.

    Use as the base class for the definition of a command line application.

    :param name: name of the application
    :param parent: (optional) parent <WingCommander> object

    Usage: ::

        from wingcommander import WingCommander

        class ShellApp(WingCommander):
            pass

        app = ShellApp(name='example')

    """
    END_CMDS = ['back', 'exit', 'EOF']

    def __init__(self, name="", parent=None, *args, **kwargs):
        cmd.Cmd.__init__(self, *args, **kwargs)
        self.parent = parent
        self.name = name
        self.prompt = util.gen_prompt(self)
        self.handler = logging.StreamHandler(sys.stdout)

    @classmethod
    def command(cls, cmd=None, completions=None):
        """decorator method to convert a function and properties into a command
        for the new command line application.

        returns a :class:`Command <Command>` object.

        :param completions: (optional) A completion definition (see:
         :doc:`user/completions`)
        :param cmd: function to be converted into a command in the application
         (it is the one being decorated)


        Usage::

            @ShellApp.command
            def count(app):
                app.count = (app.count or 0) + 1
                return app.count

            @ShellApp.command(completions=["start", "stop"])
            def app(app, action="start"):
                if action == "start":
                    app.state = "started"
                elif action == "stop":
                    app.state = "stopped"
                return True
        """
        if not cmd:
            return lambda f: cls.command(cmd=f, completions=completions)

        if not isinstance(cmd, Command):
            cmd = Command(cmd)
            cmd.update_completion(completions)

        cmd.__attach__(cls)

        return cmd

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
