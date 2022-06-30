__version__: str = '1.0'
__author__: str = 'BlueRed'
__license__: str= 'MIT'

from pystyle import *
from io import BytesIO

# must to be edited
prog = ...

# can be edited (suggested)
default_banner = ''
default_banner_second_chars = ['░', '▒', '▓', '█']
title_format = r':name: :version:'
titleEnabled = True

def setTitleFormat(format):
    r"""
    Set the format of the title
    """
    globals()['title_format'] = format

def setDefaultBanner(banner):
    r"""
    Set the default banner used when the banner of a panel is not set
    """
    globals()['default_banner'] = banner

def enable_title():
    r"""
    Enable the title
    """
    globals()['titleEnabled'] = True

def disable_title():
    r"""
    Disable the title
    """
    globals()['titleEnabled'] = False



setSize = System.Size

_events = {
    'onStart': {
        'command': (lambda command: ...)
    },
    'onLog': (lambda message: ...),
    'onError': (lambda ctx, exception: Colorate.Error(str(exception)))
}

logs = BytesIO()

def _log(text):
    logs.write(text.encode('utf-8', 'replace'))
    _events['onLog'](text)

def event(name = None):
    r"""
    Set a function to be called when the event is triggered
    """
    def decorator(func):
        nonlocal name
        name = name or func.__name__

        if name not in {'on_start_command', 'on_log', 'on_error'}:
            raise Exception(f'The event {name!r} is not supported')

        if name == 'on_start_command':
            _events['onStart']['command'] = func

        if name == 'on_log':
            _events['onLog'] = func

        if name == 'on_error':
            _events['onError'] = func

        return func
    return decorator

class Context():
    r"""
    The context class, used to pass informations to the commands as a class and not as multiple arguments
    """

    def __init__(self, panel, func) -> None:
        self.panel = panel
        self.function = func

        _log(f'Added context for {self.panel}/{self.function}')

    def __str__(self) -> str:
        return f'c~{id(self)}'
    
    def __repr__(self) -> str:
        return f'<context from {self.panel} for {self.function}>'

class Command():
    r"""
    The command class
    """

    def __init__(self, func) -> None:
        self.command = func
        self.name = func.__name__
        self.results = []

        _log(f'Added command for {self.command}')

    def __str__(self) -> str:
        return f'command {self.name}'

    def __repr__(self) -> str:
        return f'<command {self.name}>'

    def __call__(self, ctx: Context, *args, **kwargs):
        onStart = _events['onStart']['command'](self, ctx)
        result = self.command(ctx, *args, **kwargs)
        self.results.append((onStart, result))
        _log(f'{self.name} returned {result}')
        return result

