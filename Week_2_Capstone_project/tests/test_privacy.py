# ============================================================
# WEEK 2 CAPSTONE - STEP 4: PRIVACY TESTS
# ============================================================
# OBJECTIVE:
# Verify that the privacy masking function works correctly.
# ============================================================

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

# STEP 1: IMPORT LIBRARIES
import pytest
from src.privacy import mask_pii


# STEP 2: TEST EMAIL MASKING
def test_email_masking():
    text = "Contact mary@example.com"

    masked, replacements = mask_pii(text)

    assert masked == "Contact [EMAIL_1]"
    assert replacements["[EMAIL_1]"] == "mary@example.com"


# STEP 3: TEST KENYAN PHONE NUMBERS
@pytest.mark.parametrize(
    "phone",
    ["0712345678", "0112345678", "+254712345678", "254712345678", "+254 712 345 678"],
)
def test_phone_masking(phone):
    masked, replacements = mask_pii(f"Call {phone}")

    assert masked == "Call [PHONE_1]"
    assert replacements["[PHONE_1]"] == phone


# STEP 4: TEST MULTIPLE SENSITIVE VALUES
def test_multiple_pii():
    text = "Email mary@example.com or john@example.com " "and call 0712345678"

    masked, replacements = mask_pii(text)

    assert "[EMAIL_1]" in masked
    assert "[EMAIL_2]" in masked
    assert "[PHONE_1]" in masked
    assert len(replacements) == 3


# STEP 5: TEST MESSAGE WITHOUT PERSONAL DATA
def test_no_pii():
    text = "What insurance does AfyaPlus accept?"

    masked, replacements = mask_pii(text)

    assert masked == text
    assert replacements == {}


# STEP 6: TEST EMPTY MESSAGE
def test_empty_message():
    masked, replacements = mask_pii("")

    assert masked == ""
    assert replacements == {}
