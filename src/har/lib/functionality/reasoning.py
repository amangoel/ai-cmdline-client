from ..api_keys import get_api_key
from .chat import get_chat_response_for_single_message
from .providers import ProviderAndModel, ChatResponse, ReasoningPromptResponse
from .providers.ag_openai import ProviderOpenAI
from openai.types.chat.chat_completion import ChatCompletion as OpenAIChatCompletion


def get_reasoning(provider_and_model: ProviderAndModel, reasoning_prompt: str) -> ReasoningPromptResponse:
    chat_response: ChatResponse = get_chat_response_for_single_message(provider_and_model, reasoning_prompt)
    return ReasoningPromptResponse(
        response_text=chat_response.get_response_text(),
        input_tokens_known_by_provider_as=chat_response.get_input_tokens_known_by_provider_as(),
        num_input_tokens=chat_response.get_num_input_tokens(),
        output_tokens_known_by_provider_as=chat_response.get_output_tokens_known_by_provider_as(),
        num_output_tokens=chat_response.get_num_output_tokens()
    )

