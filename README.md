# Shopping list readme

My shopping list maintenance

## Prerequisites

* [`hatch`](https://hatch.pypa.io/) -- install via `pipx hatch` or `pip install --user hatch`

## Install
```shell
make deploy
# or
hatch build
pipx install dist/shopping_list-0.1.3-py3-none-any.whl
```

## Syntax
```shell
usage: shopping-list-cli [-h] [--version] [-q] [-d] [-l PATH] [-i PATH] [-c] {add,done,rm} ...

options:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
  -q, --quiet           Log less (default: False)
  -d, --debug           Log more (default: False)
  -l PATH, --log-root PATH
                        Log root path (specify '' to suppress logging to a file) (default: logs)
  -i PATH, --db-file PATH
                        Input file (default: ~/.local/state/shopping-list.db)
  -c, --closed          Show closed items too (default: False)

subcommands:
  If no command specified, only list items

  {add,done,rm}
    add                 Add item(s)
    done                Close item(s)
    rm                  Delete item(s)
```

## Run

* **Add** items; repeated items are omitted:
```shell
shopping-list-cli -i shop.db add foo baz bar baz
2024-05-07 09:31:03.225 | INFO  | shopping_list.models - Opening DB shop.db
2024-05-07 09:31:03.227 | INFO  | shopping_list.items - Adding 'foo'
2024-05-07 09:31:03.233 | INFO  | shopping_list.items - Adding 'baz'
2024-05-07 09:31:03.234 | INFO  | shopping_list.items - Adding 'bar'
  #  done    title    created                     updated
---  ------  -------  --------------------------  --------------------------
  3  [ ]     bar      2024-05-06 23:31:03.234800  2024-05-06 23:31:03.234800
  2  [ ]     baz      2024-05-06 23:31:03.233934  2024-05-06 23:31:03.233934
  1  [ ]     foo      2024-05-06 23:31:03.227801  2024-05-06 23:31:03.227801

Showed 3 row(s)
```

* Mark an item as **done**:
```shell
shopping-list-cli -i shop.db -c done 2
2024-05-07 09:35:33.810 | INFO  | shopping_list.models - Opening DB shop.db
2024-05-07 09:35:33.811 | INFO  | shopping_list.items - Marking '2' as done
  #  done    title    created                     updated
---  ------  -------  --------------------------  --------------------------
  2  [x]     baz      2024-05-06 23:31:03.233934  2024-05-06 23:35:33.813289
  3  [ ]     bar      2024-05-06 23:31:03.234800  2024-05-06 23:31:03.234800
  1  [ ]     foo      2024-05-06 23:31:03.227801  2024-05-06 23:31:03.227801

Showed 3 row(s)
```

* **Remove** an item:
```shell
shopping-list-cli -i shop.db -c rm 3
2024-05-07 09:36:33.162 | INFO  | shopping_list.models - Opening DB shop.db
2024-05-07 09:36:33.163 | INFO  | shopping_list.items - Removing '3'
  #  done    title    created                     updated
---  ------  -------  --------------------------  --------------------------
  2  [x]     baz      2024-05-06 23:31:03.233934  2024-05-06 23:35:33.813289
  1  [ ]     foo      2024-05-06 23:31:03.227801  2024-05-06 23:31:03.227801

Showed 2 row(s)
```

## Development

```console
# run the CLI
hatch run cli
make cli

# run the CLI help
hatch run help
make help

# or append any CLI-defined args, like --help
hatch run cli --help
make cli EXTRA='...'

# run mypy
hatch run types:check
make mypy

# run tests
hatch run test

# go to the venv shell
hatch shell
```
