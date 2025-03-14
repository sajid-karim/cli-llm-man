from setuptools import setup, find_packages
import os

def read_requirements():
    with open('requirements.txt') as f:
        return [line.strip() for line in f if line.strip() and not line.startswith('//') and not line.startswith('#')]

def read_long_description():
    with open("README.md", encoding="utf-8") as f:
        return f.read()

setup(
    name="smartman",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=read_requirements(),
    long_description=read_long_description(),
    long_description_content_type="text/markdown",
    url="https://github.com/sajid-karim/cli-llm-man",
    author="Sajid karim",
    author_email="sajidkareem1914@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    entry_points={
        "console_scripts": [
            "smartman=cli_llm_man.main:cli",
            "setup-smartman-alias=cli_llm_man.setup_alias:setup_alias",
        ],
    },
)