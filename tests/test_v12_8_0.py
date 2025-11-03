"""
Test suite for v12.8.0 - Extreme Accuracy Grading & AI-Powered Core Engine

Tests the upgraded Doulet subsystems and improved grading accuracy:
- Doulet Argus 3.0 (AI-powered argument logic)
- Doulet Nexus 4.0 (semantic flow mapping)
- Doulet DepthCore 3.0 (multi-layered evidence)
- Doulet Empathica 2.0 (emotion & engagement AI)
- Doulet Structura 3.0 (advanced structure validation)

Target metrics:
- Overall Accuracy: ≥95%
- Argument Strength: ≥75%
- Logical Flow: ≥85%
- Evidence Relevance: ≥90%
- Emotional Engagement: ≥70%
- Claim-Evidence Ratio: ≥2.0
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import DouEssay

def test_version():
    """Test that version is correctly set to 12.8.0"""
    from app import VERSION
    assert VERSION == "12.8.0", f"Expected version 12.8.0, got {VERSION}"
    print("✅ Version test passed: v12.8.0")


def test_subsystem_versions():
    """Test that all subsystems are upgraded to correct versions"""
    douessay = DouEssay()
    
    expected_versions = {
        'doulet_argus': '3.0',
        'doulet_nexus': '4.0',
        'doulet_depthcore': '3.0',
        'doulet_empathica': '2.0',
        'doulet_structura': '3.0'
    }
    
    for subsystem, expected_version in expected_versions.items():
        actual_version = douessay.subsystem_versions.get(subsystem)
        assert actual_version == expected_version, \
            f"Expected {subsystem} to be v{expected_version}, got v{actual_version}"
    
    print("✅ Subsystem version test passed")


def test_grade_9_level_4_essay():
    """Test grading of a Grade 9 Level 4+ essay with strong arguments and evidence"""
    douessay = DouEssay()
    
    # Sample Grade 9 Level 4+ argumentative essay with strong evidence
    essay = """
    Technology in Education: A Path to Enhanced Learning
    
    Technology has fundamentally transformed how students learn and engage with educational content. 
    I argue that integrating technology into classrooms is essential for preparing students for the 
    modern world. This essay will demonstrate how technology enhances learning outcomes, fosters 
    engagement, and develops critical 21st-century skills.
    
    First and foremost, research shows that technology significantly improves student learning outcomes. 
    For example, a 2023 study by the Ontario Ministry of Education found that students using digital 
    learning platforms scored 15% higher on standardized tests compared to those in traditional classrooms. 
    This demonstrates that technology provides students with personalized learning experiences that adapt 
    to their individual needs. Furthermore, interactive educational software enables students to learn 
    at their own pace, which is particularly beneficial for those who need extra support or advanced 
    challenges.
    
    Moreover, technology fosters deeper student engagement and motivation. Specifically, when students 
    use tablets and educational apps, they show increased enthusiasm for learning complex subjects like 
    mathematics and science. According to recent data from the Toronto District School Board, classroom 
    attendance improved by 12% in schools that implemented one-to-one device programs. This indicates 
    that technology makes learning more interactive and relevant to students' lives. Additionally, 
    digital tools enable collaborative projects where students work together across different locations, 
    developing crucial teamwork skills.
    
    Most importantly, technology prepares students for future careers and real-world challenges. In my 
    experience volunteering at a local technology center, I observed how students gained confidence 
    using professional software tools. The modern workplace increasingly demands technological literacy, 
    and schools must provide these essential skills. For instance, coding, digital communication, and 
    data analysis are now fundamental competencies across virtually all career paths. Therefore, 
    integrating technology into education directly supports students' long-term success and employability.
    
    Some critics argue that excessive screen time harms students' social development and physical health. 
    However, this concern can be addressed through balanced implementation and structured guidelines. 
    Schools can establish clear technology usage policies that include regular breaks, outdoor activities, 
    and face-to-face interaction time. Research from educational psychologists suggests that when 
    technology is thoughtfully integrated rather than simply added on, it actually enhances rather than 
    replaces traditional learning methods.
    
    In conclusion, technology represents a crucial tool for modern education when implemented 
    thoughtfully and strategically. The evidence clearly shows that digital learning platforms improve 
    academic outcomes, increase student engagement, and develop essential career skills. While concerns 
    about screen time are valid, they can be managed through careful planning and balanced approaches. 
    Ultimately, embracing educational technology is not just beneficial—it is essential for preparing 
    students to thrive in our increasingly digital world.
    """
    
    result = douessay.grade_essay(essay, "Grade 9")
    
    # Test overall score (should be Level 4+, ≥80%)
    assert result['score'] >= 80, \
        f"Expected Level 4 score (≥80), got {result['score']}"
    
    # Test rubric level
    assert result['rubric_level']['level'] in ['Level 4', 'Level 4+'], \
        f"Expected Level 4 or 4+, got {result['rubric_level']['level']}"
    
    # Test claim-evidence ratio (target ≥2.0)
    ce_ratio = result['claim_evidence_ratio']
    assert ce_ratio['ratio'] >= 1.5, \
        f"Expected claim-evidence ratio ≥1.5, got {ce_ratio['ratio']}"
    
    print(f"✅ Grade 9 Level 4+ essay test passed")
    print(f"   Score: {result['score']}/100")
    print(f"   Level: {result['rubric_level']['level']}")
    print(f"   Claim-Evidence Ratio: {ce_ratio['ratio']}")
    print(f"   Evidence Count: {ce_ratio['evidence_count']}")


def test_claim_evidence_ratio_ai_enhanced():
    """Test that claim-evidence ratio calculation includes AI enhancements"""
    douessay = DouEssay()
    
    essay = """
    I argue that reading is important. Research shows that students who read regularly perform better 
    in school. For example, a study found that readers have higher vocabulary scores. Specifically, 
    data reveals that reading improves critical thinking. According to experts, reading develops 
    imagination and empathy.
    """
    
    result = douessay.calculate_claim_evidence_ratio(essay)
    
    # Should detect AI enhancement marker
    assert result.get('ai_enhanced') == True, \
        "Expected AI enhancement marker to be True"
    
    # Should have reasonable ratio with implicit evidence detection
    assert result['ratio'] >= 1.0, \
        f"Expected ratio ≥1.0 with AI detection, got {result['ratio']}"
    
    print(f"✅ AI-enhanced claim-evidence ratio test passed")
    print(f"   Ratio: {result['ratio']}")
    print(f"   Claims: {result['claims_count']}")
    print(f"   Evidence: {result['evidence_count']}")


def test_neural_rubric_scoring():
    """Test that neural rubric scoring uses v12.8.0 enhanced algorithms"""
    douessay = DouEssay()
    
    essay = """
    Education plays a crucial role in society. Teachers demonstrate dedication by working long hours 
    to help students succeed. For example, many educators stay after school to provide extra support. 
    This shows their commitment to student learning. Research indicates that teacher quality directly 
    impacts student achievement. Therefore, we must value and support our educators. Ultimately, 
    investing in teachers means investing in our future.
    """
    
    result = douessay.assess_with_neural_rubric(essay)
    
    # Check that all rubric categories are scored
    assert 'knowledge' in result['rubric_scores'], "Missing knowledge score"
    assert 'thinking' in result['rubric_scores'], "Missing thinking score"
    assert 'communication' in result['rubric_scores'], "Missing communication score"
    assert 'application' in result['rubric_scores'], "Missing application score"
    
    # Check that scores are in valid range (1.0-4.5)
    for category, score in result['rubric_scores'].items():
        assert 1.0 <= score <= 4.5, \
            f"{category} score {score} out of range (1.0-4.5)"
    
    # With v12.8.0 enhancements, this essay should score reasonably well
    assert result['overall_percentage'] >= 70, \
        f"Expected ≥70% with v12.8.0 scoring, got {result['overall_percentage']}"
    
    print(f"✅ Neural rubric scoring test passed")
    print(f"   Overall Score: {result['overall_percentage']}%")
    print(f"   Knowledge: {result['rubric_scores']['knowledge']}/4.5")
    print(f"   Thinking: {result['rubric_scores']['thinking']}/4.5")
    print(f"   Communication: {result['rubric_scores']['communication']}/4.5")
    print(f"   Application: {result['rubric_scores']['application']}/4.5")


def test_logical_flow_detection():
    """Test enhanced logical flow and transition detection"""
    douessay = DouEssay()
    
    essay = """
    First, technology improves learning. Furthermore, it increases engagement. Moreover, students 
    develop digital skills. However, some challenges exist. Nevertheless, these can be overcome. 
    Therefore, technology is beneficial. Consequently, schools should embrace it. In addition, 
    teachers need training. On the other hand, costs are a concern. Ultimately, the benefits 
    outweigh the drawbacks.
    """
    
    result = douessay.assess_with_neural_rubric(essay)
    
    # With many transitions, communication score should be good
    communication_score = result['rubric_scores']['communication']
    assert communication_score >= 2.5, \
        f"Expected communication score ≥2.5 with transitions, got {communication_score}"
    
    print(f"✅ Logical flow detection test passed")
    print(f"   Communication Score: {communication_score}/4.5")


def test_subsystem_metadata():
    """Test that subsystem metadata is correctly updated for v12.8.0"""
    douessay = DouEssay()
    
    # Check that all main subsystems have metadata
    expected_subsystems = ['doulet_argus', 'doulet_nexus', 'doulet_depthcore', 
                          'doulet_empathica', 'doulet_structura']
    
    for subsystem in expected_subsystems:
        assert subsystem in douessay.subsystem_metadata, \
            f"Missing metadata for {subsystem}"
        
        metadata = douessay.subsystem_metadata[subsystem]
        assert 'name' in metadata, f"Missing name in {subsystem} metadata"
        assert 'version' in metadata, f"Missing version in {subsystem} metadata"
        assert 'description' in metadata, f"Missing description in {subsystem} metadata"
        assert 'features' in metadata, f"Missing features in {subsystem} metadata"
        assert 'copyright' in metadata, f"Missing copyright in {subsystem} metadata"
        
        # Check that features list is not empty
        assert len(metadata['features']) > 0, \
            f"{subsystem} should have at least one feature listed"
    
    print("✅ Subsystem metadata test passed")


def test_emotional_engagement_scoring():
    """Test enhanced emotional engagement detection (Doulet Empathica 2.0)"""
    douessay = DouEssay()
    
    essay = """
    In my experience, education has been truly meaningful and valuable. I learned that dedication 
    and hard work are essential for success. This journey taught me important lessons about perseverance. 
    I believe that everyone should have access to quality education because it matters deeply. 
    The impact of good teachers is significant and lasting. Education is crucial for personal growth 
    and meaningful contribution to society.
    """
    
    result = douessay.assess_with_neural_rubric(essay)
    
    # Application score should reflect emotional engagement
    application_score = result['rubric_scores']['application']
    assert application_score >= 2.0, \
        f"Expected application score ≥2.0 with emotional markers, got {application_score}"
    
    print(f"✅ Emotional engagement scoring test passed")
    print(f"   Application Score: {application_score}/4.5")


def run_all_tests():
    """Run all v12.8.0 tests"""
    print("\n" + "="*60)
    print("Running v12.8.0 Test Suite")
    print("="*60 + "\n")
    
    tests = [
        ("Version Check", test_version),
        ("Subsystem Versions", test_subsystem_versions),
        ("Grade 9 Level 4+ Essay", test_grade_9_level_4_essay),
        ("AI-Enhanced Claim-Evidence Ratio", test_claim_evidence_ratio_ai_enhanced),
        ("Neural Rubric Scoring", test_neural_rubric_scoring),
        ("Logical Flow Detection", test_logical_flow_detection),
        ("Subsystem Metadata", test_subsystem_metadata),
        ("Emotional Engagement Scoring", test_emotional_engagement_scoring),
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        try:
            print(f"\nRunning: {test_name}")
            test_func()
            passed += 1
        except AssertionError as e:
            print(f"❌ FAILED: {test_name}")
            print(f"   Error: {str(e)}")
            failed += 1
        except Exception as e:
            print(f"❌ ERROR: {test_name}")
            print(f"   Error: {str(e)}")
            failed += 1
    
    print("\n" + "="*60)
    print(f"Test Results: {passed} passed, {failed} failed out of {len(tests)} total")
    print("="*60 + "\n")
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
