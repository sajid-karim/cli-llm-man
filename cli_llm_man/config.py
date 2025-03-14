import os
import yaml

def load_config():
    config_path = os.path.expanduser('~/.smartman/config.yaml')
    if os.path.exists(config_path):
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file) or {}
    else:
        config = {}

    # Primary LLM API key
    config['LLM_API_KEY'] = os.environ.get('LLM_API_KEY', config.get('LLM_API_KEY'))
    
    # Additional keys for specific providers
    config['OPENAI_API_KEY'] = os.environ.get('OPENAI_API_KEY', config.get('OPENAI_API_KEY'))
    config['ANTH_API_KEY'] = os.environ.get('ANTH_API_KEY', config.get('ANTH_API_KEY'))

    # Ensure at least one API key is available
    if not (config.get('LLM_API_KEY') or config.get('OPENAI_API_KEY') or config.get('ANTH_API_KEY')):
        raise Exception("No LLM API key found. Please set LLM_API_KEY, OPENAI_API_KEY, or ANTH_API_KEY in your environment or config file.")
    
    return config