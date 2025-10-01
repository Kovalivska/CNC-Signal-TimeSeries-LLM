#!/usr/bin/env python3
"""
Test to verify Database approach does NOT get real answers
"""

import sys
sys.path.append('/Users/svitlanakovalivska/CNC')

def test_database_fairness():
    """Test that Database approach doesn't get unfair advantages"""
    
    print("🧪 TESTING DATABASE APPROACH FAIRNESS")
    print("="*60)
    
    try:
        # Read the source code to check for cheating
        with open('/Users/svitlanakovalivska/CNC/langchain_implementation_fixed.py', 'r') as f:
            source_code = f.read()
        
        # Check for problematic patterns that give away answers
        cheating_patterns = [
            "prog_count:,} occurrences",  # Giving exact program count
            "records ({auto_pct:.1f}%)",  # Giving exact percentages  
            "Auto/Manual ratio: {ratio:.2f}",  # Giving exact ratio
            "ACTIVE status: {active_count:,} records",  # Giving exact active count
            "DIREKTEN Zugang zu diesen EXAKTEN Werten",  # Direct access claim
            "exakte Zahl aus der Datenbank",  # Exact values from database
            "ACTUAL values from the data",  # Actual values claim
        ]
        
        cheating_found = []
        for pattern in cheating_patterns:
            if pattern in source_code:
                cheating_found.append(pattern)
        
        print("🔍 Checking for unfair advantages in Database approach...")
        
        if cheating_found:
            print(f"❌ UNFAIR PATTERNS FOUND:")
            for pattern in cheating_found:
                print(f"   - {pattern}")
        else:
            print("✅ No unfair patterns found")
        
        # Check what information Database approach gets
        database_section_start = source_code.find('elif approach == "database":')
        if database_section_start != -1:
            database_section_end = source_code.find('else:', database_section_start)
            if database_section_end == -1:
                database_section_end = database_section_start + 2000
            
            database_code = source_code[database_section_start:database_section_end]
            
            print(f"\n📋 Database approach gets access to:")
            
            # What's allowed (fair)
            fair_access = [
                "total_records",  # Just the count, not answers
                "columns",  # Column names are fair
                "Column types",  # Schema info is fair
            ]
            
            # What's not allowed (unfair)
            unfair_access = [
                "prog_count",  # Exact program counts
                "auto_pct",   # Exact percentages
                "manual_pct", # Exact percentages
                "ratio",      # Exact ratios
                "active_count", # Exact active counts
            ]
            
            fair_found = [item for item in fair_access if item in database_code]
            unfair_found = [item for item in unfair_access if item in database_code]
            
            if fair_found:
                print(f"✅ Fair access: {fair_found}")
            if unfair_found:
                print(f"❌ Unfair access: {unfair_found}")
            else:
                print("✅ No unfair data access found")
        
        # Overall assessment
        is_fair = len(cheating_found) == 0 and len(unfair_found) == 0
        
        print(f"\n🎯 ASSESSMENT:")
        if is_fair:
            print("✅ Database approach is FAIR - no pre-given answers")
            print("✅ All approaches now compete on equal terms")
            print("✅ Database approach relies on analytical reasoning, not lookup")
        else:
            print("❌ Database approach has UNFAIR advantages")
            print("❌ It gets real answers that other approaches don't have")
            print("❌ This makes comparison invalid")
        
        print(f"\n📊 Expected results with fair testing:")
        print("- BASIC: Lowest performance (simple prompt)")
        print("- EXPERT: Better (structured prompt)")  
        print("- ENHANCED: Best reasoning (optimized prompt)")
        print("- DATABASE: Varies (depends on LLM's analytical abilities)")
        print("\n💡 Now all approaches test prompt engineering fairly!")
        
        return is_fair
        
    except Exception as e:
        print(f"❌ Test error: {e}")
        return False

if __name__ == "__main__":
    is_fair = test_database_fairness()
    
    if is_fair:
        print(f"\n🎉 Database approach is now FAIR!")
        print("Ready to run honest comparison test.")
    else:
        print(f"\n⚠️  Database approach still has unfair advantages")
        print("Need to remove pre-given answers.")
    
    print(f"\n🔧 Key principle:")
    print("All approaches should rely on LLM reasoning, not pre-given data!")
    print("Database approach = better analytical prompting, not data lookup")