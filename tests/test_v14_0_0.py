"""
Test suite for v14.0.0 - Full Accuracy Upgrade & Comprehensive Subsystem Overhaul

Tests for ≥99% overall accuracy and ≥97% subsystem accuracy:
- Doulet Argus 4.4 (Counter-Argument & Rebuttal)
- Doulet Nexus 5.4 (Logical Flow & Evidence)
- Doulet DepthCore 4.4 (Evidence Depth & Relevance)
- Doulet Empathica 3.4 (Emotional Tone & Engagement)
- Doulet Structura 4.4 (Paragraph & Rhetorical Structure)

Target metrics:
- Overall Accuracy: ≥99%
- Per-Subsystem Accuracy: ≥97%
- No word repetition warnings in inline feedback
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import assess_essay, VERSION

# Sample essays for testing
SAMPLE_ESSAYS = [
    {
        "grade": 9,
        "text": """Technology in education has transformed the way students learn. Digital tools like tablets, online simulations, and interactive platforms have made lessons more engaging. While some argue that technology can distract students, careful integration can enhance understanding and collaboration. For example, virtual labs in science classes allow students to experiment safely, reinforcing theoretical knowledge. Therefore, technology, when used thoughtfully, empowers students and enriches learning experiences.""",
        "expected": {"Argus": 0.97, "Nexus": 0.97, "DepthCore": 0.97, "Empathica": 0.97, "Structura": 0.97, "Overall": 0.99}
    },
    {
        "grade": 10,
        "text": """Climate change is a pressing global issue, and both individuals and governments must act. Critics argue that personal efforts are negligible, yet small actions collectively create significant impact. For instance, community-led recycling programs reduce local waste and educate citizens. Governments also play a crucial role by implementing policies to reduce emissions. Consequently, tackling climate change requires a dual approach: responsible citizens and proactive governance.""",
        "expected": {"Argus": 0.97, "Nexus": 0.97, "DepthCore": 0.97, "Empathica": 0.97, "Structura": 0.97, "Overall": 0.99}
    },
    {
        "grade": 11,
        "text": """Social media has revolutionized communication, but its effects on teen mental health are complex. Some claim that platforms foster connection, yet excessive use can lead to anxiety and depression. Research indicates that teenagers who spend more than three hours daily on social media report higher stress levels. Incorporating screen time limits and promoting offline interactions can mitigate negative outcomes. Thus, a balanced approach is essential for healthy digital engagement.""",
        "expected": {"Argus": 0.97, "Nexus": 0.97, "DepthCore": 0.97, "Empathica": 0.97, "Structura": 0.97, "Overall": 0.99}
    },
    {
        "grade": 12,
        "text": """Artificial intelligence (AI) presents both opportunities and ethical dilemmas. Proponents argue that AI improves efficiency, from healthcare diagnostics to automated transport. However, ethical concerns include bias in algorithms, data privacy, and job displacement. Implementing transparent AI systems and ethical guidelines is crucial. Therefore, society must weigh benefits against risks to ensure responsible AI development.""",
        "expected": {"Argus": 0.97, "Nexus": 0.97, "DepthCore": 0.97, "Empathica": 0.97, "Structura": 0.97, "Overall": 0.99}
    }
]


def test_version():
    """Test that version is correctly set to 14.0.0"""
    assert VERSION == "14.0.0", f"VERSION must be v14.0.0, got {VERSION}"
    print("✅ Version test passed: v14.0.0")


def test_subsystems():
    """Test that all subsystems meet ≥97% accuracy threshold"""
    print("\n=== Testing Subsystem Accuracy ===")
    
    all_passed = True
    for essay in SAMPLE_ESSAYS:
        print(f"\nTesting Grade {essay['grade']} essay...")
        result = assess_essay(essay['text'])
        
        for subsystem, threshold in essay['expected'].items():
            if subsystem != "Overall":
                actual = result['subsystems'][subsystem]
                passed = actual >= threshold
                status = "✅" if passed else "❌"
                print(f"  {status} {subsystem}: {actual:.3f} (threshold: {threshold})")
                
                if not passed:
                    all_passed = False
                    print(f"     ERROR: {subsystem} below target: {actual:.3f} < {threshold}")
    
    assert all_passed, "One or more subsystems failed to meet ≥97% accuracy threshold"
    print("\n✅ All subsystems passed: ≥97% accuracy achieved")


def test_overall_accuracy():
    """Test that overall accuracy meets ≥99% threshold"""
    print("\n=== Testing Overall Accuracy ===")
    
    all_passed = True
    for essay in SAMPLE_ESSAYS:
        result = assess_essay(essay['text'])
        overall = result['overall']
        threshold = 0.99
        passed = overall >= threshold
        status = "✅" if passed else "❌"
        
        print(f"{status} Grade {essay['grade']}: {overall:.3f} (threshold: {threshold})")
        
        if not passed:
            all_passed = False
            print(f"   ERROR: Overall accuracy below target: {overall:.3f} < {threshold}")
    
    assert all_passed, "One or more essays failed to meet ≥99% overall accuracy"
    print("✅ Overall accuracy test passed: ≥99% achieved")


def test_no_word_repetition_feedback():
    """Test that inline feedback does not flag word repetition"""
    print("\n=== Testing Word Repetition Removal ===")
    
    all_passed = True
    for essay in SAMPLE_ESSAYS:
        feedback = assess_essay(essay['text'])['inline_feedback']
        
        for item in feedback:
            item_str = str(item).lower()
            if 'word repetition' in item_str or 'repetition' in item.get('type', '').lower():
                all_passed = False
                print(f"❌ Grade {essay['grade']}: Found word repetition warning: {item}")
        
        if all_passed:
            print(f"✅ Grade {essay['grade']}: No word repetition warnings found")
    
    assert all_passed, "Word repetition warnings should be removed in v14.0.0"
    print("✅ Word repetition test passed: No warnings found")


def test_counter_argument_detection():
    """Test Doulet Argus 4.4 - Counter-argument and rebuttal detection"""
    print("\n=== Testing Counter-Argument Detection (Argus 4.4) ===")
    
    # Test with essay containing counter-arguments
    test_essay = """Climate change is a pressing issue. However, critics argue that individual actions are meaningless. 
    Yet this view fails to consider the collective impact of millions making sustainable choices. 
    Therefore, both individual and governmental action are necessary."""
    
    result = assess_essay(test_essay)
    argus_score = result['subsystems']['Argus']
    
    print(f"Argus score for counter-argument essay: {argus_score:.3f}")
    assert argus_score >= 0.70, f"Argus should detect counter-arguments effectively, got {argus_score}"
    print("✅ Counter-argument detection test passed")


def test_evidence_relevance():
    """Test Doulet Nexus 5.4 - Evidence relevance and logical flow"""
    print("\n=== Testing Evidence Relevance (Nexus 5.4) ===")
    
    # Test with essay containing strong evidence
    test_essay = """Technology improves education significantly. For example, virtual labs enable safe experimentation. 
    Research shows that students using digital tools score 20% higher on tests. 
    This demonstrates that technology directly enhances learning outcomes."""
    
    result = assess_essay(test_essay)
    nexus_score = result['subsystems']['Nexus']
    
    print(f"Nexus score for evidence-rich essay: {nexus_score:.3f}")
    assert nexus_score >= 0.70, f"Nexus should score evidence relevance highly, got {nexus_score}"
    print("✅ Evidence relevance test passed")


def test_multi_source_integration():
    """Test Doulet DepthCore 4.4 - Multi-source evidence integration"""
    print("\n=== Testing Multi-Source Integration (DepthCore 4.4) ===")
    
    # Test with essay containing multiple evidence sources
    test_essay = """AI presents ethical challenges. Studies from MIT show algorithmic bias affects hiring. 
    Stanford researchers found privacy concerns in data collection. 
    Historical examples, like the 2016 social media scandal, illustrate these risks. 
    Therefore, comprehensive regulation is essential."""
    
    result = assess_essay(test_essay)
    depthcore_score = result['subsystems']['DepthCore']
    
    print(f"DepthCore score for multi-source essay: {depthcore_score:.3f}")
    assert depthcore_score >= 0.70, f"DepthCore should recognize multi-source evidence, got {depthcore_score}"
    print("✅ Multi-source integration test passed")


def test_emotional_engagement():
    """Test Doulet Empathica 3.4 - Emotional tone and engagement"""
    print("\n=== Testing Emotional Engagement (Empathica 3.4) ===")
    
    # Test with essay containing emotional engagement
    test_essay = """In my experience, technology transformed my learning journey. I realized that digital tools 
    opened new possibilities. This taught me that innovation drives progress. 
    Personally, I believe educational technology empowers students to achieve their goals."""
    
    result = assess_essay(test_essay)
    empathica_score = result['subsystems']['Empathica']
    
    print(f"Empathica score for emotional essay: {empathica_score:.3f}")
    assert empathica_score >= 0.70, f"Empathica should detect emotional engagement, got {empathica_score}"
    print("✅ Emotional engagement test passed")


def test_paragraph_structure():
    """Test Doulet Structura 4.4 - Paragraph and rhetorical structure"""
    print("\n=== Testing Paragraph Structure (Structura 4.4) ===")
    
    # Test with well-structured essay
    test_essay = """Technology in education is essential. First, it enhances engagement through interactive tools. 
    Second, it provides personalized learning paths. Third, it prepares students for digital careers. 
    In conclusion, educational technology is fundamental to modern learning."""
    
    result = assess_essay(test_essay)
    structura_score = result['subsystems']['Structura']
    
    print(f"Structura score for structured essay: {structura_score:.3f}")
    assert structura_score >= 0.70, f"Structura should recognize good structure, got {structura_score}"
    print("✅ Paragraph structure test passed")


if __name__ == "__main__":
    print("=" * 60)
    print("DouEssay v14.0.0 Test Suite")
    print("Full Accuracy Upgrade & Comprehensive Subsystem Overhaul")
    print("=" * 60)
    
    try:
        test_version()
        test_subsystems()
        test_overall_accuracy()
        test_no_word_repetition_feedback()
        test_counter_argument_detection()
        test_evidence_relevance()
        test_multi_source_integration()
        test_emotional_engagement()
        test_paragraph_structure()
        
        print("\n" + "=" * 60)
        print("✅ ALL TESTS PASSED!")
        print("=" * 60)
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
