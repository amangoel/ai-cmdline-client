from .providers import ProviderAndModel
from .providers.ag_anthropic import ProviderAnthropic
from .providers.ag_openai import ProviderOpenAI
from .providers.xai import ProviderXAI


CHAT = 'CHAT'
IMAGE_UNDERSTANDING = 'IMAGE-UNDERSTANDING'
DEFAULT_PROVIDER_MODEL_PER_FUNCTIONALITY = {}


def get_default_provider_model_for(functionality: str) -> ProviderAndModel:
    if functionality not in DEFAULT_PROVIDER_MODEL_PER_FUNCTIONALITY:
        if functionality == CHAT:
            DEFAULT_PROVIDER_MODEL_PER_FUNCTIONALITY[CHAT] = ProviderAndModel(ProviderOpenAI.NAME, 'gpt-4o-mini')
        elif functionality == IMAGE_UNDERSTANDING:
            DEFAULT_PROVIDER_MODEL_PER_FUNCTIONALITY[functionality] = ProviderAndModel(ProviderOpenAI.NAME, 'gpt-4o')
        else:
            raise ValueError()
    return DEFAULT_PROVIDER_MODEL_PER_FUNCTIONALITY[functionality]


def set_default_provider_model_for(functionality: str, provider_and_model: ProviderAndModel):
    DEFAULT_PROVIDER_MODEL_PER_FUNCTIONALITY[functionality] = provider_and_model


def get_available_functionality_and_models():
    functionality_to_models_map = {}
    functionality_to_models_map[CHAT] = []
    for model in ProviderAnthropic.models_with_text_generation_capabilities():
        functionality_to_models_map[CHAT].append(ProviderAndModel(ProviderAnthropic.NAME, model))
    for model in ProviderOpenAI.models_with_text_generation_capabilities():
        functionality_to_models_map[CHAT].append(ProviderAndModel(ProviderOpenAI.NAME, model))
    for model in ProviderXAI.models_with_text_generation_capabilities():
        functionality_to_models_map[CHAT].append(ProviderAndModel(ProviderXAI.NAME, model))

    functionality_to_models_map[IMAGE_UNDERSTANDING] = []
    for model in ProviderAnthropic.models_with_vision_capabilities():
        functionality_to_models_map[IMAGE_UNDERSTANDING].append(ProviderAndModel(ProviderAnthropic.NAME, model))
    for model in ProviderOpenAI.models_with_vision_capabilities():
        functionality_to_models_map[IMAGE_UNDERSTANDING].append(ProviderAndModel(ProviderOpenAI.NAME, model))
    for model in ProviderXAI.models_with_vision_capabilities():
        functionality_to_models_map[IMAGE_UNDERSTANDING].append(ProviderAndModel(ProviderXAI.NAME, model))

    return functionality_to_models_map
