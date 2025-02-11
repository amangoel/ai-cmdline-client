from ...common import PROVIDER_NAME_ANTHROPIC
from anthropic import Anthropic
from anthropic.types import Message


class ProviderAnthropic:
    NAME = PROVIDER_NAME_ANTHROPIC

    @classmethod
    def models_with_text_generation_capabilities(cls):
        return ['claude-3-5-haiku-latest', 'claude-3-5-sonnet-latest']

    @classmethod
    def models_with_vision_capabilities(cls):
        return ['claude-3-5-sonnet-latest']

    def __init__(self, *, api_key: str):
        self.client = Anthropic(api_key=api_key)

    def get_text_completion(self, model: str, messages) -> Message:
        return self.client.messages.create(
            model=model,
            max_tokens=1024,
            messages=messages
        )

