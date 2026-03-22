"""
Project Setup & Verification Script
Run this to ensure all files are in the correct location and dependencies are installed
"""

import os
import sys
import shutil
from pathlib import Path
import subprocess

# Define paths
SOURCE_PATH = Path(r"C:\Users\junea\OneDrive\Desktop\Code")
TARGET_PATH = Path(r"D:\GenerativeAI\AICustomerCopilot")

def print_section(title):
    """Print formatted section header"""
    print("\n" + "="*70)
    print(f" {title}")
    print("="*70)

def check_and_copy_files():
    """Check source files and copy to target"""
    print_section("1. Checking Source Files")
    
    if not SOURCE_PATH.exists():
        print(f"❌ Source path not found: {SOURCE_PATH}")
        print("Please ensure the 'Code' folder is on your desktop with all project files")
        return False
    
    print(f"✅ Source path found: {SOURCE_PATH}")
    
    # Create target directory if it doesn't exist
    TARGET_PATH.mkdir(parents=True, exist_ok=True)
    print(f"✅ Target directory created/verified: {TARGET_PATH}")
    
    # List files to copy
    files_to_copy = [
        "main.py",
        "config.py",
        "requirements.txt",
        ".env"
    ]
    
    directories_to_copy = [
        "agents",
        "tools",
        "utils",
        "data",
        "tests",
        "notebooks"
    ]
    
    print_section("2. Copying Files")
    
    # Copy individual files
    for file in files_to_copy:
        src = SOURCE_PATH / file
        dst = TARGET_PATH / file
        if src.exists():
            shutil.copy2(src, dst)
            print(f"✅ Copied: {file}")
        else:
            print(f"⚠️  Not found: {file} (will be created if needed)")
    
    # Copy directories
    for dir_name in directories_to_copy:
        src_dir = SOURCE_PATH / dir_name
        dst_dir = TARGET_PATH / dir_name
        
        if src_dir.exists():
            # Remove existing directory if it exists
            if dst_dir.exists():
                shutil.rmtree(dst_dir)
            shutil.copytree(src_dir, dst_dir)
            print(f"✅ Copied directory: {dir_name}/")
        else:
            print(f"⚠️  Directory not found: {dir_name}/ (will be created)")
            dst_dir.mkdir(exist_ok=True)
    
    return True

def verify_project_structure():
    """Verify all required files and directories exist"""
    print_section("3. Verifying Project Structure")
    
    required_dirs = [
        "agents",
        "tools", 
        "utils",
        "data",
        "tests",
        "notebooks",
        "logs"
    ]
    
    required_files = [
        "main.py",
        "config.py",
        "requirements.txt",
        ".env"
    ]
    
    # Check directories
    all_present = True
    for dir_name in required_dirs:
        dir_path = TARGET_PATH / dir_name
        if dir_path.exists() and dir_path.is_dir():
            print(f"✅ Directory present: {dir_name}/")
        else:
            print(f"❌ Missing directory: {dir_name}/")
            dir_path.mkdir(exist_ok=True)
            print(f"   Created: {dir_name}/")
            all_present = False
    
    # Check files
    for file_name in required_files:
        file_path = TARGET_PATH / file_name
        if file_path.exists():
            print(f"✅ File present: {file_name}")
        else:
            print(f"⚠️  Missing file: {file_name}")
            all_present = False
    
    return all_present

