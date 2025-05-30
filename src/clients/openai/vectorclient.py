"""
Handles producing vectors from string inputs by calling OpenAI's API.

[tool.poetry.dependencies]
langchain-openai = ">=0.3.7,<0.4.0"
"""
from typing import (
    List,
    Optional,
)

from openai import AzureOpenAI, AsyncAzureOpenAI, OpenAI, AsyncOpenAI
from ..abstract.vectorclient import VectorClient

class AzureVectorClient(VectorClient):
    """
    A vector client compatible with Azure OpenAI deployments.
    """
    def __init__(self, 
        api_key: str,
        api_version: str,
        azure_endpoint: str,
        model: str = "text-embedding-3-large",
        enforce_size: Optional[int] = None,
    ):
        """
        Initialize a vector client.

        Parameters:
            model (str):
                The name of the model deployment on AzureOpenAI.
            enforce_size (int, optional):
                If set to a value, ensures .vectorize() output vector is the specified size.
                Uses the string "a" to test.
        """
        self.model = model
        self.api_key = api_key
        self.api_version = api_version
        self.azure_endpoint = azure_endpoint
  
        self.client = AzureOpenAI(api_key=api_key, api_version=api_version, azure_endpoint=azure_endpoint)
        self.async_client = AsyncAzureOpenAI(api_key=api_key, api_version=api_version, azure_endpoint=azure_endpoint)

        if enforce_size is not None:
            vector = self.vectorize("a")
            if len(vector) != enforce_size:
                raise ValueError(f"The embeddings model returned a vector of length {len(vector)} whereas {enforce_size} was expected.")

    def vectorize(self, text: str) -> List[float]:
        response = self.client.embeddings.create(
            input = text,
            model = self.model
        )
        return response.data[0].embedding
    
    async def avectorize(self, text: str) -> List[float]:
        response = await self.async_client.embeddings.create(
            input = text,
            model = self.model
        )
        return response.data[0].embedding


class OpenAIVectorClient(AzureVectorClient):
    """
    A vector client compatible with standard OpenAI API.
    """
    def __init__(self, 
        api_key: str,
        model: str = "text-embedding-3-large",
        enforce_size: Optional[int] = None,
    ):
        """
        Initialize a vector client for standard OpenAI API.

        Parameters:
            api_key (str):
                The OpenAI API key starting with 'sk-'.
            model (str):
                The name of the embeddings model.
            enforce_size (int, optional):
                If set to a value, ensures .vectorize() output vector is the specified size.
                Uses the string "a" to test.
        """
        self.model = model
        self.api_key = api_key
  
        self.client = OpenAI(api_key=api_key)
        self.async_client = AsyncOpenAI(api_key=api_key)

        if enforce_size is not None:
            vector = self.vectorize("a")
            if len(vector) != enforce_size:
                raise ValueError(f"The embeddings model returned a vector of length {len(vector)} whereas {enforce_size} was expected.")
