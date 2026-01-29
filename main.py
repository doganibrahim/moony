import json
import os
import uuid
import datetime
from cryptography.fernet import Fernet
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()
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


class Note:
    def __init__(self, title, content):
        self.id = str(uuid.uuid4())[:8]
        self.title = title
        self.content = content
        self.created_at = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'created_at': self.created_at,
        }


class Notebook:
    def __init__(self):
        self.notes = []
        self.file_name = 'notes.bin'
        self.security = SecurityManager()
        self.load_notes()

    def add_note(self, title, content):
        new_note = Note(title, content)
        self.notes.append(new_note)
        self.save_notes()

    def del_note(self, note_id):
        self.notes = [note for note in self.notes if note.id != note_id]
        self.save_notes()

    def save_notes(self):
        # convert Note objects to list of dicts
        data_to_save = [note.to_dict() for note in self.notes]
        json_str = json.dumps(data_to_save)
        encrypted_data = self.security.encrypt(json_str)
        with open(self.file_name, 'wb') as f:
            f.write(encrypted_data)

    def load_notes(self):
        if not os.path.exists(self.file_name):
            return
        with open(self.file_name, 'rb') as f:
            encrypted_data = f.read()
        try:
            json_str = self.security.decrypt(encrypted_data)
            notes_data = json.loads(json_str)
            self.notes = []
            for datum in notes_data:
                note = Note(datum['title'], datum['content'])
                note.id = datum['id']
                note.created_at = datum['created_at']
                self.notes.append(note)
        except Exception as e:
            console.print(f'[bold red]error loading notes: {e}[/bold red]')

def main():
    notebook = Notebook()

    while True:
        console.clear()
        console.print(Panel('[bold cyan]🌕 moony v1.0[/bold cyan]', expand=False))

        table = Table(show_header=True, header_style="bold magenta")
        table.add_column('id', style='dim', width=12)
        table.add_column('title', min_width=20)
        table.add_column('date', style='green')

        # fill table
        for note in notebook.notes:
            table.add_row(note.id, note.title, note.created_at)
        console.print(table)
        console.print('\n[1]add note  [2]read note [3]delete  [4]exit', style='bold yellow')
        choice = input('select action > ')

        if choice == '1':
            title = input('enter note title: ')
            content = input('enter note content: ')
            notebook.add_note(title, content)
            console.print('[green]saved successfully![/green]')
        elif choice == '2':
            target_id = input('enter note id: ')
            found_note = next((n for n in notebook.notes if n.id == target_id), None)

            if found_note:
                console.print(Panel(found_note.content, title=found_note.title))
                input('press enter to continue')
            else:
                console.print('[red] note not found![/red]')

        elif choice == '3':
            target_id = input('enter note id: ')
            notebook.del_note(target_id)

        elif choice == '4':
            break

if __name__ == '__main__':
    main()