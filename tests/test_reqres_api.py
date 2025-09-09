import requests
import pytest

BASE = "https://reqres.in/api"


def _skip_if_unauthorized(status_code: int):
    """If your network blocks external calls and returns 401, skip the test instead of failing."""
    if status_code == 401:
        pytest.skip("Received 401 from environment (proxy/firewall). Skipping in restricted network.")


def test_list_users_status_and_has_data():
    """Validate a successful 200 and that response contains a 'data' list."""
    resp = requests.get(f"{BASE}/users")
    _skip_if_unauthorized(resp.status_code)
    assert resp.status_code == 200
    j = resp.json()
    assert "data" in j and isinstance(j["data"], list)


def test_get_single_user_valid_and_content():
    """Validate 200 + content: id==2 and email key exists."""
    resp = requests.get(f"{BASE}/users/2")
    _skip_if_unauthorized(resp.status_code)
    assert resp.status_code == 200
    j = resp.json()
    assert j["data"]["id"] == 2
    assert "email" in j["data"] and j["data"]["email"].endswith("@reqres.in")


def test_get_single_user_not_found():
    """Validate error handling: non-existent user returns 404 and empty object."""
    resp = requests.get(f"{BASE}/users/23")  # known non-existent id
    _skip_if_unauthorized(resp.status_code)
    assert resp.status_code == 404
    # Reqres returns {}, not an error structure
    assert resp.json() == {}


def test_login_missing_password_shows_error():
    """Validate error handling: missing password => 400 + error message."""
    payload = {"email": "peter@klaven"}  # no password
    resp = requests.post(f"{BASE}/login", json=payload)
    _skip_if_unauthorized(resp.status_code)
    assert resp.status_code == 400
    j = resp.json()
    assert j.get("error") == "Missing password"
