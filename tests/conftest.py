"""
Global pytest fixtures and test configuration.

This module contains fixtures that are automatically applied to all tests.
These fixtures help isolate tests by mocking external dependencies.
"""

import pytest
import os
from unittest.mock import patch, MagicMock

# Sample test data that can be reused across tests
TEST_DATA = {
    'commands': {
        'ls': {
            'summary': "List directory contents - provides a detailed view of files and directories",
            'example': "ls -la\nls -lh\nls --color=auto",
            'man_page': "LS(1)  User Commands  LS(1)\nNAME\n       ls - list directory contents\nSYNOPSIS\n       ls [OPTION]... [FILE]..."
        },
        'grep': {
            'summary': "Search for patterns in text using regular expressions",
            'example': "grep 'pattern' file.txt\ngrep -i 'case insensitive' file.txt\ngrep -r 'recursive' directory/",
            'man_page': "GREP(1)  User Commands  GREP(1)\nNAME\n       grep, egrep, fgrep - print lines that match patterns\nSYNOPSIS\n       grep [OPTION]... PATTERNS [FILE]..."
        },
        'invalid': {
            'summary': "Command not found",
            'example': "Command not found",
            'man_page': "NO_DOCUMENTATION: Command not found"
        }
    }
}

@pytest.fixture(autouse=True)
def mock_env_vars():
    """
    Set environment variables for testing.
    
    This fixture ensures API keys are available for tests without requiring
    actual API credentials, making tests reproducible in any environment.
    """
    # Save any existing environment variables
    old_env = {}
    for key in ['OPENAI_API_KEY', 'ANTH_API_KEY', 'LLM_API_KEY']:
        if key in os.environ:
            old_env[key] = os.environ[key]
    
    # Set test environment variables
    os.environ['OPENAI_API_KEY'] = 'test_openai_api_key_for_testing'
    os.environ['ANTH_API_KEY'] = 'test_anthropic_api_key_for_testing'
    os.environ['LLM_API_KEY'] = 'test_general_api_key_for_testing'
    
    yield
    
    # Restore original environment or remove test variables
    for key in ['OPENAI_API_KEY', 'ANTH_API_KEY', 'LLM_API_KEY']:
        if key in old_env:
            os.environ[key] = old_env[key]
        elif key in os.environ:
            del os.environ[key]

@pytest.fixture(autouse=True)
def mock_llm_interface():
    """
    Mock the LLM interface to avoid any API calls.
    
    This fixture replaces the LLMInterface with a mock that returns
    predefined responses, ensuring tests don't make actual API calls.
    """
    with patch('smartman.main.LLMInterface') as mock_llm:
        instance = MagicMock()
        
        # Configure default return values
        instance.generate_summary.return_value = "Mock summary text"
        instance.generate_example.return_value = "Mock example text"
        instance.generate_command.return_value = "Mock command text"
        
        # Make the mock more flexible by allowing customization of responses
        def get_summary_for_command(text):
            # Extract command name from man page text if possible
            command = next((cmd for cmd in TEST_DATA['commands'] if cmd in text), 'ls')
            return TEST_DATA['commands'][command]['summary']
            
        def get_example_for_command(text):
            command = next((cmd for cmd in TEST_DATA['commands'] if cmd in text), 'ls')
            return TEST_DATA['commands'][command]['example']
            
        def generate_command_from_intent(intent):
            if 'list' in intent and 'file' in intent:
                return "ls -la # Lists all files including hidden ones"
            elif 'search' in intent or 'find' in intent:
                return "grep 'pattern' file.txt # Searches for pattern in file"
            else:
                return "echo 'Command generated based on: " + intent + "'"
        
        # Configure side effect functions that can dynamically respond based on input
        instance.generate_summary.side_effect = get_summary_for_command
        instance.generate_example.side_effect = get_example_for_command
        instance.generate_command.side_effect = generate_command_from_intent
        
        mock_llm.return_value = instance
        yield mock_llm

@pytest.fixture(autouse=True)
def mock_man_page():
    """
    Mock the man page retriever.
    
    This fixture prevents actual system calls to retrieve man pages,
    instead returning predefined content based on the command.
    """
    with patch('smartman.main.man_retriever.get_man_page') as mock_get:
        def get_man_page_for_command(command):
            # Return predefined man pages for common commands or a default for unknown ones
            if command in TEST_DATA['commands']:
                return TEST_DATA['commands'][command]['man_page']
            else:
                return TEST_DATA['commands']['invalid']['man_page']
                
        mock_get.side_effect = get_man_page_for_command
        yield mock_get

@pytest.fixture
def cli_runner():
    """
    Provide a Click CLI test runner.
    
    This fixture simplifies testing Click commands by providing a preconfigured runner.
    """
    from click.testing import CliRunner
    return CliRunner()

@pytest.fixture
def disable_mocks():
    """
    Temporarily disable all automatic mocks.
    
    Use this fixture in tests where you want to test with real implementations
    rather than mocks. Note that this may require actual API keys.
    """
    # This is a helper fixture for potential integration tests
    # It doesn't do anything by itself since it can't undo autouse fixtures
    # but is useful documentation for future integration test development
    return None 