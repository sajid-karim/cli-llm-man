import click
from cli_llm_man import man_retriever
from cli_llm_man.llm_interface import LLMInterface
from cli_llm_man.config import load_config
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown

# Initialize rich console
console = Console()

@click.group()
def cli():
    """CLI LLM Man: Generate man page summaries and commands."""
    pass

@cli.command()
@click.argument('command_name')
def summary(command_name):
    """Generate a summary for a given command."""
    # Load configuration first
    config = load_config()
    
    # Create LLM interface instance
    llm = LLMInterface(api_key=config.get('LLM_API_KEY'))
    
    # Get documentation for the command
    console.print(f"[bold blue]Retrieving documentation for [cyan]{command_name}[/cyan]...[/bold blue]")
    doc_text = man_retriever.get_man_page(command_name)
    
    # Check the type of documentation retrieved and adapt the message
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
    
    # Format and display the summary as markdown
    md = Markdown(summary_text)
    console.print(Panel(md, title=f"Summary of '{command_name}'", border_style="green"))

@cli.command()
@click.argument('command_name')
def example(command_name):
    """Show usage examples for a given command."""
    # Load configuration first
    config = load_config()
    
    # Create LLM interface instance
    llm = LLMInterface(api_key=config.get('LLM_API_KEY'))
    
    # Get documentation for the command
    console.print(f"[bold blue]Retrieving documentation for [cyan]{command_name}[/cyan]...[/bold blue]")
    doc_text = man_retriever.get_man_page(command_name)
    
    # Check the type of documentation retrieved and adapt the message
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
    
    # Format and display the examples as markdown
    md = Markdown(example_text)
    console.print(Panel(md, title=f"Examples for '{command_name}'", border_style="yellow"))

@cli.command()
@click.argument('intent')
def generate(intent):
    """Generate a command based on your intent."""
    # Load configuration first
    config = load_config()
    
    # Create LLM interface instance
    llm = LLMInterface(api_key=config.get('LLM_API_KEY'))
    
    # Generate command
    console.print(f"[bold blue]Generating command for: [cyan]{intent}[/cyan][/bold blue]")
    command = llm.generate_command(intent)
    
    # Format and display the command as markdown
    md = Markdown(command)
    console.print(Panel(md, title="Generated Command", border_style="magenta"))

@cli.command()
def interactive():
    """Start an interactive session with the CLI tool."""
    # Load configuration first
    config = load_config()
    
    # Create LLM interface instance
    llm = LLMInterface(api_key=config.get('LLM_API_KEY'))
    
    console.print(Panel("[bold]CLI LLM Man Interactive Mode[/bold]\nType 'exit' to quit.", 
                        border_style="blue"))
    
    while True:
        command = click.prompt('> ', type=str)
        if command.lower() == 'exit':
            break
        
        parts = command.split(' ', 1)
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
                console.print("[bold red]Unknown command.[/bold red] Use: summary <cmd>, example <cmd>, or generate <intent>")
        except Exception as e:
            console.print(f"[bold red]Error:[/bold red] {str(e)}")

if __name__ == '__main__':
    cli()