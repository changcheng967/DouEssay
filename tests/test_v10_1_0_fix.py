#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

"""
Test script for v10.1.0 hotfix
Tests the TypeError fix and schema validation
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

# Import the helper functions from app.py
from app import extract_rubric_level, normalize_grading_result, get_level_description

def test_extract_rubric_level():
    """Test extract_rubric_level with various inputs"""
    print("Testing extract_rubric_level()...")
    
    # Test 1: Dict with level and description (v8.0.0 format)
    result1 = {
        'rubric_level': {
            'level': 'Level 3',
            'description': 'Good - Meets Standards'
        },
        'score': 75
    }
    extracted1 = extract_rubric_level(result1)
    assert extracted1['level'] == 'Level 3', f"Test 1 failed: {extracted1}"
    assert extracted1['description'] == 'Good - Meets Standards', f"Test 1 failed: {extracted1}"
    print("✓ Test 1: Dict format passed")
    
    # Test 2: String format (v9.0.0 format - this was causing the bug!)
    result2 = {
        'rubric_level': 'Level 3',
        'score': 75
    }
    extracted2 = extract_rubric_level(result2)
    assert extracted2['level'] == 'Level 3', f"Test 2 failed: {extracted2}"
    assert 'Good' in extracted2['description'], f"Test 2 failed: {extracted2}"
    print("✓ Test 2: String format passed (BUG FIX VERIFIED)")
    
    # Test 3: JSON-stringified dict
    import json
    result3 = {
        'rubric_level': json.dumps({'level': 'Level 4', 'description': 'Excellent'}),
        'score': 85
    }
    extracted3 = extract_rubric_level(result3)
    assert extracted3['level'] == 'Level 4', f"Test 3 failed: {extracted3}"
    print("✓ Test 3: JSON string format passed")
    
    # Test 4: Missing rubric_level (edge case)
    result4 = {
        'score': 70
    }
    extracted4 = extract_rubric_level(result4)
    assert extracted4['level'] == 'Unknown', f"Test 4 failed: {extracted4}"
    print("✓ Test 4: Missing rubric_level passed")
    
    # Test 5: Invalid input type (should not crash!)
    result5 = "not a dict"
    extracted5 = extract_rubric_level(result5)
    assert extracted5['level'] == 'Unknown', f"Test 5 failed: {extracted5}"
    print("✓ Test 5: Invalid type handled gracefully")
    
    print("✓ All extract_rubric_level tests passed!\n")

def test_normalize_grading_result():
    """Test normalize_grading_result with various inputs"""
    print("Testing normalize_grading_result()...")
    
    # Test 1: Result with string rubric_level (v9.0.0 - the bug scenario)
    raw_result1 = {
        'score': 75,
        'rubric_level': 'Level 3',
        'feedback': ['Good work'],
        'corrections': [],
        'inline_feedback': []
    }
    normalized1 = normalize_grading_result(raw_result1)
    assert isinstance(normalized1['rubric_level'], dict), "Test 1 failed: rubric_level should be dict"
    assert normalized1['rubric_level']['level'] == 'Level 3', f"Test 1 failed: {normalized1}"
    print("✓ Test 1: String rubric_level normalized")
    
    # Test 2: Result with dict rubric_level (v8.0.0)
    raw_result2 = {
        'score': 85,
        'rubric_level': {'level': 'Level 4', 'description': 'Excellent'},
        'feedback': ['Great!'],
        'corrections': [],
        'inline_feedback': []
    }
    normalized2 = normalize_grading_result(raw_result2)
    assert normalized2['rubric_level']['level'] == 'Level 4', f"Test 2 failed: {normalized2}"
    print("✓ Test 2: Dict rubric_level preserved")
    
    # Test 3: Invalid input (should not crash!)
    raw_result3 = "not a dict"
    normalized3 = normalize_grading_result(raw_result3)
    assert isinstance(normalized3, dict), "Test 3 failed: should return dict"
    assert 'rubric_level' in normalized3, "Test 3 failed: missing rubric_level"
    print("✓ Test 3: Invalid input handled gracefully")
    
    print("✓ All normalize_grading_result tests passed!\n")

def test_get_level_description():
    """Test get_level_description function"""
    print("Testing get_level_description()...")
    
    assert 'Exceeds' in get_level_description('Level 4'), "Level 4 description failed"
    assert 'Meets' in get_level_description('Level 3'), "Level 3 description failed"
    assert 'Approaching' in get_level_description('Level 2+'), "Level 2+ description failed"
    assert 'in progress' in get_level_description('Unknown'), "Unknown description failed"
    
    print("✓ All get_level_description tests passed!\n")

def test_bug_scenario():
    """Test the exact bug scenario that was reported"""
    print("Testing the exact bug scenario from issue report...")
    
    # This is what was causing: TypeError: string indices must be integers
    # result['rubric_level']['level'] when rubric_level was a string
    
    result = {
        'score': 75.5,
        'rubric_level': 'Level 3',  # This was a string in v9.0.0!
        'feedback': ['Good work'],
        'corrections': [],
        'inline_feedback': [],
        'neural_rubric': {},
        'emotionflow': {},
        'detailed_analysis': {}
    }
    
    # This is what save_draft() used to do (would crash):
    # level = result['rubric_level']['level']  # TypeError!
    
    # This is what it does now (safe):
    rubric = extract_rubric_level(result)
    level = rubric['level']
    
    assert level == 'Level 3', f"Bug scenario failed: {level}"
    print("✓ Bug scenario test passed - No TypeError!")
    print("  - Old code would crash with: TypeError: string indices must be integers")
    print("  - New code handles it gracefully\n")

if __name__ == '__main__':
    print("=" * 60)
    print("DouEssay v10.1.0 Hotfix Test Suite")
    print("Testing TypeError fix and schema validation")
    print("=" * 60)
    print()
    
    try:
        test_extract_rubric_level()
        test_normalize_grading_result()
        test_get_level_description()
        test_bug_scenario()
        
        print("=" * 60)
        print("✅ ALL TESTS PASSED!")
        print("=" * 60)
        print()
        print("The v10.1.0 hotfix successfully prevents the TypeError and")
        print("implements robust schema validation and error handling.")
        sys.exit(0)
    except AssertionError as e:
        print()
        print("=" * 60)
        print("❌ TEST FAILED!")
        print("=" * 60)
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        print()
        print("=" * 60)
        print("❌ UNEXPECTED ERROR!")
        print("=" * 60)
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
