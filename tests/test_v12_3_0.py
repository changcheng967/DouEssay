"""
Test suite for DouEssay v12.3.0 
Tests version updates, daily limits, pricing, and grading accuracy improvements
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import DouEssay, VERSION, VERSION_NAME

def test_version_info():
    """Test that version is correctly updated to 12.3.0"""
    assert VERSION == "12.3.0", f"Expected VERSION='12.3.0', got '{VERSION}'"
    assert "95%+ accuracy" in VERSION_NAME or "95%" in VERSION_NAME, \
        f"Expected VERSION_NAME to mention 95%+ accuracy, got '{VERSION_NAME}'"
    print("✅ Version info correct: v12.3.0")

def test_daily_limits():
    """Test that daily limits are correctly updated for v12.3.0"""
    grader = DouEssay()
    
    # Test free_trial limit
    assert grader.license_manager.feature_access['free_trial']['daily_limit'] == 3, \
        "Free trial should have 3 essays/day"
    
    # Test student_basic limit
    assert grader.license_manager.feature_access['student_basic']['daily_limit'] == 7, \
        "Student Basic should have 7 essays/day"
    
    # Test student_premium limit
    assert grader.license_manager.feature_access['student_premium']['daily_limit'] == 12, \
        "Student Premium should have 12 essays/day"
    
    # Test teacher_suite limit (unlimited)
    assert grader.license_manager.feature_access['teacher_suite']['daily_limit'] == float('inf'), \
        "Teacher Suite should have unlimited essays"
    
    print("✅ Daily limits correct: Free=3, Basic=7, Premium=12, Teacher=unlimited")

def test_grading_accuracy():
    """Test that grading system handles evidence coherence and counter-arguments properly"""
    grader = DouEssay()
    
    # Test essay with strong evidence and counter-arguments
    essay = """
    Technology has fundamentally transformed modern education in ways that are both beneficial and challenging. 
    While critics argue that technology creates distractions in classrooms, the evidence overwhelmingly demonstrates 
    that when properly integrated, digital tools enhance learning outcomes significantly.
    
    First, research from Stanford University (2024) shows that students using adaptive learning platforms 
    improved their test scores by an average of 23% compared to traditional instruction alone. This directly 
    demonstrates the effectiveness of technology in personalized learning environments. The study specifically 
    indicates that AI-powered tutoring systems can identify learning gaps and provide targeted interventions 
    more effectively than conventional methods.
    
    Moreover, collaborative tools like Google Workspace enable students to work together seamlessly, even when 
    physically separated. For instance, during the COVID-19 pandemic, schools that had already integrated 
    cloud-based collaboration tools maintained 85% of their pre-pandemic academic performance, according to 
    data from the Ontario Ministry of Education. This contextual evidence reveals that technology infrastructure 
    was crucial for educational continuity.
    
    However, some may contend that technology leads to decreased attention spans and increased plagiarism. 
    While these concerns have merit, they reflect implementation challenges rather than inherent technological 
    flaws. Research from the University of Toronto demonstrates that when teachers receive proper training 
    in digital pedagogy, student engagement actually increases by 31%, and academic integrity violations 
    decrease by 18%. This suggests that the key factor is not technology itself, but how educators utilize it.
    
    In conclusion, technology represents a powerful tool for educational enhancement when thoughtfully 
    implemented. The evidence from peer-reviewed studies, institutional data, and real-world applications 
    consistently points to improved learning outcomes. While challenges exist, they are addressable through 
    proper training and strategic implementation rather than technology avoidance.
    """
    
    result = grader.grade_essay(essay, "Grade 10")
    
    # Check that the essay receives a good score (should be 80+)
    assert result['score'] >= 80, \
        f"Expected score >= 80 for well-argued essay, got {result['score']}"
    
    # Check that evidence analysis is present
    assert 'detailed_analysis' in result, "Should have detailed_analysis"
    
    # Check for feedback quality
    assert len(result['feedback']) > 0, "Should provide feedback"
    
    print(f"✅ Grading accuracy test passed: Score={result['score']}, Level={result['rubric_level']['level']}")

def test_short_essay_handling():
    """Test that short essays are handled appropriately"""
    grader = DouEssay()
    
    short_essay = "Technology is important. It helps students learn better."
    
    result = grader.grade_essay(short_essay, "Grade 9")
    
    # Short essays should receive lower scores
    assert result['score'] < 80, \
        f"Short essay should score < 80, got {result['score']}"
    
    # Should provide feedback about length
    feedback_text = " ".join(result['feedback']).lower()
    assert 'short' in feedback_text or 'length' in feedback_text or 'expand' in feedback_text, \
        "Feedback should mention essay length"
    
    print(f"✅ Short essay handling correct: Score={result['score']}")

def test_emotionflow_analysis():
    """Test that EmotionFlow analysis is working"""
    grader = DouEssay()
    
    reflective_essay = """
    Looking back on my experience volunteering at the local community center, I realize how profoundly 
    it transformed my understanding of empathy and social responsibility. Initially, I approached 
    volunteering as merely a requirement for school credits, but what I discovered changed my perspective 
    entirely.
    
    Working with elderly residents taught me to appreciate the wisdom that comes with life experience. 
    For example, Mrs. Chen shared stories about immigrating to Canada in the 1960s, facing discrimination, 
    yet persevering to build a successful business. Her resilience inspired me to reconsider my own 
    challenges as opportunities for growth rather than insurmountable obstacles.
    
    This experience applies directly to my future career aspirations in social work. I now understand 
    that genuine connection requires patience, active listening, and the humility to learn from others. 
    These insights will be invaluable as I pursue my goal of supporting marginalized communities.
    """
    
    result = grader.grade_essay(reflective_essay, "Grade 11")
    
    # Check for application/insight scoring
    assert 'detailed_analysis' in result
    assert 'application' in result['detailed_analysis']
    
    # Reflective essay should have decent application score
    app_score = result['detailed_analysis']['application']['score']
    assert app_score >= 6, f"Reflective essay should have application score >= 6, got {app_score}"
    
    print(f"✅ EmotionFlow analysis working: Application score={app_score}")

def test_paragraph_structure_detection():
    """Test that paragraph structure is properly analyzed"""
    grader = DouEssay()
    
    structured_essay = """
    This essay will examine the impact of social media on teenage mental health, arguing that while 
    these platforms offer connectivity benefits, they ultimately pose significant psychological risks 
    that require urgent attention.
    
    First, research from the American Psychological Association indicates that teenagers who spend 
    more than 3 hours daily on social media are 35% more likely to experience symptoms of depression. 
    This demonstrates a clear correlation between excessive social media use and mental health challenges.
    
    Furthermore, the constant comparison with curated online personas creates unrealistic expectations 
    and damages self-esteem. Studies show that 60% of teenagers report feeling inadequate after viewing 
    social media content, particularly on image-focused platforms like Instagram.
    
    However, critics argue that social media provides valuable social connections, especially for 
    isolated teenagers. While this point has merit, the negative psychological effects outweigh these 
    benefits, as evidenced by rising teen anxiety rates correlating with increased social media adoption.
    
    In conclusion, the evidence overwhelmingly supports implementing stricter regulations on teenage 
    social media use to protect mental health during these critical developmental years.
    """
    
    result = grader.grade_essay(structured_essay, "Grade 10")
    
    # Check structure scoring
    assert 'detailed_analysis' in result
    assert 'structure' in result['detailed_analysis']
    
    structure_score = result['detailed_analysis']['structure']['score']
    assert structure_score >= 6, \
        f"Well-structured essay should have structure score >= 6, got {structure_score}"
    
    print(f"✅ Paragraph structure detection working: Structure score={structure_score}")

def test_backward_compatibility():
    """Test that v12.3.0 maintains backward compatibility"""
    grader = DouEssay()
    
    # Test that all expected methods exist
    assert hasattr(grader, 'grade_essay'), "Should have grade_essay method"
    assert hasattr(grader, 'license_manager'), "Should have license_manager"
    assert hasattr(grader, 'validate_license_and_increment'), "Should have validate_license_and_increment"
    
    # Test that grading still returns expected structure
    simple_essay = "Education is important for society. Students need good teachers."
    result = grader.grade_essay(simple_essay, "Grade 9")
    
    expected_keys = ['score', 'rubric_level', 'feedback', 'corrections', 'detailed_analysis']
    for key in expected_keys:
        assert key in result, f"Result should contain '{key}' field"
    
    print("✅ Backward compatibility maintained")

def test_license_validation():
    """Test that license validation works with updated limits"""
    grader = DouEssay()
    
    # Test offline mode (no Supabase connection)
    license_result = grader.license_manager.validate_license("test_key_12345")
    
    assert license_result['valid'] == True, "Should be valid in offline mode"
    assert 'user_type' in license_result, "Should return user_type"
    assert 'daily_limit' in license_result, "Should return daily_limit"
    assert 'features' in license_result, "Should return features"
    
    print("✅ License validation working in offline mode")

def run_all_tests():
    """Run all v12.3.0 tests"""
    print("\n" + "="*60)
    print("Running DouEssay v12.3.0 Test Suite")
    print("="*60 + "\n")
    
    tests = [
        test_version_info,
        test_daily_limits,
        test_grading_accuracy,
        test_short_essay_handling,
        test_emotionflow_analysis,
        test_paragraph_structure_detection,
        test_backward_compatibility,
        test_license_validation,
    ]
    
    passed = 0
    failed = 0
    
    for test_func in tests:
        try:
            print(f"\nRunning: {test_func.__name__}")
            test_func()
            passed += 1
        except AssertionError as e:
            print(f"❌ FAILED: {test_func.__name__}")
            print(f"   Error: {e}")
            failed += 1
        except Exception as e:
            print(f"❌ ERROR: {test_func.__name__}")
            print(f"   Error: {e}")
            failed += 1
    
    print("\n" + "="*60)
    print(f"Test Results: {passed} passed, {failed} failed")
    print("="*60 + "\n")
    
    return failed == 0

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