def create_missing_csv_files():
    """Create CSV data files if they don't exist"""
    print_section("4. Creating Data Files")
    
    data_dir = TARGET_PATH / "data"
    
    # Attractions CSV
    attractions_csv = data_dir / "attractions.csv"
    if not attractions_csv.exists():
        print("Creating attractions.csv...")
        attractions_content = """id,name,category,location,description,entry_fee,opening_hours,rating,tags
AT001,Marina Bay Sands,Landmark,Bayfront,Iconic integrated resort with sky park and infinity pool,23.00,"10:00-22:00",4.8,"luxury,view,architecture"
AT002,Gardens by the Bay,Attraction,Bayfront,Supertree Grove and Cloud Forest conservatory,28.00,"9:00-21:00",4.7,"nature,family,photo"
AT003,Sentosa Island,Attraction,Sentosa,Resort island with beaches and Universal Studios,6.00,"24/7",4.6,"beach,entertainment,family"
AT004,Singapore Zoo,Zoo,Mandai,World-renowned zoo with open concept exhibits,48.00,"8:30-18:00",4.8,"animals,family,educational"
AT005,Chinatown,Cultural,Chinatown,Historic area with temples and traditional shops,0.00,"24/7",4.5,"culture,shopping,heritage"
AT006,Little India,Cultural,Little India,Vibrant district with colorful shops and temples,0.00,"24/7",4.5,"culture,food,colorful"
AT007,Orchard Road,Shopping,Orchard,Prime shopping belt with luxury brands,0.00,"24/7",4.4,"shopping,luxury,christmas"
AT008,Singapore Flyer,Attraction,Marina Centre,Giant observation wheel with city views,33.00,"10:00-22:00",4.4,"view,romantic,photo"
AT009,Merlion Park,Landmark,Marina Bay,Iconic Merlion statue with waterfront views,0.00,"24/7",4.5,"iconic,photo,landmark"
AT010,Botanic Gardens,Nature,Bukit Timah,UNESCO heritage site with orchids,0.00,"5:00-00:00",4.7,"nature,walking,unesco"
"""
        attractions_csv.write_text(attractions_content)
        print("✅ attractions.csv created")
    
    # Restaurants CSV
    restaurants_csv = data_dir / "restaurants.csv"
    if not restaurants_csv.exists():
        print("Creating restaurants.csv...")
        restaurants_content = """id,name,cuisine,location,price_range,description,rating,must_try
R001,Maxwell Food Centre,Local Hawker,Chinatown,$,"Famous hawker center with Michelin-starred chicken rice",4.6,"Tian Tian Chicken Rice"
R002,Jumbo Seafood,Seafood,East Coast,$$$,Famous for chili crab with waterfront dining,4.7,"Chili Crab, Black Pepper Crab"
R003,Lau Pa Sat,Local Hawker,Raffles Place,$,Historic market with satay street,4.4,"Satay, Local Kopi"
R004,Odette,French,City Hall,$$$$,Three-Michelin-star French fine dining,4.9,"Signature tasting menu"
R005,Din Tai Fung,Chinese,Multiple Locations,$$,Famous for xiaolongbao and noodles,4.6,"Xiaolongbao, Fried Rice"
R006,Newton Food Centre,Local Hawker,Newton,$,Popular hawker centre featured in Crazy Rich Asians,4.3,"Hokkien Mee, BBQ Seafood"
R007,PS.Cafe,Western,Multiple Locations,$$,Trendy cafe chain with brunch menu,4.4,"Truffle Fries, Sunday Roast"
R008,The Coconut Club,Local,Siglap,$$,Famous for authentic nasi lemak,4.5,"Nasi Lemak, Chendol"
R009,Hawker Chan,Local,Chinatown,$,Michelin-starred soya sauce chicken,4.4,"Soya Sauce Chicken Rice"
R010,Atlas,Bar,City Hall,$$$$,Gin bar in art deco building with European cuisine,4.7,"Gin Tasting, Oysters"
"""
        restaurants_csv.write_text(restaurants_content)
        print("✅ restaurants.csv created")
    
    # Shops CSV
    shops_csv = data_dir / "shops.csv"
    if not shops_csv.exists():
        print("Creating shops.csv...")
        shops_content = """id,name,category,location,description,price_range,rating
S001,ION Orchard,Shopping Mall,Orchard Road,"Luxury mall with international brands",$$$$,4.6
S002,Marina Bay Sands Shoppes,Shopping Mall,Bayfront,"High-end mall with canal boat rides",$$$$,4.7
S003,Chinatown Street Market,Market,Chinatown,"Traditional street market with souvenirs",$,4.3
S004,Tangs,Department Store,Orchard Road,"Singapore's iconic department store",$$$,4.5
S005,Sim Lim Square,Electronics,Rochor,"Electronics and gadget hub",$$,4.0
S006,Clarke Quay,Retail,Riverside,"Riverside shopping and entertainment",$$,4.4
S007,Scotts Square,Luxury Retail,Orchard Road,"Boutique luxury brands",$$$$,4.5
S008,Bugis Street Market,Market,Bugis,"Affordable fashion and accessories",$,4.2
S009,Takashimaya,Department Store,Orchard Road,"Japanese department store with luxury brands",$$$,4.6
S010,The Shoppes at Marina Bay,Shopping Mall,Bayfront,"Luxury shopping and dining",$$$$,4.7
"""
        shops_csv.write_text(shops_content)
        print("✅ shops.csv created")
    
    # Customers CSV
    customers_csv = data_dir / "customers.csv"
    if not customers_csv.exists():
        print("Creating customers.csv...")
        customers_content = """customer_id,name,country,preferences,visit_date,budget,group_size
C001,John Smith,USA,"luxury,photography,food","2026-03-15",5000,2
C002,Maria Garcia,Spain,"culture,history,museums","2026-03-20",3000,1
C003,Kenji Tanaka,Japan,"shopping,technology,anime","2026-04-01",4000,3
C004,Emma Wilson,UK,"nature,food,family","2026-03-25",3500,4
C005,Li Wei,China,"luxury,nightlife,entertainment","2026-03-18",6000,2
C006,Sarah Chen,Singapore,"local food,shopping,staycation","2026-03-22",1500,2
C007,David Miller,Australia,"adventure,beach,outdoor","2026-04-05",4000,2
C008,Aisha Khan,India,"cultural,heritage,food","2026-03-28",2500,3
C009,Pierre Dubois,France,"art,museums,architecture","2026-04-10",4500,1
C010,Hannah Lee,South Korea,"beauty,fashion,cafe","2026-03-30",3500,2
"""
        customers_csv.write_text(customers_content)
        print("✅ customers.csv created")
    
    # Transactions CSV
    transactions_csv = data_dir / "transactions.csv"
    if not transactions_csv.exists():
        print("Creating transactions.csv...")
        transactions_content = """transaction_id,customer_id,merchant_id,merchant_type,amount,date,category
T001,C001,R004,restaurant,350.00,2026-03-15,dining
T002,C001,S001,retail,1250.00,2026-03-15,shopping
T003,C001,AT001,attraction,46.00,2026-03-16,attraction
T004,C002,R001,restaurant,15.00,2026-03-20,dining
T005,C002,AT005,attraction,0.00,2026-03-20,attraction
T006,C002,S003,retail,45.00,2026-03-20,shopping
T007,C003,S005,retail,800.00,2026-04-01,electronics
T008,C003,R005,restaurant,85.00,2026-04-01,dining
T009,C003,AT003,attraction,18.00,2026-04-02,attraction
T010,C004,R001,restaurant,42.00,2026-03-25,dining
T011,C004,AT004,attraction,192.00,2026-03-26,attraction
T012,C004,S008,retail,35.00,2026-03-26,shopping
T013,C005,S002,retail,2300.00,2026-03-18,shopping
T014,C005,R002,restaurant,180.00,2026-03-18,dining
T015,C005,AT002,attraction,56.00,2026-03-19,attraction
T016,C006,R008,restaurant,42.00,2026-03-22,dining
T017,C006,S009,retail,125.00,2026-03-22,shopping
T018,C007,AT003,attraction,12.00,2026-04-05,attraction
T019,C007,R006,restaurant,65.00,2026-04-05,dining
T020,C008,R009,restaurant,28.00,2026-03-28,dining
T021,C008,AT006,attraction,0.00,2026-03-28,attraction
T022,C008,S010,retail,95.00,2026-03-28,shopping
T023,C009,AT008,attraction,66.00,2026-04-10,attraction
T024,C009,R007,restaurant,98.00,2026-04-10,dining
T025,C010,S007,retail,450.00,2026-03-30,shopping
"""
        transactions_csv.write_text(transactions_content)
        print("✅ transactions.csv created")
    
    # Promotions CSV
    promotions_csv = data_dir / "promotions.csv"
    if not promotions_csv.exists():
        print("Creating promotions.csv...")
        promotions_content = """id,name,type,discount,valid_from,valid_to,terms,merchant_ids
P001,Marina Bay Sands Package,Luxury,20%,2026-03-01,2026-04-30,"Minimum 2 nights stay",AT001,S002
P002,Hawker Trail Bundle,Food,15%,2026-03-01,2026-05-31,"Visit 3 hawker centers",R001,R003,R006,R009
P003,Sentosa Fun Pass,Attraction,25%,2026-03-15,2026-04-30,"3 attractions package",AT003
P004,Orchard Road Shopping,Retail,10%,2026-03-20,2026-04-20,"Minimum $200 spend",S001,S004,S007,S009
P005,Family Zoo Package,Family,30%,2026-03-01,2026-04-30,"2 adults + 2 children",AT004
P006,Cultural Heritage Tour,Culture,20%,2026-03-10,2026-04-25,"Guided tour included",AT005,AT006
P007,Singapore Sling Experience,Bar,15%,2026-03-01,2026-04-30,"At participating bars",R010
P008,Photography Tour,Special,25%,2026-03-05,2026-04-15,"Professional guide",AT001,AT002,AT009
"""
        promotions_csv.write_text(promotions_content)
        print("✅ promotions.csv created")
    
    print("✅ All CSV data files created successfully")

