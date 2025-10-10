#!/usr/bin/env python3
"""
Quick test for improved number extraction - only Q1, Q2, Q3
"""

import sys
sys.path.append('/Users/svitlanakovalivska/CNC')

from langchain_implementation_fixed import CNCValidationWorkflow
from datetime import datetime

class SuperQuickTest(CNCValidationWorkflow):
    """Super quick test - only first 3 questions"""
    
    def __init__(self, data_path: str, ionos_api_key: str = None):
        super().__init__(data_path, ionos_api_key)
        
        # Override with only first 3 questions
        first_3_questions = dict(list(self.test_questions.items())[:3])
        self.test_questions = first_3_questions
        
        print(f"⚡ SUPER QUICK Test: Testing only {len(self.test_questions)} questions")

if __name__ == "__main__":
    print("⚡ SUPER QUICK TEST - Fixed Number Selection Logic")
    
    data_path = "data/sample_cnc_data.xlsx"  # Sample data for demonstration
    
    try:
        with open("/Users/svitlanakovalivska/CNC/LLM_Project/config/ionos_token.txt", 'r') as f:
            ionos_api_key = f.read().strip()
    except:
        exit(1)
    
    try:
        workflow = SuperQuickTest(data_path, ionos_api_key)
        
        print("\n" + "="*40)
        print("⚡ STARTING SUPER QUICK TEST")
        print("📝 Questions: Q1 (Total Records), Q2 (Program Count), Q3 (Program %)")  
        print("🔧 All 4 approaches")
        print("="*40)
        
        results = workflow.run_complete_validation()
        
        # Detailed analysis per question
        successful_results = [r for r in results['results'] if 'error' not in r]
        if successful_results:
            print(f"\n📊 DETAILED QUICK RESULTS:")
            
            # Group by question and approach
            by_question = {}
            for result in successful_results:
                q_id = result['question_id']
                approach = result['approach']
                if q_id not in by_question:
                    by_question[q_id] = {}
                by_question[q_id][approach] = {
                    'response': result['response'][:100] + '...' if len(result['response']) > 100 else result['response'],
                    'extracted': result['validation_scores']['extracted_numbers'],
                    'accuracy': result['validation_scores']['numerical_accuracy']
                }
            
            for q_id in sorted(by_question.keys()):
                print(f"\n  📝 {q_id.upper()}:")
                for approach in ['basic', 'expert', 'enhanced', 'database']:
                    if approach in by_question[q_id]:
                        data = by_question[q_id][approach]
                        accuracy_symbol = "✅" if data['accuracy'] == 1.0 else "❌"
                        print(f"    {approach.upper()}: {accuracy_symbol} {data['accuracy']:.1f} - {data['extracted']} - \"{data['response']}\"")
            
            # Overall numerical accuracy
            approach_scores = {}
            for result in successful_results:
                approach = result['approach']
                if approach not in approach_scores:
                    approach_scores[approach] = []
                approach_scores[approach].append(result['validation_scores']['numerical_accuracy'])
            
            print(f"\n📊 NUMERICAL ACCURACY SUMMARY:")
            for approach, scores in approach_scores.items():
                correct_count = sum(1 for s in scores if s == 1.0)
                avg = sum(scores) / len(scores)
                print(f"  {approach.upper()}: {correct_count}/{len(scores)} correct = {avg:.3f} accuracy")
            
            # Detailed number extraction analysis
            print(f"\n🔍 DETAILED NUMBER EXTRACTION ANALYSIS:")
            for q_id in sorted(by_question.keys()):
                print(f"\n  📝 {q_id.upper()}:")
                question_data = workflow.test_questions[q_id]
                expected = question_data['expected_values']
                print(f"    Expected: {expected}")
                
                for approach in ['basic', 'expert', 'enhanced', 'database']:
                    if approach in by_question[q_id]:
                        data = by_question[q_id][approach]
                        print(f"    {approach.upper()}: Extracted {data['extracted']} from response")
                        print(f"      Response: \"{data['response'][:150]}...\"")
                        
                        # Check why extraction might fail
                        response = data['response']
                        import re
                        numbers_in_text = re.findall(r'\d+(?:\.\d+)?', response)
                        print(f"      Raw numbers found: {numbers_in_text}")
                        print()
        
        print(f"\n⚡ Super quick test completed!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()