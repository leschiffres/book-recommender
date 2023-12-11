from abc import ABC, abstractmethod
from sentence_transformers import SentenceTransformer, util
import torch

class EmbeddingsProducer(ABC):
    """
    We create a parent class so that we can replace SentenceTransformersEmbeddings with any class
    that can compute the embedding and provide a distance function for it.
    """
    @abstractmethod
    def get_embedding(self, text):
        pass

    @abstractmethod
    def get_distance(self, a, b):
        pass

class SentenceTransformersEmbeddings(EmbeddingsProducer):

    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
    
    def get_embedding(self, text):
        return self.model.encode(text, show_progress_bar=False)

    def get_distance(self, embedding1, embedding2):
        return util.pytorch_cos_sim(embedding1, embedding2).item()
    

if __name__ == '__main__':
    t = input("give me whatever:\n")
    transformer = SentenceTransformersEmbeddings()
    print(transformer.get_embedding(t))