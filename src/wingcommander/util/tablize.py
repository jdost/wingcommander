# -*- coding: utf8 -*-


DIVIDERS = ["|", "", ""]
BOX_DIVIDERS = ["│", "─", "┼"]
CENTER = 'c'
LEFT = 'l'
RIGHT = 'r'
COLUMN_TEMPLATE = " {{:{0}{1}.{1}}} "


class Table(list):
    def __str__(self, *args, **kwargs):
        return '\n'.join(self)


def tablize(data, max_length=-1, keys=None, dividers=DIVIDERS, labels=None,
            alignment=None):
    '''Converts a tabular set of data into an aligned table for easier display
    in the terminal.

    There are a number of options for customizing the output.  The ``keys``
    parameter will limit the keys to pull from each ``dict`` of data in the
    dataset.  The ``labels`` parameter enables the header row and fills in
    the labels for each column.

    The ``dividers`` parameter is used to configure the characters used to
    divide the various data cells.  It is a `list` of length 3 that is defined:

    0. The character used to divide between columns
    1. The character used to divide between rows
    2. The character used when the division between columns and rows occurs

    The default is to display a pipe between columns and nothing between rows.
    A more ornamental set of dividers using box drawing characters, it can be
    found by importing ``BOX_DIVIDERS`` from ``wingcommander.util.tablize``.

    The ``alignment`` parameter is used to determine the alignment of the
    text in each column.  The list should mirror the number of columns
    available and should probably be used with the ``keys`` parameter.  The
    possible values are ``l``, ``c``, and ``r`` which correspond to
    left, center, and right aligned text respectively.  You can also use the
    values ``LEFT``, ``CENTER``, and ``RIGHT`` from the
    ``wingcommander.util.tablize`` module.

    :param data: a ``list`` of ``dict`` sets of data to be displayed
    :param max_length: a limit on the maximum wdith of a column/length of a
     data point, a value of -1 means there is no limit
    :param keys: a ``list`` of keys to be used from the ``dict`` of data
     provided, if this is set to ``None`` all of the keys will be used
    :param dividers: a ``list`` defining the dividers to use when displaying
     the tabular data.
    :param labels: a ``list`` of the labels to be displayed above the table,
     if ``None`` no labels will be displayed
    :param alignment: a ``list`` of the alignment setup associated with each
     column

    Usage: ::

        >>> from wingcommander.util import tablize
        >>> from wingcommander.util.tablize import BOX_DIVIDERS, LEFT, RIGHT
        >>> tablize([{"name": "Joe", "occupation": "Teacher", "age": 45},
        ...   {"name": "Jane", "occupation": "Engineer", "age": 27},
        ...   {"name": "Mark", "occupation": "Astronomer", "age": 33}],
        ...  keys=["name", "occupation", "age"], max_length=7,
        ...  dividers=BOX_DIVIDERS, labels=["Name", "Job", "Age"],
        ...  alignment=[LEFT, LEFT, RIGHT])
        ...
        Name │ Job     │ Age
        ─────┼─────────┼─────
        Joe  │ Teacher │  45
        ─────┼─────────┼─────
        Jane │ Enginee │  27
        ─────┼─────────┼─────
        Mark │ Astrono │  33

    '''
    if not len(data):
        return None
    if len(data) and isinstance(data[0], dict):
        data = extract_dicts(data, keys)

    data = clean_up(data)
    sizes = calc_columns(data, max_length)

    frmt = []
    row_divider = ""
    for i in range(len(sizes)):
        frmt.append(COLUMN_TEMPLATE.format(
            translate_alignment(alignment[i] if alignment else None),
            str(sizes[i])))
    frmt = (dividers[0] if dividers[0] else ' ').join(frmt).strip()

    if dividers[1]:
        row_divider = (dividers[2] if dividers[2] else dividers[1]).join(
            [(s + 2) * dividers[1] for s in sizes])

    output = Table([frmt.format(*labels)] if labels else [])

    for d in data:
        if output and row_divider:
            output.append(row_divider)
        output.append(frmt.format(*d))

    return output


def extract_dicts(data, keys):
    if keys is None:
        keys = data[0].keys()

    return [[d.get(k, '') for k in keys] for d in data]


def calc_columns(data, max_length):
    if len(data) > 1:
        sizes = map(
            lambda x: max(*map(lambda s: len(str(s)), [d[x] for d in data])),
            range(len(data[0])))
    else:
        sizes = map(lambda s: len(str(s)), data[0])

    if isinstance(max_length, list):
        return [min(max_length[i], sizes[i]) for i in range(len(sizes))]
    elif max_length > 0:
        return map(lambda x: min(x, max_length), sizes)

    return sizes


def clean_up(d):
    return map(lambda x: map(str, x), d)


def translate_alignment(alignment="l"):
    return "<" if alignment == "l" else "^" if alignment == "c" else ">"
