# Testing SmartMan

This directory contains tests for the SmartMan CLI tool. The tests are organized into several files, each testing different aspects of the application.

## Test Structure

- **conftest.py**: Contains global fixtures and test configuration that is shared across all test files.
- **test_main.py**: Tests for the main CLI interface and commands.
- **test_mock.py**: Demonstrates how to effectively use mocks for testing.
- **test_cache.py**: Tests for the response caching functionality.

## Running Tests

To run all tests:

```bash
pytest
```

To run tests with verbose output:

```bash
pytest -v
```

To run a specific test file:

```bash
pytest tests/test_main.py
```

To run a specific test:

```bash
pytest tests/test_main.py::TestBasicCommands::test_summary_command
```

## Adding New Tests

When adding new tests, follow these guidelines:

1. **Test Organization**: Add related tests to the appropriate test class/file, or create a new one if needed.
2. **Documentation**: Each test function should have a clear docstring explaining what it tests and how.
3. **Mocking**: Use the provided fixtures to mock external dependencies.
4. **Assertions**: Be specific in assertions, and add helpful error messages.

## Test Fixtures

The test suite provides several useful fixtures that you can use in your tests:

- **cli_runner**: A Click CLI test runner for invoking CLI commands.
- **mock_env_vars**: Sets environment variables for testing with LLM API keys.
- **mock_llm_interface**: Mocks the LLM interface to avoid making actual API calls.
- **mock_man_page**: Mocks the man page retriever to avoid system calls.
- **temp_cache_dir**: Creates a temporary directory for cache testing.
- **disable_mocks**: (For future use) A placeholder for disabling automatic mocks.

## Test Data

Test data is defined in `conftest.py` and includes sample man pages, summaries, and examples for different commands. You can extend this data to support new test cases.

## Best Practices

When writing tests for SmartMan, follow these best practices:

1. **Test in Isolation**: Avoid dependencies on external services or APIs.
2. **Test Behavior, Not Implementation**: Focus on testing what the code does, not how it does it.
3. **Keep Tests Fast**: Tests should run quickly to encourage frequent testing.
4. **Make Tests Readable**: Tests should be clear and well-documented to serve as examples.
5. **Test Edge Cases**: Include tests for error conditions and edge cases.

## Integration Tests

The current test suite focuses on unit testing. If you want to add integration tests that make actual API calls or system calls, consider:

1. Creating a separate integration test suite that can be run separately.
2. Using the `disable_mocks` fixture (to be implemented) to selectively disable mocking.
3. Adding environment variables to control whether integration tests are run.

## Contributing

When contributing to SmartMan, please ensure that:

1. Your code passes all existing tests.
2. You add new tests for any new functionality.
3. Your tests follow the patterns and best practices in this README.

This ensures that SmartMan remains reliable and maintainable as it grows. 