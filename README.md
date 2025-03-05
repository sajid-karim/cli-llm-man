# CLI LLM Man

CLI LLM Man is a command-line interface tool designed to generate summaries, examples, and custom commands based on user intent using man pages and a language model API. This tool aims to simplify the process of retrieving and understanding command-line documentation.

## Features

- Generate concise summaries of man pages.
- Display usage examples for specific commands.
- Create custom commands based on natural language descriptions.

## Installation

To install the CLI LLM Man tool, you can either clone the repository or install it via pip.

### Option 1: Install via pip

```bash
pip install .
```

### Option 2: Clone the repository

```bash
git clone https://github.com/yourusername/cli-llm-man.git
cd cli-llm-man
pip install -r requirements.txt
```

## Configuration

Before using the tool, you need to configure your LLM API key. You can do this in two ways:

### Option 1: Environment Variable

Set the environment variable `LLM_API_KEY`:

```bash
export LLM_API_KEY=your_key_here
```

### Option 2: Configuration File

Create a configuration file at `~/.cli_llm_man/config.yaml` with the following content:

```yaml
LLM_API_KEY: your_key_here
```

You can find a sample configuration file in `config.example.yaml`.

## Usage

Once installed and configured, you can use the CLI LLM Man tool with the following commands:

### Generate Summary

To generate a summary for a given command:

```bash
python -m cli_llm_man.main summary <command_name>
```

### Show Usage Examples

To display usage examples for a specific command:

```bash
python -m cli_llm_man.main example <command_name>
```

### Generate Command

To create a command based on your intent:

```bash
python -m cli_llm_man.main generate "<user intent>"
```

## Troubleshooting

If you encounter any issues, please ensure that your API key is set correctly and that all dependencies are installed. Check the `tests/` directory for unit tests to verify functionality.

## Contributing

Contributions are welcome! Please read the [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on how to contribute to this project.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.