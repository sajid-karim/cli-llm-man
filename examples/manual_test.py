# Add to examples/manual_test.py

import os
import sys
import subprocess

def run_tests():
    """Run a series of commands to test the CLI tool"""
    print("Testing Smartman tool...")
    
    # Check if API key is set
    if not os.environ.get('LLM_API_KEY'):
        print("Warning: LLM_API_KEY environment variable not set!")
        print("Setting a temporary dummy key for testing (will cause API errors)")
        os.environ['LLM_API_KEY'] = 'dummy_key_for_testing'

    # Test commands
    commands = [
        ["python", "-m", "cli_llm_man.main", "summary", "ls"],
        ["python", "-m", "cli_llm_man.main", "example", "grep"],
        ["python", "-m", "cli_llm_man.main", "generate", "find all PDF files in current directory"]
    ]
    
    for cmd in commands:
        print(f"\nRunning command: {' '.join(cmd)}")
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                print(f"Success! Output:\n{result.stdout[:200]}...")
            else:
                print(f"Error (code {result.returncode}):\n{result.stderr}")
        except Exception as e:
            print(f"Exception: {e}")

if __name__ == "__main__":
    run_tests()