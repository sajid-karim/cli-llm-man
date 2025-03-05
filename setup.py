from setuptools import setup, find_packages

setup(
    name='cli-llm-man',
    version='0.1.0',
    description='A CLI tool for generating man page summaries and commands using LLMs.',
    author='Your Name',
    author_email='your.email@example.com',
    url='https://github.com/yourusername/cli-llm-man',
    packages=find_packages(),
    install_requires=[
        'click',
        'pyyaml',
        'requests',  # Assuming requests is needed for LLM API calls
    ],
    entry_points={
        'console_scripts': [
            'cli-llm-man=cli_llm_man.main:cli',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)