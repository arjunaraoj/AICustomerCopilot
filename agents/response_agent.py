from typing import Dict, Any
from .base_agent import BaseAgent
from utils.openai_client import OpenAIClient
import json

class ResponseAgent(BaseAgent):
    """Formats and generates final response for the user"""
    
    def __init__(self, openai_client: OpenAIClient):
        super().__init__("ResponseAgent")
        self.openai_client = openai_client
        
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        original_query = input_data.get("original_query", "")
        agent_responses = input_data.get("agent_responses", {})
        plan = input_data.get("plan", {})
        
        self.log_info("Generating final response")
        
        combined_data = self._combine_agent_outputs(agent_responses)
        
        final_response = await self._generate_response(
            original_query, combined_data, plan
        )
        
        return {
            "agent": "ResponseAgent",
            "response": final_response,
            "formatted": True
        }
    
    def _combine_agent_outputs(self, agent_responses: Dict) -> Dict:
        combined = {}
        
        for agent_name, response in agent_responses.items():
            if agent_name == "RetrievalAgent":
                combined["retrieved_data"] = response.get("retrieved_data", {})
            elif agent_name == "AnalyticsAgent":
                combined["analytics"] = response.get("results", {})
            elif agent_name == "MarketingAgent":
                combined["marketing"] = response.get("content", "")
                combined["promotions"] = response.get("promotions", [])
            elif agent_name == "PlannerAgent":
                combined["plan"] = response.get("plan", {})
        
        return combined
    
    async def _generate_response(self, query: str, data: Dict, plan: Dict) -> str:
        prompt = f"""
        User Query: {query}
        
        Retrieved Data: {json.dumps(data.get('retrieved_data', {}), indent=2)}
        Analytics: {json.dumps(data.get('analytics', {}), indent=2)}
        Marketing Content: {data.get('marketing', 'None')}
        Promotions: {json.dumps(data.get('promotions', []), indent=2)}
        
        Create a helpful, friendly response for the user that:
        1. Directly answers their query
        2. Uses the retrieved data to provide specific recommendations
        3. Mentions relevant promotions if applicable
        4. Uses a warm, welcoming tone appropriate for tourism
        5. Is well-structured and easy to read
        
        Format the response in a conversational style.
        """
        
        response = await self.openai_client.chat_completion(
            messages=[
                {"role": "system", "content": "You are a friendly Singapore Tourism copilot."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        
        return response
