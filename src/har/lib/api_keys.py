import json
import os
import os.path
from .common import PROVIDER_NAME_ANTHROPIC, PROVIDER_NAME_OPENAI, PROVIDER_NAME_XAI

API_KEYS_FILE_UNDER_HOME_DIR = '.har/keys.json'
API_KEYS = None
SUPPORTED_PROVIDERS = [PROVIDER_NAME_ANTHROPIC, PROVIDER_NAME_OPENAI, PROVIDER_NAME_XAI]


def read_api_keys_from_file():
    global API_KEYS
    home_dir = os.environ['HOME']
    api_keys_file_abs_path = os.path.join(home_dir, API_KEYS_FILE_UNDER_HOME_DIR)
    if not os.path.exists(api_keys_file_abs_path):
        raise FileNotFoundError()
    with open(api_keys_file_abs_path, 'r') as fh:
        API_KEYS = json.load(fh)
    for key in API_KEYS.keys():
        if key not in SUPPORTED_PROVIDERS:
            raise Exception(f'Invalid key found - {key}')


def get_api_key(provider_name: str) -> str:
    if not API_KEYS:
        read_api_keys_from_file()
    return API_KEYS[provider_name]
