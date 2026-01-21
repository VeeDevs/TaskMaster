#!/usr/bin/env python
"""Run all tests and report results."""

import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from django.test.utils import get_runner
from django.conf import settings

TestRunner = get_runner(settings)
test_runner = TestRunner(verbosity=1, interactive=False, keepdb=False)
failures = test_runner.run_tests(['myapp'])

print("\n" + "="*60)
if failures == 0:
    print("✓ ALL TESTS PASSED!")
else:
    print(f"✗ TESTS FAILED: {failures} failures")
print("="*60)

sys.exit(failures)
