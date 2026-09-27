import sys


def test_venv_and_pytest_config_work() -> None:
    assert sys.version_info[:2] == (3, 12)
