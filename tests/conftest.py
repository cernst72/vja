import os
import subprocess
import sys


def _login_as_test_user():
    result = subprocess.run('vja logout'.split(), check=False)
    if result.returncode:
        print(result.stdout)
        print(result.stderr)
        return result.returncode

    result = subprocess.run('vja --username=test --password=test user show'.split(), check=False)
    if result.returncode:
        print(result.stdout)
        print(result.stderr)
    return result.returncode


def pytest_configure():
    if 'VJA_CONFIGDIR' not in os.environ:
        print('!!! Precondition not met. You must set VJA_CONFIGDIR in environment variables !!!')
        sys.exit(1)

    if _login_as_test_user() > 0:
        print('!!! Precondition not met. Cannot connect to Vikunja with user test/test')
        sys.exit(1)
