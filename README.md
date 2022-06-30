# PyPanel

PyPanel is a module used to create beautiful tools

## Setup your program

```python
# (!) This is just a example

import PyPanel
from PyPanel import *

prog = Program(
    'Socket Tools', # the name
    '1.0', # the version
    ('BlueRed',), # the authors
    'A simple socket toolkit for many http protocols', # the description
    'MIT' # the license
)

# set the program in the module
setattr(PyPanel, 'prog', prog)
```

## The Context class

The Context class is used to pass informations to the commands as a class and not as multiple arguments

when the Context arg is passed, it has for arguments:

- `ctx.panel`: the current panel that is used
- `ctx.function`: the command that is currently called

## Set events

There are many events like:

- `on_start_command`: when a command is executed
- `on_log`: when the module log something
- `on_error`: when a command raise an error

```python
# (!) This is just a example

from PyPanel import *

# create a function that will be called when a command is used
@event('on_start_command')
def on_start_command(command: Command, ctx: Context) -> None:
    print(f'You called {command.name!r} from the panel {ctx.panel}!')

# create a function that will be called when a command raise an error
@event('on_error')
def on_error(ctx: Context, exception) -> None:
    input(f'An error has occurred in the command {ctx.function}: {exception}')
```

# Create commands

To create commands, first: create just a normal function witch contain an argument for the Context when it be called at the first place, and use the decorator `@Command`

```python
# (!) This is just a example

from PyPanel import *
import requests as http

# create the POST request command
@Command
def http_post(ctx: Context) -> None:
    url = input('url: ')
    response = http.post(url)
    print(f'The response code is {response.status_code}')

# create the GET request command
@Command
def http_get(ctx: Context) -> None:
    url = input('url: ')
    response = http.get(url)
    print(f'The response code is {response.status_code}')

# create the PUT request command
@Command
def http_put(ctx: Context) -> None:
    url = input('url: ')
    response = http.put(url)
    print(f'The response code is {response.status_code}')
```

## Create a panel

To create a panel, you have to use the Panel class with the name of the panel, it instructions (commands) and other arguments

```python
# (!) This is just a example

from PyPanel import *

banner = r'''
                            __                  __     ________                   __ 
                           |  \                |  \   |        \                 |  \
  _______  ______   _______| ▓▓   __  ______  _| ▓▓_   \▓▓▓▓▓▓▓▓ ______   ______ | ▓▓
 /       \/      \ /       \ ▓▓  /  \/      \|   ▓▓ \    | ▓▓   /      \ /      \| ▓▓
|  ▓▓▓▓▓▓▓  ▓▓▓▓▓▓\  ▓▓▓▓▓▓▓ ▓▓_/  ▓▓  ▓▓▓▓▓▓\\▓▓▓▓▓▓    | ▓▓  |  ▓▓▓▓▓▓\  ▓▓▓▓▓▓\ ▓▓
 \▓▓    \| ▓▓  | ▓▓ ▓▓     | ▓▓   ▓▓| ▓▓    ▓▓ | ▓▓ __   | ▓▓  | ▓▓  | ▓▓ ▓▓  | ▓▓ ▓▓
 _\▓▓▓▓▓▓\ ▓▓__/ ▓▓ ▓▓_____| ▓▓▓▓▓▓\| ▓▓▓▓▓▓▓▓ | ▓▓|  \  | ▓▓  | ▓▓__/ ▓▓ ▓▓__/ ▓▓ ▓▓
|       ▓▓\▓▓    ▓▓\▓▓     \ ▓▓  \▓▓\\▓▓     \  \▓▓  ▓▓  | ▓▓   \▓▓    ▓▓\▓▓    ▓▓ ▓▓
 \▓▓▓▓▓▓▓  \▓▓▓▓▓▓  \▓▓▓▓▓▓▓\▓▓   \▓▓ \▓▓▓▓▓▓▓   \▓▓▓▓    \▓▓    \▓▓▓▓▓▓  \▓▓▓▓▓▓ \▓▓
'''[1:-1]

main = Panel('Main', (Colors.rainbow), [
    ('POST request', http_post),
    ('GET request', http_get),
    ('PUT request', http_put)
], banner)
```

## Start your program
To start your program, select your main panel, and use the `listen` function

```python
# (!) This is just a example

main.listen()
```