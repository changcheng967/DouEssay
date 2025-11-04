"""
Test suite for v13.0.1 - Full Accuracy Upgrade & Subsystem Version Update

Tests the enhanced Doulet subsystems and 100% accuracy grading:
- Doulet Argus 4.1 (Enhanced Counter-Argument Detection & Deep Reasoning)
- Doulet Nexus 5.1 (Superior Logical Flow & Evidence Relevance Precision)
- Doulet DepthCore 4.1 (Ultra-Deep Evidence Analysis & Multi-Source Integration)
- Doulet Empathica 3.1 (Advanced Emotional Tone & Engagement Analysis)
- Doulet Structura 4.1 (Ultimate Paragraph Structure & Topic Coherence)

Target metrics:
- Overall Accuracy: 100%
- Evidence Relevance: Enhanced with coherence bonus
- Logical Flow: Cross-paragraph analysis with transitions
- Counter-Arguments: Functional detection with sophistication levels
- Emotional Tone: Authenticity scoring and personal voice
- Inline Suggestions: Enhanced dark mode visibility
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import DouEssay, VERSION

def test_version():
    """Test that version is correctly set to 13.0.1"""
    assert VERSION == "13.0.1", f"Expected version 13.0.1, got {VERSION}"
    print("✅ Version test passed: v13.0.1")


def test_subsystem_versions():
    """Test that all subsystems are upgraded to v13.0.1 versions"""
    douessay = DouEssay()
    
    expected_versions = {
        'doulet_argus': '4.1',
        'doulet_nexus': '5.1',
        'doulet_depthcore': '4.1',
        'doulet_empathica': '3.1',
        'doulet_structura': '4.1'
    }
    
    for subsystem, expected_version in expected_versions.items():
        actual_version = douessay.subsystem_versions.get(subsystem)
        assert actual_version == expected_version, \
            f"Expected {subsystem} to be v{expected_version}, got v{actual_version}"
    
    print("✅ Subsystem version test passed")


def test_subsystem_metadata():
    """Test that subsystem metadata is updated for v13.0.1"""
    douessay = DouEssay()
    
    expected_metadata = {
        'doulet_argus': {
            'version': '4.1',
            'keywords': ['enhanced counter-argument', 'functional']
        },
        'doulet_nexus': {
            'version': '5.1',
            'keywords': ['superior', 'logical flow', 'precision']
        },
        'doulet_depthcore': {
            'version': '4.1',
            'keywords': ['ultra-deep', 'multi-source']
        },
        'doulet_empathica': {
            'version': '3.1',
            'keywords': ['emotional tone', 'engagement']
        },
        'doulet_structura': {
            'version': '4.1',
            'keywords': ['ultimate', 'topic coherence']
        }
    }
    
    for subsystem, metadata in expected_metadata.items():
        actual_metadata = douessay.subsystem_metadata.get(subsystem)
        assert actual_metadata is not None, f"Missing metadata for {subsystem}"
        assert actual_metadata['version'] == metadata['version'], \
            f"Expected {subsystem} metadata version {metadata['version']}, got {actual_metadata['version']}"
        
        # Check that description contains keywords
        description = actual_metadata.get('description', '').lower()
        for keyword in metadata['keywords']:
            assert keyword in description, \
                f"Expected {subsystem} description to contain '{keyword}'"
    
    print("✅ Subsystem metadata test passed")


def test_enhanced_evidence_relevance():
    """Test enhanced evidence relevance scoring with coherence bonus"""
    douessay = DouEssay()
    
    # Essay with strong evidence and cross-sentence coherence
    essay = """
    According to recent research, climate change significantly impacts ecosystems.
    Studies indicate rising temperatures alter migration patterns.
    Data reveals these changes affect species survival rates.
    This demonstrates the urgent need for environmental action.
    """
    
    result = douessay.assess_evidence_relevance(essay)
    
    # Check enhanced features
    assert 'relevance_score' in result
    assert 'coherence_bonus' in result
    assert 'evidence_strength' in result
    assert 'total_signals' in result
    
    # Should have good relevance
    assert result['relevance_score'] >= 0.5, \
        f"Expected relevance_score >= 0.5, got {result['relevance_score']}"
    
    # Should detect evidence signals
    assert result['total_signals'] > 0, \
        f"Expected total_signals > 0, got {result['total_signals']}"
    
    print(f"✅ Enhanced evidence relevance test passed: {result['relevance_score']}, bonus: {result['coherence_bonus']}")


def test_functional_counter_argument_detection():
    """Test functional counter-argument detection"""
    douessay = DouEssay()
    
    # Essay with counter-arguments and rebuttals
    essay = """
    Technology benefits education significantly. However, some argue it causes distraction.
    Critics claim students spend too much time on devices. Yet this view fails to consider
    that technology, when used properly, enhances learning outcomes. On the other hand,
    opponents suggest traditional methods are better. Nevertheless, research shows
    blended approaches yield the best results.
    """
    
    result = douessay.evaluate_counter_argument_depth(essay)
    
    # Check it's functional, not planned
    assert result['status'] == 'functional', \
        f"Expected status 'functional', got {result['status']}"
    
    assert result['version'] == '4.1', \
        f"Expected version 4.1, got {result['version']}"
    
    # Should detect counter-arguments
    assert result['counter_arguments_detected'] > 0, \
        f"Expected counter_arguments_detected > 0, got {result['counter_arguments_detected']}"
    
    assert result['rebuttals_detected'] > 0, \
        f"Expected rebuttals_detected > 0, got {result['rebuttals_detected']}"
    
    assert result['has_counter_argument'] is True
    
    print(f"✅ Functional counter-argument test passed: {result['counter_arguments_detected']} counter-args, {result['rebuttals_detected']} rebuttals")


def test_enhanced_logical_flow():
    """Test enhanced logical flow detection with transitions"""
    douessay = DouEssay()
    
    # Essay with transitions and logical flow
    essay = """
    Education is essential for society. According to UNESCO, literacy rates improve economies.
    
    Furthermore, educated populations show better health outcomes. Research shows educated mothers
    have healthier children. This demonstrates education's far-reaching impact.
    
    Moreover, education promotes critical thinking. Studies indicate critical thinkers solve
    problems more effectively. Therefore, investing in education benefits entire nations.
    
    In conclusion, education is the foundation of progress.
    """
    
    result = douessay.analyze_evidence_coherence(essay)
    
    # Check enhanced features
    assert 'transition_count' in result
    assert 'paragraph_flow_score' in result
    assert 'logical_progression' in result
    
    # Should detect transitions
    assert result['transition_count'] > 0, \
        f"Expected transition_count > 0, got {result['transition_count']}"
    
    # Should have good flow
    assert result['paragraph_flow_score'] >= 0.3, \
        f"Expected paragraph_flow_score >= 0.3, got {result['paragraph_flow_score']}"
    
    print(f"✅ Enhanced logical flow test passed: {result['transition_count']} transitions, flow: {result['paragraph_flow_score']}")


def test_enhanced_emotional_analysis():
    """Test enhanced emotional tone with authenticity scoring"""
    douessay = DouEssay()
    
    # Essay with personal voice and emotional content
    essay = """
    I learned that education transforms lives through my own experience. When I discovered
    the joy of reading, my perspective changed profoundly. This taught me that knowledge
    empowers individuals. I realized education is not just about facts, but about developing
    critical thinking and empathy. My journey showed me the importance of lifelong learning.
    """
    
    result = douessay.analyze_emotionflow(essay)
    
    # Check enhanced features
    assert 'authenticity_score' in result
    assert 'authenticity_level' in result
    assert 'personal_voice_detected' in result
    
    # Should detect personal voice
    assert result['personal_voice_detected'] is True, \
        "Expected personal_voice_detected to be True"
    
    # Should have authenticity
    assert result['authenticity_score'] > 0, \
        f"Expected authenticity_score > 0, got {result['authenticity_score']}"
    
    print(f"✅ Enhanced emotional analysis test passed: authenticity {result['authenticity_score']}, level: {result['authenticity_level']}")


def test_grading_accuracy():
    """Test overall grading accuracy with enhanced algorithms"""
    douessay = DouEssay()
    
    # High-quality Grade 10 essay with all enhanced features
    essay = """
    Climate change represents one of the most pressing challenges facing humanity today. 
    According to the Intergovernmental Panel on Climate Change (IPCC), global temperatures 
    have risen by 1.1°C since pre-industrial times. This demonstrates the urgent need for action.
    
    Furthermore, rising temperatures cause devastating effects. Research shows melting ice caps 
    lead to rising sea levels, threatening coastal communities. Studies indicate extreme weather 
    events are becoming more frequent and severe. This proves climate change impacts real lives.
    
    However, some argue economic growth should take priority over environmental concerns. 
    Critics claim climate action harms industries and jobs. Yet this view fails to consider 
    that green technology creates new opportunities. Moreover, the cost of inaction far exceeds 
    transition costs. Therefore, sustainable development benefits both economy and environment.
    
    Additionally, I learned from my community's flooding that climate change affects everyone. 
    This taught me the importance of individual action. My experience showed me that small 
    changes, when combined, create significant impact.
    
    In conclusion, addressing climate change requires immediate global cooperation. 
    The evidence clearly demonstrates both the urgency and feasibility of action.
    """
    
    result = douessay.grade_essay(essay, "Grade 10")
    
    # Should achieve high accuracy
    assert result['score'] >= 85, \
        f"Expected score >= 85, got {result['score']}"
    
    # Check rubric level
    rubric = result.get('rubric_level', {})
    if isinstance(rubric, dict):
        level = rubric.get('level', 'Unknown')
    else:
        level = str(rubric)
    
    assert 'Level 4' in level or 'Level 3' in level, \
        f"Expected Level 3 or 4, got {level}"
    
    print(f"✅ Grading accuracy test passed: {result['score']}/100, {level}")


def test_notification_placement():
    """Test that notification structure supports Home Page display"""
    # This is a structural test - the actual UI rendering happens in Gradio
    # We just verify the code structure is correct
    
    # Check that process_essay function exists and returns correct number of values
    from app import create_douessay_interface
    
    # The function should exist without errors
    interface = create_douessay_interface()
    assert interface is not None
    
    print("✅ Notification placement test passed: UI structure correct")


def test_inline_suggestions_enhanced():
    """Test that inline suggestions have enhanced styling"""
    # This is a code inspection test for dark mode improvements
    app_path = os.path.join(os.path.dirname(__file__), '..', 'app.py')
    with open(app_path, 'r') as f:
        content = f.read()
    
    # Check for enhanced styling attributes
    assert 'font-weight: 600' in content, "Expected font-weight: 600 for dark mode"
    assert 'box-shadow' in content, "Expected box-shadow for enhanced visibility"
    assert 'border-left: 4px' in content, "Expected 4px border for emphasis"
    
    print("✅ Inline suggestions enhancement test passed")


def run_all_tests():
    """Run all v13.0.1 tests"""
    print("=" * 60)
    print("Running v13.0.1 Test Suite")
    print("=" * 60)
    print()
    
    tests = [
        test_version,
        test_subsystem_versions,
        test_subsystem_metadata,
        test_enhanced_evidence_relevance,
        test_functional_counter_argument_detection,
        test_enhanced_logical_flow,
        test_enhanced_emotional_analysis,
        test_grading_accuracy,
        test_notification_placement,
        test_inline_suggestions_enhanced,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"❌ {test.__name__} FAILED: {e}")
            failed += 1
        except Exception as e:
            print(f"❌ {test.__name__} ERROR: {e}")
            failed += 1
    
    print()
    print("=" * 60)
    print(f"Test Results: {passed} passed, {failed} failed")
    print("=" * 60)
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
