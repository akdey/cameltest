import os
from camel.models import ModelFactory
from camel.types import ModelPlatformType, ModelType

def get_llm(provider="azure", model_name=None):
    """
    Returns the configured LLM model for the CAMEL agents.
    Set the provider to 'azure', 'local', or 'openai'.
    """
    if provider == "azure":
        # Required env vars: AZURE_OPENAI_API_KEY, AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_API_VERSION, AZURE_DEPLOYMENT_NAME
        api_key = os.getenv("AZURE_OPENAI_API_KEY")
        url = os.getenv("AZURE_OPENAI_ENDPOINT")
        api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2023-05-15")
        deployment_name = os.getenv("AZURE_DEPLOYMENT_NAME", "gpt-4o")

        return ModelFactory.create(
            model_platform=ModelPlatformType.AZURE,
            model_type=model_name or ModelType.GPT_4O, 
            model_config_dict={
                "temperature": 0.2,
                "api_key": api_key,
                "base_url": url,
                "api_version": api_version,
                "deployment_name": deployment_name
            }
        )
    elif provider == "local":
        return ModelFactory.create(
            model_platform=ModelPlatformType.OPENAI,
            model_type=model_name or "llama3", 
            model_config_dict={
                "temperature": 0.2,
                "api_base": os.getenv("LOCAL_LLM_API_BASE", "http://localhost:11434/v1"),
                "api_key": "ollama"
            }
        )
    else:
        return ModelFactory.create(
            model_platform=ModelPlatformType.OPENAI,
            model_type=model_name or ModelType.GPT_4O,
            model_config_dict={"temperature": 0.2}
        )

if __name__ == "__main__":
    print("Testing model initialization...")
    model = get_llm("azure")
    print(f"Model initialized: {model}")
