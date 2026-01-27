import pandas as pd
from openai import OpenAI
from kpi_intel.app.core.config import config
from kpi_intel.app.core.logger import logger


class RecommendationEngine:
    def __init__(self):
        self.client = OpenAI(
            base_url=config.OPENROUTER_BASE_URL,
            api_key=config.OPENROUTER_API_KEY
        )
        
        # Simple cause-to-action mapping
        self.action_map = {
            'Discount': 'Adjust discount strategy to optimize revenue vs. margin',
            'M_Spend': 'Revise marketing spend allocation for better ROI',
            'Supply_Chain_E': 'Address supply chain inefficiencies and bottlenecks',
            'Price': 'Review pricing strategy for competitive positioning',
            'Rating': 'Improve product quality and customer experience'
        }
    
    def generate_recommendations(self, causal_analysis):
        """Generate actionable business recommendations"""
        logger.info("Generating recommendations...")
        
        alert = causal_analysis['alert']
        causes = causal_analysis['causes']
        
        if not causes:
            return {
                'recommendations': [],
                'summary': 'No actionable insights available from current data.'
            }
        
        # Generate recommendations for top causes
        recommendations = []
        
        for cause in causes[:3]:  # Top 3 causes
            feature = cause['feature']
            base_action = self.action_map.get(feature, f"Review {feature} impact on revenue")
            
            rec = {
                'cause': feature,
                'priority': 'High' if abs(cause['importance_score']) > 50 else 'Medium',
                'action': base_action,
                'impact': f"{cause['change_pct']:+.1f}% change observed",
                'details': self._generate_detailed_action(alert, cause)
            }
            recommendations.append(rec)
        
        # Generate executive summary using LLM
        summary = self._generate_executive_summary(alert, causes, recommendations)
        
        logger.info(f"Generated {len(recommendations)} recommendations")
        
        return {
            'recommendations': recommendations,
            'summary': summary
        }
    
    def _generate_detailed_action(self, alert, cause):
        """Generate specific action based on cause"""
        feature = cause['feature']
        change = cause['change_pct']
        alert_type = alert['type']
        
        if feature == 'Discount':
            if alert_type == 'decrease' and change < 0:
                return "Discounts decreased leading to revenue drop. Consider strategic promotions."
            else:
                return "Discount changes impacting revenue. Optimize discount levels for profitability."
        
        elif feature == 'M_Spend':
            if alert_type == 'decrease' and change < 0:
                return "Marketing spend reduction correlates with revenue drop. Increase targeted campaigns."
            else:
                return "Marketing spend changes affecting revenue. Analyze campaign effectiveness."
        
        elif feature == 'Supply_Chain_E':
            if change < 0:
                return "Supply chain efficiency dropped. Investigate delays and find alternate suppliers."
            else:
                return "Supply chain improvements detected. Maintain current operational standards."
        
        elif feature == 'Price':
            if alert_type == 'decrease' and change > 0:
                return "Price increases may be hurting sales volume. Review competitive pricing."
            else:
                return "Price adjustments impacting revenue. Conduct price elasticity analysis."
        
        elif feature == 'Rating':
            if change < 0:
                return "Product ratings declined. Focus on quality improvement and customer feedback."
            else:
                return "Rating improvements supporting revenue. Continue quality initiatives."
        
        return f"Monitor {feature} closely and adjust strategy accordingly."
    
    def _generate_executive_summary(self, alert, causes, recommendations):
        """Generate executive-ready summary using LLM"""
        causes_text = "\n".join([
            f"- {c['feature']}: {c['change_pct']:+.1f}% change"
            for c in causes[:3]
        ])
        
        recs_text = "\n".join([
            f"- {r['action']}"
            for r in recommendations
        ])
        
        prompt = f"""You are a business executive advisor. Create a concise executive summary (2-3 sentences) based on:

Revenue Alert:
- Date: {alert['date']}
- Change: {alert['change_pct']:+.1f}% ({alert['type']})

Key Factors:
{causes_text}

Recommended Actions:
{recs_text}

Write a clear, action-oriented summary for executives."""
        
        try:
            response = self.client.chat.completions.create(
                model=config.OPENROUTER_MODEL,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3
            )
            
            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"Error generating summary: {e}")
            return f"Revenue {alert['type']}d by {abs(alert['change_pct']):.1f}% on {alert['date']}. Immediate action required on {', '.join([c['feature'] for c in causes[:2]])}."

recommender = RecommendationEngine()