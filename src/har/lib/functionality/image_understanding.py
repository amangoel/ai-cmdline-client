import base64
import os.path
from ..common import get_api_key
from .providers import ProviderAndModel, ImageUnderstandingResponse
from .providers.ag_anthropic import ProviderAnthropic
from .providers.ag_openai import ProviderOpenAI
from .providers.xai import ProviderXAI
from anthropic.types import Message as AnthropicMessage
from openai.types.chat.chat_completion import ChatCompletion as OpenAIChatCompletion


SUPPORTED_EXTENSIONS_FOR_IMAGE_UNDERSTANDING_LOWERCASE = ['png', 'jpeg', 'jpg']


def get_image_format_specifier_for_image_file_extension(provider: str, ext: str) -> str:
    if ext not in SUPPORTED_EXTENSIONS_FOR_IMAGE_UNDERSTANDING_LOWERCASE:
        raise ValueError
    format_specifier = ext
    # OpenAI and XAI accept both 'jpg' and 'jpeg' as format specifiers for JPEG
    # Anthropic only accepts 'jpeg', not 'jpg'
    if provider == ProviderAnthropic.NAME and ext == 'jpg':
        format_specifier = 'jpeg'
    return format_specifier


def understand_image(provider_model: ProviderAndModel, image_path: str, text_prompt: str) -> ImageUnderstandingResponse:
    provider = provider_model.provider
    model = provider_model.model
    with open(image_path, 'rb') as fh:
        image_content = fh.read()
    image_encoded = base64.b64encode(image_content).decode('utf-8')
    image_extension = os.path.splitext(image_path)[1].lower()[1:]
    if provider == ProviderAnthropic.NAME:
        anthropic_provider = ProviderAnthropic(api_key=get_api_key(ProviderAnthropic.NAME))
        image_format_specifier = get_image_format_specifier_for_image_file_extension(
            ProviderAnthropic.NAME, image_extension
        )
        messages = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": f'image/{image_format_specifier}',
                            "data": image_encoded,
                        },
                    },
                    {
                        "type": "text",
                        "text": text_prompt
                    }
                ]
            }
        ]
        response_message: AnthropicMessage = anthropic_provider.get_text_completion(model, messages)
        return ImageUnderstandingResponse(
            response_text=response_message.content[0].text,
            input_tokens_known_by_provider_as='input',
            num_input_tokens=response_message.usage.input_tokens,
            output_tokens_known_by_provider_as='output',
            num_output_tokens=response_message.usage.output_tokens
        )

    if provider in (ProviderOpenAI.NAME, ProviderXAI.NAME):
        if provider == ProviderOpenAI.NAME:
            openai_or_xai_provider = ProviderOpenAI(api_key=get_api_key(ProviderOpenAI.NAME))
            image_format_specifier = get_image_format_specifier_for_image_file_extension(
                ProviderOpenAI.NAME, image_extension
            )
        else:
            openai_or_xai_provider = ProviderXAI(api_key=get_api_key(ProviderXAI.NAME))
            image_format_specifier = get_image_format_specifier_for_image_file_extension(
                ProviderXAI.NAME, image_extension
            )
        messages = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/{image_format_specifier};base64,{image_encoded}"
                        }
                    },
                    {
                        "type": "text",
                        "text": text_prompt
                    }
                ]
            }
        ]
        chat_completion: OpenAIChatCompletion = openai_or_xai_provider.get_text_completion(model, messages)
        if provider == ProviderOpenAI.NAME:
            return ImageUnderstandingResponse(
                response_text=chat_completion.choices[0].message.content,
                input_tokens_known_by_provider_as='prompt',
                num_input_tokens=chat_completion.usage.prompt_tokens,
                output_tokens_known_by_provider_as='completion',
                num_output_tokens=chat_completion.usage.completion_tokens
            )
        else:
            return ImageUnderstandingResponse(
                response_text=chat_completion.choices[0].message.content,
                input_tokens_known_by_provider_as='input',
                num_input_tokens=chat_completion.usage.prompt_tokens,
                output_tokens_known_by_provider_as='output',
                num_output_tokens=chat_completion.usage.completion_tokens
            )

    raise Exception()       # if provider did not match any of the above
