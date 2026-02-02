import sys

from rich.table import Table
from rich.panel import Panel
from rich import box
from utils import console, TextFormatter, get_multiline_input
from models import Notebook
from auth import UserManager

def main():
    user_manager = UserManager()
    console.clear()

    if not user_manager.is_registered():
        user_manager.register()

    if not user_manager.login():
        console.print("[bold red]⛔ access denied.[/bold red]")
        sys.exit()
    notebook = Notebook()

    while True:
        console.clear()
        console.print(Panel('[bold cyan]🌕 moony v1.0[/bold cyan]', expand=False))

        table = Table(show_header=True, header_style="bold magenta")
        table.add_column('id', style='dim', width=12)
        table.add_column('title', min_width=20)
        table.add_column('tags', style='bold yellow')
        table.add_column('date', style='green')

        # fill table
        for note in notebook.notes:
            tag_str = " ".join([f"[reverse] {t} [/]" for t in note.tags])
            table.add_row(note.id, note.title, tag_str, note.created_at)
        console.print(table)
        console.print('\n[1]add note [2]read note [3]delete [4]exit', style='bold yellow')
        choice = input('select action > ')

        if choice == '1':
            title = input('enter note title: ')
            tags_input = input('enter tags (comma separated): ')
            tags_list = [t.strip() for t in tags_input.split(",") if t.strip()]
            content = get_multiline_input()
            if content is None:
                continue

            notebook.add_note(title, content, tags_list)
            console.print('[green]saved successfully![/green]')
        elif choice == '2':
            target_id = input('enter note id: ')
            found_note = next((n for n in notebook.notes if n.id == target_id), None)

            if found_note:
                formatted_title = TextFormatter().parse(found_note.title)
                formatted_content = TextFormatter.parse(found_note.content)
                console.print(Panel(formatted_content, title=formatted_title))
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