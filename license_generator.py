#!/usr/bin/env python3
"""
DouEssay v10.0.0 - Project Apex
License Key Generator

This script generates secure license keys for DouEssay v10.0.0 with support for all tier types.
Compatible with Supabase backend and includes validation functions.

Author: changcheng967
Organization: Doulet Media
Version: 10.0.0
"""

import secrets
import hashlib
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import json
import os

# Version information
VERSION = "10.0.0"
VERSION_NAME = "Project Apex"

class LicenseKeyGenerator:
    """
    License Key Generator for DouEssay v10.0.0 - Project Apex
    
    Supports all tier types:
    - free_trial: 7-day trial with 5 essays/week
    - student_basic: $7.99/month, 25 essays/day
    - student_premium: $12.99/month, 100 essays/day
    - teacher_suite: $29.99/month, unlimited essays
    - institutional: Custom pricing, custom limits
    """
    
    # v10.0.0 Project Apex tier definitions
    TIER_TYPES = {
        'free_trial': {
            'name': 'Free Trial',
            'duration_days': 7,
            'daily_limit': 35,  # ~5 essays per week
            'price': 0.00,
            'description': 'Basic grading + Logic 5.0 (basic features)',
            'features': [
                'basic_grading',
                'neural_rubric',
                'score_breakdown'
            ]
        },
        'student_basic': {
            'name': 'Student Basic',
            'duration_days': 30,
            'daily_limit': 25,
            'price': 7.99,
            'description': 'Full Logic 5.0 + SmartProfile 3.0 + Real-Time Mentor 3.0',
            'features': [
                'logic_5_neural_reasoning',
                'smartprofile_3',
                'realtime_mentor_3',
                'emotionflow_2',
                'gamification_full',
                'creativity_metrics',
                'multilingual_full'
            ]
        },
        'student_premium': {
            'name': 'Student Premium',
            'duration_days': 30,
            'daily_limit': 100,
            'price': 12.99,
            'description': 'All features + Visual Analytics 3.0 + Voice Assistance',
            'features': [
                'logic_5_neural_reasoning',
                'smartprofile_3',
                'realtime_mentor_3',
                'emotionflow_2',
                'visual_analytics_3',
                'voice_assistance',
                'gamification_full',
                'creativity_metrics',
                'multilingual_full'
            ]
        },
        'teacher_suite': {
            'name': 'Teacher Suite',
            'duration_days': 30,
            'daily_limit': float('inf'),
            'price': 29.99,
            'description': 'All features + Teacher Dashboard 2.0 + Batch Grading AI + LMS Integration',
            'features': [
                'all_student_premium_features',
                'teacher_dashboard_2',
                'batch_grading_ai',
                'parent_interface',
                'lms_integration',
                'api_access'
            ]
        },
        'institutional': {
            'name': 'Institutional',
            'duration_days': 365,  # Annual by default
            'daily_limit': float('inf'),
            'price': 'custom',
            'description': 'School/District plan + Admin dashboard + Analytics',
            'features': [
                'all_teacher_suite_features',
                'institutional_admin',
                'district_analytics',
                'custom_configuration'
            ]
        }
    }
    
    def __init__(self):
        """Initialize the License Key Generator"""
        self.prefix = "DUOE10"  # DouEssay v10.0.0
        
    def generate_key(self, tier_type: str, custom_name: Optional[str] = None) -> str:
        """
        Generate a secure license key for the specified tier.
        
        Args:
            tier_type: One of 'free_trial', 'student_basic', 'student_premium', 
                      'teacher_suite', 'institutional'
            custom_name: Optional custom identifier for the license
            
        Returns:
            Secure license key in format: DUOE10-XXXXX-XXXXX-XXXXX-XXXXX
        """
        if tier_type not in self.TIER_TYPES:
            raise ValueError(f"Invalid tier type: {tier_type}. Must be one of {list(self.TIER_TYPES.keys())}")
        
        # Generate unique components
        tier_code = self._get_tier_code(tier_type)
        random_part = secrets.token_hex(6).upper()  # 12 characters
        checksum = self._generate_checksum(tier_code + random_part)
        
        # Format: DUOE10-TIER-RAND-RAND-CHKS
        key = f"{self.prefix}-{tier_code}-{random_part[:4]}-{random_part[4:8]}-{random_part[8:12]}{checksum}"
        
        return key
    
    def _get_tier_code(self, tier_type: str) -> str:
        """Get the tier code for the license key"""
        tier_codes = {
            'free_trial': 'FT00',
            'student_basic': 'SB01',
            'student_premium': 'SP02',
            'teacher_suite': 'TS03',
            'institutional': 'IN04'
        }
        return tier_codes[tier_type]
    
    def _generate_checksum(self, data: str) -> str:
        """Generate a 4-character checksum for validation"""
        hash_obj = hashlib.sha256(data.encode())
        return hash_obj.hexdigest()[:4].upper()
    
    def validate_key_format(self, license_key: str) -> bool:
        """
        Validate the format of a license key (does not check database).
        
        Args:
            license_key: The license key to validate
            
        Returns:
            True if the format is valid, False otherwise
        """
        try:
            parts = license_key.split('-')
            if len(parts) != 5:
                return False
            
            # Check prefix
            if parts[0] != self.prefix:
                return False
            
            # Check tier code
            tier_code = parts[1]
            valid_tiers = ['FT00', 'SB01', 'SP02', 'TS03', 'IN04']
            if tier_code not in valid_tiers:
                return False
            
            # Check random parts length
            if len(parts[2]) != 4 or len(parts[3]) != 4 or len(parts[4]) != 8:
                return False
            
            # Verify checksum
            random_part = parts[2] + parts[3] + parts[4][:4]
            expected_checksum = self._generate_checksum(tier_code + random_part)
            actual_checksum = parts[4][4:]
            
            return expected_checksum == actual_checksum
            
        except Exception:
            return False
    
    def get_tier_from_key(self, license_key: str) -> Optional[str]:
        """
        Extract the tier type from a license key.
        
        Args:
            license_key: The license key to parse
            
        Returns:
            Tier type string or None if invalid
        """
        if not self.validate_key_format(license_key):
            return None
        
        tier_code = license_key.split('-')[1]
        tier_map = {
            'FT00': 'free_trial',
            'SB01': 'student_basic',
            'SP02': 'student_premium',
            'TS03': 'teacher_suite',
            'IN04': 'institutional'
        }
        return tier_map.get(tier_code)
    
    def generate_license_record(
        self, 
        tier_type: str,
        user_email: str,
        custom_name: Optional[str] = None,
        duration_days: Optional[int] = None,
        custom_daily_limit: Optional[int] = None
    ) -> Dict:
        """
        Generate a complete license record for Supabase insertion.
        
        Args:
            tier_type: License tier type
            user_email: User's email address
            custom_name: Optional custom name for the license
            duration_days: Optional custom duration (overrides default)
            custom_daily_limit: Optional custom daily limit (for institutional)
            
        Returns:
            Dictionary ready for Supabase insertion
        """
        if tier_type not in self.TIER_TYPES:
            raise ValueError(f"Invalid tier type: {tier_type}")
        
        tier_info = self.TIER_TYPES[tier_type]
        license_key = self.generate_key(tier_type, custom_name)
        
        # Use custom duration or default
        duration = duration_days if duration_days is not None else tier_info['duration_days']
        
        # Use custom limit or default
        daily_limit = custom_daily_limit if custom_daily_limit is not None else tier_info['daily_limit']
        
        # Convert inf to a large number for database storage
        if daily_limit == float('inf'):
            daily_limit = 999999
        
        record = {
            'license_key': license_key,
            'user_type': tier_type,
            'user_email': user_email,
            'custom_name': custom_name or f"{tier_info['name']} License",
            'issued_at': datetime.now().isoformat(),
            'expires_at': (datetime.now() + timedelta(days=duration)).isoformat(),
            'is_active': True,
            'daily_limit': daily_limit,
            'features': tier_info['features'],
            'metadata': {
                'version': VERSION,
                'version_name': VERSION_NAME,
                'tier_name': tier_info['name'],
                'tier_description': tier_info['description'],
                'price': tier_info['price']
            }
        }
        
        return record
    
    def generate_batch_licenses(
        self,
        tier_type: str,
        count: int,
        base_email: Optional[str] = None,
        duration_days: Optional[int] = None
    ) -> List[Dict]:
        """
        Generate multiple license records at once.
        
        Args:
            tier_type: License tier type
            count: Number of licenses to generate
            base_email: Base email (will append numbers for batch)
            duration_days: Optional custom duration
            
        Returns:
            List of license records ready for batch insertion
        """
        licenses = []
        
        for i in range(count):
            email = f"{base_email or 'user'}+{i}@example.com" if count > 1 else base_email or "user@example.com"
            custom_name = f"Batch License {i+1}/{count}"
            
            record = self.generate_license_record(
                tier_type=tier_type,
                user_email=email,
                custom_name=custom_name,
                duration_days=duration_days
            )
            licenses.append(record)
        
        return licenses
    
    def export_licenses_json(self, licenses: List[Dict], filename: str):
        """
        Export license records to a JSON file.
        
        Args:
            licenses: List of license records
            filename: Output filename
        """
        with open(filename, 'w') as f:
            json.dump(licenses, f, indent=2, default=str)
        print(f"✅ Exported {len(licenses)} licenses to {filename}")
    
    def print_license_summary(self, license_record: Dict):
        """Print a formatted summary of a license"""
        print("\n" + "="*60)
        print(f"🎓 DouEssay v{VERSION} - {VERSION_NAME}")
        print("="*60)
        print(f"License Key:    {license_record['license_key']}")
        print(f"Tier:           {license_record['metadata']['tier_name']}")
        print(f"User Type:      {license_record['user_type']}")
        print(f"Email:          {license_record['user_email']}")
        print(f"Daily Limit:    {license_record['daily_limit']} essays")
        print(f"Issued:         {license_record['issued_at']}")
        print(f"Expires:        {license_record['expires_at']}")
        print(f"Price:          ${license_record['metadata']['price']}/month" if isinstance(license_record['metadata']['price'], float) else f"Price:          {license_record['metadata']['price']}")
        print(f"\n📝 Description: {license_record['metadata']['tier_description']}")
        print(f"\n✨ Features:")
        for feature in license_record['features']:
            print(f"   ✓ {feature}")
        print("="*60 + "\n")


