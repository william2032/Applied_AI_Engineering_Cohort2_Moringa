# ============================================================
# WEEK 2 CAPSTONE - STEP 10: SAFE OUTPUT DE-MASKING
# ============================================================
# OBJECTIVE:
# Restore only explicitly approved personal information
# after the AI has generated its response.
# ============================================================

# STEP 1: IMPORT LIBRARIES
import re

from src.privacy import mask_pii

# STEP 2: DEFINE THE PLACEHOLDER PATTERN
TOKEN_PATTERN = re.compile(r"\[(?:EMAIL|PHONE)_\d+\]")


# STEP 3: CREATE THE DE-MASKING FUNCTION
def demask_approved_output(
    response: str,
    replacements: dict[str, str],
    approved_placeholders: set[str] | None = None,
) -> str:
    """Restore only placeholders approved by the application."""

    # By default, do not restore any personal information
    approved = approved_placeholders or set()

    # Replace a token only if approval exists
    def restore(match):
        placeholder = match.group()

        if placeholder in approved and placeholder in replacements:
            return replacements[placeholder]

        return placeholder

    return TOKEN_PATTERN.sub(restore, response)


# STEP 4: TEST THE FUNCTION
if __name__ == "__main__":

    # Fictional patient details
    user_input = "My email is mary@example.com " "and my phone is 0712345678."

    # Hide sensitive information
    masked_input, replacements = mask_pii(user_input)

    # Simulated AI response containing placeholders
    ai_response = "Confirmation can be sent to [EMAIL_1]. " "Phone number: [PHONE_1]."

    # Only the email placeholder has been approved
    final_response = demask_approved_output(
        response=ai_response,
        replacements=replacements,
        approved_placeholders={"[EMAIL_1]"},
    )

    print("\n--- DE-MASKING TEST ---")
    print("Masked input:", masked_input)
    print("Final response:", final_response)
