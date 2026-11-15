# ============================================================
# WEEK 2 CAPSTONE - STEP 3: PRIVACY MASKING
# ============================================================
# OBJECTIVE:
# Detect Kenyan phone numbers and email addresses.
# Replace sensitive information with placeholders.
# ============================================================

# STEP 1: IMPORT LIBRARY
import re

# STEP 2: DEFINE PATTERNS
EMAIL_PATTERN = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")

# Supports common Kenyan mobile formats:
# 0712345678, 0112345678, +254712345678,
# 254712345678, +254 712 345 678
PHONE_PATTERN = re.compile(r"(?<!\w)(?:\+254|254|0)[ \t-]?[17](?:[ \t-]?\d){8}(?!\d)")


# STEP 3: CREATE THE MASKING FUNCTION
def mask_pii(text: str) -> tuple[str, dict[str, str]]:
    """Replace email addresses and Kenyan mobile numbers."""

    replacements = {}
    email_count = 0
    phone_count = 0

    # Replace email addresses
    def replace_email(match):
        nonlocal email_count
        email_count += 1

        placeholder = f"[EMAIL_{email_count}]"
        replacements[placeholder] = match.group()

        return placeholder

    # Replace Kenyan phone numbers
    def replace_phone(match):
        nonlocal phone_count
        phone_count += 1

        placeholder = f"[PHONE_{phone_count}]"
        replacements[placeholder] = match.group()

        return placeholder

    masked_text = EMAIL_PATTERN.sub(replace_email, text)
    masked_text = PHONE_PATTERN.sub(replace_phone, masked_text)

    return masked_text, replacements


# STEP 4: TEST THE FUNCTION
if __name__ == "__main__":

    # Fictional patient information for testing
    user_input = (
        "My phone number is 0712345678 "
        "and my email is mary@example.com. "
        "Please check my insurance coverage."
    )

    masked_text, replacements = mask_pii(user_input)

    print("\n--- PRIVACY MASKING TEST ---")
    print("Masked text:", masked_text)
    print("Number of sensitive values hidden:", len(replacements))
