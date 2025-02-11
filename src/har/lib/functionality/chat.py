from ..common import get_api_key
from .providers import ProviderAndModel, ChatResponse
from .providers.ag_anthropic import ProviderAnthropic
from .providers.ag_openai import ProviderOpenAI
from .providers.xai import ProviderXAI
from anthropic.types import Message as AnthropicMessage
from openai.types.chat.chat_completion import ChatCompletion as OpenAIChatCompletion


def get_chat_response_for_single_message(provider_model: ProviderAndModel, usr_msg: str) -> ChatResponse:
    provider = provider_model.provider
    model = provider_model.model
    if not usr_msg:
        raise ValueError()
    messages = [
        {
            'role': 'user',
            'content': usr_msg
        }
    ]
    if provider == ProviderAnthropic.NAME:
        anthropic_provider = ProviderAnthropic(api_key=get_api_key(ProviderAnthropic.NAME))
        message: AnthropicMessage = anthropic_provider.get_text_completion(model, messages)
        return ChatResponse(
            response_text=message.content[0].text,
            input_tokens_known_by_provider_as='input',
            num_input_tokens=message.usage.input_tokens,
            output_tokens_known_by_provider_as='output',
            num_output_tokens=message.usage.output_tokens
        )
    if provider == ProviderOpenAI.NAME:
        openai_provider = ProviderOpenAI(api_key=get_api_key(ProviderOpenAI.NAME))
        chat_completion: OpenAIChatCompletion = openai_provider.get_text_completion(model, messages)
        return ChatResponse(
            response_text=chat_completion.choices[0].message.content,
            input_tokens_known_by_provider_as='prompt',
            num_input_tokens=chat_completion.usage.prompt_tokens,
            output_tokens_known_by_provider_as='completion',
            num_output_tokens=chat_completion.usage.completion_tokens
        )
    if provider == ProviderXAI.NAME:
        xai_provider = ProviderXAI(api_key=get_api_key(ProviderXAI.NAME))
        chat_completion: OpenAIChatCompletion = xai_provider.get_text_completion(model, messages)
        return ChatResponse(
            response_text=chat_completion.choices[0].message.content,
            input_tokens_known_by_provider_as='input',
            num_input_tokens=chat_completion.usage.prompt_tokens,
            output_tokens_known_by_provider_as='output',
            num_output_tokens=chat_completion.usage.completion_tokens
        )

    raise Exception()   # if the provider didn't match any of the above

