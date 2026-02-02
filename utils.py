import os
import re
from cryptography.fernet import Fernet
from rich.console import Console
from prompt_toolkit.styles import Style as PromptStyle
from prompt_toolkit import prompt
from prompt_toolkit.key_binding import KeyBindings

console = Console()

class TextFormatter:
    @staticmethod
    def parse(text):
        #warning (red text)
        text = re.sub(r'!w\{(.*?)}', r'[bold red]\1[/bold red]', text)

        #info (green)
        text = re.sub(r'!i\{(.*?)}', r'[bold green]\1[/bold green]', text)

        #highlighted (yellow)
        text = re.sub(r'!h\{(.*?)}', r'[black on yellow]\1[/]', text)

        #note (blue)
        text = re.sub(r'!n\{(.*?)}', r'[bold cyan]\1[/bold cyan]', text)

        return text

def get_multiline_input():
    console.print('[dim]enter note content below. press [bold]ENTER[/] for new line, [bold]CTRL + C[/] (or ESC then ENTER) to save.[/dim]')

    editor_style = PromptStyle.from_dict({
        'prompt': '#888'
    })

    kb = KeyBindings()
    @kb.add('c-s')
    def _(event):
        'accept the input (save)'
        event.app.exit(result=event.app.current_buffer.text)

    try:
        text = prompt(
            '> ',
            multiline=True,
            style=editor_style,
            key_bindings=kb,
            bottom_toolbar=" [CTRL + S] save | [CTRL + C] cancel "
        )
        return text
    except KeyboardInterrupt:
        # handle [CTRL + C]
        return None

class SecurityManager:
    def __init__(self):
        self.key_file = 'secret.key'
        self.key = None

        #check if key file exists
        if os.path.exists(self.key_file):
            with open(self.key_file, 'rb') as f:
                self.key = f.read()
        else:
            #generate new key
            self.key = Fernet.generate_key()
            with open(self.key_file, 'wb') as f:
                f.write(self.key)

    def encrypt(self, plain_text):
        f = Fernet(self.key)
        #convert string to bytes, then encrypt
        return f.encrypt(plain_text.encode())

    def decrypt(self, cipher_text):
        f = Fernet(self.key)
        return f.decrypt(cipher_text).decode()