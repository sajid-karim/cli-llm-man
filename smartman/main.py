import os
import click
from smartman import man_retriever
from smartman.llm_interface import LLMInterface
from smartman.config import load_config
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown

# Initialize rich console
console = Console()

# Check if this is first run
def check_first_run():
    """Check if this is the first time running the tool."""
    home = os.path.expanduser("~")
    config_dir = os.path.join(home, ".smartman")
    flag_file = os.path.join(config_dir, ".first_run_complete")
    
    # Create config directory if it doesn't exist
    if not os.path.exists(config_dir):
        os.makedirs(config_dir, exist_ok=True)
        
    if not os.path.exists(flag_file):
        console.print(Panel(
            "[bold]Welcome to Smartman![/bold]\n\n"
            "For a shorter command, run: [cyan]setup-llm-man-alias[/cyan]\n"
            "This will add an alias called 'llm-man' to your shell profile.", 
            border_style="green"
        ))
        
        # Create flag file so the welcome message is not shown again
        with open(flag_file, 'w') as f:
            f.write("First run completed")
        
    return

@click.group()
def cli():
    """Smartman: Generate man page summaries and commands."""
    check_first_run()

@cli.command()
def help():
    """Show this help message."""
    ctx = click.get_current_context()
    click.echo(cli.get_help(ctx))

@cli.command()
@click.argument('command_name')
def summary(command_name):
    """Generate a summary for a given command."""
    config = load_config()
    llm = LLMInterface(api_key=config.get('LLM_API_KEY'))
    
    console.print(f"[bold blue]Retrieving documentation for [cyan]{command_name}[/cyan]...[/bold blue]")
    doc_text = man_retriever.get_man_page(command_name)
    
    if doc_text.startswith("SHELL BUILTIN COMMAND:"):
        console.print("[bold yellow]Found shell builtin documentation.[/bold yellow]")
    elif doc_text.startswith("COMMAND HELP OUTPUT:"):
        console.print("[bold yellow]Found command help output.[/bold yellow]")
    elif doc_text.startswith("NO_DOCUMENTATION:"):
        console.print("[bold orange]No documentation found. Using LLM's general knowledge.[/bold orange]")
    else:
        console.print("[bold green]Found man page documentation.[/bold green]")
    
    console.print("[bold blue]Generating summary...[/bold blue]")
    summary_text = llm.generate_summary(doc_text)
    md = Markdown(summary_text)
    console.print(Panel(md, title=f"Summary of '{command_name}'", border_style="green"))

@cli.command()
@click.argument('command_name')
def example(command_name):
    """Show usage examples for a given command."""
    config = load_config()
    llm = LLMInterface(api_key=config.get('LLM_API_KEY'))
    
    console.print(f"[bold blue]Retrieving documentation for [cyan]{command_name}[/cyan]...[/bold blue]")
    doc_text = man_retriever.get_man_page(command_name)
    
    if doc_text.startswith("SHELL BUILTIN COMMAND:"):
        console.print("[bold yellow]Found shell builtin documentation.[/bold yellow]")
    elif doc_text.startswith("COMMAND HELP OUTPUT:"):
        console.print("[bold yellow]Found command help output.[/bold yellow]")
    elif doc_text.startswith("NO_DOCUMENTATION:"):
        console.print("[bold orange]No documentation found. Using LLM's general knowledge.[/bold orange]")
    else:
        console.print("[bold green]Found man page documentation.[/bold green]")
    
    console.print("[bold blue]Generating examples...[/bold blue]")
    example_text = llm.generate_example(doc_text)
    md = Markdown(example_text)
    console.print(Panel(md, title=f"Examples for '{command_name}'", border_style="yellow"))

@cli.command()
@click.argument('intent')
def generate(intent):
    """Generate a command based on your intent."""
    config = load_config()
    llm = LLMInterface(api_key=config.get('LLM_API_KEY'))
    
    console.print(f"[bold blue]Generating command for: [cyan]{intent}[/cyan][/bold blue]")
    command = llm.generate_command(intent)
    md = Markdown(command)
    console.print(Panel(md, title="Generated Command", border_style="magenta"))

@cli.command()
def interactive():
    """Start an interactive session with the CLI tool."""
    config = load_config()
    llm = LLMInterface(api_key=config.get('LLM_API_KEY'))
    
    console.print(Panel("[bold]Smartman Interactive Mode[/bold]\nType 'exit' to quit.", 
                        border_style="blue"))
    
    while True:
        user_input = click.prompt('> ', type=str)
        if user_input.lower() == 'exit':
            break
        parts = user_input.split(' ', 1)
        action = parts[0].lower()
        try:
            if action == 'summary' and len(parts) > 1:
                man_text = man_retriever.get_man_page(parts[1])
                md = Markdown(llm.generate_summary(man_text))
                console.print(Panel(md, title=f"Summary of '{parts[1]}'", border_style="green"))
            elif action == 'example' and len(parts) > 1:
                man_text = man_retriever.get_man_page(parts[1])
                md = Markdown(llm.generate_example(man_text))
                console.print(Panel(md, title=f"Examples for '{parts[1]}'", border_style="yellow"))
            elif action == 'generate' and len(parts) > 1:
                md = Markdown(llm.generate_command(parts[1]))
                console.print(Panel(md, title="Generated Command", border_style="magenta"))
            else:
                console.print("[bold red]Unknown command.[/bold red] Use: summary <cmd>, example <cmd>, generate <intent>, interactive, or help")
        except Exception as e:
            console.print(f"[bold red]Error:[/bold red] {str(e)}")

if __name__ == '__main__':
    cli()