README.md 
markdown
# AI Customer Copilot
AI-powered multi-agent system to help users discover attractions, restaurants, and shopping recommendations fro Singapore Tourism Board Simulation.

## Quick Start
### 1. Clone
bash
git clone https://github.com/arjunaraoj/AICustomerCopilot.git
cd AICustomerCopilot

### 2. Install
bash
pip install -r requirements.txt

### 3. Setup API Key
Create a .env file:

bash
OPENAI_API_KEY=your-key-here

### 4. Run

bash
python run.py

## Example Queries
* What are the best tourist places?
* Suggest good restaurants
* Any shopping deals?
* Places for photography?

## Project Structure
agents/      - AI agents  
data/        - CSV data  
tools/       - utilities  
utils/       - helpers  
main.py      - main logic  
run.py       - run app  
config.py    - settings  


## Technologies

* Python
* OpenAI
* FAISS
* Pandas
## Requirements
* Python 3.9 or higher
* OpenAI API key

## Notes
Do not upload:
* .env file
* API keys
* large files
