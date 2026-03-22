import pandas as pd
from pathlib import Path
import logging

class DataLoader:
    def __init__(self, data_dir: Path):
        self.data_dir = data_dir
        self.logger = logging.getLogger(__name__)
        
    def load_csv(self, filename: str) -> pd.DataFrame:
        """Load CSV file with error handling"""
        filepath = self.data_dir / filename
        try:
            # Try to read with proper encoding
            df = pd.read_csv(filepath, encoding='utf-8')
            self.logger.info(f"Loaded {len(df)} records from {filename}")
            return df
        except Exception as e:
            self.logger.error(f"Failed to load {filename}: {e}")
            # Return empty DataFrame on error
            return pd.DataFrame()
    
    def load_attractions(self) -> pd.DataFrame:
        return self.load_csv("attractions.csv")
    
    def load_restaurants(self) -> pd.DataFrame:
        return self.load_csv("restaurants.csv")
    
    def load_shops(self) -> pd.DataFrame:
        return self.load_csv("shops.csv")
    
    def load_customers(self) -> pd.DataFrame:
        return self.load_csv("customers.csv")
    
    def load_transactions(self) -> pd.DataFrame:
        return self.load_csv("transactions.csv")
    
    def load_promotions(self) -> pd.DataFrame:
        return self.load_csv("promotions.csv")
