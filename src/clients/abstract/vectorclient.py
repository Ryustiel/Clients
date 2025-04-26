from typing import (
    List,
)
from abc import abstractmethod

class VectorClient:
    @abstractmethod
    def vectorize(self, text: str) -> List[float]:
        """
        Vectorize the input vector. 
        Size = 3072 if model == "text-embedding-3-large"
        """
        raise NotImplementedError("Implement vectorize() in your subclass.")
    
    @abstractmethod
    def avectorize(self, text: str) -> List[float]:
        """
        Vectorize the input vector. 
        Size = 3072 if model == "text-embedding-3-large"
        """
        raise NotImplementedError("Implement avectorize() in your subclass.")
