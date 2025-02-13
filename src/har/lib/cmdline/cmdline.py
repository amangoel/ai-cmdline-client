from ..common import FUNCTIONALITY_CHAT, FUNCTIONALITY_IMAGE_UNDERSTANDING, FUNCTIONALITY_REASONING
from ..common import FUNCTIONALITY_TO_PROMPT_SYMBOL_MAP, SUPPORTED_FUNCTIONALITY
from ..functionality import get_default_provider_model_for, set_default_provider_model_for
from ..functionality import get_available_functionality_and_models
from ..functionality.chat import get_chat_response_for_single_message
from ..functionality.image_understanding import SUPPORTED_EXTENSIONS_FOR_IMAGE_UNDERSTANDING_LOWERCASE, understand_image
from ..functionality.reasoning import get_reasoning
from .help import print_help
import os.path
import re


NOT_INVOKED = -1
QUIT = 0
NEXT_PROMPT = 1


def print_available_functionality_and_models():
    func_to_models_map = get_available_functionality_and_models()
    functionalities = sorted(func_to_models_map.keys())
    for functionality in functionalities:
        default_prov_n_model = get_default_provider_model_for(functionality)
        prompt_symbol = FUNCTIONALITY_TO_PROMPT_SYMBOL_MAP[functionality]
        print(f'Available models for {functionality} (symbol = {prompt_symbol}):')
        provider_and_models = func_to_models_map[functionality]
        num_provider_and_models = len(provider_and_models)
        for i in range(num_provider_and_models):
            provider_and_model = provider_and_models[i]
            if default_prov_n_model.provider == provider_and_model.provider and \
                    default_prov_n_model.model == provider_and_model.model:
                print(f'\t{i} {provider_and_model.provider}.{provider_and_model.model} (current)')
            else:
                print(f'\t{i} {provider_and_model.provider}.{provider_and_model.model}')


def process_tool_command_model(tokens) -> int:
    if tokens[1] != 'model':
        return NOT_INVOKED

    if len(tokens) == 2:
        return NOT_INVOKED

    if tokens[2] not in ('list', 'set'):
        return NOT_INVOKED

    if tokens[2] == 'list':
        print_available_functionality_and_models()
        return NEXT_PROMPT

    if len(tokens) < 5:
        return NOT_INVOKED

    functionality_of_to_be_set_model = None
    for k, v in FUNCTIONALITY_TO_PROMPT_SYMBOL_MAP.items():
        if v == tokens[3]:
            functionality_of_to_be_set_model = k
            break
    if not functionality_of_to_be_set_model or functionality_of_to_be_set_model not in SUPPORTED_FUNCTIONALITY:
        return NOT_INVOKED

    try:
        specified_model_num = int(tokens[4])
    except:
        specified_model_num = -1

    available_prov_n_models = get_available_functionality_and_models()[functionality_of_to_be_set_model]
    if specified_model_num >= len(available_prov_n_models) or specified_model_num < 0:
        print_available_functionality_and_models()
        return NEXT_PROMPT
    else:
        provider_and_model_to_set = available_prov_n_models[specified_model_num]
        set_default_provider_model_for(functionality_of_to_be_set_model, provider_and_model_to_set)
        print(f'Have set current model for {functionality_of_to_be_set_model} to ', end='')
        print(f'{provider_and_model_to_set.provider}.{provider_and_model_to_set.model}')
        return NEXT_PROMPT


def process_tool_command(user_input: str) -> int:
    tokens = user_input.split()
    if tokens[0] != '!':
        return NOT_INVOKED
    if len(tokens) == 1:
        return NOT_INVOKED
    if len(tokens) == 2 and tokens[1].lower() == 'h':
        print_help()
        return NEXT_PROMPT
    elif len(tokens) == 2 and tokens[1].lower() in ('bye', 'exit', 'q', 'quit', 'stop'):
        return QUIT
    elif tokens[1] == 'model':
        return process_tool_command_model(tokens)
    else:
        return NOT_INVOKED


