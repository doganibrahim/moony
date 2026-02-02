import hashlib
import os
import sys
from rich.panel import Panel
from utils import console

class UserManager:
    def __init__(self):
        self.lock_file = 'user.lock'

    def get_hash(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def is_registered(self):
        return os.path.exists(self.lock_file)

    def register(self):
        console.print(Panel('[bold yellow] set password [/bold yellow]'))
        while True:
            pwd = console.input('password: ')
            pwd_again = console.input('password again: ')

            if pwd == pwd_again and len(pwd) > 0:
                hashed_pwd = self.get_hash(pwd)
                with open(self.lock_file, 'w') as f:
                    f.write(hashed_pwd)
                console.print('[green]successfully registered[/green]')
                return True
            else:
                console.print('[red]passwords do not match or blank[/red]')

    def login(self):
        with open(self.lock_file, 'r') as f:
            stored_hash = f.read().strip()
        while True:
            console.print('[bold cyan]login[/bold cyan]')
            console.print('[dim](type [bold white]!exit[/bold white] to exit)[/dim]')
            entered_pwd = console.input('password: ')

            if self.get_hash(entered_pwd) == stored_hash:
                console.print('[green]successfully logged in[/green]')
                return True
            elif entered_pwd.strip() == '!exit':
                sys.exit()
            else:
                console.print('[red]wrong password[/red]')