def create_env_file():
    """Create .env file if it doesn't exist"""
    print_section("5. Setting up Environment")
    
    env_file = TARGET_PATH / ".env"
    if not env_file.exists():
        print("Creating .env file...")
        env_content = """# OpenAI Configuration
OPENAI_API_KEY=your-openai-key-here
OPENAI_MODEL=gpt-4
OPENAI_TEMPERATURE=0.7
MAX_TOKENS=2000

# Logging Configuration
LOG_LEVEL=INFO
"""
        env_file.write_text(env_content)
        print("✅ .env file created")
        print("⚠️  IMPORTANT: Edit .env and add your OpenAI API key!")
    else:
        print("✅ .env file already exists")

def install_dependencies():
    """Install Python dependencies"""
    print_section("6. Installing Dependencies")
    
    response = input("Do you want to install dependencies now? (y/n): ")
    if response.lower() == 'y':
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "-r", str(TARGET_PATH / "requirements.txt")], 
                         check=True, cwd=TARGET_PATH)
            print("✅ Dependencies installed successfully")
        except subprocess.CalledProcessError as e:
            print(f"❌ Error installing dependencies: {e}")
            print("Please install manually: pip install -r requirements.txt")
    else:
        print("Skipping dependency installation")

def create_test_query_script():
    """Create a test script for quick testing"""
    print_section("7. Creating Test Script")
    
    test_script = TARGET_PATH / "test_query.py"
    if not test_script.exists():
        test_content = '''"""
Quick test script for AI Customer Copilot
"""

import asyncio
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from main import AICustomerCopilot

async def test_queries():
    """Test various queries"""
    copilot = AICustomerCopilot()
    
    test_queries = [
        "What are the best attractions in Singapore?",
        "Where can I find good local food?",
        "Any promotions for Sentosa?",
        "I love shopping, where should I go?",
        "What's good for families with kids?"
    ]
    
    print("\\n" + "="*70)
    print("Testing AI Customer Copilot")
    print("="*70)
    
    for query in test_queries:
        print(f"\\n\\n📝 Query: {query}")
        print("-"*50)
        response = await copilot.process_query(query)
        print(f"🤖 Response: {response}")
        print("\\n" + "="*70)
        input("Press Enter for next query...")

if __name__ == "__main__":
    asyncio.run(test_queries())
'''
        test_script.write_text(test_content)
        print("✅ test_query.py created")
        print("   Run 'python test_query.py' to test the system")

def main():
    """Main setup function"""
    print_section("AI Customer Copilot - Project Setup")
    print(f"Source: {SOURCE_PATH}")
    print(f"Target: {TARGET_PATH}")
    
    # Step 1: Check and copy files
    if not check_and_copy_files():
        print("\\n❌ Setup failed. Please check source files.")
        return
    
    # Step 2: Verify structure
    verify_project_structure()
    
    # Step 3: Create CSV files if missing
    create_missing_csv_files()
    
    # Step 4: Create .env file
    create_env_file()
    
    # Step 5: Install dependencies
    install_dependencies()
    
    # Step 6: Create test script
    create_test_query_script()
    
    print_section("Setup Complete!")
    print("""
    Next steps:
    1. Edit .env file and add your OpenAI API key
    2. Activate virtual environment: venv\\Scripts\\activate
    3. Install dependencies: pip install -r requirements.txt
    4. Run the copilot: python main.py
    5. Or test with: python test_query.py
    
    Example queries to try:
    - "What are the best attractions for families?"
    - "Where can I find good chili crab?"
    - "Any promotions for shopping?"
    - "I love photography, where should I go?"
    """)

if __name__ == "__main__":
    main()