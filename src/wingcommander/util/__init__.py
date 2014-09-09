__all__ = ["gen_prompt", "is_iterable", "run", "watch", "tablize",
           "gen_completion"]


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

    if len(args) > 1:
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
                sys.stdout.write("\033[2K\033[F" * (longest))
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


from wingcommander.util.tablize import tablize
from wingcommander.util.completion import gen_completion