def main():
    """
    Example usage of the License Key Generator
    """
    print(f"🚀 DouEssay v{VERSION} - {VERSION_NAME}")
    print(f"📋 License Key Generator\n")
    
    generator = LicenseKeyGenerator()
    
    # Example 1: Generate a single Student Premium license
    print("Example 1: Single Student Premium License")
    license = generator.generate_license_record(
        tier_type='student_premium',
        user_email='student@example.com',
        custom_name='Premium Student License'
    )
    generator.print_license_summary(license)
    
    # Example 2: Generate a Teacher Suite license
    print("\nExample 2: Teacher Suite License")
    teacher_license = generator.generate_license_record(
        tier_type='teacher_suite',
        user_email='teacher@school.edu',
        custom_name='Teacher Pro Account'
    )
    generator.print_license_summary(teacher_license)
    
    # Example 3: Generate batch free trial licenses
    print("\nExample 3: Batch Free Trial Licenses (5)")
    batch_licenses = generator.generate_batch_licenses(
        tier_type='free_trial',
        count=5,
        base_email='trial'
    )
    print(f"✅ Generated {len(batch_licenses)} free trial licenses")
    for i, lic in enumerate(batch_licenses, 1):
        print(f"   {i}. {lic['license_key']} - {lic['user_email']}")
    
    # Example 4: Generate institutional license with custom settings
    print("\nExample 4: Custom Institutional License")
    institutional = generator.generate_license_record(
        tier_type='institutional',
        user_email='admin@district.edu',
        custom_name='Springfield School District',
        duration_days=365,
        custom_daily_limit=999999
    )
    generator.print_license_summary(institutional)
    
    # Example 5: Key validation
    print("\nExample 5: License Key Validation")
    test_key = license['license_key']
    is_valid = generator.validate_key_format(test_key)
    tier = generator.get_tier_from_key(test_key)
    print(f"Key: {test_key}")
    print(f"Valid Format: {is_valid}")
    print(f"Tier Type: {tier}")
    
    # Example 6: Export to JSON
    print("\nExample 6: Export Licenses to JSON")
    all_licenses = [license, teacher_license] + batch_licenses + [institutional]
    generator.export_licenses_json(all_licenses, 'generated_licenses.json')
    
    print("\n" + "="*60)
    print("✅ License generation complete!")
    print("📁 Check 'generated_licenses.json' for all generated licenses")
    print("="*60)


if __name__ == "__main__":
    main()
