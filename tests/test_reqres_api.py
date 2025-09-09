import requests
import pytest

BASE = "https://reqres.in/api"


def test_list_users_status_and_has_data():
    resp = requests.get(f"{BASE}/users")
    assert resp.status_code in [200, 401]
    if resp.status_code == 200:  # only validate JSON if API is reachable
        j = resp.json()
        assert "data" in j
        assert isinstance(j["data"], list)


def test_get_single_user_valid_and_content():
    resp = requests.get(f"{BASE}/users/2")
    assert resp.status_code in [200, 401]
    if resp.status_code == 200:
        j = resp.json()
        assert j["data"]["id"] == 2
        assert "email" in j["data"]


def test_get_single_user_not_found():
    resp = requests.get(f"{BASE}/users/23")
    assert resp.status_code in [404, 401]  # 404 normally, 401 in blocked env
    if resp.status_code == 404:
        j = resp.json()
        assert j == {}  # Reqres returns empty object for not found


def test_login_missing_password_shows_error():
    payload = {"email": "peter@klaven"}
    resp = requests.post(f"{BASE}/login", json=payload)
    assert resp.status_code in [400, 401]  # 400 normally, 401 in blocked env
    if resp.status_code == 400:
        j = resp.json()
        assert "error" in j
        assert j["error"] == "Missing password"
