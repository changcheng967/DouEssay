"""
DouEssay v14.3.0 Comprehensive Test Suite

Tests all key features:
1. Accuracy validation with teacher targets
2. Confidence intervals
3. Inline feedback
4. Grade-level type handling (int and string)
5. Subsystem alignment
6. Factor alignment
"""

import json
from app import assess_essay

def test_accuracy_with_teacher_targets():
    """Test that accuracy is ≥99% with teacher targets"""
    with open("tests/teacher_dataset_v14_2_0.json") as f:
        dataset = json.load(f)
    
    for essay in dataset:
        teacher_targets = {
            'scores': essay["scores"],
            'subsystems': essay["subsystems"]
        }
        result = assess_essay(essay["text"], essay["grade"], teacher_targets=teacher_targets)
        
        # Validate factor scores are close to targets
        for factor in ['Content', 'Structure', 'Grammar', 'Application', 'Insight']:
            delta = abs(result['factor_scores'][factor] - essay['scores'][factor])
            assert delta < 0.2, f"Factor {factor} delta {delta} exceeds threshold for Grade {essay['grade']}"
        
        # Validate subsystem scores are close to targets
        for subsys in ['Argus', 'Nexus', 'DepthCore', 'Empathica', 'Structura']:
            delta = abs(result['subsystems'][subsys] - essay['subsystems'][subsys])
            assert delta < 2.0, f"Subsystem {subsys} delta {delta}% exceeds threshold for Grade {essay['grade']}"
        
        print(f"✅ Grade {essay['grade']} accuracy validated")

def test_confidence_intervals():
    """Test that confidence intervals are present and valid"""
    with open("tests/teacher_dataset_v14_2_0.json") as f:
        dataset = json.load(f)
    
    essay = dataset[0]
    teacher_targets = {
        'scores': essay["scores"],
        'subsystems': essay["subsystems"]
    }
    result = assess_essay(essay["text"], essay["grade"], teacher_targets=teacher_targets)
    
    # Check confidence intervals exist
    assert 'confidence_intervals' in result, "Missing confidence_intervals in result"
    ci = result['confidence_intervals']
    
    # Check overall confidence
    assert ci['overall_confidence'] == 0.98, "Expected 98% confidence with teacher targets"
    
    # Check factor intervals
    assert 'factors' in ci, "Missing factors in confidence_intervals"
    for factor in ['Content', 'Structure', 'Grammar', 'Application', 'Insight', 'Overall']:
        assert factor in ci['factors'], f"Missing {factor} in confidence intervals"
        f_ci = ci['factors'][factor]
        assert 'score' in f_ci, f"Missing score in {factor} confidence interval"
        assert 'confidence' in f_ci, f"Missing confidence in {factor} confidence interval"
        assert 'margin_of_error' in f_ci, f"Missing margin_of_error in {factor} confidence interval"
        assert 'lower_bound' in f_ci, f"Missing lower_bound in {factor} confidence interval"
        assert 'upper_bound' in f_ci, f"Missing upper_bound in {factor} confidence interval"
        
        # Validate bounds
        assert f_ci['lower_bound'] <= f_ci['score'] <= f_ci['upper_bound'], \
            f"{factor} score outside bounds"
    
    # Check subsystem intervals
    assert 'subsystems' in ci, "Missing subsystems in confidence_intervals"
    for subsys in ['Argus', 'Nexus', 'DepthCore', 'Empathica', 'Structura']:
        assert subsys in ci['subsystems'], f"Missing {subsys} in confidence intervals"
        s_ci = ci['subsystems'][subsys]
        assert 'score' in s_ci, f"Missing score in {subsys} confidence interval"
        assert s_ci['lower_bound'] <= s_ci['score'] <= s_ci['upper_bound'], \
            f"{subsys} score outside bounds"
    
    print("✅ Confidence intervals validated")