def process_chat_prompt(user_input: str) -> int:
    tokens = user_input.split()
    if tokens[0] not in ('?', '?<'):
        return NOT_INVOKED
    if tokens[0] == '?':
        if len(tokens) == 1:
            return NOT_INVOKED
        user_prompt = user_input[2:].strip()
    else:  # tokens[0] == '?<'
        if len(tokens) != 2:
            return NOT_INVOKED
        prompt_file_path = tokens[1]
        if not os.path.exists(prompt_file_path):
            print('Cannot find file at the given path.')
            return NEXT_PROMPT
        with open(prompt_file_path) as fh:
            user_prompt = fh.read().strip()
        print('Sending the following prompt:')
        print('------------------------------')
        print(user_prompt)
        print('------------------------------')

    provider_model = get_default_provider_model_for(FUNCTIONALITY_CHAT)
    chat_response = get_chat_response_for_single_message(provider_model, user_prompt)
    print(f'{provider_model.provider}.{provider_model.model} says ', end='')
    print(
        f'(#{chat_response.get_input_tokens_known_by_provider_as()} tokens={chat_response.get_num_input_tokens()} ',
        end=''
    )
    print(
        f'#{chat_response.get_output_tokens_known_by_provider_as()} tokens={chat_response.get_num_output_tokens()}):'
    )
    print(chat_response.get_response_text())
    return NEXT_PROMPT


def process_image_understanding_prompt(user_input: str) -> int:
    tokens = user_input.split()
    if tokens[0] != '#':
        return NOT_INVOKED
    if len(tokens) < 3:
        return NOT_INVOKED
    image_path = tokens[1]
    if not os.path.exists(image_path):
        print('Cannot find image at the given path.')
        return NEXT_PROMPT
    image_extension = os.path.splitext(image_path)[1].lower()
    if image_extension:
        image_extension = image_extension[1:]
    if image_extension not in SUPPORTED_EXTENSIONS_FOR_IMAGE_UNDERSTANDING_LOWERCASE:
        comma_separated_exts = ', '.join(SUPPORTED_EXTENSIONS_FOR_IMAGE_UNDERSTANDING_LOWERCASE)
        print(f'Only the following extensions are supported: {comma_separated_exts}')
        return NEXT_PROMPT
    match_obj = re.search(re.escape(image_path), user_input)
    text_prompt = user_input[match_obj.end():].strip()
    if not text_prompt:
        return NOT_INVOKED
    provider_model = get_default_provider_model_for(FUNCTIONALITY_IMAGE_UNDERSTANDING)
    image_understanding_response = understand_image(provider_model, image_path, text_prompt)
    response_text = image_understanding_response.get_response_text()
    input_tokens_known_by_provider_as = image_understanding_response.get_input_tokens_known_by_provider_as()
    num_input_tokens = image_understanding_response.get_num_input_tokens()
    output_tokens_known_by_provider_as = image_understanding_response.get_output_tokens_known_by_provider_as()
    num_output_tokens = image_understanding_response.get_num_output_tokens()
    print(f'{provider_model.provider}.{provider_model.model} says ', end='')
    print(f'(#{input_tokens_known_by_provider_as} tokens={num_input_tokens}, ', end='')
    print(f'#{output_tokens_known_by_provider_as} tokens={num_output_tokens}):')
    print(response_text)
    return NEXT_PROMPT


def process_reasoning_prompt(user_input: str) -> int:
    tokens = user_input.split()
    if tokens[0] != '$':
        return NOT_INVOKED
    if len(tokens) == 1:
        return NOT_INVOKED
    reasoning_prompt = user_input[len(tokens[0]):].strip()
    provider_model = get_default_provider_model_for(FUNCTIONALITY_REASONING)
    reasoning_response = get_reasoning(provider_model, reasoning_prompt)
    print(f'{provider_model.provider}.{provider_model.model} says ', end='')
    print(
        f'(#{reasoning_response.get_input_tokens_known_by_provider_as()} tokens={reasoning_response.get_num_input_tokens()} ',
        end=''
    )
    print(
        f'#{reasoning_response.get_output_tokens_known_by_provider_as()} tokens={reasoning_response.get_num_output_tokens()}):'
    )
    print(reasoning_response.get_response_text())
    return NEXT_PROMPT

