import argparse
import sys
from tabulate import tabulate
from app.services.talk_to_data import agent
from app.services.monitor import monitor
from app.services.causal import analyzer
from app.services.recommend import recommender
from app.core.logger import logger

def print_header(title):
    """Print formatted header"""
    print("\n" + "="*80)
    print(f"  {title}")
    print("="*80 + "\n")

def cmd_ask(args):
    """Handle talk-to-data queries"""
    print_header("TALK-TO-DATA")
    print(f"Question: {args.question}\n")
    
    result = agent.query(args.question)
    
    print("Result:")
    print("-" * 80)
    print(result['result'])
    print("-" * 80)
    
    print(f"\nExplanation:\n{result['explanation']}")
    
    if args.show_code:
        print(f"\nGenerated Code:\n{result['code']}")

def cmd_monitor(args):
    """Handle KPI monitoring"""
    print_header("KPI MONITORING")
    
    results = monitor.detect_changes(
        start_date=args.start_date,
        end_date=args.end_date,
        product=args.product,
        category=args.category
    )
    
    alerts = results['alerts']
    summary = results['summary']
    
    print(f"Date Range: {summary['date_range']}")
    print(f"Total Revenue: ${summary['total_revenue']:,.2f}")
    print(f"Avg Daily Revenue: ${summary['avg_daily_revenue']:,.2f}")
    print(f"Alerts Found: {summary['total_alerts']}\n")
    
    if alerts:
        table_data = [
            [
                a['date'],
                a['metric'],
                f"${a['current_value']:,.2f}",
                f"${a['baseline']:,.2f}",
                f"{a['change_pct']:+.1f}%",
                a['type'].upper()
            ]
            for a in alerts
        ]
        
        headers = ['Date', 'Metric', 'Current', 'Baseline', 'Change', 'Type']
        print(tabulate(table_data, headers=headers, tablefmt='grid'))
    else:
        print("No significant KPI changes detected.")

def cmd_explain(args):
    """Handle causal analysis"""
    print_header("CAUSAL ANALYSIS")
    
    # Get recent alerts
    results = monitor.get_recent_changes(days=args.days)
    alerts = results['alerts']
    
    if not alerts:
        print("No recent alerts to analyze.")
        return
    
    # Analyze the most recent or specified alert
    alert_to_analyze = alerts[0] if not args.alert_index else alerts[min(args.alert_index, len(alerts)-1)]
    
    print(f"Analyzing alert from {alert_to_analyze['date']}:")
    print(f"Revenue {alert_to_analyze['type']}d by {alert_to_analyze['change_pct']:+.1f}%\n")
    
    analysis = analyzer.analyze_cause(alert_to_analyze)
    
    if analysis['causes']:
        print("Identified Causes:")
        print("-" * 80)
        
        table_data = [
            [
                c['feature'],
                f"{c['baseline_value']:.2f}",
                f"{c['alert_value']:.2f}",
                f"{c['change_pct']:+.1f}%",
                f"{c['importance_score']:.1f}"
            ]
            for c in analysis['causes']
        ]
        
        headers = ['Factor', 'Baseline', 'Current', 'Change', 'Importance']
        print(tabulate(table_data, headers=headers, tablefmt='grid'))
        
        print(f"\nExplanation:\n{analysis['explanation']}")
    else:
        print("No significant causes identified.")

def cmd_recommend(args):
    """Handle recommendations"""
    print_header("ACTION RECOMMENDATIONS")
    
    # Get recent alerts
    results = monitor.get_recent_changes(days=args.days)
    alerts = results['alerts']
    
    if not alerts:
        print("No recent alerts to generate recommendations for.")
        return
    
    # Analyze and recommend for most recent alert
    alert_to_analyze = alerts[0]
    
    print(f"Recommendations for alert on {alert_to_analyze['date']}:")
    print(f"Revenue {alert_to_analyze['type']}d by {alert_to_analyze['change_pct']:+.1f}%\n")
    
    # Get causal analysis first
    analysis = analyzer.analyze_cause(alert_to_analyze)
    
    # Generate recommendations
    recommendations = recommender.generate_recommendations(analysis)
    
    print("Executive Summary:")
    print("-" * 80)
    print(recommendations['summary'])
    print("-" * 80 + "\n")
    
    if recommendations['recommendations']:
        print("Recommended Actions:")
        
        for i, rec in enumerate(recommendations['recommendations'], 1):
            print(f"\n{i}. {rec['cause']} (Priority: {rec['priority']})")
            print(f"   Action: {rec['action']}")
            print(f"   Impact: {rec['impact']}")
            print(f"   Details: {rec['details']}")
    else:
        print("No specific recommendations available.")

def main():
    parser = argparse.ArgumentParser(
        description='KPI Intelligence System - AI-powered KPI monitoring and analysis',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Ask command (Talk-to-Data)
    ask_parser = subparsers.add_parser('ask', help='Ask questions about the data')
    ask_parser.add_argument('question', type=str, help='Natural language question')
    ask_parser.add_argument('--show-code', action='store_true', help='Show generated code')
    
    # Monitor command
    monitor_parser = subparsers.add_parser('monitor', help='Monitor KPI changes')
    monitor_parser.add_argument('--start-date', type=str, help='Start date (YYYY-MM-DD)')
    monitor_parser.add_argument('--end-date', type=str, help='End date (YYYY-MM-DD)')
    monitor_parser.add_argument('--product', type=str, help='Filter by product name')
    monitor_parser.add_argument('--category', type=str, help='Filter by category')
    
    # Explain command (Causal Analysis)
    explain_parser = subparsers.add_parser('explain', help='Explain why KPIs changed')
    explain_parser.add_argument('--days', type=int, default=7, help='Days to look back (default: 7)')
    explain_parser.add_argument('--alert-index', type=int, default=0, help='Alert index to analyze')
    
    # Recommend command
    recommend_parser = subparsers.add_parser('recommend', help='Get action recommendations')
    recommend_parser.add_argument('--days', type=int, default=7, help='Days to look back (default: 7)')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    try:
        if args.command == 'ask':
            cmd_ask(args)
        elif args.command == 'monitor':
            cmd_monitor(args)
        elif args.command == 'explain':
            cmd_explain(args)
        elif args.command == 'recommend':
            cmd_recommend(args)
    except Exception as e:
        logger.error(f"Error executing command: {e}")
        print(f"\nError: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main()