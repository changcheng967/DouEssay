# 🔑 DouEssay v10.0.0 - License Key Generator
## Complete Guide & Documentation

**Version**: 10.0.0 - Project Apex  
**Author**: changcheng967  
**Organization**: Doulet Media

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [Installation](#installation)
3. [Quick Start](#quick-start)
4. [Tier Types](#tier-types)
5. [Usage Examples](#usage-examples)
6. [API Reference](#api-reference)
7. [Integration with Supabase](#integration-with-supabase)
8. [Migration from v9.0.0](#migration-from-v900)
9. [Security Considerations](#security-considerations)
10. [Troubleshooting](#troubleshooting)

---

## 🎯 Overview

The DouEssay v10.0.0 License Key Generator is a comprehensive tool for creating, validating, and managing license keys for all DouEssay tier types. It generates secure, unique license keys with built-in validation and integrates seamlessly with the Supabase backend.

### Key Features

- ✅ **Secure Key Generation**: Cryptographically secure random keys with checksums
- ✅ **Multi-Tier Support**: Free Trial, Student Basic, Student Premium, Teacher Suite, Institutional
- ✅ **Batch Generation**: Create multiple licenses at once
- ✅ **Format Validation**: Built-in key format verification
- ✅ **JSON Export**: Export licenses for easy import
- ✅ **100% Compatible**: Works with DouEssay v10.0.0 app.py and Supabase schema

---

## 💻 Installation

### Prerequisites

- Python 3.8 or higher
- No external dependencies required (uses standard library only)

### Setup

1. Clone the repository or download `license_generator.py`:
```bash
git clone https://github.com/changcheng967/DouEssay.git
cd DouEssay
```

2. Make the script executable (optional):
```bash
chmod +x license_generator.py
```

3. Run the generator:
```bash
python license_generator.py
```

---

## 🚀 Quick Start

### Generate a Single License

```python
from license_generator import LicenseKeyGenerator

# Initialize the generator
generator = LicenseKeyGenerator()

# Generate a Student Premium license
license = generator.generate_license_record(
    tier_type='student_premium',
    user_email='student@example.com',
    custom_name='My Premium License'
)

# Print the license details
generator.print_license_summary(license)
```

### Generate Batch Licenses

```python
# Generate 10 Free Trial licenses
batch = generator.generate_batch_licenses(
    tier_type='free_trial',
    count=10,
    base_email='trial'
)

# Export to JSON
generator.export_licenses_json(batch, 'free_trials.json')
```

### Validate a License Key

```python
# Check if a key has valid format
key = "DUOE10-SP02-PREM-STUD-KEYA5678"
is_valid = generator.validate_key_format(key)
tier = generator.get_tier_from_key(key)

print(f"Valid: {is_valid}, Tier: {tier}")
```

---

## 🎓 Tier Types

### Free Trial
- **Duration**: 7 days
- **Daily Limit**: 35 essays (~5 per week)
- **Price**: $0.00
- **Features**: Basic grading, Logic 5.0 (basic), score breakdown
- **Key Format**: `DUOE10-FT00-XXXX-XXXX-XXXXXXXX`

### Student Basic
- **Duration**: 30 days (monthly)
- **Daily Limit**: 25 essays
- **Price**: $7.99/month
- **Features**: Full Logic 5.0, SmartProfile 3.0, Real-Time Mentor 3.0, EmotionFlow 2.0, gamification, creativity metrics, multilingual
- **Key Format**: `DUOE10-SB01-XXXX-XXXX-XXXXXXXX`

### Student Premium
- **Duration**: 30 days (monthly)
- **Daily Limit**: 100 essays
- **Price**: $12.99/month
- **Features**: All Student Basic + Visual Analytics 3.0, voice assistance, full gamification with leaderboards
- **Key Format**: `DUOE10-SP02-XXXX-XXXX-XXXXXXXX`

### Teacher Suite
- **Duration**: 30 days (monthly)
- **Daily Limit**: Unlimited
- **Price**: $29.99/month
- **Features**: All Premium + Teacher Dashboard 2.0, batch grading AI, parent interface, LMS integration, API access
- **Key Format**: `DUOE10-TS03-XXXX-XXXX-XXXXXXXX`

### Institutional
- **Duration**: 365 days (annual)
- **Daily Limit**: Unlimited (customizable)
- **Price**: Custom
- **Features**: All Teacher Suite + institutional admin, district analytics, custom configuration
- **Key Format**: `DUOE10-IN04-XXXX-XXXX-XXXXXXXX`

---

## 📚 Usage Examples

### Example 1: Single License with Custom Duration

```python
generator = LicenseKeyGenerator()

# Generate a 90-day Student Premium license
license = generator.generate_license_record(
    tier_type='student_premium',
    user_email='longterm@example.com',
    custom_name='3-Month Premium',
    duration_days=90
)

print(f"License Key: {license['license_key']}")
print(f"Expires: {license['expires_at']}")
```

### Example 2: Institutional License with Custom Limits

```python
# School district with custom daily limit
school_license = generator.generate_license_record(
    tier_type='institutional',
    user_email='admin@district.edu',
    custom_name='Springfield School District',
    duration_days=365,
    custom_daily_limit=10000  # 10,000 essays per day
)

generator.print_license_summary(school_license)
```

### Example 3: Batch Generation for Class

```python
# Generate 30 free trials for a class
class_trials = generator.generate_batch_licenses(
    tier_type='free_trial',
    count=30,
    base_email='student',
    duration_days=14  # Extended to 14 days
)

# Save to file
generator.export_licenses_json(class_trials, 'class_trials.json')
print(f"Generated {len(class_trials)} licenses")
```

### Example 4: Mix of Tier Types

```python
# Generate licenses for different user types
licenses = []

# 5 free trials
licenses.extend(generator.generate_batch_licenses('free_trial', 5))

# 10 student basic
licenses.extend(generator.generate_batch_licenses('student_basic', 10))

# 3 student premium
licenses.extend(generator.generate_batch_licenses('student_premium', 3))

# 1 teacher suite
licenses.append(generator.generate_license_record(
    'teacher_suite',
    'teacher@school.edu'
))

# Export all
generator.export_licenses_json(licenses, 'mixed_licenses.json')
```

### Example 5: Validation Workflow

```python
# Generate a key
key = generator.generate_key('student_premium')

# Validate format
if generator.validate_key_format(key):
    print(f"✅ Valid key: {key}")
    
    # Get tier information
    tier = generator.get_tier_from_key(key)
    tier_info = generator.TIER_TYPES[tier]
    
    print(f"Tier: {tier_info['name']}")
    print(f"Daily Limit: {tier_info['daily_limit']}")
    print(f"Price: ${tier_info['price']}/month")
else:
    print("❌ Invalid key format")
```

---

## 🔧 API Reference

### Class: `LicenseKeyGenerator`

#### Methods

##### `generate_key(tier_type: str, custom_name: Optional[str] = None) -> str`

Generate a secure license key for the specified tier.

**Parameters:**
- `tier_type` (str): One of 'free_trial', 'student_basic', 'student_premium', 'teacher_suite', 'institutional'
- `custom_name` (str, optional): Custom identifier for the license

**Returns:**
- `str`: License key in format `DUOE10-XXXX-XXXX-XXXX-XXXXXXXX`

**Example:**
```python
key = generator.generate_key('student_premium')
# Output: DUOE10-SP02-A3B4-C5D6-E7F8G9H0
```

---

##### `validate_key_format(license_key: str) -> bool`

Validate the format of a license key (does not check database).

**Parameters:**
- `license_key` (str): The license key to validate

**Returns:**
- `bool`: True if format is valid, False otherwise

**Example:**
```python
is_valid = generator.validate_key_format('DUOE10-SP02-A3B4-C5D6-E7F8G9H0')
```

---

##### `get_tier_from_key(license_key: str) -> Optional[str]`

Extract the tier type from a license key.

**Parameters:**
- `license_key` (str): The license key to parse

**Returns:**
- `str` or `None`: Tier type string or None if invalid

**Example:**
```python
tier = generator.get_tier_from_key('DUOE10-SP02-A3B4-C5D6-E7F8G9H0')
# Output: 'student_premium'
```

---

##### `generate_license_record(tier_type: str, user_email: str, custom_name: Optional[str] = None, duration_days: Optional[int] = None, custom_daily_limit: Optional[int] = None) -> Dict`

Generate a complete license record for Supabase insertion.

**Parameters:**
- `tier_type` (str): License tier type
- `user_email` (str): User's email address
- `custom_name` (str, optional): Custom name for the license
- `duration_days` (int, optional): Custom duration (overrides default)
- `custom_daily_limit` (int, optional): Custom daily limit (for institutional)

**Returns:**
- `Dict`: License record ready for Supabase

**Example:**
```python
license = generator.generate_license_record(
    tier_type='student_premium',
    user_email='user@example.com',
    custom_name='Premium License',
    duration_days=60
)
```

---

##### `generate_batch_licenses(tier_type: str, count: int, base_email: Optional[str] = None, duration_days: Optional[int] = None) -> List[Dict]`

Generate multiple license records at once.

**Parameters:**
- `tier_type` (str): License tier type
- `count` (int): Number of licenses to generate
- `base_email` (str, optional): Base email (will append numbers for batch)
- `duration_days` (int, optional): Custom duration

**Returns:**
- `List[Dict]`: List of license records

**Example:**
```python
batch = generator.generate_batch_licenses('free_trial', 10, 'trial')
```

---

##### `export_licenses_json(licenses: List[Dict], filename: str)`

Export license records to a JSON file.

**Parameters:**
- `licenses` (List[Dict]): List of license records
- `filename` (str): Output filename

**Example:**
```python
generator.export_licenses_json(licenses, 'licenses.json')
```

---

##### `print_license_summary(license_record: Dict)`

Print a formatted summary of a license.

**Parameters:**
- `license_record` (Dict): License record to display

**Example:**
```python
generator.print_license_summary(license)
```

---

## 🗄️ Integration with Supabase

### Step 1: Set Up Supabase Schema

Run the SQL schema file to create all necessary tables:

```sql
-- In Supabase SQL Editor
\i supabase_schema_v10.sql
```

Or copy and paste the contents of `supabase_schema_v10.sql` into the Supabase SQL editor.

### Step 2: Generate Licenses

```python
generator = LicenseKeyGenerator()

# Generate licenses
licenses = [
    generator.generate_license_record('student_premium', 'user1@example.com'),
    generator.generate_license_record('teacher_suite', 'teacher@school.edu')
]

# Export to JSON
generator.export_licenses_json(licenses, 'licenses_to_import.json')
```

### Step 3: Import to Supabase

#### Option A: Using Supabase Python Client

```python
from supabase import create_client
import json
import os

# Initialize Supabase client
supabase_url = os.environ.get('SUPABASE_URL')
supabase_key = os.environ.get('SUPABASE_KEY')
client = create_client(supabase_url, supabase_key)

# Load licenses
with open('licenses_to_import.json', 'r') as f:
    licenses = json.load(f)

# Insert into Supabase
for license in licenses:
    response = client.table('licenses').insert(license).execute()
    print(f"✅ Inserted license: {license['license_key']}")
```

#### Option B: Using Supabase Dashboard

1. Go to your Supabase project dashboard
2. Navigate to Table Editor → licenses
3. Click "Insert row"
4. Copy values from generated JSON
5. Click "Save"

### Step 4: Verify in App

The licenses are now ready to use with `app.py`:

```python
# In your application
license_manager = LicenseManager()
result = license_manager.validate_license('DUOE10-SP02-...')

if result['valid']:
    print(f"Valid license for {result['user_type']}")
    print(f"Daily usage: {result['daily_usage']}/{result['daily_limit']}")
```

---

## 🔄 Migration from v9.0.0

### Schema Differences

v10.0.0 adds new tables while maintaining backward compatibility:

**New Tables in v10.0.0:**
- `micro_missions` - Daily micro-missions
- `user_missions` - User mission progress
- `user_achievements` - Achievement badges (50+)
- `leaderboards` - Gamification rankings
- `learning_quests` - Learning quests and challenges
- `user_quests` - User quest progress
- `essay_submissions` - Complete submission history
- `teacher_classes` - Teacher class management
- `class_students` - Class enrollment

**Enhanced Tables:**
- `smartprofiles` - Now supports 30+ dimensions (up from 20+)
- `licenses` - New v10.0.0 tier types added

### Migration Steps

1. **Backup your v9.0.0 database**:
```sql
-- Create backup
pg_dump your_database > douessay_v9_backup.sql
```

2. **Run v10.0.0 schema updates**:
```sql
-- Add new tables and columns
\i supabase_schema_v10.sql
```

3. **Migrate existing licenses**:
```python
# Licenses table is backward compatible
# Legacy tier types ('free', 'plus', 'premium', 'unlimited') still work
# No migration needed for licenses
```

4. **Update SmartProfile data**:
```python
# Add new v10.0.0 dimensions to existing profiles
from supabase import create_client

client = create_client(supabase_url, supabase_key)

# Get all profiles
profiles = client.table('smartprofiles').select('*').execute()

# Update each profile with new dimensions
for profile in profiles.data:
    client.table('smartprofiles').update({
        'emotional_resilience': 50.0,
        'time_management_score': 50.0,
        'creativity_index': 50.0,
        'micro_missions_completed': 0,
        'total_points': 0,
        'current_level': 1,
        'streak_days': 0
    }).eq('user_id', profile['user_id']).execute()
```

5. **Generate new v10.0.0 licenses** as needed using the License Key Generator.

---

## 🔒 Security Considerations

### Key Generation Security

1. **Cryptographic Randomness**: Uses Python's `secrets` module for cryptographically secure random number generation.

2. **Checksum Validation**: Each key includes a SHA-256 checksum to prevent tampering.

3. **Unique Keys**: UUID-based generation ensures no collisions.

### Best Practices

1. **Never commit license keys to version control**:
```bash
# Add to .gitignore
*.json
generated_licenses.json
licenses_to_import.json
```

2. **Store generated licenses securely**:
```python
# Encrypt before storing
import json
from cryptography.fernet import Fernet

# Generate encryption key
key = Fernet.generate_key()
cipher = Fernet(key)

# Encrypt licenses
with open('licenses.json', 'r') as f:
    data = f.read().encode()
encrypted = cipher.encrypt(data)

with open('licenses.encrypted', 'wb') as f:
    f.write(encrypted)
```

3. **Use environment variables for Supabase credentials**:
```bash
export SUPABASE_URL="your_supabase_url"
export SUPABASE_KEY="your_supabase_key"
```

4. **Rotate institutional licenses regularly**:
```python
# Deactivate old licenses
client.table('licenses').update({
    'is_active': False
}).eq('user_type', 'institutional').lt('expires_at', 'NOW()').execute()
```

5. **Monitor usage for anomalies**:
```sql
-- Check for unusual usage patterns
SELECT license_key, usage_count, usage_date
FROM usage
WHERE usage_count > daily_limit * 1.5
ORDER BY usage_date DESC;
```

---

## 🐛 Troubleshooting

### Common Issues

#### Issue 1: Import Error

**Problem**: `ModuleNotFoundError: No module named 'license_generator'`

**Solution**:
```bash
# Ensure you're in the correct directory
cd /path/to/DouEssay

# Run with python -m
python -m license_generator
```

#### Issue 2: Invalid Key Format

**Problem**: Generated keys fail validation

**Solution**:
```python
# Verify the key format
key = generator.generate_key('student_premium')
print(f"Key: {key}")
print(f"Valid: {generator.validate_key_format(key)}")

# If invalid, regenerate
if not generator.validate_key_format(key):
    key = generator.generate_key('student_premium')
```

#### Issue 3: Supabase Insertion Error

**Problem**: `duplicate key value violates unique constraint "licenses_license_key_key"`

**Solution**:
```python
# Check if key already exists
existing = client.table('licenses').select('*').eq('license_key', key).execute()
if existing.data:
    print(f"Key already exists: {key}")
    # Generate a new key
    key = generator.generate_key(tier_type)
```

#### Issue 4: JSON Export Error

**Problem**: `TypeError: Object of type datetime is not JSON serializable`

**Solution**:
```python
# The generator handles this automatically, but if you're manually exporting:
import json
from datetime import datetime

# Use default=str for datetime objects
json.dump(licenses, f, indent=2, default=str)
```

### Getting Help

1. **Check the documentation**: Review this README and `supabase_schema_v10.sql` comments
2. **Review examples**: See `python license_generator.py` for working examples
3. **Check logs**: Enable debug logging in your application
4. **Open an issue**: [GitHub Issues](https://github.com/changcheng967/DouEssay/issues)

---

## 📞 Support

For questions, issues, or feature requests:

- **GitHub**: [github.com/changcheng967/DouEssay](https://github.com/changcheng967/DouEssay)
- **Issues**: [Report a bug](https://github.com/changcheng967/DouEssay/issues)
- **Documentation**: [README.md](README.md)

---

## 📝 License

Copyright © 2025 Doulet Media. All rights reserved.

This license generator is part of the DouEssay v10.0.0 - Project Apex system.

---

**Made with ❤️ for educators and students worldwide**

*"Specs vary. No empty promises—just code, hardware, and your ambition."*
