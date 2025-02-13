from ..common import FUNCTIONALITY_CHAT, FUNCTIONALITY_IMAGE_UNDERSTANDING, FUNCTIONALITY_REASONING
from ..common import SUPPORTED_PROVIDERS, SUPPORTED_FUNCTIONALITY
from .providers import ProviderAndModel, AVAILABLE_PROVIDER_CLASSES
from .providers.ag_anthropic import ProviderAnthropic
from .providers.ag_openai import ProviderOpenAI
from .providers.xai import ProviderXAI


DEFAULT_PROVIDER_MODEL_PER_FUNCTIONALITY = {}


def get_default_provider_model_for(functionality: str) -> ProviderAndModel:
    if functionality not in DEFAULT_PROVIDER_MODEL_PER_FUNCTIONALITY:
        if functionality == FUNCTIONALITY_CHAT:
            DEFAULT_PROVIDER_MODEL_PER_FUNCTIONALITY[FUNCTIONALITY_CHAT] = ProviderAndModel(ProviderOpenAI.NAME, 'gpt-4o-mini')
        elif functionality == FUNCTIONALITY_IMAGE_UNDERSTANDING:
            DEFAULT_PROVIDER_MODEL_PER_FUNCTIONALITY[functionality] = ProviderAndModel(ProviderOpenAI.NAME, 'gpt-4o')
        elif functionality == FUNCTIONALITY_REASONING:
            DEFAULT_PROVIDER_MODEL_PER_FUNCTIONALITY[functionality] = ProviderAndModel(ProviderOpenAI.NAME, 'o1-mini')
        else:
            raise ValueError()
    return DEFAULT_PROVIDER_MODEL_PER_FUNCTIONALITY[functionality]


def set_default_provider_model_for(functionality: str, provider_and_model: ProviderAndModel):
    DEFAULT_PROVIDER_MODEL_PER_FUNCTIONALITY[functionality] = provider_and_model


def get_available_functionality_and_models():
    functionality_to_models_map = {}
    supported_provider_classes = []
    for supported_provider in sorted(SUPPORTED_PROVIDERS):
        provider_class = next(filter(lambda clas: clas.NAME == supported_provider, AVAILABLE_PROVIDER_CLASSES))
        supported_provider_classes.append(provider_class)

    for functionality in SUPPORTED_FUNCTIONALITY:
        functionality_to_models_map[functionality] = []
        for provider_class in supported_provider_classes:
            if functionality == FUNCTIONALITY_CHAT:
                functionality_to_models_map[functionality].extend(
                    [ProviderAndModel(provider_class.NAME, model) for model in
                     provider_class.models_with_text_generation_capabilities()]
                )
            elif functionality == FUNCTIONALITY_IMAGE_UNDERSTANDING:
                functionality_to_models_map[functionality].extend(
                    [ProviderAndModel(provider_class.NAME, model) for model in
                     provider_class.models_with_vision_capabilities()]
                )
            elif functionality == FUNCTIONALITY_REASONING:
                functionality_to_models_map[functionality].extend(
                    [ProviderAndModel(provider_class.NAME, model) for model in
                     provider_class.models_with_reasoning_capabilities()]
                )
            else:
                raise Exception()

    return functionality_to_models_map
