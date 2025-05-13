from io import BytesIO
from pathlib import Path
import pytest
from src.app import app


def set_up_test_success_params():
    res = []
    for file in (Path.cwd() / "tests/test_files/bank_statements").iterdir():
        res.append((file.absolute(), "bank_statement"))
    for file in (Path.cwd() / "tests/test_files/drivers_licenses").iterdir():
        res.append((file.absolute(), "drivers_license"))
    for file in (Path.cwd() / "tests/test_files/invoices").iterdir():
        res.append((file.absolute(), "invoice"))
    for file in (Path.cwd() / "tests/test_files/unknown_files").iterdir():
        res.append((file.absolute(), "unknown_file"))
    return res


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_no_file_in_request(client):
    response = client.post("/classify_file")
    assert response.status_code == 400


def test_no_selected_file(client):
    data = {"file": (BytesIO(b""), "")}  # Empty filename
    response = client.post(
        "/classify_file", data=data, content_type="multipart/form-data"
    )
    assert response.status_code == 400


@pytest.mark.parametrize(
    "filename, expected_code",
    [
        ("file.pdf", 200),
        ("file.png", 200),
        ("file.jpg", 200),
        ("file.txt", 400),
        ("file", 400),
    ],
)
def test_allowed_file(client, filename, expected_code):
    data = {"file": (BytesIO(b""), filename)}
    response = client.post(
        "/classify_file", data=data, content_type="multipart/form-data"
    )
    assert response.status_code == expected_code


@pytest.mark.parametrize(
    "filepath, file_class",
    set_up_test_success_params(),
)
def test_success(client, filepath, file_class):
    with open(filepath, "rb") as f:
        data = {"file": (f, filepath.name)}
        response = client.post(
            "/classify_file", data=data, content_type="multipart/form-data"
        )
        assert (
            response.get_json() == {"file_class": file_class}
            and response.status_code == 200
        )
