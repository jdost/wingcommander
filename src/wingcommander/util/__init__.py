__all__ = ["gen_prompt", "is_iterable", "run", "watch", "tablize",
           "gen_completion", "alias", "smartparse"]


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
    ''' Behaves like the ``watch`` command from unix command line.  Will
    refresh the terminal stdout area at a specific interval with the output
    from a defined function.  This can be used to regularly show output from an
    external source and provide a realtime updating text area that will resize
    with the data to display.  Can be stopped with user input from stdin.

    :param func: function that is to be generating the output to be displayed.
     The output is whatever the function returns on each execution.
    :param wait: amount of time to sleep between executions of the function in
     order to update the display

    Usage: ::

        from wingcommander.util import watch

        def print_file():
            contents = None
            with open('data', 'r') as f:
                contents = f.readlines()
                f.close()
            return contents

        watch(print_file, 0.5)

    '''
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
from wingcommander.util.smartparse import alias, smartparse
