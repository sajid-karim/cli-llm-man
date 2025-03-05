import pytest
from cli_llm_man.main import cli
from click.testing import CliRunner

def test_summary_command():
    runner = CliRunner()
    result = runner.invoke(cli, ['summary', 'ls'])
    assert result.exit_code == 0
    assert 'list' in result.output.lower()  # Check if the output contains a summary of 'ls'

def test_example_command():
    runner = CliRunner()
    result = runner.invoke(cli, ['example', 'ls'])
    assert result.exit_code == 0
    assert 'usage' in result.output.lower()  # Check if the output contains usage examples for 'ls'

def test_generate_command():
    runner = CliRunner()
    result = runner.invoke(cli, ['generate', 'list files in current directory'])
    assert result.exit_code == 0
    assert 'ls' in result.output  # Check if the generated command is 'ls' or similar

def test_invalid_command():
    runner = CliRunner()
    result = runner.invoke(cli, ['summary', 'invalid_command'])
    assert result.exit_code != 0
    assert 'error' in result.output.lower()  # Check if an error message is returned for an invalid command