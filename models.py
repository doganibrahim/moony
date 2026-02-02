import json
import os
import uuid
from datetime import datetime
from utils import console, TextFormatter, SecurityManager


class Note:
    def __init__(self, title, content, tags = None):
        self.id = str(uuid.uuid4())[:8]
        self.title = title
        self.content = content
        self.tags = tags if tags else []
        self.created_at = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'tags': self.tags,
            'created_at': self.created_at,
        }

    @staticmethod
    def from_dict(d):
        return Note(
            d['title'],
            d['content'],
            d.get('tags', [])
        )

class Notebook:
    def __init__(self):
        self.notes = []
        self.file_name = 'notes.bin'
        self.security = SecurityManager()
        self.load_notes()

    def add_note(self, title, content, tags = []):
        new_note = Note(title, content, tags)
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
                note = Note(
                    datum['title'],
                    datum['content'],
                    datum.get('tags', [])
                )
                note.id = datum['id']
                note.created_at = datum['created_at']
                self.notes.append(note)
        except Exception as e:
            console.print(f'[bold red]error loading notes: {e}[/bold red]')