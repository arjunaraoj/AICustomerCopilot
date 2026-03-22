from typing import Dict, Any, List
from .base_agent import BaseAgent
from tools.data_loader import DataLoader
from tools.vector_store import VectorStore
import pandas as pd

class RetrievalAgent(BaseAgent):
    """Fetches relevant data from CSV files and knowledge base"""
    
    def __init__(self, data_loader: DataLoader, vector_store: VectorStore):
        super().__init__("RetrievalAgent")
        self.data_loader = data_loader
        self.vector_store = vector_store
        
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        query = input_data.get("query", "")
        entity_types = input_data.get("entity_types", ["attractions", "restaurants", "shops", "promotions"])
        limit = input_data.get("limit", 5)
        
        self.log_info(f"Retrieving data for: {query}")
        
        retrieved_data = {}
        
        # Load and search each data type
        if "attractions" in entity_types:
            attractions = self.data_loader.load_attractions()
            if not attractions.empty:
                retrieved_data["attractions"] = self._search_entities(attractions, query, limit)
                
        if "restaurants" in entity_types:
            restaurants = self.data_loader.load_restaurants()
            if not restaurants.empty:
                retrieved_data["restaurants"] = self._search_entities(restaurants, query, limit)
                
        if "shops" in entity_types:
            shops = self.data_loader.load_shops()
            if not shops.empty:
                retrieved_data["shops"] = self._search_entities(shops, query, limit)
                
        if "promotions" in entity_types:
            promotions = self.data_loader.load_promotions()
            if not promotions.empty:
                retrieved_data["promotions"] = self._search_promotions(promotions, query)
        
        return {
            "agent": "RetrievalAgent",
            "retrieved_data": retrieved_data,
            "query": query
        }
    
    def _search_entities(self, df: pd.DataFrame, query: str, limit: int) -> List[Dict]:
        """Search for entities matching the query"""
        if df.empty:
            return []
        
        results = []
        query_lower = query.lower()
        
        for _, row in df.iterrows():
            # Create searchable text from multiple fields
            searchable_fields = []
            
            # Add name
            if 'name' in row:
                searchable_fields.append(str(row['name']).lower())
            
            # Add description
            if 'description' in row:
                searchable_fields.append(str(row['description']).lower())
            
            # Add tags/category
            if 'tags' in row:
                searchable_fields.append(str(row['tags']).lower())
            if 'category' in row:
                searchable_fields.append(str(row['category']).lower())
            if 'cuisine' in row:
                searchable_fields.append(str(row['cuisine']).lower())
            
            searchable_text = ' '.join(searchable_fields)
            
            # Check if query matches any field
            if query_lower in searchable_text:
                result_dict = row.to_dict()
                # Clean up NaN values
                result_dict = {k: v for k, v in result_dict.items() if pd.notna(v)}
                results.append(result_dict)
                
        return results[:limit]
    
    def _search_promotions(self, df: pd.DataFrame, query: str) -> List[Dict]:
        """Search for promotions matching the query"""
        if df.empty:
            return []
        
        results = []
        query_lower = query.lower()
        
        for _, row in df.iterrows():
            # Search in promotion name and type
            name = str(row.get('name', '')).lower()
            promo_type = str(row.get('type', '')).lower()
            terms = str(row.get('terms', '')).lower()
            
            if (query_lower in name or 
                query_lower in promo_type or
                query_lower in terms):
                result_dict = row.to_dict()
                result_dict = {k: v for k, v in result_dict.items() if pd.notna(v)}
                results.append(result_dict)
                
        return results[:3]
