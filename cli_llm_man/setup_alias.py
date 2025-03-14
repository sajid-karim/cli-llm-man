#!/usr/bin/env python3
import os
from rich.console import Console
from rich.panel import Panel

console = Console()

def setup_alias():
    """Add the 'llm-man' alias to the user's shell profile."""
    console.print(Panel(
        "[bold]SmartMan - Alias Setup[/bold]\n\n"
        "This will add an alias 'llm-man' to your shell profile so you can run the tool using a shorter command.",
        border_style="green"
    ))
    
    home = os.path.expanduser("~")
    profile_files = [
        os.path.join(home, ".bashrc"),
        os.path.join(home, ".bash_profile"),
        os.path.join(home, ".zshrc")
    ]
    
    profile_file = None
    for file in profile_files:
        if os.path.exists(file):
            profile_file = file
            break
    
    if not profile_file:
        console.print("[bold red]Could not find a suitable shell profile file.[/bold red]")
        return False
    
    with open(profile_file, 'r') as f:
        content = f.read()
        if "alias llm-man=" in content:
            console.print(f"[bold yellow]Alias 'llm-man' already exists in {profile_file}[/bold yellow]")
            return True
    
    with open(profile_file, 'a') as f:
        f.write("\n# SmartMan alias\nalias llm-man='smartman'\n")
    
    console.print(f"[bold green]Alias 'llm-man' added to {profile_file}[/bold green]")
    console.print(f"\nRun [bold cyan]source {profile_file}[/bold cyan] to load the alias in your current session.")
    console.print(Panel(
        "Usage Examples:\n\n"
        "[bold cyan]llm-man summary ls[/bold cyan]\n"
        "[bold cyan]llm-man example grep[/bold cyan]\n"
        "[bold cyan]llm-man generate \"find all pdf files\"[/bold cyan]\n"
        "[bold cyan]llm-man interactive[/bold cyan]",
        title="SmartMan Usage",
        border_style="blue"
    ))
    return True

if __name__ == "__main__":
    setup_alias()