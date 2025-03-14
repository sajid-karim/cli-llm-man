#!/usr/bin/env python3
"""Example usage of the Smartman tool"""

import os
import subprocess
from click.testing import CliRunner
from smartman.main import cli

def run_example_using_cli_runner():
    """Run examples using Click's testing utilities"""
    runner = CliRunner()
    
    print("Summary for 'ls':")
    result = runner.invoke(cli, ['summary', 'ls'])
    print(result.output)
    
    print("\nUsage examples for 'grep':")
    result = runner.invoke(cli, ['example', 'grep'])
    print(result.output)
    
    print("\nGenerated command for intent 'list all files':")
    result = runner.invoke(cli, ['generate', 'list all files'])
    print(result.output)

def run_example_using_subprocess():
    """Run examples using actual command-line invocation"""
    print("Summary for 'ls':")
    subprocess.run(["python", "-m", "smartman.main", "summary", "ls"])
    
    print("\nUsage examples for 'grep':")
    subprocess.run(["python", "-m", "smartman.main", "example", "grep"])
    
    print("\nGenerated command for intent 'list all files':")
    subprocess.run(["python", "-m", "smartman.main", "generate", "list all files"])

if __name__ == "__main__":
    # Choose one of these methods
    run_example_using_cli_runner()
    # run_example_using_subprocess()