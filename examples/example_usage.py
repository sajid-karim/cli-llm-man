# Example usage of the CLI LLM Man tool

from cli_llm_man import main

def run_example():
    # Example command to generate a summary for the 'ls' command
    print("Summary for 'ls':")
    main.cli.invoke(main.summary, 'ls')

    # Example command to show usage examples for the 'grep' command
    print("\nUsage examples for 'grep':")
    main.cli.invoke(main.example, 'grep')

    # Example command to generate a command based on user intent
    print("\nGenerated command for intent 'list all files':")
    main.cli.invoke(main.generate, "list all files")

if __name__ == "__main__":
    run_example()