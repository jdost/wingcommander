# -*- coding: utf8 -*-


def gen_prompt(cmd_):
    tree = [cmd_.name]
    cmd = cmd_.parent

    while cmd:
        tree.append(cmd.name)
        cmd = cmd.parent

    tree.reverse()
    return ':'.join(tree) + "> "


def is_iterable(o):
    try:
        return isinstance(o, basestring)
    except NameError:
        return isinstance(o, str)


def run(cmdr):
    import sys
    args = sys.argv

    if args[0].startswith("python"):
        args = args[1:]

    if args > 1:
        return cmdr.onecmd(' '.join(args[1:]))
    else:
        return cmdr.cmdloop()


def watch(func, wait=1):
    import sys
    import time
    import thread

    longest = 0

    def input_listener():
        from getpass import getpass
        from os import devnull

        getpass('', open(devnull, "w"))
        thread.interrupt_main()

    thread.start_new_thread(input_listener, ())
    try:
        while True:
            if longest > 0:  # ANSI goes up n lines at start
                sys.stdout.write("\033[2K\033[F"*(longest))
            else:  # clear line, move to start
                sys.stdout.write("\033[2K\033[0G")

            output = func()
            if isinstance(output, str):
                output = output.split('\n')

            if len(output) < longest:
                output += [''] * (longest - len(output))
            longest = len(output)

            sys.stdout.write('\n'.join(output))
            sys.stdout.write('\n')
            time.sleep(wait)
    except (KeyboardInterrupt, SystemExit):
        return


class Tablize(object):
    DIVIDERS = ["|", "", ""]
    BOX_DIVIDERS = ["│", "─", "┼"]
    CENTER = 'c'
    LEFT = 'l'
    RIGHT = 'r'
    COLUMN_TEMPLATE = " {{:{0}{1}.{1}}} "

    @classmethod
    def __call__(cls, data, max_length=-1, keys=None,
                 dividers=DIVIDERS, labels=None, alignment=None):
        if isinstance(data[0], dict):
            data = cls.extract_dicts(data, keys)

        sizes = cls.calc_columns(data, max_length)

        frmt = []
        row_divider = ""
        for i in range(len(sizes)):
            frmt.append(cls.COLUMN_TEMPLATE.format(
                cls.translate_alignment(alignment[i] if alignment else None),
                str(sizes[i])))
        frmt = (dividers[0] if dividers[0] else ' ').join(frmt)

        if dividers[1]:
            row_divider = (dividers[2] if dividers[2] else dividers[1]).join(
                [(s+2) * dividers[1] for s in sizes])

        output = [frmt.format(*labels)] if labels else []

        for d in data:
            if output and row_divider:
                output.append(row_divider)
            output.append(frmt.format(*d))

        return output

    @classmethod
    def extract_dicts(cls, data, keys):
        if keys is None:
            keys = data[0].keys()

        return [[d.get(k, '') for k in keys] for d in data]

    @classmethod
    def calc_columns(cls, data, max_length):
        sizes = map(
            lambda x: max(*map(len, [d[x] for d in data])),
            range(len(data[0])))

        if isinstance(max_length, list):
            return [min(max_length[i], sizes[i]) for i in range(len(sizes))]
        elif max_length > 0:
            return map(lambda x: min(x, max_length), sizes)

        return sizes

    @classmethod
    def translate_alignment(cls, alignment="l"):
        return "<" if alignment == "l" else \
            "^" if alignment == "c" else ">"

tablize = Tablize()
