import pandas as pd
import numpy as np
from kpi_intel.app.core.config import config
from kpi_intel.app.core.data_loader import data_loader
from kpi_intel.app.core.logger import logger


class KPIMonitor:
    def __init__(self):
        self.df = data_loader.get_data()
        self.threshold = config.ALERT_THRESHOLD
        self.window = config.ROLLING_WINDOW
    
    def detect_changes(self, start_date=None, end_date=None, product=None, category=None):
        """Detect KPI changes and anomalies"""
        logger.info("Running KPI change detection...")
        
        # Filter data
        filtered_df = data_loader.filter_data(start_date, end_date, product, category)
        
        if filtered_df.empty:
            return {"alerts": [], "message": "No data found for given filters"}
        
        # Aggregate daily revenue
        daily_revenue = filtered_df.groupby('Date')['Overall_Revenue'].sum().sort_index()
        
        # Calculate rolling average
        rolling_avg = daily_revenue.rolling(window=self.window, min_periods=1).mean()
        
        # Detect changes
        alerts = []
        
        for i in range(self.window, len(daily_revenue)):
            current_revenue = daily_revenue.iloc[i]
            baseline = rolling_avg.iloc[i-1]
            
            if baseline > 0:
                pct_change = ((current_revenue - baseline) / baseline) * 100
                
                if abs(pct_change) >= self.threshold:
                    alert = {
                        'date': daily_revenue.index[i].strftime('%Y-%m-%d'),
                        'metric': 'Overall_Revenue',
                        'current_value': round(current_revenue, 2),
                        'baseline': round(baseline, 2),
                        'change_pct': round(pct_change, 2),
                        'type': 'increase' if pct_change > 0 else 'decrease'
                    }
                    alerts.append(alert)
                    logger.warning(f"Alert detected: {alert}")
        
        # Summary statistics
        summary = {
            'total_alerts': len(alerts),
            'date_range': f"{daily_revenue.index[0].strftime('%Y-%m-%d')} to {daily_revenue.index[-1].strftime('%Y-%m-%d')}",
            'avg_daily_revenue': round(daily_revenue.mean(), 2),
            'total_revenue': round(daily_revenue.sum(), 2),
            'filters': {
                'start_date': start_date,
                'end_date': end_date,
                'product': product,
                'category': category
            }
        }
        
        logger.info(f"Detection complete. Found {len(alerts)} alerts.")
        
        return {
            'alerts': alerts,
            'summary': summary
        }
    
    def get_recent_changes(self, days=7):
        """Get most recent KPI changes"""
        end_date = self.df['Date'].max()
        start_date = end_date - pd.Timedelta(days=days)
        
        return self.detect_changes(
            start_date=start_date.strftime('%Y-%m-%d'),
            end_date=end_date.strftime('%Y-%m-%d')
        )

monitor = KPIMonitor()