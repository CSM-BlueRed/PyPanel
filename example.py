# create the banner
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

# Import the modules
import PyPanel
from PyPanel import *
import requests as http
from pystyle import Write as Console
from threading import Thread
from time import sleep as wait

# set thye size of the terminal
setSize(200, 50)

# set the second characters of the banner
default_banner_second_chars = ['▓']

# Make the title format
setTitleFormat(r':name: version :version: / made by :authors: / in command :cmd:')

# configure the program
prog = Program(
    'Socket Tools', # the name
    '1.0', # the version
    ('BlueRed',), # the authors
    'A simple socket toolkit for many http protocols', # the description
    'MIT' # the license
)

# set the program in the module
setattr(PyPanel, 'prog', prog)

# create the clas with all commands
class Tools():

    # create the POST request command
    @Command
    def http_post(ctx: Context) -> None:

        # define the code of the command
        url = Console.Input('Enter the URL >>> ', ctx.panel.colors, 0.005)
        response = http.post(url)
        Console.Print(f'The response code is {response.status_code}', ctx.panel.colors, 0.005)

    # create the GET request command
    @Command
    def http_get(ctx: Context) -> None:

        # define the code of the command
        url = Console.Input('Enter the URL >>> ', ctx.panel.colors, 0.005)
        response = http.get(url)
        Console.Print(f'The response code is {response.status_code}', ctx.panel.colors, 0.005)

    # create the PUT request command
    @Command
    def http_put(ctx: Context) -> None:

        # define the code of the command
        url = Console.Input('Enter the URL >>> ', ctx.panel.colors, 0.005)
        response = http.put(url)
        Console.Print(f'The response code is {response.status_code}', ctx.panel.colors, 0.005)

    # create the DELETE request command
    @Command
    def http_delete(ctx: Context) -> None:

        # define the code of the command
        url = Console.Input('Enter the URL >>> ', ctx.panel.colors, 0.005)
        response = http.delete(url)
        Console.Print(f'The response code is {response.status_code}', ctx.panel.colors, 0.005)

    # create the HEAD request command
    @Command
    def http_head(ctx: Context) -> None:

        # define the code of the command
        url = Console.Input('Enter the URL >>> ', ctx.panel.colors, 0.005)
        response = http.head(url)
        Console.Print(f'The response code is {response.status_code}', ctx.panel.colors, 0.005)

    # create the PATCH request command
    @Command
    def http_patch(ctx: Context) -> None:

        # define the code of the command
        url = Console.Input('Enter the URL >>> ', ctx.panel.colors, 0.005)
        response = http.patch(url)
        Console.Print(f'The response code is {response.status_code}', ctx.panel.colors, 0.005)

    # create the OPTIONS request command
    @Command
    def http_options(ctx: Context) -> None:

        # define the code of the command
        url = Console.Input('Enter the URL >>> ', ctx.panel.colors, 0.005)
        response = http.options(url)
        Console.Print(f'The response code is {response.status_code}', ctx.panel.colors, 0.005)

# create a function that will be called when a command is used
@event('on_start_command')
def on_start_command(command: Command, ctx: Context) -> None:
    print(f'You called {command.name!r} from the panel {ctx.panel}!')

# create a function that will be called when the system log something
@event('on_log')
def on_log(msg: str) -> None:
    pass

test = Panel('Test', (Colors.blue_to_red), [
    ('Test', Tools.http_post)
], banner)

# create the main menu
main = Panel('Main menu', (Colors.blue_to_red), [
    ('POST request', Tools.http_post),
    ('GET request', Tools.http_get),
    ('PUT request', Tools.http_put),
    ('DELETE request', Tools.http_delete),
    ('HEAD request', Tools.http_head),
    ('PATCH request', Tools.http_patch),
    ('OPTIONS request', Tools.http_options),
    ('Test', test)
], banner)

# Make text and style to the panel
border = '\n'.join((' ' * 2) + line + (' ' * 2) for line in [
    'Support: github.com/CSM-BlueRed',
    'Made with PyPanel',
])

main.MakeOutText(
    middle = f'{prog.name} by {", ".join(prog.authors)}!\nMake sure to install PyPanel!',
    bottom = f'made by PyPanel',
    bottom_left = border,
    bottom_right = border
)

main.listen()