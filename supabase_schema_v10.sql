-- ========================================
-- DouEssay v10.0.0 - Project Apex
-- Supabase Database Schema
-- ========================================
-- Author: changcheng967
-- Organization: Doulet Media
-- Version: 10.0.0
-- Compatible with: DouEssay v10.0.0 and License Key Generator
-- ========================================

-- Enable UUID extension if not already enabled
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ========================================
-- 1. LICENSES TABLE
-- Core license management for all tier types
-- ========================================

CREATE TABLE IF NOT EXISTS licenses (
    -- Primary identification
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    license_key VARCHAR(50) UNIQUE NOT NULL,
    
    -- User information
    user_type VARCHAR(30) NOT NULL CHECK (user_type IN (
        'free_trial', 
        'student_basic', 
        'student_premium', 
        'teacher_suite', 
        'institutional',
        -- Legacy support (v9.0.0 and earlier)
        'free',
        'plus',
        'premium',
        'unlimited'
    )),
    user_email VARCHAR(255) NOT NULL,
    custom_name VARCHAR(255),
    
    -- Timing
    issued_at TIMESTAMP DEFAULT NOW(),
    expires_at TIMESTAMP NOT NULL,
    last_used_at TIMESTAMP,
    
    -- Status
    is_active BOOLEAN DEFAULT TRUE,
    
    -- Limits
    daily_limit INTEGER DEFAULT 25,
    
    -- Features (JSON array of feature flags)
    features JSONB DEFAULT '[]'::jsonb,
    
    -- Metadata
    metadata JSONB DEFAULT '{}'::jsonb,
    
    -- Audit trail
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Indexes for licenses table
CREATE INDEX idx_licenses_key ON licenses(license_key);
CREATE INDEX idx_licenses_email ON licenses(user_email);
CREATE INDEX idx_licenses_type ON licenses(user_type);
CREATE INDEX idx_licenses_active ON licenses(is_active);
CREATE INDEX idx_licenses_expires ON licenses(expires_at);

-- Comment
COMMENT ON TABLE licenses IS 'v10.0.0: License key management for all DouEssay tiers';

-- ========================================
-- 2. USAGE TABLE
-- Daily usage tracking per license
-- ========================================

CREATE TABLE IF NOT EXISTS usage (
    -- Primary identification
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    license_key VARCHAR(50) NOT NULL REFERENCES licenses(license_key) ON DELETE CASCADE,
    
    -- Usage tracking
    usage_date DATE NOT NULL,
    usage_count INTEGER DEFAULT 0,
    
    -- Statistics
    last_essay_at TIMESTAMP,
    total_words_processed INTEGER DEFAULT 0,
    average_essay_length INTEGER DEFAULT 0,
    
    -- Audit
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    
    -- Ensure one record per license per day
    UNIQUE(license_key, usage_date)
);

-- Indexes for usage table
CREATE INDEX idx_usage_license ON usage(license_key);
CREATE INDEX idx_usage_date ON usage(usage_date);
CREATE INDEX idx_usage_license_date ON usage(license_key, usage_date);

-- Comment
COMMENT ON TABLE usage IS 'v10.0.0: Daily usage tracking for license enforcement';

-- ========================================
-- 3. SMARTPROFILES TABLE (v10.0.0)
-- SmartProfile 3.0 - Hyper-Adaptive Learning
-- Tracks 30+ dimensions of student learning
-- ========================================

CREATE TABLE IF NOT EXISTS smartprofiles (
    -- Primary identification
    user_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    license_key VARCHAR(50) REFERENCES licenses(license_key) ON DELETE CASCADE,
    user_email VARCHAR(255) NOT NULL,
    
    -- Basic statistics
    total_essays INTEGER DEFAULT 0,
    average_score DECIMAL(5,2) DEFAULT 0.00,
    highest_score DECIMAL(5,2) DEFAULT 0.00,
    lowest_score DECIMAL(5,2) DEFAULT 0.00,
    
    -- v10.0.0: 30+ dimension scores (JSON object with dimension name as key)
    -- Example: {"clarity": 75.5, "argument_depth": 82.3, "tone_control": 68.9, ...}
    dimension_scores JSONB DEFAULT '{}'::jsonb,
    
    -- v10.0.0: New dimensions added in Project Apex
    emotional_resilience FLOAT DEFAULT 50.0,
    time_management_score FLOAT DEFAULT 50.0,
    creativity_index FLOAT DEFAULT 50.0,
    peer_comparison_opt_in BOOLEAN DEFAULT FALSE,
    
    -- Historical data
    essay_history JSONB DEFAULT '[]'::jsonb,
    
    -- Achievement tracking (v10.0.0: 50+ badges)
    achievements TEXT[] DEFAULT ARRAY[]::TEXT[],
    
    -- v10.0.0: Gamification
    total_points INTEGER DEFAULT 0,
    current_level INTEGER DEFAULT 1,
    streak_days INTEGER DEFAULT 0,
    longest_streak INTEGER DEFAULT 0,
    last_activity_date DATE,
    
    -- v10.0.0: Micro-missions tracking
    micro_missions_completed INTEGER DEFAULT 0,
    daily_missions_active JSONB DEFAULT '[]'::jsonb,
    
    -- Growth trends
    growth_trends JSONB DEFAULT '{}'::jsonb,
    
    -- v10.0.0: Learning velocity and predictions
    learning_velocity FLOAT DEFAULT 0.0,
    predicted_next_score FLOAT,
    
    -- v10.0.0: Multi-device sync
    device_ids TEXT[] DEFAULT ARRAY[]::TEXT[],
    last_sync_timestamp TIMESTAMP,
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    
    -- Constraints
    CONSTRAINT valid_scores CHECK (
        average_score >= 0 AND average_score <= 100 AND
        highest_score >= 0 AND highest_score <= 100 AND
        lowest_score >= 0 AND lowest_score <= 100
    )
);

-- Indexes for smartprofiles table
CREATE INDEX idx_smartprofiles_user ON smartprofiles(user_id);
CREATE INDEX idx_smartprofiles_license ON smartprofiles(license_key);
CREATE INDEX idx_smartprofiles_email ON smartprofiles(user_email);
CREATE INDEX idx_smartprofiles_updated ON smartprofiles(updated_at);
CREATE INDEX idx_smartprofiles_points ON smartprofiles(total_points);
CREATE INDEX idx_smartprofiles_level ON smartprofiles(current_level);

-- Comment
COMMENT ON TABLE smartprofiles IS 'v10.0.0: SmartProfile 3.0 with 30+ adaptive learning dimensions';

-- ========================================
-- 4. MICRO_MISSIONS TABLE (v10.0.0)
-- Daily micro-missions for skill building
-- ========================================

CREATE TABLE IF NOT EXISTS micro_missions (
    -- Primary identification
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    
    -- Mission definition
    mission_type VARCHAR(50) NOT NULL,
    mission_title VARCHAR(255) NOT NULL,
    mission_description TEXT NOT NULL,
    
    -- Difficulty and requirements
    difficulty VARCHAR(20) CHECK (difficulty IN ('easy', 'medium', 'hard')),
    estimated_time_minutes INTEGER DEFAULT 15,
    required_level INTEGER DEFAULT 1,
    
    -- Prompt and criteria
    prompt TEXT NOT NULL,
    success_criteria JSONB NOT NULL,
    
    -- Rewards
    reward_points INTEGER DEFAULT 10,
    reward_badges TEXT[] DEFAULT ARRAY[]::TEXT[],
    
    -- Metadata
    category VARCHAR(50),
    tags TEXT[] DEFAULT ARRAY[]::TEXT[],
    
    -- Status
    is_active BOOLEAN DEFAULT TRUE,
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Indexes for micro_missions table
CREATE INDEX idx_micro_missions_type ON micro_missions(mission_type);
CREATE INDEX idx_micro_missions_difficulty ON micro_missions(difficulty);
CREATE INDEX idx_micro_missions_active ON micro_missions(is_active);
CREATE INDEX idx_micro_missions_category ON micro_missions(category);

-- Comment
COMMENT ON TABLE micro_missions IS 'v10.0.0: Daily micro-missions for bite-sized practice';

-- ========================================
-- 5. USER_MISSIONS TABLE (v10.0.0)
-- Tracks user progress on micro-missions
-- ========================================

CREATE TABLE IF NOT EXISTS user_missions (
    -- Primary identification
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES smartprofiles(user_id) ON DELETE CASCADE,
    mission_id UUID NOT NULL REFERENCES micro_missions(id) ON DELETE CASCADE,
    
    -- Timing
    assigned_date DATE NOT NULL DEFAULT CURRENT_DATE,
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    
    -- Submission
    submission_text TEXT,
    
    -- Results
    score FLOAT,
    performance_evaluation JSONB,
    
    -- Status
    status VARCHAR(20) DEFAULT 'assigned' CHECK (status IN (
        'assigned', 'in_progress', 'completed', 'abandoned'
    )),
    
    -- Rewards earned
    points_earned INTEGER DEFAULT 0,
    badges_earned TEXT[] DEFAULT ARRAY[]::TEXT[],
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Indexes for user_missions table
CREATE INDEX idx_user_missions_user ON user_missions(user_id);
CREATE INDEX idx_user_missions_mission ON user_missions(mission_id);
CREATE INDEX idx_user_missions_status ON user_missions(status);
CREATE INDEX idx_user_missions_date ON user_missions(assigned_date);

-- Comment
COMMENT ON TABLE user_missions IS 'v10.0.0: User progress on daily micro-missions';

-- ========================================
-- 6. USER_ACHIEVEMENTS TABLE (v10.0.0)
-- Achievement badge tracking for gamification
-- ========================================

CREATE TABLE IF NOT EXISTS user_achievements (
    -- Primary identification
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES smartprofiles(user_id) ON DELETE CASCADE,
    
    -- Achievement details
    badge_id VARCHAR(50) NOT NULL,
    badge_name VARCHAR(255) NOT NULL,
    badge_category VARCHAR(50),
    
    -- Earning details
    earned_date TIMESTAMP DEFAULT NOW(),
    points_awarded INTEGER DEFAULT 0,
    
    -- Notification
    notification_sent BOOLEAN DEFAULT FALSE,
    notification_sent_at TIMESTAMP,
    
    -- Metadata
    metadata JSONB DEFAULT '{}'::jsonb,
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT NOW()
);

-- Indexes for user_achievements table
CREATE INDEX idx_user_achievements_user ON user_achievements(user_id);
CREATE INDEX idx_user_achievements_badge ON user_achievements(badge_id);
CREATE INDEX idx_user_achievements_earned ON user_achievements(earned_date);
CREATE INDEX idx_user_achievements_category ON user_achievements(badge_category);

-- Comment
COMMENT ON TABLE user_achievements IS 'v10.0.0: 50+ achievement badges for gamification';

-- ========================================
-- 7. LEADERBOARDS TABLE (v10.0.0)
-- Global, school, and individual leaderboards
-- ========================================

CREATE TABLE IF NOT EXISTS leaderboards (
    -- Primary identification
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    
    -- User identification (anonymized for privacy)
    user_id_hash VARCHAR(64) NOT NULL,  -- SHA-256 hash for privacy
    display_name VARCHAR(100),  -- Optional public display name
    
    -- Categorization
    category VARCHAR(50) NOT NULL CHECK (category IN (
        'growth', 'score', 'creativity', 'streak', 'missions', 'overall'
    )),
    
    -- Scope
    leaderboard_type VARCHAR(20) NOT NULL CHECK (leaderboard_type IN (
        'individual', 'school', 'regional', 'global'
    )),
    
    -- Score and ranking
    score FLOAT NOT NULL,
    rank INTEGER,
    
    -- Context
    grade_level INTEGER,
    region VARCHAR(50),
    school_id VARCHAR(100),
    
    -- Privacy
    opt_in BOOLEAN DEFAULT FALSE,
    show_publicly BOOLEAN DEFAULT FALSE,
    
    -- Temporal
    period VARCHAR(20) CHECK (period IN ('daily', 'weekly', 'monthly', 'all_time')),
    period_start DATE,
    period_end DATE,
    
    -- Timestamps
    last_updated TIMESTAMP DEFAULT NOW(),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Indexes for leaderboards table
CREATE INDEX idx_leaderboards_hash ON leaderboards(user_id_hash);
CREATE INDEX idx_leaderboards_category ON leaderboards(category);
CREATE INDEX idx_leaderboards_type ON leaderboards(leaderboard_type);
CREATE INDEX idx_leaderboards_rank ON leaderboards(rank);
CREATE INDEX idx_leaderboards_school ON leaderboards(school_id);
CREATE INDEX idx_leaderboards_period ON leaderboards(period, period_start, period_end);

-- Comment
COMMENT ON TABLE leaderboards IS 'v10.0.0: Privacy-safe leaderboards for gamification';

-- ========================================
-- 8. LEARNING_QUESTS TABLE (v10.0.0)
-- Learning quests and challenges
-- ========================================

CREATE TABLE IF NOT EXISTS learning_quests (
    -- Primary identification
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    
    -- Quest definition
    quest_type VARCHAR(50) NOT NULL CHECK (quest_type IN (
        'timed', 'skill_specific', 'creative', 'marathon', 'challenge'
    )),
    quest_title VARCHAR(255) NOT NULL,
    quest_description TEXT NOT NULL,
    
    -- Difficulty
    difficulty VARCHAR(20) CHECK (difficulty IN ('easy', 'medium', 'hard', 'expert')),
    
    -- Requirements
    required_level INTEGER DEFAULT 1,
    prerequisite_quests UUID[] DEFAULT ARRAY[]::UUID[],
    
    -- Duration and timing
    estimated_time_minutes INTEGER,
    time_limit_minutes INTEGER,  -- For timed quests
    
    -- Prompts and criteria
    prompts JSONB NOT NULL,  -- Array of prompts for the quest
    success_criteria JSONB NOT NULL,
    
    -- Rewards
    reward_points INTEGER DEFAULT 50,
    reward_badges TEXT[] DEFAULT ARRAY[]::TEXT[],
    unlock_features TEXT[] DEFAULT ARRAY[]::TEXT[],
    
    -- Quest chain
    part_of_series VARCHAR(100),
    series_order INTEGER,
    
    -- Availability
    is_active BOOLEAN DEFAULT TRUE,
    available_from DATE,
    available_until DATE,
    
    -- Metadata
    category VARCHAR(50),
    tags TEXT[] DEFAULT ARRAY[]::TEXT[],
    
    -- Statistics
    total_attempts INTEGER DEFAULT 0,
    total_completions INTEGER DEFAULT 0,
    average_completion_time INTEGER,
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Indexes for learning_quests table
CREATE INDEX idx_learning_quests_type ON learning_quests(quest_type);
CREATE INDEX idx_learning_quests_difficulty ON learning_quests(difficulty);
CREATE INDEX idx_learning_quests_active ON learning_quests(is_active);
CREATE INDEX idx_learning_quests_series ON learning_quests(part_of_series);
CREATE INDEX idx_learning_quests_category ON learning_quests(category);

-- Comment
COMMENT ON TABLE learning_quests IS 'v10.0.0: Learning quests for skill-building challenges';

-- ========================================
-- 9. USER_QUESTS TABLE (v10.0.0)
-- User progress on learning quests
-- ========================================

CREATE TABLE IF NOT EXISTS user_quests (
    -- Primary identification
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES smartprofiles(user_id) ON DELETE CASCADE,
    quest_id UUID NOT NULL REFERENCES learning_quests(id) ON DELETE CASCADE,
    
    -- Timing
    started_at TIMESTAMP DEFAULT NOW(),
    completed_at TIMESTAMP,
    time_taken_minutes INTEGER,
    
    -- Submissions
    submissions JSONB DEFAULT '[]'::jsonb,  -- Array of essay submissions for quest
    
    -- Results
    final_score FLOAT,
    performance_breakdown JSONB,
    
    -- Status
    status VARCHAR(20) DEFAULT 'in_progress' CHECK (status IN (
        'in_progress', 'completed', 'abandoned', 'failed'
    )),
    
    -- Rewards
    points_earned INTEGER DEFAULT 0,
    badges_earned TEXT[] DEFAULT ARRAY[]::TEXT[],
    features_unlocked TEXT[] DEFAULT ARRAY[]::TEXT[],
    
    -- Attempts (for retryable quests)
    attempt_number INTEGER DEFAULT 1,
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Indexes for user_quests table
CREATE INDEX idx_user_quests_user ON user_quests(user_id);
CREATE INDEX idx_user_quests_quest ON user_quests(quest_id);
CREATE INDEX idx_user_quests_status ON user_quests(status);
CREATE INDEX idx_user_quests_completed ON user_quests(completed_at);

-- Comment
COMMENT ON TABLE user_quests IS 'v10.0.0: User progress on learning quests';

-- ========================================
-- 10. ESSAY_SUBMISSIONS TABLE (v10.0.0)
-- Comprehensive essay submission history
-- ========================================

CREATE TABLE IF NOT EXISTS essay_submissions (
    -- Primary identification
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES smartprofiles(user_id) ON DELETE CASCADE,
    license_key VARCHAR(50) REFERENCES licenses(license_key) ON DELETE CASCADE,
    
    -- Essay content
    essay_text TEXT NOT NULL,
    word_count INTEGER NOT NULL,
    
    -- Grading results
    overall_score DECIMAL(5,2),
    rubric_scores JSONB,  -- Knowledge, Thinking, Communication, Application
    
    -- v10.0.0: Logic 5.0 Neural Reasoning results
    logic_5_analysis JSONB,
    creativity_metrics JSONB,
    
    -- v10.0.0: EmotionFlow 2.0 results
    emotionflow_analysis JSONB,
    
    -- Feedback
    inline_feedback JSONB,
    vocabulary_suggestions JSONB,
    grammar_corrections JSONB,
    
    -- Metadata
    grade_level INTEGER,
    essay_type VARCHAR(50),
    language VARCHAR(10) DEFAULT 'en',
    
    -- Version tracking
    draft_version INTEGER DEFAULT 1,
    parent_submission_id UUID REFERENCES essay_submissions(id),
    
    -- Timestamps
    submitted_at TIMESTAMP DEFAULT NOW(),
    graded_at TIMESTAMP,
    
    -- Processing
    processing_time_ms INTEGER
);

-- Indexes for essay_submissions table
CREATE INDEX idx_essay_submissions_user ON essay_submissions(user_id);
CREATE INDEX idx_essay_submissions_license ON essay_submissions(license_key);
CREATE INDEX idx_essay_submissions_submitted ON essay_submissions(submitted_at);
CREATE INDEX idx_essay_submissions_parent ON essay_submissions(parent_submission_id);

-- Comment
COMMENT ON TABLE essay_submissions IS 'v10.0.0: Complete essay submission and grading history';

-- ========================================
-- 11. TEACHER_CLASSES TABLE (v10.0.0)
-- Teacher Suite: Class management
-- ========================================

CREATE TABLE IF NOT EXISTS teacher_classes (
    -- Primary identification
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    teacher_license_key VARCHAR(50) NOT NULL REFERENCES licenses(license_key) ON DELETE CASCADE,
    
    -- Class information
    class_name VARCHAR(255) NOT NULL,
    class_code VARCHAR(20) UNIQUE NOT NULL,
    grade_level INTEGER,
    subject VARCHAR(100),
    
    -- Academic period
    academic_year VARCHAR(20),
    semester VARCHAR(20),
    
    -- Settings
    class_settings JSONB DEFAULT '{}'::jsonb,
    
    -- LMS integration
    lms_type VARCHAR(50),  -- canvas, moodle, google_classroom, teams, blackboard, schoology
    lms_course_id VARCHAR(255),
    lms_sync_enabled BOOLEAN DEFAULT FALSE,
    
    -- Status
    is_active BOOLEAN DEFAULT TRUE,
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Indexes for teacher_classes table
CREATE INDEX idx_teacher_classes_teacher ON teacher_classes(teacher_license_key);
CREATE INDEX idx_teacher_classes_code ON teacher_classes(class_code);
CREATE INDEX idx_teacher_classes_lms ON teacher_classes(lms_type, lms_course_id);

-- Comment
COMMENT ON TABLE teacher_classes IS 'v10.0.0: Teacher Suite class management';

-- ========================================
-- 12. CLASS_STUDENTS TABLE (v10.0.0)
-- Student enrollment in teacher classes
-- ========================================

CREATE TABLE IF NOT EXISTS class_students (
    -- Primary identification
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    class_id UUID NOT NULL REFERENCES teacher_classes(id) ON DELETE CASCADE,
    student_user_id UUID REFERENCES smartprofiles(user_id) ON DELETE CASCADE,
    
    -- Student information
    student_email VARCHAR(255) NOT NULL,
    student_name VARCHAR(255),
    
    -- Enrollment
    enrolled_at TIMESTAMP DEFAULT NOW(),
    enrollment_status VARCHAR(20) DEFAULT 'active' CHECK (enrollment_status IN (
        'active', 'inactive', 'withdrawn', 'completed'
    )),
    
    -- Parent access
    parent_email VARCHAR(255),
    parent_access_enabled BOOLEAN DEFAULT FALSE,
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    
    -- Unique constraint
    UNIQUE(class_id, student_email)
);

-- Indexes for class_students table
CREATE INDEX idx_class_students_class ON class_students(class_id);
CREATE INDEX idx_class_students_user ON class_students(student_user_id);
CREATE INDEX idx_class_students_email ON class_students(student_email);

-- Comment
COMMENT ON TABLE class_students IS 'v10.0.0: Student enrollment in teacher classes';

-- ========================================
-- TRIGGERS
-- Automatic timestamp updates
-- ========================================

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Apply to all tables with updated_at column
CREATE TRIGGER update_licenses_updated_at BEFORE UPDATE ON licenses
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_usage_updated_at BEFORE UPDATE ON usage
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_smartprofiles_updated_at BEFORE UPDATE ON smartprofiles
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_micro_missions_updated_at BEFORE UPDATE ON micro_missions
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_user_missions_updated_at BEFORE UPDATE ON user_missions
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_learning_quests_updated_at BEFORE UPDATE ON learning_quests
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_user_quests_updated_at BEFORE UPDATE ON user_quests
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_teacher_classes_updated_at BEFORE UPDATE ON teacher_classes
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_class_students_updated_at BEFORE UPDATE ON class_students
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ========================================
-- SAMPLE DATA
-- Example records for testing
-- ========================================

-- Sample free trial license
INSERT INTO licenses (license_key, user_type, user_email, custom_name, expires_at, daily_limit, features)
VALUES (
    'DUOE10-FT00-SMPL-TEST-KEYF1234',
    'free_trial',
    'trial@example.com',
    'Sample Free Trial',
    NOW() + INTERVAL '7 days',
    35,
    '["basic_grading", "neural_rubric", "score_breakdown"]'::jsonb
) ON CONFLICT (license_key) DO NOTHING;

-- Sample student premium license
INSERT INTO licenses (license_key, user_type, user_email, custom_name, expires_at, daily_limit, features)
VALUES (
    'DUOE10-SP02-PREM-STUD-KEYA5678',
    'student_premium',
    'premium@example.com',
    'Sample Premium Student',
    NOW() + INTERVAL '30 days',
    100,
    '["logic_5_neural_reasoning", "smartprofile_3", "realtime_mentor_3", "emotionflow_2", "visual_analytics_3", "voice_assistance", "gamification_full", "creativity_metrics", "multilingual_full"]'::jsonb
) ON CONFLICT (license_key) DO NOTHING;

-- ========================================
-- VIEWS
-- Convenient views for common queries
-- ========================================

-- Active licenses view
CREATE OR REPLACE VIEW active_licenses AS
SELECT 
    license_key,
    user_type,
    user_email,
    custom_name,
    daily_limit,
    issued_at,
    expires_at,
    EXTRACT(DAY FROM (expires_at - NOW())) AS days_remaining
FROM licenses
WHERE is_active = TRUE AND expires_at > NOW()
ORDER BY expires_at ASC;

-- User statistics view
CREATE OR REPLACE VIEW user_statistics AS
SELECT 
    sp.user_id,
    sp.user_email,
    sp.total_essays,
    sp.average_score,
    sp.total_points,
    sp.current_level,
    sp.streak_days,
    sp.micro_missions_completed,
    ARRAY_LENGTH(sp.achievements, 1) AS total_achievements,
    l.user_type AS license_tier
FROM smartprofiles sp
LEFT JOIN licenses l ON sp.license_key = l.license_key;

-- Today's usage summary
CREATE OR REPLACE VIEW todays_usage AS
SELECT 
    u.license_key,
    l.user_email,
    l.user_type,
    u.usage_count,
    l.daily_limit,
    l.daily_limit - u.usage_count AS remaining_essays
FROM usage u
JOIN licenses l ON u.license_key = l.license_key
WHERE u.usage_date = CURRENT_DATE
ORDER BY u.usage_count DESC;

-- ========================================
-- COMPLETION
-- ========================================

-- Grant permissions (adjust as needed for your setup)
-- GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO your_app_user;
-- GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO your_app_user;

-- Display summary
DO $$
BEGIN
    RAISE NOTICE '========================================';
    RAISE NOTICE 'DouEssay v10.0.0 - Project Apex';
    RAISE NOTICE 'Database Schema Installation Complete';
    RAISE NOTICE '========================================';
    RAISE NOTICE 'Created Tables:';
    RAISE NOTICE '  1. licenses - License key management';
    RAISE NOTICE '  2. usage - Daily usage tracking';
    RAISE NOTICE '  3. smartprofiles - SmartProfile 3.0 (30+ dimensions)';
    RAISE NOTICE '  4. micro_missions - Daily micro-missions';
    RAISE NOTICE '  5. user_missions - User mission progress';
    RAISE NOTICE '  6. user_achievements - Achievement badges';
    RAISE NOTICE '  7. leaderboards - Gamification leaderboards';
    RAISE NOTICE '  8. learning_quests - Learning quests';
    RAISE NOTICE '  9. user_quests - User quest progress';
    RAISE NOTICE '  10. essay_submissions - Essay history';
    RAISE NOTICE '  11. teacher_classes - Teacher class management';
    RAISE NOTICE '  12. class_students - Class enrollment';
    RAISE NOTICE '';
    RAISE NOTICE 'Created Views:';
    RAISE NOTICE '  - active_licenses';
    RAISE NOTICE '  - user_statistics';
    RAISE NOTICE '  - todays_usage';
    RAISE NOTICE '';
    RAISE NOTICE 'Sample data inserted for testing';
    RAISE NOTICE '========================================';
END $$;
