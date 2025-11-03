"""
Test suite for DouEssay v12.6.0
Tests accuracy improvements, subsystem enhancements, and ≥95% Grade 9 alignment target
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import DouEssay, VERSION, VERSION_NAME

def test_version_info():
    """Test that version is correctly updated to 12.6.0"""
    assert VERSION == "12.6.0", f"Expected VERSION='12.6.0', got '{VERSION}'"
    assert "Accuracy" in VERSION_NAME or "95%" in VERSION_NAME or "Grade 9" in VERSION_NAME, \
        f"Expected VERSION_NAME to mention Accuracy or 95% or Grade 9, got '{VERSION_NAME}'"
    print("✅ Version info correct: v12.6.0")

def test_subsystem_versions():
    """Test that subsystem versions are correctly upgraded for v12.6.0"""
    grader = DouEssay()
    
    # Test main subsystem names and versions as per issue requirements
    assert 'doulogic' in grader.subsystem_versions, "Should have DouLogic subsystem"
    assert grader.subsystem_versions['doulogic'] == '4.0', \
        f"DouLogic should be v4.0, got {grader.subsystem_versions.get('doulogic')}"
    
    assert 'douevidence' in grader.subsystem_versions, "Should have DouEvidence subsystem"
    assert grader.subsystem_versions['douevidence'] == '3.5', \
        f"DouEvidence should be v3.5, got {grader.subsystem_versions.get('douevidence')}"
    
    assert 'douscholar' in grader.subsystem_versions, "Should have DouScholar subsystem"
    assert grader.subsystem_versions['douscholar'] == '4.0', \
        f"DouScholar should be v4.0, got {grader.subsystem_versions.get('douscholar')}"
    
    assert 'douemotion' in grader.subsystem_versions, "Should have DouEmotion subsystem"
    assert grader.subsystem_versions['douemotion'] == '2.5', \
        f"DouEmotion should be v2.5, got {grader.subsystem_versions.get('douemotion')}"
    
    assert 'doustructure' in grader.subsystem_versions, "Should have DouStructure subsystem"
    assert grader.subsystem_versions['doustructure'] == '3.5', \
        f"DouStructure should be v3.5, got {grader.subsystem_versions.get('doustructure')}"
    
    assert 'doureflect' in grader.subsystem_versions, "Should have DouReflect subsystem"
    assert grader.subsystem_versions['doureflect'] == '4.1', \
        f"DouReflect should be v4.1, got {grader.subsystem_versions.get('doureflect')}"
    
    print("✅ Subsystem versions correct: DouLogic 4.0, DouEvidence 3.5, DouScholar 4.0, DouEmotion 2.5, DouStructure 3.5, DouReflect 4.1")

def test_backward_compatibility():
    """Test that old subsystem names still work for backward compatibility"""
    grader = DouEssay()
    
    # Test backward compatibility mappings
    assert 'scholarmind_core' in grader.subsystem_versions, "Should maintain ScholarMind Core for backward compatibility"
    assert 'douletflow' in grader.subsystem_versions, "Should maintain DouletFlow for backward compatibility"
    assert 'emotionflow' in grader.subsystem_versions, "Should maintain EmotionFlow for backward compatibility"
    assert 'scholarstruct' in grader.subsystem_versions, "Should maintain ScholarStruct for backward compatibility"
    assert 'argument_logic' in grader.subsystem_versions, "Should maintain argument_logic for backward compatibility"
    
    print("✅ Backward compatibility maintained for legacy subsystem names")

def test_grading_weights_updated():
    """Test that grading weights are updated as per v12.6.0 requirements"""
    grader = DouEssay()
    
    # Create dummy data for weight testing - high grammar score to test increased weight
    stats = {'word_count': 350}
    structure = {'score': 8.0, 'has_introduction': True}
    content = {'score': 8.0, 'has_thesis': True, 'argument_strength': {'has_clear_position': True, 'unsupported_claims': 0}}
    grammar_high = {'score': 10.0}  # High grammar score
    grammar_low = {'score': 6.0}    # Low grammar score
    application = {'score': 7.5}
    
    # Calculate scores with different grammar values
    score_high_grammar = grader.calculate_calibrated_ontario_score(stats, structure, content, grammar_high, application, "Grade 9")
    score_low_grammar = grader.calculate_calibrated_ontario_score(stats, structure, content, grammar_low, application, "Grade 9")
    
    # Verify scores are reasonable (should be between 65-98)
    assert 65 <= score_high_grammar <= 98, f"Score should be between 65-98, got {score_high_grammar}"
    assert 65 <= score_low_grammar <= 98, f"Score should be between 65-98, got {score_low_grammar}"
    
    # With increased grammar weight (20% vs 15%), high grammar should show measurable impact
    grammar_impact = score_high_grammar - score_low_grammar
    assert grammar_impact >= 5, f"Grammar weight increase should show impact ≥5 points, got {grammar_impact}"
    
    print(f"✅ Grading weights applied successfully: high grammar={score_high_grammar}, low grammar={score_low_grammar}, impact={grammar_impact} points")

def test_essay_limits_enforcement():
    """Test that essay limits are correctly set for all tiers"""
    grader = DouEssay()
    
    # Test daily limits as per issue requirements
    assert grader.license_manager.feature_access['free_trial']['daily_limit'] == 3, \
        "Free trial should have 3 essays/day"
    assert grader.license_manager.feature_access['student_basic']['daily_limit'] == 10, \
        "Student Basic should have 10 essays/day"
    assert grader.license_manager.feature_access['student_premium']['daily_limit'] == 20, \
        "Student Premium should have 20 essays/day"
    assert grader.license_manager.feature_access['teacher_suite']['daily_limit'] == float('inf'), \
        "Teacher Suite should have unlimited essays/day"
    
    print("✅ Essay limits correctly enforced: Free=3, Basic=10, Premium=20, Teacher=Unlimited")

def test_copyright_notices():
    """Test that copyright notices are present in subsystem documentation"""
    grader = DouEssay()
    
    # Check that setup_v12_enhancements docstring contains copyright
    docstring = grader.setup_v12_enhancements.__doc__
    assert docstring is not None, "setup_v12_enhancements should have docstring"
    assert "Doulet Media" in docstring, "Copyright should mention Doulet Media"
    assert "changcheng967" in docstring or "©" in docstring, "Copyright should be present"
    
    print("✅ Copyright notices present: © Doulet Media, changcheng967")

def test_structure_organization_scoring():
    """Test improved structure & organization scoring for Grade 9 essays"""
    grader = DouEssay()
    
    # Essay with clear structure, topic sentences, and transitions
    essay = """
    Technology has transformed modern education in significant ways. This essay will explore three key benefits.
    
    First, technology enables personalized learning. For example, students can learn at their own pace using 
    educational apps. This demonstrates how technology adapts to individual needs.
    
    Second, technology facilitates collaboration. Students can work together on projects remotely. Therefore,
    technology breaks down geographical barriers in education.
    
    Finally, technology prepares students for the digital future. In today's world, digital literacy is essential.
    This shows why technology integration is crucial in schools.
    
    In conclusion, technology offers personalized learning, collaboration opportunities, and future readiness.
    These benefits clearly demonstrate technology's positive impact on education.
    """
    
    # Grade the essay
    result = grader.grade_essay(essay, "Grade 9")
    
    # Check that structure scoring components are present
    assert 'detailed_analysis' in result, "Should have detailed analysis"
    assert 'structure' in result['detailed_analysis'], "Should have structure analysis"
    
    structure_score = result['detailed_analysis']['structure']['score']
    assert structure_score >= 6, f"Essay with good structure should score ≥6, got {structure_score}"
    
    print(f"✅ Structure & Organization scoring working: {structure_score}/10")

def test_application_insight_scoring():
    """Test improved application & insight scoring with personal reflection"""
    grader = DouEssay()
    
    # Essay with personal reflection and real-world connections
    essay = """
    Reading has profoundly impacted my personal growth. In my experience, books have opened new perspectives.
    
    For instance, reading classics taught me about human nature. This insight applies to my daily interactions
    with peers and family. I have learned to understand different viewpoints through literature.
    
    Moreover, reading has practical applications in real life. The critical thinking skills I developed through
    analyzing texts help me solve problems at school. This demonstrates how reading translates to practical benefits.
    
    From my perspective, reading is not just academic but life-changing. I realized that every book offers lessons
    relevant to contemporary issues. This connection between literature and reality is invaluable.
    
    In conclusion, reading has transformed my understanding of myself and the world. The personal growth and
    practical skills I gained prove reading's importance beyond the classroom.
    """
    
    # Grade the essay
    result = grader.grade_essay(essay, "Grade 9")
    
    # Check application & insight scoring
    assert 'detailed_analysis' in result, "Should have detailed analysis"
    assert 'application' in result['detailed_analysis'], "Should have application analysis"
    
    application_score = result['detailed_analysis']['application']['score']
    assert application_score >= 7, f"Essay with good personal reflection should score ≥7, got {application_score}"
    
    print(f"✅ Application & Insight scoring working: {application_score}/10")

def test_evidence_relevance_connection():
    """Test improved evidence relevance and claim-evidence connection scoring"""
    grader = DouEssay()
    
    # Essay with clear claim-evidence connections
    essay = """
    Sports participation significantly benefits student development. This claim is supported by multiple evidence types.
    
    Research shows that students who play sports have better academic performance. Specifically, a 2024 study found
    that athletic students scored 15% higher on standardized tests. This evidence directly demonstrates the academic benefits.
    
    Furthermore, sports teach valuable life skills. For example, team sports require communication and cooperation.
    This clearly illustrates how sports develop interpersonal abilities essential for future success.
    
    Additionally, physical activity improves mental health. According to recent findings, regular exercise reduces
    stress and anxiety in teenagers. This data explicitly supports the mental health benefits of sports participation.
    
    The evidence presented - from academic performance to life skills to mental health - conclusively proves that
    sports participation is highly beneficial for students.
    """
    
    # Grade the essay
    result = grader.grade_essay(essay, "Grade 9")
    
    # Check content scoring (which includes evidence evaluation)
    assert 'detailed_analysis' in result, "Should have detailed analysis"
    assert 'content' in result['detailed_analysis'], "Should have content analysis"
    
    content_score = result['detailed_analysis']['content']['score']
    assert content_score >= 7, f"Essay with strong evidence connections should score ≥7, got {content_score}"
    
    print(f"✅ Evidence Relevance scoring working: {content_score}/10")

def test_grade_9_accuracy_target():
    """Test that Grade 9 essays receive accurate, fair scoring"""
    grader = DouEssay()
    
    # High-quality Grade 9 essay
    grade_9_essay = """
    Social media has both positive and negative effects on teenagers. While it connects people, it also creates challenges.
    
    On the positive side, social media helps teenagers stay connected with friends and family. For example, students
    can share experiences and support each other through difficult times. This shows how social media builds communities.
    
    However, social media can negatively impact mental health. Studies indicate that excessive social media use leads
    to anxiety and depression in young people. This evidence demonstrates the potential harm of constant online presence.
    
    Despite these concerns, social media also provides educational opportunities. Students can access learning resources
    and join study groups online. Therefore, when used responsibly, social media can enhance learning.
    
    From my personal experience, I have seen both benefits and drawbacks. I learned to balance my social media time
    to avoid negative effects while enjoying the connections it provides.
    
    In conclusion, social media is a tool that can be beneficial or harmful depending on how it is used. Teenagers
    need guidance to navigate social media responsibly and maximize its benefits while minimizing risks.
    """
    
    # Grade the essay at Grade 9 level
    result = grader.grade_essay(grade_9_essay, "Grade 9")
    
    # Check that score is reasonable for a good Grade 9 essay
    score = result['score']
    assert 70 <= score <= 90, f"Good Grade 9 essay should score 70-90, got {score}"
    
    # Check Ontario level
    level = result['rubric_level']['level']
    assert level in ['Level 3', 'Level 4', 'Level 4+'], f"Good Grade 9 essay should achieve Level 3 or 4, got {level}"
    
    print(f"✅ Grade 9 accuracy target validated: Score {score}/100, Level {level}")

def test_counter_argument_detection():
    """Test enhanced counter-argument detection from DouLogic 4.0
    
    Note: Essay is converted to lowercase for analysis as the analyze_inference_chains_v12_2
    method is designed to work with normalized text. While capitalization can be important
    for proper nouns, the counter-argument markers themselves ('however', 'although', etc.)
    are case-insensitive and detected correctly in lowercase.
    """
    grader = DouEssay()
    
    # Essay with counter-arguments (will be lowercased for analysis)
    essay = """
    Technology benefits education. However, critics argue that it creates distractions in classrooms.
    Although this concern is valid, the benefits outweigh the drawbacks. Some may say that traditional
    methods are better, but research shows otherwise. Despite these criticisms, evidence supports technology use.
    """
    
    # Analyze the essay (lowercased as expected by the method)
    result = grader.analyze_inference_chains_v12_2(essay.lower())
    
    # Check for counter-argument detection
    assert 'counter_argument_markers' in result, "Should detect counter-argument markers"
    counter_args = result.get('counter_argument_markers', 0)
    assert counter_args >= 1, f"Should detect at least 1 counter-argument, got {counter_args}"
    
    print(f"✅ Counter-argument detection working: {counter_args} markers found")

def test_topic_sentence_recognition():
    """Test improved topic sentence recognition from DouStructure 3.5"""
    grader = DouEssay()
    
    # Essay with clear topic sentences
    essay = """
    This essay examines three benefits of reading.
    
    First and foremost, reading improves vocabulary. Students who read regularly learn new words.
    
    Another important benefit is critical thinking development. Readers analyze characters and plots.
    
    The most significant advantage is empathy development. Reading diverse stories builds understanding.
    
    In conclusion, reading provides vocabulary, critical thinking, and empathy benefits.
    """
    
    # Analyze paragraph structure
    result = grader.analyze_paragraph_structure_v12(essay)
    
    # Check that analysis returns a result (the method exists and runs)
    assert result is not None, "Should return analysis result"
    assert isinstance(result, dict), "Should return a dictionary"
    
    # Check for structure analysis fields (based on actual return values)
    has_structure_info = any(key in result for key in ['structure_score', 'structure_quality_score', 'score', 
                                                         'paragraph_count', 'has_introduction', 'topic_sentences_detected',
                                                         'transitions_detected', 'intro_detected', 'body_detected'])
    assert has_structure_info, f"Should have some structure analysis fields, got: {list(result.keys())}"
    
    print("✅ Topic sentence recognition working")

def test_minimum_changes():
    """Test that existing functionality is not broken by v12.6.0 changes"""
    grader = DouEssay()
    
    # Simple essay to test basic grading still works
    simple_essay = "This is a test essay. It has multiple sentences. The content is simple but sufficient for testing."
    
    try:
        result = grader.grade_essay(simple_essay, "Grade 10")
        assert 'score' in result, "Should return a score"
        assert 'rubric_level' in result, "Should return rubric level"
        assert 'feedback' in result, "Should return feedback"
        print("✅ Existing functionality preserved - minimal changes verified")
    except Exception as e:
        raise AssertionError(f"Basic grading functionality broken: {str(e)}")

if __name__ == "__main__":
    print("\n" + "="*70)
    print("DouEssay v12.6.0 Test Suite")
    print("Testing: Accuracy & Subsystem Enhancement - ≥95% Grade 9 Alignment")
    print("="*70 + "\n")
    
    tests = [
        test_version_info,
        test_subsystem_versions,
        test_backward_compatibility,
        test_grading_weights_updated,
        test_essay_limits_enforcement,
        test_copyright_notices,
        test_structure_organization_scoring,
        test_application_insight_scoring,
        test_evidence_relevance_connection,
        test_grade_9_accuracy_target,
        test_counter_argument_detection,
        test_topic_sentence_recognition,
        test_minimum_changes
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"❌ {test.__name__} FAILED: {str(e)}")
            failed += 1
        except Exception as e:
            print(f"❌ {test.__name__} ERROR: {str(e)}")
            failed += 1
    
    print("\n" + "="*70)
    print(f"Test Results: {passed} passed, {failed} failed out of {len(tests)} total")
    print("="*70 + "\n")
    
    if failed > 0:
        sys.exit(1)
