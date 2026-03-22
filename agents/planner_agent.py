from typing import Dict, Any
from .base_agent import BaseAgent
from utils.openai_client import OpenAIClient
import json

class PlannerAgent(BaseAgent):
    """Orchestrates tasks and decides which agents to invoke"""
    
    def __init__(self, openai_client: OpenAIClient):
        super().__init__("PlannerAgent")
        self.openai_client = openai_client
        
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        user_query = input_data.get("user_query", "")
        user_context = input_data.get("user_context", {})
        
        self.log_info(f"Planning for query: {user_query}")
        
        prompt = self._create_planning_prompt(user_query, user_context)
        
        response = await self.openai_client.chat_completion(
            messages=[
                {"role": "system", "content": "You are a planning agent for a tourism copilot."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )
        
        plan = self._parse_plan(response)
        
        return {
            "agent": "PlannerAgent",
            "plan": plan,
            "original_query": user_query,
            "user_context": user_context
        }
    
    def _create_planning_prompt(self, query: str, context: Dict) -> str:
        return f"""
        User Query: {query}
        User Context: {json.dumps(context)}
        
        Determine what the user needs:
        1. If asking about attractions/locations -> use RetrievalAgent
        2. If asking for recommendations/insights -> use AnalyticsAgent  
        3. If asking about promotions/marketing -> use MarketingAgent
        4. For general queries about Singapore -> use RetrievalAgent
        
        Output a JSON plan with:
        - primary_agent: main agent to handle request
        - secondary_agents: supporting agents needed
        - intent: what the user wants to do
        - key_entities: important items mentioned
        
        Return only valid JSON.
        """
    
    def _parse_plan(self, llm_response: str) -> Dict:
        try:
            plan = json.loads(llm_response)
            return plan
        except:
            return {
                "primary_agent": "RetrievalAgent",
                "secondary_agents": [],
                "intent": "general_inquiry",
                "key_entities": []
            }
