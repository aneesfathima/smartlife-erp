#!/usr/bin/env python3
"""
Test script for User Activity API endpoints
Tests automatic loyalty point awarding for user activities
"""

import requests
import json
import time
import sys
import os

# Fix Windows console encoding
if sys.platform == 'win32':
    os.system('chcp 65001 > nul')
    sys.stdout.reconfigure(encoding='utf-8')

# Configuration
BASE_URL = "http://localhost:8091"
AUTH_ENDPOINT = f"{BASE_URL}/api/v2/auth/get_tokens"
ACTIVITY_ENDPOINTS = {
    "track_app_usage": f"{BASE_URL}/api/v1/activity/track_app_usage",
    "track_engagement": f"{BASE_URL}/api/v1/activity/track_engagement",
    "activity_summary": f"{BASE_URL}/api/v1/activity/summary",
    "track_manual": f"{BASE_URL}/api/v1/activity/track_manual",
    "streak_info": f"{BASE_URL}/api/v1/activity/streak_info"
}
LOYALTY_BALANCE_ENDPOINT = f"{BASE_URL}/api/v1/loyalty/balance"

# Test credentials
LOGIN_DATA = {
    "username": "admin@adigielite.com",
    "password": "P4BusWSNB7StMw88N"
}

def make_jsonrpc_request(url, method_data, access_token=None):
    """Make REST request (returns wrapped dict to maintain compatibility with test assertions)"""
    headers = {
        'Content-Type': 'application/json',
    }

    if access_token:
        headers['Authorization'] = f'Bearer {access_token}'

    try:
        response = requests.post(url,
                               headers=headers,
                               data=json.dumps(method_data),
                               timeout=30)

        if response.status_code in [200, 201]:
            try:
                result = response.json()
                return {'result': result}
            except json.JSONDecodeError as e:
                print(f"JSON decode error: {e}")
                print(f"Response content: {response.text}")
                return None
        else:
            print(f"HTTP Error {response.status_code}: {response.text}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return None

def test_authentication():
    """Test user authentication"""
    print("=== Testing Authentication ===")

    result = make_jsonrpc_request(AUTH_ENDPOINT, LOGIN_DATA)

    if result and 'result' in result:
        data = result['result']
        if 'access_token' in data:
            print(f"✓ Authentication successful")
            print(f"  User: {data.get('display_name', 'Unknown')}")
            print(f"  Access Token: {data['access_token'][:20]}...")
            return data['access_token']
        else:
            print(f"✗ Authentication failed: {data.get('message', 'Unknown error')}")
            print(f"  Full response data: {data}")
            return None
    else:
        print(f"✗ Authentication request failed")
        print(f"  Full result: {result}")
        return None

def test_track_app_usage(access_token):
    """Test app usage tracking"""
    print("\n=== Testing App Usage Tracking ===")

    test_data = {
        "duration_minutes": 25.5,
        "session_data": {
            "app_version": "1.0.0",
            "platform": "mobile"
        }
    }

    result = make_jsonrpc_request(ACTIVITY_ENDPOINTS["track_app_usage"], test_data, access_token)

    if result and 'result' in result:
        data = result['result']
        if data.get('success'):
            response_data = data.get('data', {})
            print(f"✓ App usage tracked successfully")
            print(f"  Total Points Awarded: {response_data.get('total_points_awarded', 0)}")
            print(f"  Activities Tracked: {response_data.get('activities_tracked', 0)}")
            return True
        else:
            print(f"✗ App usage tracking failed: {data.get('message', 'Unknown error')}")
            return False
    else:
        print(f"✗ App usage tracking request failed")
        return False

def test_track_engagement(access_token):
    """Test user engagement tracking"""
    print("\n=== Testing User Engagement Tracking ===")

    test_data = {
        "engagement_type": "profile_updated",
        "details": "Updated profile picture and bio"
    }

    result = make_jsonrpc_request(ACTIVITY_ENDPOINTS["track_engagement"], test_data, access_token)

    if result and 'result' in result:
        data = result['result']
        if data.get('success'):
            response_data = data.get('data', {})
            print(f"✓ User engagement tracked successfully")
            print(f"  Points Awarded: {response_data.get('points_awarded', 0)}")
            return True
        else:
            print(f"✗ User engagement tracking failed: {data.get('message', 'Unknown error')}")
            return False
    else:
        print(f"✗ User engagement tracking request failed")
        return False

def test_manual_activity(access_token):
    """Test manual activity tracking"""
    print("\n=== Testing Manual Activity Tracking ===")

    test_data = {
        "activity_type": "task_completion",
        "description": "Completed project milestone - API development",
        "duration_minutes": 120
    }

    result = make_jsonrpc_request(ACTIVITY_ENDPOINTS["track_manual"], test_data, access_token)

    if result and 'result' in result:
        data = result['result']
        if data.get('success'):
            response_data = data.get('data', {})
            print(f"✓ Manual activity tracked successfully")
            print(f"  Activity ID: {response_data.get('activity_id')}")
            print(f"  Points Awarded: {response_data.get('points_awarded', 0)}")
            print(f"  Is New Activity: {response_data.get('is_new_activity', False)}")
            return True
        else:
            print(f"✗ Manual activity tracking failed: {data.get('message', 'Unknown error')}")
            return False
    else:
        print(f"✗ Manual activity tracking request failed")
        return False

def test_activity_summary(access_token):
    """Test activity summary retrieval"""
    print("\n=== Testing Activity Summary ===")

    test_data = {
        "days": 7
    }

    result = make_jsonrpc_request(ACTIVITY_ENDPOINTS["activity_summary"], test_data, access_token)

    if result and 'result' in result:
        data = result['result']
        if data.get('success'):
            summary = data.get('data', {})
            print(f"✓ Activity summary retrieved successfully")
            print(f"  Total Activities: {summary.get('total_activities', 0)}")
            print(f"  Total Points Earned: {summary.get('total_points_earned', 0)}")
            print(f"  Daily Streak: {summary.get('daily_streak', 0)}")
            print(f"  Last Activity: {summary.get('last_activity_date', 'None')}")

            breakdown = summary.get('activity_breakdown', {})
            if breakdown:
                print("  Activity Breakdown:")
                for activity_type, stats in breakdown.items():
                    print(f"    {activity_type}: {stats.get('count', 0)} activities, {stats.get('points', 0)} points")

            return True
        else:
            print(f"✗ Activity summary failed: {data.get('message', 'Unknown error')}")
            return False
    else:
        print(f"✗ Activity summary request failed")
        return False

def test_streak_info(access_token):
    """Test streak information retrieval"""
    print("\n=== Testing Streak Information ===")

    test_data = {
        "activity_type": "daily_login"
    }

    result = make_jsonrpc_request(ACTIVITY_ENDPOINTS["streak_info"], test_data, access_token)

    if result and 'result' in result:
        data = result['result']
        if data.get('success'):
            streak_info = data.get('data', {})
            print(f"✓ Streak information retrieved successfully")
            print(f"  Current Streak: {streak_info.get('current_streak', 0)} days")
            print(f"  Next Milestone: {streak_info.get('next_milestone', 'None')}")
            print(f"  Days to Next Milestone: {streak_info.get('days_to_next_milestone', 'N/A')}")
            print(f"  Current Multiplier: {streak_info.get('current_multiplier', 1.0)}x")
            return True
        else:
            print(f"✗ Streak information failed: {data.get('message', 'Unknown error')}")
            return False
    else:
        print(f"✗ Streak information request failed")
        return False

def test_loyalty_balance(access_token):
    """Test loyalty balance check"""
    print("\n=== Testing Loyalty Balance ===")

    result = make_jsonrpc_request(LOYALTY_BALANCE_ENDPOINT, {}, access_token)

    if result and 'result' in result:
        data = result['result']
        # Handle both wrapped and unwrapped styles
        balance_data = data.get('data', data) if isinstance(data, dict) else {}
        is_success = data.get('success') or 'available_balance' in data

        if is_success:
            print(f"✓ Loyalty balance retrieved successfully")
            print(f"  Available Balance: {balance_data.get('available_balance', 0)} points")
            print(f"  Ledger Balance: {balance_data.get('ledger_balance', 0)} points")
            print(f"  Pending Reserved: {balance_data.get('pending_reserved_points', 0)} points")
            return True
        else:
            print(f"✗ Loyalty balance failed: {data.get('message', 'Unknown error')}")
            return False
    else:
        print(f"✗ Loyalty balance request failed")
        return False

def main():
    """Run all user activity API tests"""
    print("SmartLife ERP - User Activity API Test Suite")
    print("=" * 50)

    # Test authentication
    access_token = test_authentication()
    if not access_token:
        print("Authentication failed. Cannot proceed with tests.")
        return

    # Wait a moment
    time.sleep(1)

    # Run all tests
    tests = [
        ("Track App Usage", test_track_app_usage),
        ("Track Engagement", test_track_engagement),
        ("Track Manual Activity", test_manual_activity),
        ("Activity Summary", test_activity_summary),
        ("Streak Information", test_streak_info),
        ("Loyalty Balance", test_loyalty_balance)
    ]

    results = {}
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func(access_token)
            time.sleep(0.5)  # Small delay between tests
        except Exception as e:
            print(f"✗ {test_name} test crashed: {e}")
            results[test_name] = False

    # Summary
    print("\n" + "=" * 50)
    print("TEST SUMMARY")
    print("=" * 50)

    passed = sum(1 for result in results.values() if result)
    total = len(results)

    for test_name, result in results.items():
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{test_name}: {status}")

    print(f"\nOverall: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 All user activity API tests passed!")
    else:
        print("⚠️  Some tests failed. Check the output above for details.")

if __name__ == "__main__":
    main()