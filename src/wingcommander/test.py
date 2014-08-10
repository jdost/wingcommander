import unittest
from wingcommander import WingCommander
from StringIO import StringIO


class TestShell(WingCommander):
    pass


class CmdTestCase(unittest.TestCase):
    def setUp(self):
        self.stdin = StringIO("")
        self.stdout = StringIO("")
        self.cmd = TestShell(
            name=__name__, stdin=self.stdin, stdout=self.stdout)

    def tearDown(self):
        self.stdin.seek(0)
        self.stdin.truncate()

        self.stdout.seek(0)
        self.stdout.truncate()

    def seedInput(self, lines=[]):
        ''' seedInput:
        Generate simulated input for stdin using the lines argument.
        '''
        self.stdin.write("\n".join(lines))
        self.stdin.seek(0)

    def collectOutput(self):
        ''' collectOutput:
        Collect the stored stdout into a list of lines.
        '''
        self.stdout.seek(0)
        return [line for line in self.stdout.readline()]

    def cmd_name(self, cmd):
        return "cmd_%s" % cmd

    def cmp_name(self, cmd):
        return "complete_%s" % cmd

    def help_name(self, cmd):
        return "help_%s" % cmd

    def assertCompletes(self, cmd, src_completions, line=""):
        ''' assertCompletes:
        Generates completions for the `cmd` function and asserts the output of
        the completion function against the expected completions.
        '''
        line = cmd + ' ' + line
        tmp = line.split(' ')
        current = tmp[-1]
        completions = getattr(self.cmd, self.cmp_name(cmd))(
            current, line, 0, len(tmp))

        self.assertListEqual(src_completions, completions)

    def runWithInput(self, cmd, lines=[]):
        ''' runWithInput:
        Takes a command and input lines that will be used as simulated input
        via stdin.  It will return either the return value from the executed
        command or the lines from stdout (if the return value was a boolean or
        None).
        '''
        cmd_ = cmd.split(' ')
        args = ' '.join(cmd_[1:]) if len(cmd_) > 1 else ''
        cmd_ = cmd_[0]

        self.seedInput(lines)
        r = getattr(self.cmd, self.cmd_name(cmd_))(args)
        return self.collectOutput() if (isinstance(r, bool) or r is None) \
            else r
