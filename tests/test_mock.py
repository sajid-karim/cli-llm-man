# Add to tests/test_mock.py

import pytest
from unittest.mock import patch, MagicMock
from cli_llm_man.main import cli
from click.testing import CliRunner

@pytest.fixture
def mock_llm():
    """Mock the LLM interface to avoid actual API calls"""
    with patch('cli_llm_man.llm_interface.LLMInterface') as mock_llm:
        instance = MagicMock()
        instance.generate_summary.return_value = "Mock summary of the command"
        instance.generate_example.return_value = "Mock usage examples"
        instance.generate_command.return_value = "ls -la # Mock generated command"
        mock_llm.return_value = instance
        yield mock_llm

@pytest.fixture
def mock_man_page():
    """Mock the man page retriever"""
    with patch('cli_llm_man.man_retriever.get_man_page') as mock_get:
        mock_get.return_value = "Mock man page content"
        yield mock_get

def test_summary_with_mocks(mock_llm, mock_man_page):
    runner = CliRunner()
    result = runner.invoke(cli, ['summary', 'ls'])
    assert result.exit_code == 0
    assert "Mock summary" in result.output