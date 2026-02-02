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
        console.clear()
        console.print("\n  [white]SETUP[/]\n")
        while True:
            pwd = console.input('  password › ', password=True)
            pwd_again = console.input('  confirm  › ', password=True)

            if pwd == pwd_again and len(pwd) > 0:
                hashed_pwd = self.get_hash(pwd)
                with open(self.lock_file, 'w') as f:
                    f.write(hashed_pwd)
                console.print('\n  [dim green]✓ registered[/]')
                console.input('\n  [dim]press enter...[/]')
                return True
            else:
                console.print('\n  [dim red]mismatch[/]\n')

    def login(self):
        with open(self.lock_file, 'r') as f:
            stored_hash = f.read().strip()
        console.clear()
        while True:
            console.print("\n  [white]LOGIN[/]\n")
            console.print('  [dim]type !exit to quit[/]\n')
            entered_pwd = console.input('  password › ', password=True)

            if self.get_hash(entered_pwd) == stored_hash:
                console.print('\n  [dim green]✓ access granted[/]')
                console.input('\n  [dim]press enter...[/]')
                return True
            elif entered_pwd.strip() == '!exit':
                sys.exit()
            else:
                console.print('\n  [dim red]incorrect[/]\n')