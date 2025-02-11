import os
import os.path

PROVIDER_NAME_ANTHROPIC = 'Anthropic'
PROVIDER_NAME_OPENAI = 'OpenAI'
PROVIDER_NAME_XAI = 'XAI'
OPENAI_API_KEYS_FILE_RELATIVE_TO_HOME_DIR_PATH = '.openai/keys'
XAI_API_KEYS_FILE_RELATIVE_TO_HOME_DIR_PATH = '.xai/keys'
ANTHROPIC_API_KEYS_FILE_RELATIVE_TO_HOME_DIR_PATH = '.anthropic/keys'


def get_api_key(provider: str) -> str:
    home_dir = os.environ['HOME']
    if provider not in (PROVIDER_NAME_ANTHROPIC, PROVIDER_NAME_OPENAI, PROVIDER_NAME_XAI):
        raise ValueError
    if provider == PROVIDER_NAME_OPENAI:
        keys_file = os.path.join(home_dir, OPENAI_API_KEYS_FILE_RELATIVE_TO_HOME_DIR_PATH)
    elif provider == PROVIDER_NAME_XAI:
        keys_file = os.path.join(home_dir, XAI_API_KEYS_FILE_RELATIVE_TO_HOME_DIR_PATH)
    elif provider == PROVIDER_NAME_ANTHROPIC:
        keys_file = os.path.join(home_dir, ANTHROPIC_API_KEYS_FILE_RELATIVE_TO_HOME_DIR_PATH)
    else:
        raise Exception
    with open(keys_file) as fh:
        api_key = fh.readline()
        if api_key[-1] == '\n':
            api_key = api_key[:-1]
    return api_key


