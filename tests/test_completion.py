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
        '''
        self.setup_function(self.basic_completion)

        self.assertCompletes("foo", ["test1", "test2"], "")
        self.assertCompletes("foo", ["test1", "test2"], "a")

    def test_list(self):
        ''' Tests the completion function generation from a list
        '''
        self.setup_function(["foo", "bar", "baz"])

        self.assertCompletes("foo", ["foo", "bar", "baz"], "")
        self.assertCompletes("foo", ["foo"], "f")
        self.assertCompletes("foo", ["bar", "baz"], "b")
        self.assertCompletes("foo", [], "z")

    def test_dict(self):
        ''' Tests the tiered completion function from a dict
        '''
        self.setup_function({"foo": ["foo", "baz"], "bar": ["baz"]})

        self.assertCompletes("foo", ["foo", "bar"], "")
        self.assertCompletes("foo", ["foo", "baz"], "foo ")
        self.assertCompletes("foo", ["baz"], "foo b")
