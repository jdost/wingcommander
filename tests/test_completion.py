import wingcommander.test as unittest


def foo(cmdr, *args):
    pass


class CompletionTest(unittest.CmdTestCase):
    def setup_function(self, completion):
        tmp = self.cmd.command(completions=completion)
        tmp(foo)

    def basic_completion(self, *args):
        return ["test1", "test2"]

    def test_basic(self):
        ''' Tests the basic function based completion
        Uses a generator function to always return the same options (ignores
        any of the actual arguments).
        '''
        self.setup_function(self.basic_completion)

        self.assertCompletes("foo", ["test1", "test2"], "")
        self.assertCompletes("foo", ["test1", "test2"], "a")

    def test_list(self):
        ''' Tests the completion function generation from a list
        Passes a list to have a completion function be generated to always
        use the list to see the completion filter.
        '''
        self.setup_function(["foo", "bar", "baz"])

        self.assertCompletes("foo", ["foo", "bar", "baz"], "")
        self.assertCompletes("foo", ["foo"], "f")
        self.assertCompletes("foo", ["bar", "baz"], "b")
        self.assertCompletes("foo", [], "z")
        self.assertCompletes("foo", ["foo"], "z f")

    def test_dict(self):
        ''' Tests the tiered completion function from a dict
        Passes a dictionary to have a tiered completion function be generated.
        This uses keys for the first level and then seeds the second level with
        the values for the key used in the first level.
        '''
        self.setup_function({"foo": ["foo", "baz"], "bar": ["baz"]})

        self.assertCompletes("foo", ["foo", "bar"], "")
        self.assertCompletes("foo", ["foo", "baz"], "foo ")
        self.assertCompletes("foo", ["baz"], "foo b")
