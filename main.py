import sys
from rich.table import Table
from rich.panel import Panel
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
        console.print("\n  [bold white]MOONY[/]  [dim white]—[/]  [dim]minimalist notes[/]\n")

        table = Table(
            show_header=True,
            header_style="bold white",
            border_style="dim white",
            show_edge=False,
            pad_edge=False,
            padding=(0, 2)
        )
        table.add_column('ID', style='dim white', width=10, no_wrap=True)
        table.add_column('TITLE', style='white', min_width=20)
        table.add_column('TAGS', style='dim cyan', no_wrap=True)
        table.add_column('DATE', style='dim white', justify='right', width=18)

        # fill table
        for note in notebook.notes:
            tag_str = " ".join([f"#{t}" for t in note.tags]) if note.tags else "—"
            table.add_row(note.id, note.title, tag_str, note.created_at)
        console.print(table)
        console.print("\n  [dim white]1[/] add  [dim white]2[/] read  [dim white]3[/] delete  [dim white]4[/] search  [dim white]5[/] exit")
        choice = console.input("\n  [white]›[/] ")

        if choice == '1':
            console.clear()
            console.print("\n  [white]NEW NOTE[/]\n")
            title = console.input("  title   › ")
            tags_input = console.input("  tags    › ")
            tags_list = [t.strip() for t in tags_input.split(",") if t.strip()]
            console.print("  content › ")
            content = get_multiline_input()
            if content is None:
                continue

            notebook.add_note(title, content, tags_list)
            console.print("\n  [dim green]✓ saved[/]")
            console.input("\n  [dim]press enter...[/]")
        elif choice == '2':
            target_id = console.input("\n  id › ")
            found_note = next((n for n in notebook.notes if n.id == target_id), None)

            if found_note:
                while True:
                    console.clear()
                    formatted_title = TextFormatter().parse(found_note.title)
                    formatted_content = TextFormatter.parse(found_note.content)
                    tag_display = " ".join([f"[dim cyan]#{t}[/]" for t in found_note.tags]) if found_note.tags else ""
                    
                    console.print(f"\n  [bold white]{formatted_title}[/]")
                    if tag_display:
                        console.print(f"  {tag_display}")
                    console.print(f"  [dim white]{found_note.created_at}[/]\n")
                    console.print("  " + formatted_content.replace("\n", "\n  "))
                    
                    console.print("\n\n  [dim white]e[/] edit  [dim white]enter[/] back")
                    action = console.input("\n  › ")
                    
                    if action.lower() == 'e':
                        console.clear()
                        console.print("\n  [white]EDIT NOTE[/]\n")
                        console.print(f"  [dim]current: {found_note.title}[/]")
                        new_title = console.input("  title   › ")
                        if not new_title.strip():
                            new_title = found_note.title
                        
                        current_tags = ",".join(found_note.tags) if found_note.tags else ""
                        console.print(f"  [dim]current: {current_tags if current_tags else '(none)'}[/]")
                        new_tags_input = console.input("  tags    › ")
                        if not new_tags_input.strip():
                            new_tags = found_note.tags
                        else:
                            new_tags = [t.strip() for t in new_tags_input.split(",") if t.strip()]
                        
                        console.print("\n  [white]content[/] [dim](edit below, CTRL + S to save)[/]\n")
                        new_content = get_multiline_input(found_note.content)
                        
                        if new_content is not None:
                            notebook.edit_note(target_id, new_title, new_content, new_tags)
                            found_note.title = new_title
                            found_note.content = new_content
                            found_note.tags = new_tags
                            console.print("\n  [dim green]✓ updated[/]")
                            console.input("\n  [dim]press enter...[/]")
                    else:
                        break
            else:
                console.print("\n  [dim red]not found[/]")
                console.input("\n  [dim]press enter...[/]")

        elif choice == '3':
            target_id = console.input("\n  id › ")
            notebook.del_note(target_id)
            console.print("\n  [dim green]✓ deleted[/]")
            console.input("\n  [dim]press enter...[/]")

        elif choice == '4':
            console.clear()
            console.print("\n  [white]SEARCH[/]\n")
            search_query = console.input("  query › ").lower()
            
            if not search_query:
                console.print("\n  [dim red]empty query[/]")
                console.input("\n  [dim]press enter...[/]")
                continue

            results = [
                note for note in notebook.notes
                if search_query in note.title.lower() or
                   search_query in note.content.lower() or
                   any(search_query in tag.lower() for tag in note.tags)
            ]

            if results:
                console.print(f"\n  [dim white]found {len(results)}[/]\n")
                
                search_table = Table(
                    show_header=True,
                    header_style="bold white",
                    border_style="dim white",
                    show_edge=False,
                    pad_edge=False,
                    padding=(0, 2)
                )
                search_table.add_column('ID', style='dim white', width=10)
                search_table.add_column('TITLE', style='white', min_width=20)
                search_table.add_column('TAGS', style='dim cyan')
                search_table.add_column('DATE', style='dim white', justify='right', width=18)

                for note in results:
                    tag_str = " ".join([f"#{t}" for t in note.tags]) if note.tags else "—"
                    search_table.add_row(note.id, note.title, tag_str, note.created_at)
                
                console.print(search_table)
            else:
                console.print("\n  [dim red]no results[/]")
            
            console.input("\n  [dim]press enter...[/]")

        elif choice == '5':
            console.clear()
            console.print("\n  [dim white]goodbye[/]\n")
            break

if __name__ == '__main__':
    main()