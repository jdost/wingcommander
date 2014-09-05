# Wing Commander

Status: [![Travis Status](https://travis-ci.org/jdost/wingcommander.svg?branch=master)](https://travis-ci.org/jdost/wingcommander)

## Making python's `cmd` module better

The `cmd` module for python makes writing readline applications accessible, this is
just an improved wrapper on this.  It allows for you to create instances easily 
using decorators and comes with a varied toolbelt for handling various use cases of
the system.

## Easy creation

```python
from wingcommander import WingCommander, run


class TestShell(WingCommander):
   pass


@TestShell.command
def hello(cmdr, *args):
   ''' Say hello:
   echoes 'hello'
   '''
   print("hello")


if __name__ == '__main__':
   commander = TestShell(name="sample")
   run(commander)
```

The `TestShell.command` decorator converts the `hello` function into a command for
the readline instance.  The help text for the command gets pulled from the docstring
(can be overriden).

## Tab completion

You can include a `completions` argument in the decorator to enable tab completion 
for the function as well:

```python
@TestShell.command(completions=["world", "jdost"])
```

This takes a function, `dict`, or `list`.  If it is a list, it will complete 
anything from that list for every argument, if it is a dictionary, it will complete
a key for the first argument and then one of the values for the second (you can nest
dictionaries too).  For a function, it works the same as the [`completedefault`][1]
function.

[1]: https://docs.python.org/2/library/cmd.html#cmd.Cmd.completedefault

## Subshells

WingCommander supports subshells out of the box.  This means that you can import
and start another WingCommander command shell inside of an existing one and it will
both denote the state and transition smoothly.

## Toolbelt

This also comes with a set of helper functions to ease various output scenarios.

### `watch`

```python
def cat():
   f = open("editthis.txt", "r")
   return [l.strip() for l in f.readlines()]

wingcommander.watch(cat)
```

The first is the `watch` function.  This works in the same way as the unix `watch`
command where it will print the output of the supplied function on a determined
frequency.  The output can be multiline and the area covered will grow as the output
gets larger.  This uses ANSI control characters (has only been tested using `urxvt`
for now).

### `tablize`

```python
def list_users():
   return [["jdost", "github", "python"],
            ["tester", "twitter", "tweets"]]

print(tablize(list_users()))
```

The `tablize` function takes a list of lists (or dictionaries) and creates an 
aligned output in a table form.  The above command would output:
```
 jdost |  github | python
tester | twitter | tweets
```

The function takes various optional arguments such as `max_length`, `keys`, 
`dividers`, `labels`, and `alignment`.

* `max_length` is just a number that limits the width any column can be (if it is a
  list, each number will be applied to the corresponding column)
* `keys` is for use with a list of dictionaries, rather than printing all the keys,
  just the keys in the list will be printed (in the order they are listed)
* `dividers` is a list or dictionary giving the characters to use as dividers, the
  order is [`VERTICAL`, `HORIZONTAL`, `CROSS`], any omitted will use the defaults,
  * `VERTICAL` are the pipes that separate the columns, default: `|`
  * `HORIZONTAL` are the spaces that divide the rows, if empty, no divider is used 
    (default)
  * `CROSS` is the character used (if both `VERTICAL` and `HORIZONTAL` are set) to
    mark the intersection of these markers
* `labels` is a list of strings that will label the columns
* `alignment` is a list of characters that denote how the columns will be aligned,
  options are `c` for center, `r` for right, and `l` for left, you can also use
  `tablize.LEFT`, `tablize.CENTER`, and `tablize.RIGHT` (this is preferable)
