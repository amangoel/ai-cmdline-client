from .ag_anthropic import ProviderAnthropic
from .ag_openai import ProviderOpenAI
from .xai import ProviderXAI


AVAILABLE_PROVIDER_CLASSES = [ProviderAnthropic, ProviderOpenAI, ProviderXAI]


class ChatResponse:
    def __init__(self, response_text,
                 input_tokens_known_by_provider_as: str, num_input_tokens: int,
                 output_tokens_known_by_provider_as: str, num_output_tokens: int):
        self._response_text = response_text
        self._input_tokens_known_by_provider_as = input_tokens_known_by_provider_as
        self._num_input_tokens = num_input_tokens
        self._output_tokens_known_by_provider_as = output_tokens_known_by_provider_as
        self._num_output_tokens = num_output_tokens

    def get_response_text(self) -> str:
        return self._response_text

    def get_input_tokens_known_by_provider_as(self) -> str:
        return self._input_tokens_known_by_provider_as

    def get_num_input_tokens(self) -> int:
        return self._num_input_tokens

    def get_output_tokens_known_by_provider_as(self) -> str:
        return self._output_tokens_known_by_provider_as

    def get_num_output_tokens(self) -> int:
        return self._num_output_tokens


class ImageUnderstandingResponse(ChatResponse):
    pass


class ReasoningPromptResponse(ChatResponse):
    pass


class ProviderAndModel:
    def __init__(self, provider: str, model: str):
        self.provider = provider
        self.model = model
