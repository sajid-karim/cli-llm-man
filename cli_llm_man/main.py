import click
from cli_llm_man import man_retriever, llm_interface, config

@click.group()
def cli():
    """CLI LLM Man: Generate man page summaries and commands."""
    config.load_config()  # Ensures API key is loaded

@cli.command()
@click.argument('command_name')
def summary(command_name):
    """Generate a summary for a given command."""
    man_text = man_retriever.get_man_page(command_name)
    summary = llm_interface.generate_summary(man_text)
    click.echo(summary)

@cli.command()
@click.argument('command_name')
def example(command_name):
    """Show usage examples for a given command."""
    man_text = man_retriever.get_man_page(command_name)
    example_text = llm_interface.generate_example(man_text)
    click.echo(example_text)

@cli.command()
@click.argument('intent')
def generate(intent):
    """Generate a command based on your intent."""
    command = llm_interface.generate_command(intent)
    click.echo(command)

@cli.command()
def interactive():
    """Start an interactive session with the CLI tool."""
    click.echo("CLI LLM Man Interactive Mode. Type 'exit' to quit.")
    while True:
        command = click.prompt('> ', type=str)
        if command.lower() == 'exit':
            break
        
        parts = command.split(' ', 1)
        action = parts[0].lower()
        
        try:
            if action == 'summary' and len(parts) > 1:
                man_text = man_retriever.get_man_page(parts[1])
                click.echo(llm_interface.generate_summary(man_text))
            elif action == 'example' and len(parts) > 1:
                man_text = man_retriever.get_man_page(parts[1])
                click.echo(llm_interface.generate_example(man_text))
            elif action == 'generate' and len(parts) > 1:
                click.echo(llm_interface.generate_command(parts[1]))
            else:
                click.echo("Unknown command. Use: summary <cmd>, example <cmd>, or generate <intent>")
        except Exception as e:
            click.echo(f"Error: {str(e)}")

if __name__ == '__main__':
    cli()