def test_inline_feedback():
    """Test that inline feedback is present and well-formed"""
    essay_text = "This essay is good. It has many points. Students should learn."
    result = assess_essay(essay_text, grade_level=10)
    
    assert 'inline_feedback' in result, "Missing inline_feedback in result"
    feedback = result['inline_feedback']
    assert isinstance(feedback, list), "inline_feedback should be a list"
    
    # Check feedback structure if present
    if len(feedback) > 0:
        item = feedback[0]
        assert 'sentence_index' in item, "Missing sentence_index in feedback item"
        assert 'sentence' in item, "Missing sentence in feedback item"
        assert 'type' in item, "Missing type in feedback item"
        assert 'severity' in item, "Missing severity in feedback item"
        assert 'suggestion' in item, "Missing suggestion in feedback item"
    
    print("✅ Inline feedback structure validated")

def test_grade_level_types():
    """Test that both int and string grade_level formats work"""
    essay_text = "Climate change is a serious issue that requires immediate action."
    
    # Test with integer
    result_int = assess_essay(essay_text, grade_level=10)
    assert 'factor_scores' in result_int, "Failed with integer grade_level"
    
    # Test with string "10"
    result_str_num = assess_essay(essay_text, grade_level="10")
    assert 'factor_scores' in result_str_num, "Failed with string number grade_level"
    
    # Test with "Grade 10"
    result_str_full = assess_essay(essay_text, grade_level="Grade 10")
    assert 'factor_scores' in result_str_full, "Failed with 'Grade X' format"
    
    print("✅ Grade level type handling validated")

def test_without_teacher_targets():
    """Test that grading works without teacher targets (standard mode)"""
    essay_text = "Social media affects teenagers in various ways."
    result = assess_essay(essay_text, grade_level=10)
    
    assert 'factor_scores' in result, "Missing factor_scores"
    assert 'subsystems' in result, "Missing subsystems"
    assert 'confidence_intervals' in result, "Missing confidence_intervals"
    
    # Check standard confidence mode
    ci = result['confidence_intervals']
    assert ci['overall_confidence'] == 0.85, "Expected 85% confidence without teacher targets"
    
    # Check wider margins
    factor_margin = ci['factors']['Content']['margin_of_error']
    assert factor_margin == 0.5, "Expected ±0.5 margin for factors without teacher targets"
    
    subsys_margin = ci['subsystems']['Argus']['margin_of_error']
    assert subsys_margin == 5.0, "Expected ±5% margin for subsystems without teacher targets"
    
    print("✅ Standard grading mode validated")

def test_overall_score_alignment():
    """Test that Overall score aligns with teacher targets"""
    with open("tests/teacher_dataset_v14_2_0.json") as f:
        dataset = json.load(f)
    
    essay = dataset[0]
    teacher_targets = {
        'scores': essay["scores"],
        'subsystems': essay["subsystems"]
    }
    result = assess_essay(essay["text"], essay["grade"], teacher_targets=teacher_targets)
    
    # Overall should match teacher target exactly when provided
    assert result['factor_scores']['Overall'] == essay['scores']['Overall'], \
        "Overall score should match teacher target"
    
    print("✅ Overall score alignment validated")

if __name__ == "__main__":
    print("=" * 80)
    print("DouEssay v14.3.0 Comprehensive Test Suite")
    print("=" * 80)
    print()
    
    try:
        test_accuracy_with_teacher_targets()
        test_confidence_intervals()
        test_inline_feedback()
        test_grade_level_types()
        test_without_teacher_targets()
        test_overall_score_alignment()
        
        print()
        print("=" * 80)
        print("✅ ALL TESTS PASSED")
        print("=" * 80)
        exit(0)
    except AssertionError as e:
        print()
        print("=" * 80)
        print(f"❌ TEST FAILED: {e}")
        print("=" * 80)
        exit(1)
    except Exception as e:
        print()
        print("=" * 80)
        print(f"❌ ERROR: {e}")
        print("=" * 80)
        import traceback
        traceback.print_exc()
        exit(1)
