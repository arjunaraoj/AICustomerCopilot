from typing import Dict, Any, List
from .base_agent import BaseAgent
from utils.openai_client import OpenAIClient
from tools.data_loader import DataLoader
import json

class MarketingAgent(BaseAgent):
    """Generates marketing content and promotional recommendations"""
    
    def __init__(self, openai_client: OpenAIClient, data_loader: DataLoader):
        super().__init__("MarketingAgent")
        self.openai_client = openai_client
        self.data_loader = data_loader
        
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        content_type = input_data.get("content_type", "promotion")
        target_audience = input_data.get("target_audience", {})
        context = input_data.get("context", "")
        
        self.log_info(f"Generating {content_type} content")
        
        promotions_df = self.data_loader.load_promotions()
        relevant_promotions = self._get_relevant_promotions(promotions_df, context)
        
        content = await self._generate_marketing_content(
            content_type, target_audience, relevant_promotions, context
        )
        
        return {
            "agent": "MarketingAgent",
            "content_type": content_type,
            "content": content,
            "promotions": relevant_promotions
        }
    
    def _get_relevant_promotions(self, promotions_df, context: str) -> List[Dict]:
        if promotions_df.empty:
            return []
        
        relevant = []
        context_lower = context.lower()
        
        for _, row in promotions_df.iterrows():
            if (context_lower in row.get('name', '').lower() or 
                context_lower in row.get('type', '').lower()):
                relevant.append(row.to_dict())
        
        return relevant[:3]
    
    async def _generate_marketing_content(self, content_type: str, 
                                          target_audience: Dict,
                                          promotions: List[Dict],
                                          context: str) -> str:
        prompt = f"""
        Generate {content_type} content for Singapore tourism.
        
        Target Audience: {json.dumps(target_audience)}
        Context: {context}
        Available Promotions: {json.dumps(promotions)}
        
        Create engaging, persuasive content that:
        1. Highlights unique Singapore experiences
        2. Mentions relevant promotions if available
        3. Includes call-to-action
        4. Is tailored to the target audience
        
        Return the content as a string.
        """
        
        response = await self.openai_client.chat_completion(
            messages=[
                {"role": "system", "content": "You are a marketing expert for Singapore tourism."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.8
        )
        
        return response
