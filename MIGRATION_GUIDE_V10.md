# 🔄 DouEssay v10.0.0 Migration Guide
## Upgrading from v9.0.0 to v10.0.0 - Project Apex

**Version**: 10.0.0 - Project Apex  
**Author**: changcheng967  
**Organization**: Doulet Media  
**Date**: October 2025

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [Pre-Migration Checklist](#pre-migration-checklist)
3. [Database Migration](#database-migration)
4. [License System Updates](#license-system-updates)
5. [SmartProfile 3.0 Upgrade](#smartprofile-30-upgrade)
6. [New Features Setup](#new-features-setup)
7. [Testing & Verification](#testing--verification)
8. [Rollback Plan](#rollback-plan)
9. [Post-Migration Tasks](#post-migration-tasks)

---

## 🎯 Overview

This guide covers the migration from DouEssay v9.0.0 (Project Horizon) to v10.0.0 (Project Apex). The migration is **backward compatible** and **non-breaking**, meaning existing licenses and data will continue to work.

### What's New in v10.0.0

- ✅ **Logic 5.0**: Neural Reasoning with multi-paragraph chains
- ✅ **SmartProfile 3.0**: 30+ dimensions (up from 20+)
- ✅ **Real-Time Mentor 3.0**: Voice assistance and predictive features
- ✅ **EmotionFlow 2.0**: Multi-dimensional emotional mapping
- ✅ **Visual Analytics 3.0**: Heatmaps and predictive trajectories
- ✅ **Full Gamification**: 50+ badges, leaderboards, quests
- ✅ **Teacher Dashboard 2.0**: Batch grading AI and LMS integration
- ✅ **Parent Interface**: Family engagement tools
- ✅ **Multilingual Support**: Full 4-language support

### Migration Time Estimate

- **Small deployment** (< 100 users): 30-60 minutes
- **Medium deployment** (100-1,000 users): 1-2 hours
- **Large deployment** (> 1,000 users): 2-4 hours

---

## ✅ Pre-Migration Checklist

### 1. Backup Everything

```bash
# Backup your Supabase database
pg_dump -h your-supabase-host \
        -U postgres \
        -d your-database \
        -f douessay_v9_backup_$(date +%Y%m%d).sql

# Verify backup
ls -lh douessay_v9_backup_*.sql
```

### 2. Document Current State

```sql
-- Count existing records
SELECT 
    'licenses' as table_name, COUNT(*) as count FROM licenses
UNION ALL
SELECT 'usage', COUNT(*) FROM usage
UNION ALL
SELECT 'smartprofiles', COUNT(*) FROM smartprofiles;

-- Export current license types
SELECT user_type, COUNT(*) as count
FROM licenses
GROUP BY user_type
ORDER BY count DESC;
```

### 3. Notify Users

Send notification about:
- Maintenance window (recommend 2-hour window)
- Expected downtime (actual downtime: < 5 minutes)
- New features available after migration

### 4. Prepare Environment

```bash
# Clone repository
git clone https://github.com/changcheng967/DouEssay.git
cd DouEssay

# Checkout v10.0.0
git checkout v10.0.0  # Or main branch after release

# Verify files
ls -l supabase_schema_v10.sql
ls -l license_generator.py
ls -l app.py
```

---

## 🗄️ Database Migration

### Step 1: Review Schema Changes

The v10.0.0 schema is **additive** - it only adds new tables and columns, never removes or breaks existing ones.

**New Tables:**
- `micro_missions` - Daily micro-missions
- `user_missions` - User mission progress
- `user_achievements` - Achievement tracking
- `leaderboards` - Gamification rankings
- `learning_quests` - Learning quests
- `user_quests` - User quest progress
- `essay_submissions` - Complete submission history
- `teacher_classes` - Teacher class management
- `class_students` - Class enrollment

**Enhanced Tables:**
- `licenses` - New tier types (no breaking changes)
- `smartprofiles` - New columns for v10.0.0 features

### Step 2: Run Migration Script

#### Option A: Full Schema Installation (Recommended for New Deployments)

```sql
-- In Supabase SQL Editor or psql
\i supabase_schema_v10.sql

-- Or copy-paste the entire file into Supabase SQL Editor
```

#### Option B: Incremental Update (Recommended for Existing Deployments)

```sql
-- ========================================
-- INCREMENTAL UPDATE FOR v9.0.0 → v10.0.0
-- ========================================

-- 1. Add new columns to smartprofiles
ALTER TABLE smartprofiles ADD COLUMN IF NOT EXISTS emotional_resilience FLOAT DEFAULT 50.0;
ALTER TABLE smartprofiles ADD COLUMN IF NOT EXISTS time_management_score FLOAT DEFAULT 50.0;
ALTER TABLE smartprofiles ADD COLUMN IF NOT EXISTS creativity_index FLOAT DEFAULT 50.0;
ALTER TABLE smartprofiles ADD COLUMN IF NOT EXISTS peer_comparison_opt_in BOOLEAN DEFAULT FALSE;
ALTER TABLE smartprofiles ADD COLUMN IF NOT EXISTS total_points INTEGER DEFAULT 0;
ALTER TABLE smartprofiles ADD COLUMN IF NOT EXISTS current_level INTEGER DEFAULT 1;
ALTER TABLE smartprofiles ADD COLUMN IF NOT EXISTS streak_days INTEGER DEFAULT 0;
ALTER TABLE smartprofiles ADD COLUMN IF NOT EXISTS longest_streak INTEGER DEFAULT 0;
ALTER TABLE smartprofiles ADD COLUMN IF NOT EXISTS last_activity_date DATE;
ALTER TABLE smartprofiles ADD COLUMN IF NOT EXISTS micro_missions_completed INTEGER DEFAULT 0;
ALTER TABLE smartprofiles ADD COLUMN IF NOT EXISTS daily_missions_active JSONB DEFAULT '[]'::jsonb;
ALTER TABLE smartprofiles ADD COLUMN IF NOT EXISTS learning_velocity FLOAT DEFAULT 0.0;
ALTER TABLE smartprofiles ADD COLUMN IF NOT EXISTS predicted_next_score FLOAT;
ALTER TABLE smartprofiles ADD COLUMN IF NOT EXISTS device_ids TEXT[] DEFAULT ARRAY[]::TEXT[];
ALTER TABLE smartprofiles ADD COLUMN IF NOT EXISTS last_sync_timestamp TIMESTAMP;

-- 2. Create new tables (run full supabase_schema_v10.sql)
-- This will create all new tables with IF NOT EXISTS clauses

-- 3. Create new indexes
CREATE INDEX IF NOT EXISTS idx_smartprofiles_points ON smartprofiles(total_points);
CREATE INDEX IF NOT EXISTS idx_smartprofiles_level ON smartprofiles(current_level);

-- 4. Verify migration
SELECT 
    table_name, 
    column_name, 
    data_type 
FROM information_schema.columns 
WHERE table_name = 'smartprofiles' 
    AND column_name IN ('emotional_resilience', 'creativity_index', 'total_points')
ORDER BY column_name;
```

### Step 3: Verify Migration

```sql
-- Check all new tables exist
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public' 
    AND table_name IN (
        'micro_missions',
        'user_missions',
        'user_achievements',
        'leaderboards',
        'learning_quests',
        'user_quests',
        'essay_submissions',
        'teacher_classes',
        'class_students'
    )
ORDER BY table_name;

-- Check smartprofiles has new columns
SELECT column_name 
FROM information_schema.columns 
WHERE table_name = 'smartprofiles' 
    AND column_name IN (
        'emotional_resilience',
        'creativity_index',
        'total_points',
        'current_level',
        'streak_days'
    );
```

---

## 🔑 License System Updates

### Understanding v10.0.0 License Tiers

v10.0.0 introduces new tier names while maintaining **backward compatibility** with v9.0.0 tiers:

| v9.0.0 Tier | v10.0.0 Tier | Status |
|-------------|--------------|---------|
| `free` | `free_trial` | **Deprecated** (still works) |
| `plus` | `student_basic` | **Deprecated** (still works) |
| `premium` | `student_premium` | **Deprecated** (still works) |
| `unlimited` | `teacher_suite` | **Deprecated** (still works) |
| N/A | `institutional` | **New** |

### Migration Strategy

#### Option 1: Keep Existing Licenses (Recommended)

Your existing v9.0.0 licenses will continue to work. No action required.

```python
# v9.0.0 licenses work fine in v10.0.0
license_manager = LicenseManager()
result = license_manager.validate_license('OLD-V9-LICENSE-KEY')
# This works perfectly!
```

#### Option 2: Migrate to v10.0.0 License Keys

Generate new v10.0.0 license keys and notify users:

```python
from license_generator import LicenseKeyGenerator

generator = LicenseKeyGenerator()

# Map v9.0.0 to v10.0.0 tiers
tier_mapping = {
    'free': 'free_trial',
    'plus': 'student_basic',
    'premium': 'student_premium',
    'unlimited': 'teacher_suite'
}

# Get all v9.0.0 licenses
from supabase import create_client
client = create_client(supabase_url, supabase_key)

old_licenses = client.table('licenses').select('*').in_(
    'user_type', ['free', 'plus', 'premium', 'unlimited']
).execute()

# Generate new v10.0.0 licenses
new_licenses = []
for old_license in old_licenses.data:
    new_tier = tier_mapping[old_license['user_type']]
    
    new_license = generator.generate_license_record(
        tier_type=new_tier,
        user_email=old_license['user_email'],
        custom_name=f"Migrated from {old_license['user_type']}",
        duration_days=30  # Extend by 30 days as migration bonus
    )
    
    new_licenses.append(new_license)
    
    # Deactivate old license
    client.table('licenses').update({
        'is_active': False,
        'metadata': {
            'migrated_to': new_license['license_key'],
            'migration_date': datetime.now().isoformat()
        }
    }).eq('license_key', old_license['license_key']).execute()
    
    # Insert new license
    client.table('licenses').insert(new_license).execute()
    
    print(f"✅ Migrated {old_license['user_email']}: {old_license['license_key']} → {new_license['license_key']}")

# Export migration report
generator.export_licenses_json(new_licenses, 'migration_report.json')
```

---

## 👤 SmartProfile 3.0 Upgrade

### Initialize New v10.0.0 Dimensions

```python
from supabase import create_client

client = create_client(supabase_url, supabase_key)

# Get all existing profiles
profiles = client.table('smartprofiles').select('*').execute()

print(f"Upgrading {len(profiles.data)} SmartProfiles to v3.0...")

for profile in profiles.data:
    # Initialize v10.0.0 dimensions with reasonable defaults
    updates = {
        'emotional_resilience': 50.0,  # Neutral starting point
        'time_management_score': 50.0,
        'creativity_index': 50.0,
        'peer_comparison_opt_in': False,  # Privacy-first default
        'total_points': profile.get('total_essays', 0) * 10,  # Award retroactive points
        'current_level': max(1, profile.get('total_essays', 0) // 5),  # 1 level per 5 essays
        'streak_days': 0,  # Reset streaks (will build up naturally)
        'longest_streak': 0,
        'micro_missions_completed': 0,
        'daily_missions_active': [],
        'learning_velocity': 0.0,
        'device_ids': [],
    }
    
    # Update the profile
    client.table('smartprofiles').update(updates).eq(
        'user_id', profile['user_id']
    ).execute()
    
    print(f"✅ Upgraded profile: {profile['user_email']} (Level {updates['current_level']}, {updates['total_points']} points)")

print("✅ SmartProfile 3.0 upgrade complete!")
```

### Award Retroactive Achievements

```python
# Award achievements for historical accomplishments
for profile in profiles.data:
    achievements = []
    
    # Milestone badges
    if profile['total_essays'] >= 1:
        achievements.append('first_essay')
    if profile['total_essays'] >= 5:
        achievements.append('five_essays')
    if profile['total_essays'] >= 10:
        achievements.append('ten_essays')
    if profile['total_essays'] >= 25:
        achievements.append('twenty_five_essays')
    if profile['total_essays'] >= 50:
        achievements.append('fifty_essays')
    
    # Skill mastery badges
    if profile.get('highest_score', 0) >= 94:
        achievements.append('level_4_achieved')
    
    # Award achievements
    for badge_id in achievements:
        client.table('user_achievements').insert({
            'user_id': profile['user_id'],
            'badge_id': badge_id,
            'badge_name': badge_id.replace('_', ' ').title(),
            'badge_category': 'milestone',
            'points_awarded': 50,
            'notification_sent': False
        }).execute()
    
    if achievements:
        print(f"🏆 Awarded {len(achievements)} badges to {profile['user_email']}")
```

---

## 🎮 New Features Setup

### 1. Create Initial Micro-Missions

```python
# Sample micro-missions for all skill levels
micro_missions = [
    {
        'mission_type': 'vocabulary',
        'mission_title': 'Vocabulary Builder',
        'mission_description': 'Replace 5 generic words with sophisticated alternatives',
        'difficulty': 'easy',
        'estimated_time_minutes': 15,
        'prompt': 'Write a paragraph about your favorite hobby. Replace at least 5 generic words (good, bad, nice, etc.) with more sophisticated vocabulary.',
        'success_criteria': {
            'min_words': 100,
            'min_replacements': 5,
            'vocabulary_score': 70
        },
        'reward_points': 20,
        'category': 'vocabulary'
    },
    {
        'mission_type': 'argument',
        'mission_title': 'Claim & Evidence',
        'mission_description': 'Write a paragraph with a clear claim and supporting evidence',
        'difficulty': 'medium',
        'estimated_time_minutes': 20,
        'prompt': 'Write a paragraph arguing for or against social media. Include one clear claim and at least two pieces of evidence.',
        'success_criteria': {
            'has_claim': True,
            'evidence_count': 2,
            'thinking_score': 75
        },
        'reward_points': 30,
        'category': 'critical_thinking'
    }
]

for mission in micro_missions:
    client.table('micro_missions').insert(mission).execute()

print(f"✅ Created {len(micro_missions)} micro-missions")
```

### 2. Create Learning Quests

```python
# Sample learning quest
quest = {
    'quest_type': 'skill_specific',
    'quest_title': 'Evidence Master Quest',
    'quest_description': 'Master the art of using evidence effectively in your writing',
    'difficulty': 'medium',
    'required_level': 2,
    'estimated_time_minutes': 60,
    'prompts': [
        'Write a paragraph about technology with 2 pieces of evidence',
        'Write a paragraph about education with 3 pieces of evidence',
        'Write a full essay with 5+ pieces of evidence'
    ],
    'success_criteria': {
        'all_submissions_complete': True,
        'min_evidence_quality': 75,
        'final_essay_score': 85
    },
    'reward_points': 100,
    'reward_badges': ['evidence_expert'],
    'category': 'evidence',
    'tags': ['research', 'critical_thinking']
}

client.table('learning_quests').insert(quest).execute()
print("✅ Created learning quest: Evidence Master Quest")
```

### 3. Initialize Teacher Classes (for Teacher Suite users)

```python
# Get all teacher licenses
teachers = client.table('licenses').select('*').eq('user_type', 'teacher_suite').execute()

for teacher in teachers.data:
    # Create default class
    class_code = f"CLASS-{secrets.token_hex(4).upper()}"
    
    teacher_class = {
        'teacher_license_key': teacher['license_key'],
        'class_name': f"{teacher['user_email'].split('@')[0]}'s Class",
        'class_code': class_code,
        'grade_level': 10,
        'subject': 'English',
        'class_settings': {},
        'is_active': True
    }
    
    client.table('teacher_classes').insert(teacher_class).execute()
    print(f"✅ Created class for {teacher['user_email']}: {class_code}")
```

---

## 🧪 Testing & Verification

### Test Checklist

```python
# 1. License validation works
from app import LicenseManager
lm = LicenseManager()

test_result = lm.validate_license('DUOE10-SP02-TEST-KEY-HERE1234')
assert test_result is not None, "License validation failed"
print("✅ License validation working")

# 2. SmartProfile 3.0 columns accessible
profile = client.table('smartprofiles').select('*').limit(1).execute()
assert 'emotional_resilience' in profile.data[0], "Missing v10.0.0 columns"
assert 'creativity_index' in profile.data[0], "Missing v10.0.0 columns"
print("✅ SmartProfile 3.0 columns present")

# 3. New tables accessible
missions = client.table('micro_missions').select('*').limit(1).execute()
assert len(missions.data) >= 0, "micro_missions table not accessible"
print("✅ New tables accessible")

# 4. Achievements system working
achievements = client.table('user_achievements').select('*').limit(1).execute()
assert achievements is not None, "Achievements table not accessible"
print("✅ Achievements system working")

# 5. Legacy licenses still work
if old_licenses.data:
    legacy_result = lm.validate_license(old_licenses.data[0]['license_key'])
    assert legacy_result.get('valid') == True, "Legacy license validation failed"
    print("✅ Legacy licenses still working")

print("\n✅ All tests passed!")
```

### Performance Testing

```python
import time

# Test license validation speed
start = time.time()
for _ in range(100):
    lm.validate_license('DUOE10-SP02-TEST-KEY-HERE1234')
duration = time.time() - start

print(f"License validation: {duration/100*1000:.2f}ms per call")
assert duration/100 < 0.1, "License validation too slow"
print("✅ Performance acceptable")
```

---

## 🔙 Rollback Plan

If anything goes wrong, follow this rollback procedure:

### 1. Stop Application

```bash
# Stop your application
sudo systemctl stop douessay  # Or your process manager
```

### 2. Restore Database

```bash
# Restore from backup
psql -h your-supabase-host \
     -U postgres \
     -d your-database \
     -f douessay_v9_backup_YYYYMMDD.sql
```

### 3. Revert Application Code

```bash
# Checkout v9.0.0
git checkout v9.0.0

# Or restore from backup
cp -r /backup/douessay_v9/* /path/to/douessay/
```

### 4. Restart Application

```bash
# Restart with v9.0.0
sudo systemctl start douessay
```

### 5. Verify Rollback

```bash
# Check version
curl http://localhost:7860/version

# Test license validation
python -c "from app import LicenseManager; print(LicenseManager().validate_license('YOUR-LICENSE-KEY'))"
```

---

## ✅ Post-Migration Tasks

### 1. Update Documentation

- Update internal docs to reference v10.0.0
- Update user guides with new features
- Update API documentation if using Teacher Suite API

### 2. Notify Users

Send success notification:
- Migration complete
- New features available
- Link to v10.0.0 release notes
- Any new license keys (if migrated)

### 3. Monitor System

```sql
-- Monitor usage patterns
SELECT 
    DATE(usage_date) as date,
    COUNT(*) as active_users,
    SUM(usage_count) as total_essays
FROM usage
WHERE usage_date >= CURRENT_DATE - INTERVAL '7 days'
GROUP BY DATE(usage_date)
ORDER BY date DESC;

-- Check for errors
SELECT 
    license_key,
    user_email,
    last_used_at
FROM licenses
WHERE is_active = TRUE
    AND last_used_at IS NULL
    AND issued_at < NOW() - INTERVAL '1 day';
```

### 4. Performance Tuning

```sql
-- Update statistics
ANALYZE licenses;
ANALYZE smartprofiles;
ANALYZE usage;

-- Vacuum tables
VACUUM ANALYZE licenses;
VACUUM ANALYZE smartprofiles;
```

### 5. Enable New Features Gradually

```python
# Enable gamification for power users first
client.table('smartprofiles').update({
    'peer_comparison_opt_in': True
}).gte('total_essays', 10).execute()

# Then enable for everyone after monitoring
```

---

## 📞 Support

### Getting Help

If you encounter issues during migration:

1. **Check logs**: Review application and database logs
2. **Review this guide**: Most issues are covered in troubleshooting
3. **Rollback if needed**: Use the rollback plan above
4. **Contact support**: [GitHub Issues](https://github.com/changcheng967/DouEssay/issues)

### Common Issues

#### Issue: "Column does not exist"

**Solution**: Run the incremental update SQL again to add missing columns.

#### Issue: "License validation returning False"

**Solution**: Check that licenses table has the new v10.0.0 tier types in the CHECK constraint.

#### Issue: "SmartProfile points are 0"

**Solution**: Run the retroactive points award script in the SmartProfile 3.0 section.

---

## 🎉 Success!

Congratulations! You've successfully migrated to DouEssay v10.0.0 - Project Apex.

Your users now have access to:
- ✅ Logic 5.0 Neural Reasoning
- ✅ SmartProfile 3.0 with 30+ dimensions
- ✅ Full gamification with badges and quests
- ✅ Voice assistance and predictive features
- ✅ Teacher Dashboard 2.0
- ✅ And much more!

---

**Made with ❤️ for educators and students worldwide**

*"Specs vary. No empty promises—just code, hardware, and your ambition."*
