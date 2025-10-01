#!/usr/bin/env python3
"""
Quick test version of CNC LangChain validation - tests only first 3 questions
"""

import sys
sys.path.append('/Users/svitlanakovalivska/CNC')

from langchain_implementation_fixed import CNCValidationWorkflow
import pandas as pd
from datetime import datetime

class QuickCNCTest(CNCValidationWorkflow):
    """Quick version that tests only first 3 questions"""
    
    def __init__(self, data_path: str, ionos_api_key: str = None):
        super().__init__(data_path, ionos_api_key)
        
        # Override with only first 3 questions for quick testing
        first_3_questions = dict(list(self.test_questions.items())[:3])
        self.test_questions = first_3_questions
        
        print(f"🚀 Quick Test Mode: Testing only {len(self.test_questions)} questions")
        for q_id in self.test_questions.keys():
            print(f"   - {q_id}")

if __name__ == "__main__":
    print("🚀 Starting Quick CNC Test with IMPROVED NUMBER EXTRACTION...")
    print("🎯 Testing smart single number selection logic")
    
    # Initialize workflow
    data_path = "/Users/svitlanakovalivska/CNC/LLM_Project/M1_clean_original_names.xlsx"
    ionos_api_key = None
    
    try:
        with open("/Users/svitlanakovalivska/CNC/LLM_Project/config/ionos_token.txt", 'r') as f:
            ionos_api_key = f.read().strip()
        print("✅ IONOS API key loaded successfully")
    except Exception as e:
        print(f"⚠️ Could not load IONOS API key: {e}")
        exit(1)
    
    try:
        # Quick test
        workflow = QuickCNCTest(data_path, ionos_api_key)
        
        print("\n" + "="*50)
        print("🚀 STARTING QUICK TEST (3 questions, 4 approaches)")
        print("🔬 Testing improved single number selection")
        print("="*50)
        
        results = workflow.run_complete_validation()
        
        if results.get('interrupted'):
            print("\n⚠️ Test was interrupted")
        else:
            print("\n✅ Quick test completed!")
            
        # Generate timestamp and create visualizations if we have results
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        if results['summary']['successful_tests'] > 0:
            workflow.create_visualizations(results, timestamp + "_quick")
            print(f"\n🎉 Quick test complete! Results saved with timestamp: {timestamp}_quick")
        else:
            print("❌ No successful tests to visualize")
            
    except KeyboardInterrupt:
        print(f"\n🛑 Quick test interrupted by user")
    except Exception as e:
        print(f"❌ Error during quick test: {e}")
        import traceback
        traceback.print_exc()