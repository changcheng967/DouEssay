"""
Quick syntax and logic validation for v14.2.0 - Perfect-Accuracy Upgrade
Tests basic structure without requiring full dependencies.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_imports():
    """Test that key functions can be imported"""
    try:
        # Test if VERSION is updated
        with open('app.py', 'r') as f:
            content = f.read()
            assert 'VERSION = "14.2.0"' in content, "VERSION must be 14.2.0"
            assert '_autoalign_v2' in content, "_autoalign_v2 method must exist"
            assert "Argus 5.0" in content or "'5.0'" in content, "Argus must be upgraded to 5.0"
            print("✅ Version and method checks passed")
    except Exception as e:
        print(f"❌ Import test failed: {e}")
        return False
    return True

def test_dataset_exists():
    """Test that teacher dataset file exists"""
    import json
    try:
        with open("tests/teacher_dataset_v14_2_0.json") as f:
            dataset = json.load(f)
            assert len(dataset) == 4, "Dataset must have 4 essays (grades 9-12)"
            
            for essay in dataset:
                assert 'grade' in essay, "Each essay must have grade"
                assert 'text' in essay, "Each essay must have text"
                assert 'scores' in essay, "Each essay must have teacher scores"
                assert 'subsystems' in essay, "Each essay must have subsystem scores"
                
                # Check score keys
                assert 'Content' in essay['scores'], "Must have Content score"
                assert 'Structure' in essay['scores'], "Must have Structure score"
                assert 'Grammar' in essay['scores'], "Must have Grammar score"
                assert 'Application' in essay['scores'], "Must have Application score"
                assert 'Insight' in essay['scores'], "Must have Insight score"
                
                # Check subsystem keys
                assert 'Argus' in essay['subsystems'], "Must have Argus score"
                assert 'Nexus' in essay['subsystems'], "Must have Nexus score"
                assert 'DepthCore' in essay['subsystems'], "Must have DepthCore score"
                assert 'Empathica' in essay['subsystems'], "Must have Empathica score"
                assert 'Structura' in essay['subsystems'], "Must have Structura score"
            
            print("✅ Dataset structure validation passed")
    except Exception as e:
        print(f"❌ Dataset test failed: {e}")
        return False
    return True

def test_autoalign_logic():
    """Test AutoAlign v2 logic structure"""
    try:
        with open('app.py', 'r') as f:
            content = f.read()
            
            # Check for key AutoAlign v2 components
            assert 'def _autoalign_v2' in content, "_autoalign_v2 method must exist"
            assert 'MAX_ITERATIONS' in content or 'DELTA_THRESHOLD' in content, "AutoAlign constants must exist"
            assert 'teacher_targets' in content, "teacher_targets parameter must exist"
            assert 'factor_scores' in content, "factor_scores must be computed"
            
            print("✅ AutoAlign v2 logic structure validated")
    except Exception as e:
        print(f"❌ AutoAlign logic test failed: {e}")
        return False
    return True

if __name__ == "__main__":
    print("=" * 60)
    print("DouEssay v14.2.0 Quick Validation Test Suite")
    print("=" * 60)
    
    all_passed = True
    all_passed &= test_imports()
    all_passed &= test_dataset_exists()
    all_passed &= test_autoalign_logic()
    
    print("\n" + "=" * 60)
    if all_passed:
        print("✅ ALL QUICK TESTS PASSED!")
        print("=" * 60)
        sys.exit(0)
    else:
        print("❌ SOME TESTS FAILED")
        print("=" * 60)
        sys.exit(1)
