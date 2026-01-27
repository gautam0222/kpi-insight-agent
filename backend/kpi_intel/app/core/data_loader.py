import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from kpi_intel.app.core.config import config


class DataLoader:
    def __init__(self):
        self.df = None
        self.load_data()
    
    def load_data(self):
        """Load and preprocess the KPI data"""
        self.df = pd.read_csv(config.DATA_PATH)
        
        # Generate dates for 90 days (assuming 500 rows / 90 days ≈ 5-6 products per day)
        # Create date column
        end_date = datetime.now()
        start_date = end_date - timedelta(days=89)
        
        # Distribute rows across 90 days
        num_rows = len(self.df)
        dates = pd.date_range(start=start_date, end=end_date, periods=num_rows)
        self.df['Date'] = dates
        
        # Clean data
        self.df = self.df.fillna(0)
        
        # Calculate Overall Revenue (Sales_y + Sales_m)
        self.df['Overall_Revenue'] = self.df['Sales_y'] + self.df['Sales_m']
        
        return self.df
    
    def get_data(self):
        """Return the loaded dataframe"""
        return self.df
    
    def filter_data(self, start_date=None, end_date=None, product=None, category=None):
        """Filter data based on parameters"""
        filtered_df = self.df.copy()
        
        if start_date:
            filtered_df = filtered_df[filtered_df['Date'] >= pd.to_datetime(start_date)]
        
        if end_date:
            filtered_df = filtered_df[filtered_df['Date'] <= pd.to_datetime(end_date)]
        
        if product:
            filtered_df = filtered_df[filtered_df['Product_Name'].str.contains(product, case=False, na=False)]
        
        if category:
            filtered_df = filtered_df[filtered_df['Category'].str.contains(category, case=False, na=False)]
        
        return filtered_df

# Global data loader instance
data_loader = DataLoader()
