#!/usr/bin/env python3
"""
Test improved German number extraction
"""

import sys
sys.path.append('/Users/svitlanakovalivska/CNC')

from langchain_implementation_fixed import ValidationTool, GroundTruthData

def test_german_number_extraction():
    """Test the improved German number extraction"""
    
    # Create dummy ground truth for testing
    ground_truth = GroundTruthData(
        total_records=113855,
        columns=["pgm_STRING", "mode_STRING", "exec_STRING"],
        program_distribution={"100.362.1Y.00.01.0SP-1": 56.0},
        mode_efficiency={
            "automatic_percentage": 67.9,
            "manual_percentage": 32.1,
            "auto_vs_manual_ratio": 2.11
        },
        active_percentage=35.9
    )
    
    validation_tool = ValidationTool(ground_truth)
    
    print("🧪 TESTING IMPROVED GERMAN NUMBER EXTRACTION")
    print("="*60)
    
    test_cases = [
        # German number format tests
        ("113.855", "q1", 113855.0, "German thousand separator"),
        ("67,4", "q5", 67.4, "German decimal comma"),
        ("2,11", "q7", 2.11, "German decimal ratio"),
        ("1.234,56", "test", 1234.56, "German mixed format"),
        ("100.362.1", "test", 100362.1, "Complex German format"),
        
        # Response context tests
        ("Die Antwort ist 56.0", "q3", 56.0, "Q3 percentage response"),
        ("Insgesamt sind es 77.295 Datensätze", "q4", 77295.0, "Q4 count response"),
        ("Das ergibt 35,9%", "q9", 35.9, "Q9 percentage with comma"),
        ("Es sind genau 113,855 Datensätze vorhanden", "q1", 113855.0, "Q1 with comma"),
        ("Verhältnis: 2.11", "q7", 2.11, "Q7 ratio response"),
    ]
    
    success_count = 0
    total_tests = len(test_cases)
    
    for i, (response, question_id, expected, description) in enumerate(test_cases, 1):
        print(f"\n📋 TEST {i}: {description}")
        print(f"Response: '{response}'")
        print(f"Expected: {expected}")
        
        extracted = validation_tool.extract_number_from_response(response, question_id)
        
        # Check if result is correct (within small tolerance)
        correct = abs(extracted - expected) < 0.01 if extracted else False
        status = "✅ PASS" if correct else "❌ FAIL"
        
        print(f"Extracted: {extracted}")
        print(f"Result: {status}")
        
        if correct:
            success_count += 1
        else:
            print(f"❌ Expected {expected}, got {extracted}")
    
    print(f"\n🎯 SUMMARY:")
    print(f"Passed: {success_count}/{total_tests} ({success_count/total_tests*100:.1f}%)")
    print(f"Failed: {total_tests-success_count}/{total_tests}")
    
    if success_count == total_tests:
        print("🎉 All tests passed! German number extraction is working correctly.")
    else:
        print("⚠️  Some tests failed. Number extraction needs further improvement.")
    
    return success_count == total_tests

if __name__ == "__main__":
    print("🔧 TESTING IMPROVED GERMAN NUMBER EXTRACTION")
    success = test_german_number_extraction()
    
    print(f"\n💡 KEY IMPROVEMENTS:")
    print("1. ✅ Unified extraction function for all approaches")
    print("2. ✅ Improved German number format handling")
    print("3. ✅ Question-specific number selection logic")
    print("4. ✅ Better handling of mixed formats (1.234,56)")
    print("5. ✅ Context-aware selection based on question ID")
    
    if success:
        print(f"\n🚀 Ready to test with super_quick_test_fixed.py")
    else:
        print(f"\n🔧 Further adjustments needed before full testing")