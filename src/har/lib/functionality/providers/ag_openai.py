from ...common import PROVIDER_NAME_OPENAI
from openai import OpenAI
from openai.types.chat.chat_completion import ChatCompletion


class ProviderOpenAI:
    NAME = PROVIDER_NAME_OPENAI

    @classmethod
    def models_with_text_generation_capabilities(cls):
        return ['gpt-4o-mini', 'gpt-4o']

    @classmethod
    def models_with_vision_capabilities(cls):
        return ['gpt-4o-mini', 'gpt-4o']

    @classmethod
    def models_with_reasoning_capabilities(cls):
        return ['o1-mini']

    def __init__(self, *, api_key: str, base_url=None):
        self.client = OpenAI(api_key=api_key, base_url=base_url)

    def get_text_completion(self, model: str, messages) -> ChatCompletion:
        return self.client.chat.completions.create(
            model=model,
            store=True,
            messages=messages
        )
