import asyncio
import logging
from pathlib import Path
from typing import Dict, Any

from config import Config
from utils.logger import setup_logging
from utils.openai_client import OpenAIClient
from tools.data_loader import DataLoader
from tools.vector_store import VectorStore

from agents.planner_agent import PlannerAgent
from agents.retrieval_agent import RetrievalAgent
from agents.analytics_agent import AnalyticsAgent
from agents.marketing_agent import MarketingAgent
from agents.response_agent import ResponseAgent

class AICustomerCopilot:
    """Main orchestrator for AI Customer Copilot"""
    
    def __init__(self):
        # Setup
        setup_logging(Config.LOG_LEVEL)
        self.logger = logging.getLogger(__name__)
        
        # Initialize components
        self.openai_client = OpenAIClient(Config.OPENAI_API_KEY, Config.OPENAI_MODEL)
        self.data_loader = DataLoader(Config.DATA_DIR)
        self.vector_store = VectorStore()
        
        # Initialize agents
        self.planner = PlannerAgent(self.openai_client)
        self.retriever = RetrievalAgent(self.data_loader, self.vector_store)
        self.analytics = AnalyticsAgent(self.data_loader)
        self.marketing = MarketingAgent(self.openai_client, self.data_loader)
        self.responder = ResponseAgent(self.openai_client)
        
        self.logger.info("AI Customer Copilot initialized")
    
    async def process_query(self, user_query: str, user_context: Dict[str, Any] = None) -> str:
        """Process user query through multi-agent system"""
        
        self.logger.info(f"Processing query: {user_query}")
        
        if user_context is None:
            user_context = {}
        
        # Step 1: Plan
        plan_result = await self.planner.process({
            "user_query": user_query,
            "user_context": user_context
        })
        
        plan = plan_result.get("plan", {})
        primary_agent = plan.get("primary_agent", "RetrievalAgent")
        
        # Step 2: Execute agents based on plan
        agent_responses = {}
        
        # Always run retrieval for data
        retrieval_result = await self.retriever.process({
            "query": user_query,
            "entity_types": ["attractions", "restaurants", "shops", "promotions"],
            "limit": 3
        })
        agent_responses["RetrievalAgent"] = retrieval_result
        
        # Run analytics if needed
        if primary_agent == "AnalyticsAgent" or "analytics" in str(plan).lower():
            analytics_result = await self.analytics.process({
                "analysis_type": "general",
                "filters": user_context
            })
            agent_responses["AnalyticsAgent"] = analytics_result
        
        # Run marketing if promotion-related
        if primary_agent == "MarketingAgent" or "promotion" in user_query.lower():
            marketing_result = await self.marketing.process({
                "content_type": "promotion",
                "target_audience": user_context,
                "context": user_query
            })
            agent_responses["MarketingAgent"] = marketing_result
        
        # Step 3: Generate final response
        final_response = await self.responder.process({
            "original_query": user_query,
            "agent_responses": agent_responses,
            "plan": plan
        })
        
        return final_response.get("response", "I'm sorry, I couldn't generate a response.")
    
    async def run_interactive(self):
        """Run interactive command-line session"""
        print("\n" + "="*60)
        print("🇸🇬 AI Customer Copilot - Singapore Tourism")
        print("="*60)
        print("Ask me about attractions, restaurants, shopping, or promotions!")
        print("Type 'exit' to quit\n")
        
        while True:
            try:
                query = input("\n👤 You: ").strip()
                if query.lower() in ['exit', 'quit', 'bye']:
                    print("\n🤖 Copilot: Thank you for using Singapore Tourism Copilot! Have a great day! 🇸🇬")
                    break
                
                if query:
                    print("\n🤖 Copilot: ", end="", flush=True)
                    response = await self.process_query(query)
                    print(response)
                    
            except KeyboardInterrupt:
                print("\n\nGoodbye!")
                break
            except Exception as e:
                self.logger.error(f"Error processing query: {e}")
                print("\n🤖 Copilot: I encountered an error. Please try again.")

async def main():
    """Main entry point"""
    copilot = AICustomerCopilot()
    await copilot.run_interactive()

if __name__ == "__main__":
    asyncio.run(main())