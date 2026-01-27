
"""
Comprehensive test script for KPI Intelligence System
Run this to verify all features before the live demo
"""

import sys
from app.services.talk_to_data import agent
from app.services.monitor import monitor
from app.services.causal import analyzer
from app.services.recommend import recommender

def test_talk_to_data():
    print("\n" + "="*80)
    print("TEST 1: Talk-to-Data")
    print("="*80)
    
    questions = [
        "What is the total revenue?",
        "Show top 5 products by sales",
        "What is the average discount percentage?"
    ]
    
    for q in questions:
        print(f"\nQ: {q}")
        result = agent.query(q)
        print(f"A: {result['result'][:200]}...")
        print(f"Explanation: {result['explanation'][:150]}...")
    
    print("\n✓ Talk-to-Data working")

def test_monitoring():
    print("\n" + "="*80)
    print("TEST 2: KPI Monitoring")
    print("="*80)
    
    results = monitor.detect_changes()
    print(f"Alerts detected: {len(results['alerts'])}")
    
    if results['alerts']:
        alert = results['alerts'][0]
        print(f"Sample alert: {alert['date']} - {alert['change_pct']:+.1f}% change")
    
    print("\n✓ Monitoring working")
    return results['alerts']

def test_causal_analysis(alerts):
    print("\n" + "="*80)
    print("TEST 3: Causal Analysis")
    print("="*80)
    
    if not alerts:
        print("No alerts to analyze")
        return None
    
    alert = alerts[0]
    analysis = analyzer.analyze_cause(alert)
    
    print(f"Analyzing alert from: {alert['date']}")
    print(f"Causes found: {len(analysis['causes'])}")
    
    if analysis['causes']:
        print(f"Top cause: {analysis['causes'][0]['feature']}")
        print(f"Explanation: {analysis['explanation'][:150]}...")
    
    print("\n✓ Causal Analysis working")
    return analysis

def test_recommendations(analysis):
    print("\n" + "="*80)
    print("TEST 4: Recommendations")
    print("="*80)
    
    if not analysis:
        print("No analysis to generate recommendations")
        return
    
    recommendations = recommender.generate_recommendations(analysis)
    
    print(f"Recommendations generated: {len(recommendations['recommendations'])}")
    print(f"Summary: {recommendations['summary'][:150]}...")
    
    print("\n✓ Recommendations working")

def main():
    print("\n" + "="*80)
    print("KPI INTELLIGENCE SYSTEM - FULL TEST")
    print("="*80)
    
    try:
        test_talk_to_data()
        alerts = test_monitoring()
        analysis = test_causal_analysis(alerts)
        test_recommendations(analysis)
        
        print("\n" + "="*80)
        print("✓ ALL TESTS PASSED - System Ready for Demo!")
        print("="*80 + "\n")
        
    except Exception as e:
        print(f"\n✗ TEST FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()