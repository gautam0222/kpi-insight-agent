import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from openai import OpenAI
from kpi_intel.app.core.config import config
from kpi_intel.app.core.data_loader import data_loader
from kpi_intel.app.core.logger import logger


class CausalAnalyzer:
    def __init__(self):
        self.df = data_loader.get_data()
        self.client = OpenAI(
            base_url=config.OPENROUTER_BASE_URL,
            api_key=config.OPENROUTER_API_KEY
        )
    
    def analyze_cause(self, alert):
        """Analyze the cause of a KPI change"""
        logger.info(f"Analyzing cause for alert on {alert['date']}")
        
        # Get data around the alert date
        alert_date = pd.to_datetime(alert['date'])
        
        # Get data for alert day and previous period (window + 1 days)
        window_days = config.ROLLING_WINDOW + 1
        alert_data = self.df[self.df['Date'] == alert_date]
        baseline_data = self.df[
            (self.df['Date'] >= alert_date - pd.Timedelta(days=window_days)) &
            (self.df['Date'] < alert_date)
        ]
        
        if alert_data.empty:
            logger.warning(f"No data found for alert date {alert['date']}")
            return {
                'alert': alert,
                'causes': [],
                'explanation': "Insufficient data for causal analysis - no records found for alert date"
            }
        
        if baseline_data.empty or len(baseline_data) < 3:
            logger.warning(f"Insufficient baseline data for {alert['date']}")
            return {
                'alert': alert,
                'causes': [],
                'explanation': "Insufficient baseline data for comparison"
            }
        
        # Analyze feature changes
        causes = self._identify_causes(alert_data, baseline_data)
        
        # Generate explanation using LLM
        explanation = self._generate_causal_explanation(alert, causes)
        
        logger.info(f"Causal analysis complete. Found {len(causes)} potential causes.")
        
        return {
            'alert': alert,
            'causes': causes,
            'explanation': explanation
        }
    
    def _identify_causes(self, alert_data, baseline_data):
        """Identify potential causes using statistical analysis"""
        features = ['Discount', 'M_Spend', 'Supply_Chain_E', 'Price', 'Rating']
        causes = []
        
        for feature in features:
            if feature in alert_data.columns and feature in baseline_data.columns:
                alert_mean = alert_data[feature].mean()
                baseline_mean = baseline_data[feature].mean()
                
                if baseline_mean != 0:
                    pct_change = ((alert_mean - baseline_mean) / baseline_mean) * 100
                    
                    # Calculate correlation with revenue
                    combined = pd.concat([alert_data, baseline_data])
                    if len(combined) > 2:
                        correlation = combined[feature].corr(combined['Overall_Revenue'])
                    else:
                        correlation = 0
                    
                    # Score importance based on change magnitude and correlation
                    importance = abs(pct_change) * abs(correlation) if not np.isnan(correlation) else abs(pct_change)
                    
                    if abs(pct_change) > 5:  # Only significant changes
                        causes.append({
                            'feature': feature,
                            'baseline_value': round(baseline_mean, 2),
                            'alert_value': round(alert_mean, 2),
                            'change_pct': round(pct_change, 2),
                            'correlation': round(correlation, 3) if not np.isnan(correlation) else 0,
                            'importance_score': round(importance, 2)
                        })
        
        # Sort by importance
        causes.sort(key=lambda x: abs(x['importance_score']), reverse=True)
        
        return causes[:5]  # Top 5 causes
    
    def _generate_causal_explanation(self, alert, causes):
        """Generate human-readable causal explanation using LLM"""
        if not causes:
            return f"Revenue {alert['type']}d by {abs(alert['change_pct']):.1f}% on {alert['date']}. No significant factor changes detected in the data."
        
        causes_text = "\n".join([
            f"- {c['feature']}: changed from {c['baseline_value']} to {c['alert_value']} ({c['change_pct']:+.1f}%)"
            for c in causes
        ])
        
        prompt = f"""You are a business analyst. Explain why revenue changed based on this data:

Alert Details:
- Date: {alert['date']}
- Revenue Change: {alert['change_pct']:+.1f}% ({alert['type']})
- Current Revenue: ${alert['current_value']:,.2f}
- Baseline Revenue: ${alert['baseline']:,.2f}

Identified Factors:
{causes_text}

Provide a clear, concise explanation (3-4 sentences) of the likely causes for this revenue change in business terms.
Focus on the most important factors."""
        
        try:
            response = self.client.chat.completions.create(
                model=config.OPENROUTER_MODEL,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3
            )
            
            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"Error generating explanation: {e}")
            return f"Revenue {alert['type']}d by {abs(alert['change_pct']):.1f}% due to changes in {', '.join([c['feature'] for c in causes[:3]])}."

analyzer = CausalAnalyzer()