import os
import yaml

def load_config():
    config_path = os.path.expanduser('~/.cli_llm_man/config.yaml')
    if os.path.exists(config_path):
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)
    else:
        config = {}
    config['LLM_API_KEY'] = os.environ.get('LLM_API_KEY', config.get('LLM_API_KEY'))
    if not config.get('LLM_API_KEY'):
        raise Exception("LLM API key not found. Please set LLM_API_KEY in your environment or config file.")
    return config