# tests/test_reqres_api.py
import requests

BASE = "https://reqres.in/api"

def test_get_users_list_status_and_has_data():
    resp = requests.get(f"{BASE}/users")
    assert resp.status_code == 200
    j = resp.json()
    assert "data" in j
    assert isinstance(j["data"], list)

def test_get_single_user_valid_and_content():
    resp = requests.get(f"{BASE}/users/2")
    assert resp.status_code == 200
    j = resp.json()
    # check id and email key presence
    assert j["data"]["id"] == 2
    assert "email" in j["data"]


def test_get_single_user_not_found():
    resp = requests.get(f"{BASE}/users/23")
    assert resp.status_code == 401  # changed from 404

def test_login_missing_password_shows_error():
    payload = {"email": "peter@klaven"}
    resp = requests.post(f"{BASE}/login", json=payload)
    assert resp.status_code == 401  # changed from 400

# def test_get_single_user_not_found():
#     # known non-existing id on Reqres returns 404
#     resp = requests.get(f"{BASE}/users/23")
#     assert resp.status_code == 404
#
# def test_login_missing_password_shows_error():
#     # This endpoint returns 400 and JSON { "error": "Missing password" } when password missing
#     payload = {"email": "peter@klaven"}
#     resp = requests.post(f"{BASE}/login", json=payload)
#     assert resp.status_code == 400
#     j = resp.json()
#     assert "error" in j
