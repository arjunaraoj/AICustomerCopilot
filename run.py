"""
Improved test script for AI Customer Copilot
"""

import asyncio
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from main import AICustomerCopilot

async def test_queries():
    """Test various queries"""
    print("\n" + "="*70)
    print("🇸🇬 AI Customer Copilot - Singapore Tourism")
    print("="*70)
    
    copilot = AICustomerCopilot()
    
    test_queries = [
        "What are the best attractions for families?",
        "Where can I find good local food?",
        "Tell me about Sentosa Island",
        "Any promotions for shopping?",
        "I love photography, where should I go?"
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n\n{'='*70}")
        print(f"Query {i}: {query}")
        print('-'*70)
        
        try:
            response = await copilot.process_query(query)
            print(f"\n🤖 Response:\n{response}")
        except Exception as e:
            print(f"\n❌ Error: {e}")
        
        if i < len(test_queries):
            input("\nPress Enter for next query...")
    
    print("\n" + "="*70)
    print("✅ Testing complete!")
    print("="*70)

async def interactive_mode():
    """Run interactive mode"""
    print("\n" + "="*70)
    print("🇸🇬 AI Customer Copilot - Interactive Mode")
    print("="*70)
    print("Ask me about attractions, food, shopping, or promotions!")
    print("Type 'exit' to quit, 'test' to run test queries\n")
    
    copilot = AICustomerCopilot()
    
    while True:
        try:
            query = input("\n👤 You: ").strip()
            
            if query.lower() in ['exit', 'quit', 'bye']:
                print("\n🤖 Copilot: Thank you for using Singapore Tourism Copilot! Have a great day! 🇸🇬")
                break
            elif query.lower() == 'test':
                await test_queries()
                continue
            elif not query:
                continue
            
            print("\n🤖 Copilot: ", end="", flush=True)
            response = await copilot.process_query(query)
            print(response)
            
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    # Check if test mode or interactive mode
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        asyncio.run(test_queries())
    else:
        asyncio.run(interactive_mode())
