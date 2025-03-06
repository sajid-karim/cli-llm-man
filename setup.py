from setuptools import setup, find_packages
import os

# Read requirements from requirements.txt file
def read_requirements():
    with open('requirements.txt') as f:
        return [line.strip() for line in f 
                if line.strip() and not line.startswith('//') and not line.startswith('#')]

setup(
    name="cli-llm-man",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=read_requirements(),
    entry_points={
        "console_scripts": [
            "cli-llm-man=cli_llm_man.main:cli",
        ],
    },
)