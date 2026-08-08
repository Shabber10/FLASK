"""
Pytest Module Execution Helper for Day 16 Practice Suite
=========================================================
Importing and running tests from '3. Practice Suite - Full Test Suite for User Management API.py'.
"""

import sys
import os
import importlib.util

# Import module with spaces and leading digits dynamically
module_path = os.path.join(os.path.dirname(__file__), "3. Practice Suite - Full Test Suite for User Management API.py")
spec = importlib.util.spec_from_file_location("day16_practice_suite", module_path)
day16 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(day16)

# Expose Pytest Fixtures
app = day16.app
client = day16.client

# Expose Test Functions for Pytest Discovery
test_health_check_endpoint = day16.test_health_check_endpoint
test_user_registration_success = day16.test_user_registration_success
test_user_registration_duplicate_username = day16.test_user_registration_duplicate_username
test_user_login_invalid_credentials = day16.test_user_login_invalid_credentials
test_user_login_success = day16.test_user_login_success
