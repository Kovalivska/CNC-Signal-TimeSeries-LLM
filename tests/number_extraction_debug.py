#!/usr/bin/env python3
"""
Debug script for number extraction logic analysis
"""

import sys
sys.path.append('/Users/svitlanakovalivska/CNC')

import re
import json
from langchain_implementation_fixed import CNCValidationWorkflow

def analyze_number_extraction(response_text, question_type=""):
    """Analyze how numbers are extracted from response text"""
    print(f"\n🔍 ANALYZING: '{response_text[:100]}...'")
    print(f"📝 Question type: {question_type}")
    
    # Step 1: Extract all numbers using regex
    numbers_raw = re.findall(r'\d+(?:[,\.]\d+)*', response_text)
    print(f"Raw regex matches: {numbers_raw}")
    
    # Step 2: Clean and convert to float
    numbers = []
    for num_str in numbers_raw:
        try:
            # Handle German number format (comma as decimal separator)
            cleaned = num_str.replace(',', '.')
            # Remove thousand separators if they exist
            if '.' in cleaned and len(cleaned.split('.')[-1]) == 3 and len(cleaned.split('.')) > 2:
                # This looks like thousand separator, not decimal
                cleaned = cleaned.replace('.', '', cleaned.count('.') - 1)
            numbers.append(float(cleaned))
        except:
            continue
    
    print(f"Cleaned numbers: {numbers}")
    
    # Step 3: Apply selection logic based on question type
    selected = None
    if question_type.lower().contains("percentage") or question_type.lower().contains("prozent"):
        # For percentages, prefer numbers between 0-100
        percentage_candidates = [n for n in numbers if 0 <= n <= 100]
        if percentage_candidates:
            selected = max(percentage_candidates)  # Take the largest reasonable percentage
            print(f"✅ Selected {selected} (percentage logic)")
    
    elif question_type.lower().contains("ratio") or question_type.lower().contains("verhältnis"):
        # For ratios, prefer small decimal numbers
        ratio_candidates = [n for n in numbers if 0.1 <= n <= 10]
        if ratio_candidates:
            selected = min(ratio_candidates)  # Take the smallest reasonable ratio
            print(f"✅ Selected {selected} (ratio logic)")
    
    elif question_type.lower().contains("count") or question_type.lower().contains("anzahl"):
        # For counts, prefer larger integers
        count_candidates = [n for n in numbers if n >= 1 and n == int(n)]
        if count_candidates:
            selected = max(count_candidates)  # Take the largest integer
            print(f"✅ Selected {selected} (count logic)")
    
    if selected is None and numbers:
        # Fallback: take the most prominent number
        selected = max(numbers) if any(n > 100 for n in numbers) else numbers[0]
        print(f"⚠️ Fallback selected {selected}")
    
    return selected, numbers

def test_extraction_examples():
    """Test number extraction with example responses"""
    
    test_cases = [
        {
            "response": "113,855",
            "question_type": "total_records",
            "expected": 113855.0
        },
        {
            "response": "Um den genauen Prozentsatz zu ermitteln, müssen wir die Anzahl der Datensätze, bei denen das Programm '100.362.1Y.00.01.0SP-1' ausgeführt wird, ermitteln und diese durch die Gesamtanzahl der Datensätze teilen. Nach der Analyse ergibt sich ein Prozentsatz von 56.0%.",
            "question_type": "percentage",
            "expected": 56.0
        },
        {
            "response": "77295",
            "question_type": "automatic_count", 
            "expected": 77295.0
        },
        {
            "response": "67.4",
            "question_type": "automatic_percentage",
            "expected": 67.4
        },
        {
            "response": "2.11",
            "question_type": "ratio",
            "expected": 2.11
        }
    ]
    
    print("🧪 TESTING NUMBER EXTRACTION EXAMPLES")
    print("=" * 50)
    
    for i, case in enumerate(test_cases):
        print(f"\n📋 TEST CASE {i+1}")
        print(f"Expected: {case['expected']}")
        
        selected, all_numbers = analyze_number_extraction(
            case['response'], 
            case['question_type']
        )
        
        correct = abs(selected - case['expected']) < 0.01 if selected else False
        status = "✅ CORRECT" if correct else "❌ WRONG"
        print(f"{status}: Got {selected}, Expected {case['expected']}")

if __name__ == "__main__":
    print("🔧 NUMBER EXTRACTION DEBUG TOOL")
    print("Analyzing how numbers are extracted from LLM responses")
    
    test_extraction_examples()
    
    print(f"\n📝 RECOMMENDATIONS:")
    print("1. Use unified number extraction logic for all approaches")
    print("2. Improve context-aware number selection based on question type")
    print("3. Handle German number formats (comma as decimal separator)")
    print("4. Prioritize numbers based on expected ranges (percentages: 0-100, ratios: 0.1-10, counts: >1)")