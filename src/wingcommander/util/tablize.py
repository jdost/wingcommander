# -*- coding: utf8 -*-


DIVIDERS = ["|", "", ""]
BOX_DIVIDERS = ["│", "─", "┼"]
CENTER = 'c'
LEFT = 'l'
RIGHT = 'r'
COLUMN_TEMPLATE = " {{:{0}{1}.{1}}} "

def tablize(data, max_length=-1, keys=None, dividers=DIVIDERS, labels=None,
        alignment=None):
    if isinstance(data[0], dict):
        data = extract_dicts(data, keys)

    sizes = calc_columns(data, max_length)

    frmt = []
    row_divider = ""
    for i in range(len(sizes)):
        frmt.append(COLUMN_TEMPLATE.format(
            translate_alignment(alignment[i] if alignment else None),
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

def extract_dicts(data, keys):
    if keys is None:
        keys = data[0].keys()

    return [[d.get(k, '') for k in keys] for d in data]

def calc_columns(data, max_length):
    sizes = map(
        lambda x: max(*map(len, [d[x] for d in data])),
        range(len(data[0])))

    if isinstance(max_length, list):
        return [min(max_length[i], sizes[i]) for i in range(len(sizes))]
    elif max_length > 0:
        return map(lambda x: min(x, max_length), sizes)

    return sizes

def translate_alignment(alignment="l"):
    return "<" if alignment == "l" else "^" if alignment == "c" else ">"
