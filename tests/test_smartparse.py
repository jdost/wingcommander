from wingcommander.util.smartparse import Parser
import unittest


def foo(a, b, c=1, d=True):
    return (a, b, c, d)


class SmartParseTest(unittest.TestCase):
    def setUp(self):
        self.parser = Parser(foo)

    def test_basic(self):
        ''' Checks that a normal line goes through clean
        Just provides a list of arguments with no flags, the parser should not
        modify the argument set.
        '''
        arg_list = ["foo", "bar", "baz"]
        args, kwargs = self.parser.parse(arg_list, {})

        self.assertItemsEqual(arg_list, args)

    def test_named(self):
        ''' Named arguments become keyword args
        Provides a mixture of named and unnamed arguments in the set and
        expects to see them separated and named properly.
        '''
        arg_list = ["foo", "--bar", "baz", "arg", "--parsed", "passed"]
        args, kwargs = self.parser.parse(arg_list, {})

        self.assertItemsEqual(["foo", "arg"], args)
        self.assertDictEqual({"bar": "baz", "parsed": "passed"}, kwargs)

    def test_flags(self):
        ''' Sequential named arguments are treated as flags
        Multiple named arguments (starting with "--") are treated as boolean
        flags.
        '''
        arg_list = ["--foo", "--bar", "--baz", "arg"]
        args, kwargs = self.parser.parse(arg_list, {})

        self.assertItemsEqual([], args)
        self.assertDictEqual({"foo": True, "bar": True, "baz": "arg"}, kwargs)

    def test_smartflags(self):
        ''' Named args that are boolean in defaults are treated as flags
        If the default for the kwarg in the function signature is boolean, the
        named flag is treated as a strict boolean.  The 'no-' prefix is treated
        as a negation.
        '''
        arg_list = ["--d", "test"]
        args, kwargs = self.parser.parse(arg_list, {})

        self.assertItemsEqual(["test"], args)
        self.assertDictEqual({"d": True}, kwargs)

        arg_list = ["--no-d", "test"]
        args, kwargs = self.parser.parse(arg_list, {})

        self.assertItemsEqual(["test"], args)
        self.assertDictEqual({"d": False}, kwargs)

    def test_alias(self):
        ''' Aliased named arguments get translated properly
        Passes in the aliases for a default argument in a command and expect
        to see the alias translated when the command is run.
        '''
        self.parser.add_alias("c", "longer")
        self.assertDictEqual({"c": ["longer"]}, self.parser.aliases)

        arg_list = ["--longer", "foo"]
        args, kwargs = self.parser.parse(arg_list, {})

        self.assertDictEqual({"longer": "foo"}, kwargs)
        _, _, t, _ = self.parser(*[None, None], **kwargs)
        self.assertEquals(t, "foo")

    def test_shortflag(self):
        ''' Single character flags can have short prefix
        If a named argument is a single character, it will work with only one
        dash as a prefix.
        '''
        arg_list = ["-a", "foo"]
        args, kwargs = self.parser.parse(arg_list, {})

        self.assertDictEqual({"a": "foo"}, kwargs)

    def test_trailing_name(self):
        ''' The last argument is treated as a flag if it is named
        If the final argument is a flag, it gets honored.
        '''
        arg_list = ["--foo"]
        args, kwargs = self.parser.parse(arg_list, {})

        self.assertDictEqual({"foo": True}, kwargs)
