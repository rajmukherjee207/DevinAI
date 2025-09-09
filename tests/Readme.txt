

project_root/
│
│
├── tests/
│   │── test_reqres_api.py (run)
│   │── test_ui_iamdave.py (run)
│   └── __pycache__/  (X)
│
└── Readme.txt


test_reqres_api.py


How to Run the Tests

Open Command Prompt.

Go to your project folder:

cd path\to\your\project


Run all tests with pytest:

pytest


To run a single test file:

pytest tests\test_reqres_api.py

Dependencies

Create a file requirements.txt with:

pytest
requests


Install them using:

pip install pytest

Test Design 

I used pytest because it is simple and powerful.

Tests are written for Reqres API.

Each test checks:

✅ Success response (200)

✅ Data exists and correct

✅ Error handling (404, 400)

If network blocks API (401), test will skip.



# Website UI Tests - DaveAI

test_ui_iamdave.py
How to Run the Tests
1. Install dependencies

First install requirements:

pip install -r requirements.txt

2. Run all tests

From project root folder:

pytest

3. Run API tests only
pytest tests\test_reqres_api.py

4. Run UI tests only
pytest tests\test_ui_iamdave.py

Dependencies
pytest
requests
selenium
webdriver-manager 

install one by one:

pip install pytest requests selenium webdriver-manager


👉 Make sure you have Google Chrome browser installed.

Test Design Explanation

API tests (Reqres)

Validate 200 success and data exists.

Validate correct content (id, email).

Validate error handling (404, 400).

If network blocks API (401), test skips.

UI tests (iamdave.ai)

Check homepage loads with correct title.

Check logo is present.

Navigate to About Us page and verify URL.

Check a heading appears on homepage.

Fill and submit Book Demo form → wait for Thank You page.
  Consent/cookie popups handled if present.

---

Author: Raj Mukherjee
