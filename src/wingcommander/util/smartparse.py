class Parser(object):
    def __init__(self, function):
        self.function = function
        self.smartparse = False
        self.args = self.__inspect(self.function)
        self.aliases = {}

    @classmethod
    def __inspect(cls, function):
        import inspect
        args, catchall, _, defaults = inspect.getargspec(function)

        bools = []
        named = {}

        if defaults:
            for i in range(1, len(defaults) + 1):
                d = defaults[i * -1]
                n = args[i * -1]
                if isinstance(d, bool):
                    bools.append(n)
                else:
                    named[n] = d
        else:
            i = 0

        return {
            "booleans": bools,
            "named": named,
            "ordered": args[0:(len(args) - i)]
        }

    def add_alias(self, full, *short):
        self.aliases[full] = list(short)

    def parse(self, args_, kwargs):
        def cleanup(a):
            if len(a) == 2 and a.startswith("-"):
                return "-{}".format(a)
            return a

        args_ = map(cleanup, args_)
        name = None
        args = []

        for a in args_:
            if a.startswith("--"):
                if name:
                    kwargs[name] = True
                name = a[2:]

                if name in self.args["booleans"]:
                    kwargs[name] = True
                    name = None
                elif name.startswith("no-") \
                        and name[3:] in self.args["booleans"]:
                    kwargs[name[3:]] = False
                    name = None

                continue

            if name:
                kwargs[name] = a
                name = None
            else:
                args.append(a)

        if name:
            kwargs[name] = True

        return args, kwargs

    def __call__(self, *args, **kwargs):
        if self.smartparse:
            args, kwargs = self.parse(args, kwargs)

        for full, aliases in self.aliases.iteritems():
            translate = lambda a: full if a in aliases else a
            args = map(translate, args)

            kwargs_ = {}
            for k, v in kwargs.iteritems():
                kwargs_[translate(k)] = v

            kwargs = kwargs_

        return self.function(*args, **kwargs)


def smartparse(func):
    parser = func if isinstance(func, Parser) else Parser(func)
    parser.smartparse = True

    return parser


def alias(full, *short):
    def decorator(func):
        parser = func if isinstance(func, Parser) else Parser(func)
        parser.add_alias(full, *short)
        return parser

    return decorator