class Panel():
    r"""
    The panel class
    """
    spaces = 5
    chars = {
        'up': '═',
        'down': '═',
        'left': '║',
        'right': '║',
        'top_left': '╔',
        'top_right': '╗',
        'bottom_left': '╚',
        'bottom_right': '╝',
    }

    def __init__(self, name: str, colors: list[str], instructions: list[tuple], banner: str = default_banner, banner_second_chars: list[str] = default_banner_second_chars, **options) -> None:
        self.name = name
        self.colors = [colors, colors] if type(colors) != list else colors
        self.instructions = instructions
        self.banner_second_chars = banner_second_chars
        self.banner = banner
        self.input = options.get('input', 'Choose a command >>> ')
        self.command404 = options.get('cmd404', 'Command not found :cmd:')

        self.render()

        panelInfos = {'name': self.name, 'input': self.input, 'command 404 error': self.command404, 'instructions': self.instructions}
        _log(f'Added panel {panelInfos}')

    def render(self):
        r"""
        Render the final panel string display
        """
        cases = []
        obj = [instr[0] for instr in self.instructions]

        while len(obj) != 0:
            newObj = obj[6:]
            cases.append(obj[:6])
            obj = newObj

        count = 0

        def getIndex():
            nonlocal count
            count += 1
            return count - 1

        if len(cases) > 1:
            table = Add.Add(*['\n'.join(f'[ {getIndex()} ] ' + instr  + (' ' * Panel.spaces) for instr in instrs) for instrs in cases])
        else:
            table = '\n'.join(f'[ {getIndex()} ] ' + instr  + (' ' * Panel.spaces) for instr in cases[0])
        table = '[/] ' + self.name + '\n' + table

        width = 60
        up = Panel.chars['top_left'] + (Panel.chars['up'] * width) + Panel.chars['top_right']
        down = Panel.chars['bottom_left'] + (Panel.chars['down'] * width) + Panel.chars['bottom_right']

        final = '\n'.join((
            up,
            '\n'.join(Panel.chars['left'] + ' ' + line + (
                (' ' * (width - len(Panel.chars['left'] + ' ' + line) + 1)) + Panel.chars['right']
            ) for line in table.splitlines()),
            down
        ))

        self.table = final

        _log(f'Rendered panel {self.name}')

    def listen(self, *args):
        r"""
        Listen to the user input and execute the command
        """
        _log(f'Listening to {self.name}')
        while True:
            prog.update(self)
            print('\033[H\033[J', end = '')
            print(
                '\n'.join([
                    '',
                    Colorate.Format(Center.XCenter(self.banner), self.banner_second_chars, Colorate.Horizontal, self.colors, Col.white),
                    '',
                    Colorate.Diagonal(self.colors, Center.XCenter(self.table)),
                    ''
                ])
            )
            cmd = Write.Input(self.input, self.colors, 0.005)
            if cmd not in [str(num) for num in range(len(self.instructions))]:
                _log(f'Command {cmd} not found')
                Colorate.Error(self.command404.replace(':cmd:', cmd))
                continue
            command = self.instructions[int(cmd)][1]
            context = Context(self, command)
            if type(command) == Panel:
                command.listen(context)
            else:
                try: command(context)
                except Exception as error: _events['onError'](context, error)
                _log(f'Command {command} executed')
            input()

    def __str__(self):
        r"""
        Return the panel name
        """
        return self.name

    def __repr__(self):
        r"""
        Return the short string representation of the panel
        """
        return f'<panel {self.name}>'

    def __add__(self, other):
        r"""
        Return a custom panel that take the second one to merge the instructions in the first one
        """
        if type(other) == Panel:
            newPanel = self
            newPanel.instructions.extend(other.instructions)
            newPanel.render()
            return newPanel
        else:
            return NotImplemented

class Program():
    r"""
    The program class
    """

    def __init__(self, name: str, version: str, authors: tuple[str, ...], description: str, license: tuple, **options) -> None:
        self.name = name
        self.version = tuple(int(num) for num in version.split('.'))
        self.authors = authors
        self.description = description
        self.license = license
        self._panel = ...
        self.options = options

        progInfos = {'name': self.name, 'version': self.version, 'authors': self.authors, 'description': self.description, 'license': self.license}
        _log(f'Added program {progInfos}')

    @property
    def panel(self) -> Panel:
        r"""
        Return the current panel
        """
        return self._panel

    @panel.setter
    def panel(self, panel: Panel) -> None:
        r"""
        Set a new panel as the current
        """
        self._panel = panel
        if titleEnabled:
            title = title_format.replace(r':name:', self.name).replace(r':version:', '.'.join(str(num) for num in self.version)).replace(r':authors:', ', '.join(self.authors)).replace(r':description:', self.description).replace(r':license:', self.license).replace(r':panel:', panel.name)
            for key, value in self.options.items():
                title = title.replace(fr':{key}:', str(value))
            System.Title(title)
            _log(f'Set title to {title}')

    def update(self, panel: Panel = None) -> None:
        r"""
        Update the current panel
        """
        self.panel = panel

prog: Program