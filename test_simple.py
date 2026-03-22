import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from main import AICustomerCopilot

async def test():
    print("Testing AI Customer Copilot...")
    copilot = AICustomerCopilot()
    
    # Test a simple query
    response = await copilot.process_query("What are the best attractions in Singapore?")
    print(f"\nResponse: {response}")

if __name__ == "__main__":
    asyncio.run(test())
