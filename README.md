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
git clone https://github.com/sajid-karim/cli-llm-man.git
cd cli-llm-man
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

Create a configuration file at `~/.cli_llm_man/config.yaml` with the following content:

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
cli-llm-man summary ls

# OR using the module directly
python -m cli_llm_man.main summary ls
```

### Show Usage Examples

To display usage examples for a specific command:

```bash
cli-llm-man example grep

# OR
python -m cli_llm_man.main example grep
```

### Generate Command

To create a command based on your intent:

```bash
cli-llm-man generate "find all PDF files modified in the last 7 days"

# OR
python -m cli_llm_man.main generate "find all PDF files modified in the last 7 days"
```

### Interactive Mode
For continuous interaction with the tool:

```bash
cli-llm-man interactive

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