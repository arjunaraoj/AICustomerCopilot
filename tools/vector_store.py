import numpy as np
import faiss
from typing import List, Dict

class VectorStore:
    def __init__(self):
        self.index = None
        self.documents = []
        
    def add_documents(self, documents: List[str], embeddings: List[np.ndarray]):
        self.documents = documents
        dimension = len(embeddings[0])
        self.index = faiss.IndexFlatL2(dimension)
        vectors = np.array(embeddings).astype('float32')
        self.index.add(vectors)
        
    def search(self, query_embedding: np.ndarray, k: int = 5) -> List[Dict]:
        if self.index is None or self.index.ntotal == 0:
            return []
        
        query_embedding = query_embedding.reshape(1, -1).astype('float32')
        distances, indices = self.index.search(query_embedding, k)
        
        results = []
        for idx, dist in zip(indices[0], distances[0]):
            if idx < len(self.documents):
                results.append({
                    "document": self.documents[idx],
                    "score": float(1 / (1 + dist))
                })
        
        return results
