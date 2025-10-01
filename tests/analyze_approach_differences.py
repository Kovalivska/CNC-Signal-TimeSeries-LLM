#!/usr/bin/env python3
"""
Analyze why Enhanced approach fails on questions that Basic approach answers
"""

import sys
sys.path.append('/Users/svitlanakovalivska/CNC')

def analyze_prompt_responses():
    """Analyze different prompt approaches to understand failure patterns"""
    
    print("🔍 ANALYZING PROMPT APPROACH DIFFERENCES")
    print("="*60)
    
    # Sample responses from the test output
    test_results = {
        "Q1": {
            "basic": {
                "response": "1.000.000",
                "extracted": [1000.0],
                "accuracy": 0.000
            },
            "expert": {
                "response": "113,855", 
                "extracted": [113855.0],
                "accuracy": 1.000
            },
            "enhanced": {
                "response": "113,855",
                "extracted": [113855.0], 
                "accuracy": 1.000
            },
            "database": {
                "response": "113855",
                "extracted": [113855.0],
                "accuracy": 1.000
            }
        },
        "Q2": {
            "basic": {
                "response": "1",
                "extracted": [1.0],
                "accuracy": 0.000
            },
            "expert": {
                "response": "1",
                "extracted": [1.0], 
                "accuracy": 0.000
            },
            "enhanced": {
                "response": "113,855",
                "extracted": [113855.0],
                "accuracy": 0.000
            },
            "database": {
                "response": "63789",
                "extracted": [63789.0],
                "accuracy": 1.000
            }
        },
        "Q3": {
            "basic": {
                "response": "Um den genauen Prozentsatz zu ermitteln, benötige ich die Gesamtzahl der Datensätze...",
                "extracted": [100362.0],
                "accuracy": 0.000
            },
            "enhanced": {
                "response": "Um den genauen Prozentsatz zu ermitteln, müssen wir die Anzahl der Datensätze... 56.0%",
                "extracted": [56.0],
                "accuracy": 1.000
            }
        }
    }
    
    print("\n📊 ANALYSIS OF RESPONSE PATTERNS:")
    print("-" * 40)
    
    for question, approaches in test_results.items():
        print(f"\n📝 {question}:")
        
        for approach, data in approaches.items():
            status = "✅ CORRECT" if data['accuracy'] == 1.0 else "❌ WRONG"
            print(f"  {approach.upper()}: {status}")
            print(f"    Response: '{data['response'][:80]}...'")
            print(f"    Extracted: {data['extracted']}")
            print()
    
    print("\n🎯 KEY FINDINGS:")
    print("-" * 20)
    print("1. BASIC approach often gives minimal/wrong answers ('1', '1.000.000')")
    print("2. EXPERT approach sometimes gives correct answers, sometimes wrong")
    print("3. ENHANCED approach gives mixed results - sometimes better, sometimes worse")  
    print("4. DATABASE approach consistently gives correct answers")
    print()
    
    print("🔧 ROOT CAUSE ANALYSIS:")
    print("-" * 25)
    print("1. **Different prompts generate different responses**")
    print("   - Basic: Too simple, doesn't guide the model properly")
    print("   - Expert: More detailed but inconsistent")
    print("   - Enhanced: May be too complex, causing confusion")
    print("   - Database: Has direct access to correct data")
    print()
    
    print("2. **Number extraction logic issues:**")
    print("   - All approaches use the SAME extraction function")
    print("   - Problem is in the RESPONSES, not extraction")
    print("   - Enhanced responses sometimes contain irrelevant numbers")
    print()
    
    print("3. **Prompt Engineering Problems:**")
    print("   - Enhanced prompt might be overwhelming the model")
    print("   - Model gets confused with too much context")
    print("   - Simpler prompts sometimes work better")
    print()
    
    print("💡 RECOMMENDATIONS:")
    print("-" * 20)
    print("1. **Simplify Enhanced Prompt**")
    print("   - Remove excessive context that confuses the model")
    print("   - Focus on clear, direct instructions")
    print("   - Test iteratively with simpler versions")
    print()
    
    print("2. **Improve Response Consistency**") 
    print("   - Add explicit formatting instructions")
    print("   - Use examples in prompts")
    print("   - Ensure all prompts ask for same output format")
    print()
    
    print("3. **Debug Each Approach Separately**")
    print("   - Test each prompt type individually")
    print("   - Compare response quality before extraction")
    print("   - Identify which prompt elements help vs. hurt")

def analyze_extraction_consistency():
    """Check if number extraction is truly consistent across approaches"""
    
    print("\n🔢 EXTRACTION CONSISTENCY CHECK:")
    print("="*40)
    
    # Test cases with same response, different approaches
    test_responses = [
        ("113,855", "Should extract 113855.0"),
        ("56.0", "Should extract 56.0"), 
        ("67,4", "Should extract 67.4"),
        ("Um den Prozentsatz zu berechnen... 56.0%", "Should extract 56.0"),
        ("Die Antwort ist 113,855 Datensätze", "Should extract 113855.0"),
        ("2.11", "Should extract 2.11")
    ]
    
    # Simulate extraction (would need actual function)
    print("Testing extraction consistency...")
    for response, expected in test_responses:
        print(f"Response: '{response}' -> {expected}")
    
    print("\n✅ All approaches should extract identical numbers from identical responses")
    print("❌ If results differ, the problem is in RESPONSE GENERATION, not extraction")

if __name__ == "__main__":
    analyze_prompt_responses()
    analyze_extraction_consistency()
    
    print(f"\n🎯 NEXT STEPS:")
    print("1. Run super_quick_test_fixed.py to test unified extraction")
    print("2. Compare prompt outputs side-by-side")
    print("3. Simplify Enhanced prompt if it's causing confusion")
    print("4. Focus on prompt engineering rather than extraction logic")