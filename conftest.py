from pathlib import Path

import pytest


@pytest.fixture(scope="session")
def fixtures_path() -> Path:
    return Path(__file__).absolute().parent / "tests" / "fixtures"
