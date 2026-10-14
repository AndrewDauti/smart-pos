import os
import tempfile

_fd, _path = tempfile.mkstemp(suffix=".db")
os.close(_fd)
os.environ["DATABASE_URL"] = f"sqlite:///{_path}"
os.environ["MOCK_EINVOICE_URL"] = ""
os.environ["POS_USERNAME"] = "cashier"
os.environ["POS_PASSWORD"] = "mpepo"

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client():
    return TestClient(app)
