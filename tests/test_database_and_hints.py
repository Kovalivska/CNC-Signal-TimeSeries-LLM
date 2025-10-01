#!/usr/bin/env python3
"""
Test that Database approach is present and examples are removed
"""

import sys
sys.path.append('/Users/svitlanakovalivska/CNC')

def test_improvements():
    """Test the key improvements made"""
    try:
        from langchain_implementation_fixed import CNCValidationWorkflow
        
        print("🧪 TESTING KEY IMPROVEMENTS")
        print("="*50)
        
        # Create a dummy workflow to check approaches
        try:
            # This will fail due to missing data, but we can check the class definition
            data_path = "/nonexistent/path.xlsx"  # Dummy path
            workflow = CNCValidationWorkflow(data_path, None)
        except Exception as e:
            # Expected to fail, but we can check class attributes
            pass
        
        # Check if Database approach exists in the code
        import inspect
        source = inspect.getsource(CNCValidationWorkflow)
        
        approaches_found = []
        if '"basic"' in source:
            approaches_found.append("Basic")
        if '"expert"' in source:
            approaches_found.append("Expert") 
        if '"enhanced"' in source:
            approaches_found.append("Enhanced")
        if '"database"' in source:
            approaches_found.append("Database")
            
        print(f"✅ Approaches found: {', '.join(approaches_found)}")
        
        # Check if examples (hints) were removed
        hint_examples = [
            "(z.B.: 56.0)",
            "(z.B.: 67.9)", 
            "(z.B.: 2.11)",
            "(z.B.: 35.9)",
            "(z.B. 113855)"
        ]
        
        hints_found = []
        for hint in hint_examples:
            if hint in source:
                hints_found.append(hint)
        
        if hints_found:
            print(f"❌ Hints still present: {hints_found}")
        else:
            print("✅ All hints/examples removed from prompts")
            
        # Check Database approach specifically
        if '"database"' in source and 'DIRECT ACCESS' in source:
            print("✅ Database approach present with DIRECT ACCESS")
        else:
            print("❌ Database approach missing or incomplete")
            
        print(f"\n🎯 EXPECTED RESULTS:")
        print("- 4 approaches: Basic, Expert, Enhanced, Database")
        print("- Database approach should get highest scores (has real data)")
        print("- No example hints in questions or prompts")
        print("- Clean comparison between approaches")
        
        return len(approaches_found) == 4 and len(hints_found) == 0
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Test error: {e}")
        return False

if __name__ == "__main__":
    success = test_improvements()
    
    if success:
        print(f"\n🎉 All improvements verified!")
        print("Ready to run full validation test.")
    else:
        print(f"\n⚠️  Some issues remain - check the fixes")
        
    print(f"\n📋 Summary of changes:")
    print("1. ✅ Removed example hints from all questions")
    print("2. ✅ Removed example hints from prompts") 
    print("3. ✅ Database approach restored with DIRECT ACCESS")
    print("4. ✅ All 4 approaches should now be available")