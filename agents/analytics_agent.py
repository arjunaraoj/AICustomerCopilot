from typing import Dict, Any, List
from .base_agent import BaseAgent
from tools.data_loader import DataLoader
import pandas as pd
from datetime import datetime, timedelta

class AnalyticsAgent(BaseAgent):
    """Analyzes customer data, transactions, and provides insights"""
    
    def __init__(self, data_loader: DataLoader):
        super().__init__("AnalyticsAgent")
        self.data_loader = data_loader
        
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        analysis_type = input_data.get("analysis_type", "general")
        filters = input_data.get("filters", {})
        user_id = input_data.get("user_id")
        
        self.log_info(f"Analyzing: {analysis_type}")
        
        customers_df = self.data_loader.load_customers()
        transactions_df = self.data_loader.load_transactions()
        
        results = {}
        
        if analysis_type == "customer_insights" and user_id:
            results = self._get_customer_insights(transactions_df, customers_df, user_id)
        elif analysis_type == "trending":
            results = self._get_trending_insights(transactions_df)
        elif analysis_type == "recommendations":
            results = self._get_recommendations(transactions_df, customers_df, filters)
        else:
            results = self._get_general_insights(transactions_df, customers_df)
        
        return {
            "agent": "AnalyticsAgent",
            "analysis_type": analysis_type,
            "results": results
        }
    
    def _get_customer_insights(self, transactions_df, customers_df, user_id: str) -> Dict:
        customer = customers_df[customers_df['customer_id'] == user_id]
        customer_transactions = transactions_df[transactions_df['customer_id'] == user_id]
        
        if customer.empty:
            return {"error": "Customer not found"}
        
        total_spend = customer_transactions['amount'].sum() if not customer_transactions.empty else 0
        categories = customer_transactions['category'].value_counts().to_dict() if not customer_transactions.empty else {}
        
        return {
            "customer_name": customer.iloc[0]['name'] if not customer.empty else "Unknown",
            "country": customer.iloc[0]['country'] if not customer.empty else "Unknown",
            "preferences": customer.iloc[0]['preferences'] if not customer.empty else "None",
            "total_spend": total_spend,
            "spend_categories": categories,
            "transaction_count": len(customer_transactions)
        }
    
    def _get_trending_insights(self, transactions_df) -> Dict:
        last_7_days = datetime.now() - timedelta(days=7)
        
        transactions_df['date'] = pd.to_datetime(transactions_df['date'])
        recent = transactions_df[transactions_df['date'] >= last_7_days]
        
        popular = recent['merchant_type'].value_counts().head(3).to_dict()
        
        return {
            "trending_categories": popular,
            "total_recent_transactions": len(recent),
            "average_spend": recent['amount'].mean() if not recent.empty else 0
        }
    
    def _get_recommendations(self, transactions_df, customers_df, filters: Dict) -> List[Dict]:
        popular_merchants = transactions_df['merchant_id'].value_counts().head(5).index.tolist()
        
        recommendations = []
        for merchant in popular_merchants:
            recommendations.append({
                "merchant_id": merchant,
                "type": "popular_choice",
                "confidence": "high"
            })
        
        return recommendations
    
    def _get_general_insights(self, transactions_df, customers_df) -> Dict:
        return {
            "total_customers": len(customers_df),
            "total_transactions": len(transactions_df),
            "total_spend": transactions_df['amount'].sum(),
            "average_transaction": transactions_df['amount'].mean(),
            "top_categories": transactions_df['category'].value_counts().head(3).to_dict()
        }
