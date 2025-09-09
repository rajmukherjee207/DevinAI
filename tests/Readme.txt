# Website UI Tests - DaveAI

This project contains Selenium UI automation tests for the website:
https://www.iamdave.ai

---

## How to Run the Tests

1. Create and activate a Python virtual environment (recommended).
   Windows:
       python -m venv venv
       venv\Scripts\activate

   macOS / Linux:
       python3 -m venv venv
       source venv/bin/activate

2. Install required dependencies:
       pip install -r requirements.txt

3. Run all tests:
       pytest -v

4. Run a specific test file:
       pytest -v tests/test_ui_iamdave.py

5. Run only smoke tests (logo presence check):
       pytest -m smoke -v

---

## Dependencies

List these inside requirements.txt:

pytest
selenium
webdriver-manager

(Optional)
pytest-html  # if you want HTML reports

---

## Test Design Choices

- **Setup/Teardown**
  A pytest fixture starts Chrome before tests and quits after tests.

- **Wait Strategies**
  - Global implicit wait (5s).
  - Explicit waits for dynamic elements (WebDriverWait + ExpectedConditions).

- **Test Cases**
  1. Verify homepage loads and title contains "DaveAI".
  2. Verify the logo is visible.
  3. Navigate to About Us page and verify URL contains "about-us".
  4. Verify a heading (`h1`) is displayed on the homepage.
  5. Fill and submit the "Book Demo" form, assert redirect to /thank-you.

- **Resilience**
  JS click is used to avoid sticky headers.
  Iframe detection for the Book Demo form.
  Consent/cookie popups handled if present.

---

Author: [Your Name]
