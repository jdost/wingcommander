def gen_completion(completions):
    if isinstance(completions, list):
        return gen_from_list(completions)
    elif isinstance(completions, dict):
        return gen_from_dict(completions)
    else:
        return completions


def gen_from_list(completions):
    completions = completions

    def tmp(s, arg, text, *_args):
        if len(arg) == 0:
            return completions

        return [o for o in completions if o.startswith(arg)]

    return tmp


def gen_from_dict(completions):
    completions = completions

    def tmp(s, arg, text, *_args):
        args = text.split(' ')

        if len(args) == 1:
            return completions.keys()

        if len(args) <= 2:
            completion_set = completions.keys()
        else:
            lookup = args[len(args) - 2]
            completion_set = completions.get(lookup, [])

        if not len(arg):
            return completion_set

        return [o for o in completion_set if o.startswith(arg)]

    return tmp
