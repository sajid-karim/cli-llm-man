# SmartMan

SmartMan is a command-line interface tool designed to generate summaries, examples, and custom commands based on user intent using man pages and large language models (LLMs). This tool aims to simplify the process of retrieving and understanding command-line documentation.

## Features

- Generate concise summaries of man pages
- Display practical usage examples for specific commands
- Create custom commands based on natural language descriptions
- Interactive mode for continuous querying
- Support for multiple LLM providers (OpenAI and Anthropic)
- Response caching to reduce API calls and improve speed

## Installation

To install the SmartMan tool, you can either install via pip or clone the repository.

### Option 1: Install via pip

```bash
pip install smartman
```

For development:

```bash
python3 -m venv ~/venvs/smartman
source ~/venvs/smartman/bin/activate
pip install -e .
```

### Option 2: Clone the repository

```bash
git clone https://github.com/sajid-karim/smartman.git
cd smartman
pip install -r requirements.txt
```

## Configuration

Before using the tool, you need to configure your LLM API key. You can do this in two ways:

### Option 1: Environment Variable

Set one of the following environment variables:

# For OpenAI (preferred)
```bash
export OPENAI_API_KEY='your-key-here'
```
# For Anthropic
```bash
export ANTH_API_KEY='your-key-here'
```

### Option 2: Configuration File

Create a configuration file at `~/.smartman/config.yaml` with the following content:

```yaml
# For OpenAI
LLM_API_KEY: your_openai_key_here
PROVIDER: openai  # Optional, defaults to openai
MODEL: gpt-4o    # Optional, defaults to gpt-4o

# OR for Anthropic
LLM_API_KEY: your_anthropic_key_here
PROVIDER: anthropic
MODEL: claude-3-opus-20240229  # Optional
```

You can find a sample configuration file in `config.example.yaml`.

## Usage

Once installed and configured, you can use the SmartMan tool with the following commands:

### Generate Summary

To generate a summary for a given command:

```bash
# Using the installed command
smartman summary ls

# OR using the module directly
python -m smartman.main summary ls
```

### Show Usage Examples

To display usage examples for a specific command:

```bash
smartman example grep

# OR
python -m smartman.main example grep
```

### Generate Command

To create a command based on your intent:

```bash
smartman generate "find all PDF files modified in the last 7 days"

# OR
python -m smartman.main generate "find all PDF files modified in the last 7 days"
```

### Interactive Mode
For continuous interaction with the tool:

```bash
smartman interactive

# Then type commands like:
# summary ls
# example grep
# generate "count lines in all python files"
# exit
```

### Alias Setup

To simplify running the SmartMan tool, you can add a shortcut alias to your shell profile. This alias allows you to run the tool using the command `llm-man` instead of typing out `smartman`.

To set up the alias, run the following command in your terminal:

```bash
setup-smartman-alias
```

This command will add the alias to your shell profile (e.g. `.bashrc`, `.bash_profile`, or `.zshrc`). After running the command, reload your shell (or source the profile) with:

```bash
source ~/.bashrc
# or
source ~/.bash_profile
# or for zsh users:
source ~/.zshrc
```

Now you can run the tool using the shorter command. For example:

```bash
llm-man summary ls
llm-man example grep
llm-man generate "find all PDF files modified in the last 7 days"
```

### Caching

By default, responses are cached to improve performance and reduce API calls. The cache is stored in ~/.smartman/cache/. To disable caching, set use_cache: False in your config file.

## Testing

SmartMan has a comprehensive test suite designed to ensure reliability and make contributions easier.

To run the tests:

```bash
pip install pytest
pytest
```

The test suite includes:
- Unit tests for core functionality
- Mock-based tests to avoid API dependencies
- Tests for error handling and edge cases
- Examples of testing techniques for contributors

For more details on the testing approach and how to add new tests, see [tests/README.md](tests/README.md).

## Contributing

Contributions are welcome! Please read the [contributing.md](contributing.md) guidelines for how to contribute to this project.

Before submitting a pull request:
1. Ensure your code adheres to the project's coding style
2. Add tests for any new functionality
3. Verify that all tests pass with `pytest`
4. Update documentation as needed

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.