from langchain_openai import AzureChatOpenAI, AzureOpenAIEmbeddings
from app.config import get_settings


def get_chat_model():
    s = get_settings()
    if not s.azure_openai_endpoint or not s.azure_openai_api_key or not s.azure_openai_chat_deployment:
        raise RuntimeError("Azure OpenAI chat configuration is missing")
    return AzureChatOpenAI(
        azure_endpoint=s.azure_openai_endpoint,
        api_key=s.azure_openai_api_key,
        api_version=s.azure_openai_api_version,
        azure_deployment=s.azure_openai_chat_deployment,
        temperature=0,
        max_retries=3,
    )


def get_embeddings():
    s = get_settings()
    if not s.azure_openai_endpoint or not s.azure_openai_api_key or not s.azure_openai_embedding_deployment:
        raise RuntimeError("Azure OpenAI embedding configuration is missing")
    return AzureOpenAIEmbeddings(
        azure_endpoint=s.azure_openai_endpoint,
        api_key=s.azure_openai_api_key,
        api_version=s.azure_openai_api_version,
        azure_deployment=s.azure_openai_embedding_deployment,
    )
