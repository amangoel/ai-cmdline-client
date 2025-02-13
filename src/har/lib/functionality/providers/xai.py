from ...common import PROVIDER_NAME_XAI
from .ag_openai import ProviderOpenAI


class ProviderXAI(ProviderOpenAI):
    NAME = PROVIDER_NAME_XAI

    @classmethod
    def models_with_text_generation_capabilities(cls):
        return ['grok-2-latest']

    @classmethod
    def models_with_vision_capabilities(cls):
        return ['grok-2-vision-latest']

    @classmethod
    def models_with_reasoning_capabilities(cls):
        return []

    def __init__(self, *, api_key: str):
        super().__init__(api_key=api_key, base_url="https://api.x.ai/v1")
