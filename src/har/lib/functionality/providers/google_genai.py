from ...common import PROVIDER_NAME_GOOGLE
from google.genai import Client
from google.genai.types import GenerateContentResponse


class ProviderGoogle:
    NAME = PROVIDER_NAME_GOOGLE

    @classmethod
    def models_with_text_generation_capabilities(cls):
        return ['gemini-2.0-flash']

    @classmethod
    def models_with_vision_capabilities(cls):
        return []

    @classmethod
    def models_with_reasoning_capabilities(cls):
        return []

    def __init__(self, *, api_key):
        self.client = Client(api_key=api_key)

    def get_text_generation(self, model: str, contents: list) -> GenerateContentResponse:
        response: GenerateContentResponse = self.client.models.generate_content(model=model, contents=contents)
        return response


