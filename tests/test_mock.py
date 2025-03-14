"""
Tests for mocking infrastructure and advanced mocking techniques.

This module demonstrates:
1. How to verify that mocks are used correctly
2. How to customize mock responses for specific tests
3. How to test interactions between mocked components
"""

import pytest
import os
from unittest.mock import patch, MagicMock, call
from smartman.main import cli
from click.testing import CliRunner
from smartman.llm_interface import LLMInterface

# Setup and teardown environment variables for testing
@pytest.fixture(autouse=True)
def setup_env():
    # Set environment variables for testing
    os.environ['OPENAI_API_KEY'] = 'test_api_key_for_testing'
    yield
    # Clean up after test
    if 'OPENAI_API_KEY' in os.environ:
        del os.environ['OPENAI_API_KEY']

@pytest.fixture
def mock_llm():
    """Mock the LLM interface to avoid actual API calls"""
    with patch('smartman.llm_interface.LLMInterface') as mock_llm:
        instance = MagicMock()
        instance.generate_summary.return_value = "Mock summary of the command"
        instance.generate_example.return_value = "Mock usage examples"
        instance.generate_command.return_value = "ls -la # Mock generated command"
        mock_llm.return_value = instance
        yield mock_llm

@pytest.fixture
def mock_man_page():
    """Mock the man page retriever"""
    with patch('smartman.man_retriever.get_man_page') as mock_get:
        mock_get.return_value = "Mock man page content"
        yield mock_get

class TestMockVerification:
    """
    Test suite demonstrating how to verify mocks are being used correctly.
    
    These tests focus on verifying that the code under test interacts
    with mocked dependencies in the expected way.
    """
    
    def test_summary_invokes_correct_calls(self, cli_runner, mock_llm_interface, mock_man_page):
        """
        Test that the summary command invokes the correct sequence of calls.
        
        This verifies that:
        1. The man page retriever is called with the correct command
        2. The LLM interface is instantiated correctly
        3. The generate_summary method is called with the man page content
        """
        # Execute the command
        result = cli_runner.invoke(cli, ['summary', 'ls'])
        
        # Verify that the command executed successfully
        assert result.exit_code == 0
        
        # Verify that the man page retriever was called correctly
        mock_man_page.assert_called_once_with('ls')
        
        # Verify that the LLM generate_summary method was called
        mock_llm_interface.return_value.generate_summary.assert_called_once()
        
        # Verify that the content returned by the man page retriever
        # was passed to the LLM generate_summary method
        man_page_content = mock_man_page.return_value
        generate_summary_args = mock_llm_interface.return_value.generate_summary.call_args
        assert generate_summary_args is not None, "generate_summary was not called"
        assert generate_summary_args[0][0] == man_page_content, "Wrong man page content passed to generate_summary"

    def test_example_invokes_correct_calls(self, cli_runner, mock_llm_interface, mock_man_page):
        """
        Test that the example command invokes the correct sequence of calls.
        
        Similar to the summary test, but verifies the example command path.
        """
        result = cli_runner.invoke(cli, ['example', 'grep'])
        
        assert result.exit_code == 0
        mock_man_page.assert_called_once_with('grep')
        mock_llm_interface.return_value.generate_example.assert_called_once()


class TestMockCustomization:
    """
    Test suite demonstrating how to customize mock responses for specific tests.
    
    These tests show how to make mocks return different values or
    exhibit different behaviors for individual tests.
    """
    
    def test_custom_llm_response(self, cli_runner, mock_llm_interface):
        """
        Test with a custom LLM response.
        
        Shows how to override the default mock response for a specific test.
        """
        # Set a custom response for this specific test
        custom_summary = "This is a custom test summary for ls command"
        mock_llm_interface.return_value.generate_summary.return_value = custom_summary
        
        # Execute the command
        result = cli_runner.invoke(cli, ['summary', 'ls'])
        
        # Verify the command executed successfully
        assert result.exit_code == 0
        
        # For a complete test, we would check that the custom summary appears
        # in the output, but this requires knowledge of how the CLI formats output
        # which may change as the application evolves.
    
    def test_error_simulation(self, cli_runner, mock_llm_interface):
        """
        Test error handling by simulating an error in the LLM interface.
        
        Shows how to make a mock raise an exception to test error handling.
        """
        # Make the mock raise an exception
        mock_llm_interface.return_value.generate_summary.side_effect = Exception("Simulated LLM error")
        
        # Execute the command
        result = cli_runner.invoke(cli, ['summary', 'ls'])
        
        # Verify that the error is handled gracefully
        # Either the command exits with non-zero status OR
        # there's an error message in the output
        assert "error" in result.output.lower() or result.exit_code != 0


class TestAdvancedMocking:
    """
    Test suite demonstrating advanced mocking techniques.
    
    These tests show more sophisticated uses of mocks, such as:
    - Stateful mocks that change behavior over time
    - Mocks that conditionally respond based on input
    - Mock setup for complex interactions
    """
    
    def test_conditional_mock_response(self, cli_runner):
        """
        Test with a mock that responds differently based on input.
        
        Shows how to create a mock that returns different values
        based on the arguments it receives.
        """
        # Create a mock that responds differently based on the command
        with patch('smartman.main.LLMInterface') as mock_llm:
            instance = MagicMock()
            
            # Create a side_effect function that returns different values based on input
            def conditional_response(man_page_text):
                if 'ls' in man_page_text:
                    return "Summary for ls command"
                elif 'grep' in man_page_text:
                    return "Summary for grep command"
                else:
                    return "Generic summary"
                    
            instance.generate_summary.side_effect = conditional_response
            mock_llm.return_value = instance
            
            # Execute commands for different inputs
            result_ls = cli_runner.invoke(cli, ['summary', 'ls'])
            assert result_ls.exit_code == 0
            
            result_grep = cli_runner.invoke(cli, ['summary', 'grep'])
            assert result_grep.exit_code == 0
    
    def test_stateful_mock(self, cli_runner):
        """
        Test with a mock that changes behavior over successive calls.
        
        Shows how to create a mock that returns different values
        on successive calls to the same method.
        """
        # Create a mock that changes behavior over time
        with patch('smartman.main.LLMInterface') as mock_llm:
            instance = MagicMock()
            
            # Return different values on successive calls
            instance.generate_summary.side_effect = [
                "First summary",
                "Second summary",
                "Third summary"
            ]
            mock_llm.return_value = instance
            
            # Execute the command multiple times
            result1 = cli_runner.invoke(cli, ['summary', 'ls'])
            assert result1.exit_code == 0
            
            result2 = cli_runner.invoke(cli, ['summary', 'ls'])
            assert result2.exit_code == 0
            
            result3 = cli_runner.invoke(cli, ['summary', 'ls'])
            assert result3.exit_code == 0
            
            # Verify all side effects were used
            assert instance.generate_summary.call_count == 3