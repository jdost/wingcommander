from wingcommander import Command
import unittest


def foo(cmdr, *args):
    return args

cmd = Command(foo)


def gen_function(cmdr, *args):
    for x in args:
        yield x

gen_cmd = Command(gen_function)


class CommmandTest(unittest.TestCase):
    def test_basic(self):
        ''' Checks the basic API for the command
        The new command function/object should behave the same as the original
        function but with access to the new supplementary functionality.
        '''
        self.assertIsInstance(cmd, Command)
        self.assertEquals(["foo", "bar", "baz"],
                          cmd(None, "foo", "bar", "baz"))
        self.assertEquals(cmd.__name__, foo.__name__)

    def test_blob(self):
        ''' Returns an array when the command returns a string
        If a giant text blob is returned, it should be transformed into an
        array using new lines as the delimiter.
        '''
        def blob(cmdr, *args):
            return '\n'.join(["foo", "bar", "baz"])
        blob_cmd = Command(blob)
        self.assertEquals(["foo", "bar", "baz"], blob_cmd(None))

    def test_update(self):
        ''' Updating the completions works
        The completion system should be empty initially, but can be updated
        via the appropriate method.
        '''
        self.assertEquals(None, cmd.__complete__(""))
        cmd.update_completion(["foo", "bar"])
        self.assertNotEquals(None, cmd.__complete__("", ""))

    def test_generator(self):
        ''' Using a generator as a command works
        If the command wrapped by the Command object is a generator, it should
        be handled cleanly.
        '''
        self.assertEquals(["foo", "bar", "baz"],
                          gen_cmd(None, "foo", "bar", "baz"))

    def test_pass_generator(self):
        ''' The 'pass_generator' argument is honored
        Setting the `pass_generator` argument to True will return the generator
        rather than the list that is generated.
        '''
        import types
        self.assertIsInstance(
            gen_cmd(None, "foo", "bar", "baz", pass_generator=True),
            types.GeneratorType)
